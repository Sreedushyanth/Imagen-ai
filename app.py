from fastapi import FastAPI, UploadFile, File, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import uuid
import asyncio
from pathlib import Path
import httpx
from datetime import datetime
import json

from services.fal_service import fal_service
from config.settings import settings

app = FastAPI(
    title="StoryMaker Dynamic Image Generator", 
    version="2.0.0",
    description="AI-powered story image generation using Fal AI"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Ensure directories exist
Path("static/input").mkdir(parents=True, exist_ok=True)
Path("static/mask").mkdir(parents=True, exist_ok=True)
Path("static/results").mkdir(parents=True, exist_ok=True)
Path("logs").mkdir(parents=True, exist_ok=True)

def log_generation(session_id: str, status: str, details: dict):
    """Log generation details"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "session_id": session_id,
        "status": status,
        "details": details
    }
    
    log_file = Path("logs") / f"generation_{datetime.now().strftime('%Y%m%d')}.json"
    
    try:
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        print(f"Failed to log generation: {e}")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Main page with upload form"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "max_file_size": settings.max_file_size
    })

@app.post("/generate")
async def generate_story_images(
    face_image: UploadFile = File(...),
    mask_image: UploadFile = File(None),
    prompt: str = Form(...),
    negative_prompt: str = Form("bad quality, low resolution, NSFW, cartoonish, disfigured, broken limbs"),
    num_images: int = Form(4),
    guidance_scale: float = Form(7.5),
    num_inference_steps: int = Form(25),
    width: int = Form(1024),
    height: int = Form(1024)
):
    """Generate story images using Fal AI"""
    session_id = str(uuid.uuid4())
    
    try:
        # Validate file size
        if face_image.size > settings.max_file_size:
            raise HTTPException(
                status_code=413, 
                detail=f"File too large. Maximum size is {settings.max_file_size // 1024 // 1024}MB"
            )
        
        # Validate file type
        allowed_types = ['image/jpeg', 'image/png', 'image/webp']
        if face_image.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Please upload JPEG, PNG, or WebP images."
            )
        
        print(f"🎨 Starting generation for session: {session_id}")
        
        # Save uploaded face image
        face_image_path = f"static/input/face_{session_id}.{face_image.filename.split('.')[-1]}"
        with open(face_image_path, "wb") as buffer:
            shutil.copyfileobj(face_image.file, buffer)
        
        # Save mask image if provided
        mask_image_path = None
        if mask_image and mask_image.filename:
            if mask_image.size > settings.max_file_size:
                raise HTTPException(status_code=413, detail="Mask image too large")
            
            mask_image_path = f"static/mask/mask_{session_id}.{mask_image.filename.split('.')[-1]}"
            with open(mask_image_path, "wb") as buffer:
                shutil.copyfileobj(mask_image.file, buffer)
        
        # Log generation start
        log_generation(session_id, "started", {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "num_images": num_images,
            "guidance_scale": guidance_scale,
            "num_inference_steps": num_inference_steps
        })
        
        # Generate images using Fal AI
        result = await fal_service.generate_story_images(
            face_image_path=face_image_path,
            mask_image_path=mask_image_path,
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_images=num_images,
            guidance_scale=guidance_scale,
            num_inference_steps=num_inference_steps,
            width=width,
            height=height
        )
        
        if result["success"]:
            # Save generated images locally
            saved_images = []
            for i, image_url in enumerate(result["images"]):
                try:
                    # Download image from Fal AI
                    async with httpx.AsyncClient() as client:
                        img_response = await client.get(image_url)
                        if img_response.status_code == 200:
                            local_path = f"static/results/{session_id}_{i}.jpg"
                            with open(local_path, "wb") as f:
                                f.write(img_response.content)
                            saved_images.append(f"/{local_path}")
                except Exception as e:
                    print(f"Failed to save image {i}: {e}")
                    # Fallback to original URL
                    saved_images.append(image_url)
            
            result["images"] = saved_images
            result["session_id"] = session_id
            
            # Log successful generation
            log_generation(session_id, "completed", {
                "num_generated": len(saved_images),
                "generation_time": result.get("generation_time", 0)
            })
        else:
            # Log failed generation
            log_generation(session_id, "failed", {
                "error": result.get("error", "Unknown error")
            })
        
        return JSONResponse(content=result)
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Generation failed: {str(e)}"
        print(f"❌ {error_msg}")
        
        # Log error
        log_generation(session_id, "error", {"error": error_msg})
        
        return JSONResponse(
            content={"success": False, "error": error_msg},
            status_code=500
        )
    finally:
        # Cleanup uploaded files after processing
        try:
            if os.path.exists(face_image_path):
                os.remove(face_image_path)
            if mask_image_path and os.path.exists(mask_image_path):
                os.remove(mask_image_path)
        except Exception as e:
            print(f"Cleanup warning: {e}")

@app.post("/face-swap")
async def face_swap(
    face_image: UploadFile = File(...),
    target_image: UploadFile = File(...)
):
    """Perform face swap using Fal AI"""
    session_id = str(uuid.uuid4())
    
    try:
        # Save uploaded images
        face_image_path = f"static/input/face_{session_id}.jpg"
        target_image_path = f"static/input/target_{session_id}.jpg"
        
        with open(face_image_path, "wb") as buffer:
            shutil.copyfileobj(face_image.file, buffer)
        
        with open(target_image_path, "wb") as buffer:
            shutil.copyfileobj(target_image.file, buffer)
        
        # Perform face swap
        result = await fal_service.generate_with_face_swap(
            face_image_path, target_image_path
        )
        
        if result["success"]:
            # Save result image
            async with httpx.AsyncClient() as client:
                img_response = await client.get(result["image"])
                if img_response.status_code == 200:
                    local_path = f"static/results/faceswap_{session_id}.jpg"
                    with open(local_path, "wb") as f:
                        f.write(img_response.content)
                    result["image"] = f"/{local_path}"
        
        return JSONResponse(content=result)
        
    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": f"Face swap failed: {str(e)}"},
            status_code=500
        )
    finally:
        # Cleanup
        for path in [face_image_path, target_image_path]:
            if os.path.exists(path):
                os.remove(path)

@app.get("/gallery")
async def gallery(request: Request):
    """Display gallery of generated images"""
    results_dir = Path("static/results")
    images = []
    
    if results_dir.exists():
        for img_file in sorted(results_dir.glob("*.jpg"), key=lambda x: x.stat().st_mtime, reverse=True):
            images.append({
                "url": f"/static/results/{img_file.name}",
                "name": img_file.name,
                "created": datetime.fromtimestamp(img_file.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            })
    
    return templates.TemplateResponse("gallery.html", {
        "request": request,
        "images": images
    })

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check if Fal API key is configured
        api_configured = bool(settings.fal_api_key)
        
        return {
            "status": "healthy",
            "message": "StoryMaker API is running",
            "fal_api_configured": api_configured,
            "version": "2.0.0",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

@app.get("/stats")
async def get_stats():
    """Get generation statistics"""
    try:
        results_dir = Path("static/results")
        total_images = len(list(results_dir.glob("*.jpg"))) if results_dir.exists() else 0
        
        # Read today's logs
        today_log = Path("logs") / f"generation_{datetime.now().strftime('%Y%m%d')}.json"
        generations_today = 0
        
        if today_log.exists():
            with open(today_log, 'r') as f:
                generations_today = sum(1 for line in f if '"status": "completed"' in line)
        
        return {
            "total_images_generated": total_images,
            "generations_today": generations_today,
            "api_status": "active" if settings.fal_api_key else "not_configured"
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=7860,
        reload=settings.debug_mode
    )
