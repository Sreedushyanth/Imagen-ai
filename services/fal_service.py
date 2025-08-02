import asyncio
import base64
import io
from typing import List, Dict, Any, Optional
from PIL import Image
import httpx
from config.settings import settings

class FalAIService:
    """Service for integrating with Fal AI API"""
    
    def __init__(self):
        self.api_key = settings.fal_api_key
        self.base_url = "https://fal.run/fal-ai"
        self.timeout = settings.generation_timeout
        
        if not self.api_key:
            raise ValueError("FAL_API_KEY not found in environment variables")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers with authentication"""
        return {
            "Authorization": f"Key {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _encode_image_to_base64(self, image_path: str) -> str:
        """Encode image file to base64 string"""
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize if too large
                max_size = 1024
                if max(img.size) > max_size:
                    img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                
                # Convert to base64
                buffered = io.BytesIO()
                img.save(buffered, format="JPEG", quality=90)
                img_str = base64.b64encode(buffered.getvalue()).decode()
                return f"data:image/jpeg;base64,{img_str}"
        except Exception as e:
            raise ValueError(f"Failed to process image: {str(e)}")
    
    async def generate_story_images(
        self,
        face_image_path: str,
        prompt: str,
        negative_prompt: str = "",
        mask_image_path: Optional[str] = None,
        num_images: int = 4,
        guidance_scale: float = 7.5,
        num_inference_steps: int = 25,
        width: int = 1024,
        height: int = 1024
    ) -> Dict[str, Any]:
        """
        Generate story images using Fal AI
        """
        try:
            print(f"🎨 Starting Fal AI generation for {num_images} images...")
            
            # Encode face image
            face_image_b64 = self._encode_image_to_base64(face_image_path)
            
            # Encode mask image if provided
            mask_image_b64 = None
            if mask_image_path:
                mask_image_b64 = self._encode_image_to_base64(mask_image_path)
            
            # Prepare the payload for Fal AI
            payload = {
                "prompt": f"professional portrait, {prompt}",
                "negative_prompt": negative_prompt,
                "image": face_image_b64,
                "guidance_scale": guidance_scale,
                "num_inference_steps": num_inference_steps,
                "width": width,
                "height": height,
                "num_images": num_images,
                "safety_checker": True,
                "enhance_face": True
            }
            
            # Add mask if provided
            if mask_image_b64:
                payload["mask_image"] = mask_image_b64
                payload["strength"] = 0.8
            
            print(f"📡 Sending request to Fal AI...")
            
            # Make the API request
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/flux/schnell",
                    headers=self._get_headers(),
                    json=payload
                )
                
                if response.status_code != 200:
                    error_detail = response.text
                    print(f"❌ Fal AI API error: {response.status_code} - {error_detail}")
                    return {
                        "success": False,
                        "error": f"API error: {response.status_code} - {error_detail}"
                    }
                
                result = response.json()
                print(f"✅ Fal AI generation completed successfully!")
                
                return {
                    "success": True,
                    "images": result.get("images", []),
                    "generation_time": result.get("timings", {}).get("inference", 0),
                    "model_used": "fal-ai/flux/schnell",
                    "parameters": {
                        "guidance_scale": guidance_scale,
                        "num_inference_steps": num_inference_steps,
                        "width": width,
                        "height": height
                    }
                }
                
        except httpx.TimeoutException:
            return {
                "success": False,
                "error": "Generation timeout. Please try again with fewer images or simpler prompts."
            }
        except Exception as e:
            print(f"❌ Error in Fal AI generation: {str(e)}")
            return {
                "success": False,
                "error": f"Generation failed: {str(e)}"
            }
    
    async def generate_with_face_swap(
        self,
        face_image_path: str,
        target_image_path: str
    ) -> Dict[str, Any]:
        """Generate image with face swap using Fal AI"""
        try:
            face_image_b64 = self._encode_image_to_base64(face_image_path)
            target_image_b64 = self._encode_image_to_base64(target_image_path)
            
            payload = {
                "source_image": face_image_b64,
                "target_image": target_image_b64
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/face-swap",
                    headers=self._get_headers(),
                    json=payload
                )
                
                if response.status_code != 200:
                    return {
                        "success": False,
                        "error": f"Face swap failed: {response.status_code}"
                    }
                
                result = response.json()
                return {
                    "success": True,
                    "image": result.get("image"),
                    "model_used": "fal-ai/face-swap"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Face swap failed: {str(e)}"
            }

# Global service instance
fal_service = FalAIService()
