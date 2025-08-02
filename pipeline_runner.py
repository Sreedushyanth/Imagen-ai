import torch
import numpy as np
import cv2
from PIL import Image
import os
import traceback
from pathlib import Path

# Try to import the actual StoryMaker pipeline
try:
    from pipeline_sdxl_storymaker import StableDiffusionXLStoryMakerPipeline
    from diffusers import UniPCMultistepScheduler
    import insightface
    PIPELINE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: StoryMaker pipeline not available: {e}")
    PIPELINE_AVAILABLE = False

def run_generation(
    face_image_path,
    mask_image_path,
    prompt,
    negative_prompt,
    session_id,
    num_images=4,
    guidance_scale=7.5,
    num_inference_steps=25
):
    """
    Run the StoryMaker AI pipeline to generate story images
    """
    try:
        print(f"🎨 Starting generation for session: {session_id}")
        print(f"📝 Prompt: {prompt}")
        print(f"🚫 Negative prompt: {negative_prompt}")
        
        if not PIPELINE_AVAILABLE:
            # Fallback to demo mode with placeholder images
            return generate_demo_images(session_id, num_images, prompt)
        
        # Initialize face analysis
        print("🤖 Initializing face analysis...")
        app = insightface.app.FaceAnalysis(
            name='buffalo_l',
            root='./',
            providers=['CUDAExecutionProvider', 'CPUExecutionProvider']
        )
        app.prepare(ctx_id=0, det_size=(640, 640))
        
        # Load images
        print("🖼️ Loading images...")
        face_image = Image.open(face_image_path).convert('RGB')
        mask_image = None
        if mask_image_path:
            mask_image = Image.open(mask_image_path).convert('RGB')
        
        # Detect face
        print("👤 Detecting face...")
        face_array = cv2.cvtColor(np.array(face_image), cv2.COLOR_RGB2BGR)
        face_info = app.get(face_array)
        
        if not face_info:
            return {
                "success": False,
                "error": "No face detected in the uploaded image"
            }
        
        # Get the largest face
        face_info = sorted(
            face_info,
            key=lambda x: (x['bbox'][2] - x['bbox'][0]) * (x['bbox'][3] - x['bbox'][1])
        )[-1]
        
        print("🚀 Loading StoryMaker pipeline...")
        
        # Load the StoryMaker pipeline
        base_model = 'huaquan/YamerMIX_v11'
        image_encoder_path = 'laion/CLIP-ViT-H-14-laion2B-s32B-b79K'
        face_adapter = './checkpoints/mask.bin'
        
        # Check if face adapter exists
        if not os.path.exists(face_adapter):
            return {
                "success": False,
                "error": "Face adapter model (mask.bin) not found. Please download the required checkpoints."
            }
        
        pipe = StableDiffusionXLStoryMakerPipeline.from_pretrained(
            base_model,
            torch_dtype=torch.float16
        ).to('cuda' if torch.cuda.is_available() else 'cpu')
        
        pipe.load_storymaker_adapter(
            image_encoder_path,
            face_adapter,
            scale=0.8,
            lora_scale=0.8
        )
        
        pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
        
        # Generate images
        print(f"🎭 Generating {num_images} story images...")
        generator = torch.Generator(device='cuda' if torch.cuda.is_available() else 'cpu').manual_seed(666)
        
        generated_images = []
        
        for i in range(num_images):
            print(f"🖼️ Generating image {i+1}/{num_images}...")
            
            output = pipe(
                image=face_image,
                mask_image=mask_image,
                face_info=face_info,
                prompt=prompt,
                negative_prompt=negative_prompt,
                ip_adapter_scale=0.8,
                lora_scale=0.8,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                height=1280,
                width=960,
                generator=generator,
            ).images[0]
            
            # Save generated image
            output_path = f'static/results/{session_id}_{i}.jpg'
            output.save(output_path)
            generated_images.append(f'/{output_path}')
            
            print(f"✅ Saved image {i+1} to {output_path}")
        
        return {
            "success": True,
            "images": generated_images,
            "session_id": session_id,
            "face_detected": True,
            "num_generated": len(generated_images)
        }
        
    except Exception as e:
        print(f"❌ Error in generation: {str(e)}")
        print(traceback.format_exc())
        return {
            "success": False,
            "error": f"Generation failed: {str(e)}"
        }

def generate_demo_images(session_id, num_images, prompt):
    """
    Generate demo placeholder images when the actual pipeline is not available
    """
    print("🎭 Running in demo mode - generating placeholder images...")
    
    generated_images = []
    
    for i in range(num_images):
        # Create a simple colored image as placeholder
        img = Image.new('RGB', (960, 1280), color=(100 + i*30, 150 + i*20, 200 + i*10))
        
        # Add some text to make it look like a generated image
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(img)
        
        try:
            # Try to use a default font
            font = ImageFont.load_default()
        except:
            font = None
        
        text = f"Demo Story Image {i+1}\n\nPrompt: {prompt[:50]}..."
        draw.text((50, 50), text, fill=(255, 255, 255), font=font)
        
        # Save the demo image
        output_path = f'static/results/{session_id}_{i}.jpg'
        img.save(output_path)
        generated_images.append(f'/{output_path}')
    
    return {
        "success": True,
        "images": generated_images,
        "session_id": session_id,
        "face_detected": True,
        "num_generated": len(generated_images),
        "demo_mode": True
    }
