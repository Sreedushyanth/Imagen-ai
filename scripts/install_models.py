#!/usr/bin/env python3
"""
Model installation script for StoryMaker
Downloads and sets up all required models and checkpoints
"""

import os
import sys
import urllib.request
import zipfile
import tarfile
from pathlib import Path
import subprocess

def download_file(url, destination):
    """Download a file with progress indication"""
    print(f"📥 Downloading {os.path.basename(destination)}...")
    try:
        urllib.request.urlretrieve(url, destination)
        print(f"✅ Downloaded {os.path.basename(destination)}")
        return True
    except Exception as e:
        print(f"❌ Failed to download {os.path.basename(destination)}: {e}")
        return False

def setup_insightface_models():
    """Setup InsightFace models"""
    print("🤖 Setting up InsightFace models...")
    try:
        import insightface
        app = insightface.app.FaceAnalysis(name='buffalo_l')
        app.prepare(ctx_id=0, det_size=(640, 640))
        print("✅ InsightFace models installed successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to setup InsightFace models: {e}")
        return False

def download_storymaker_checkpoints():
    """Download StoryMaker specific checkpoints"""
    print("📦 Setting up StoryMaker checkpoints...")
    
    checkpoints_dir = Path("checkpoints")
    checkpoints_dir.mkdir(exist_ok=True)
    
    # Note: Replace these URLs with actual checkpoint URLs when available
    checkpoints = {
        "mask.bin": "https://example.com/mask.bin",  # Replace with actual URL
        # Add more checkpoints as needed
    }
    
    success = True
    for filename, url in checkpoints.items():
        destination = checkpoints_dir / filename
        if not destination.exists():
            print(f"⚠️  Checkpoint {filename} not found. Please download manually from:")
            print(f"   {url}")
            print(f"   Save to: {destination}")
            success = False
        else:
            print(f"✅ Checkpoint {filename} already exists")
    
    return success

def install_python_dependencies():
    """Install Python dependencies"""
    print("📚 Installing Python dependencies...")
    
    requirements = [
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        "torchaudio>=2.0.0",
        "opencv-python>=4.8.0",
        "numpy>=1.24.0",
        "Pillow>=10.0.0",
        "transformers>=4.30.0",
        "diffusers>=0.20.0",
        "insightface>=0.7.3",
        "accelerate>=0.20.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.23.0",
        "python-multipart>=0.0.6",
        "jinja2>=3.1.0",
        "aiofiles>=23.0.0",
        "safetensors>=0.3.0",
    ]
    
    try:
        for requirement in requirements:
            print(f"Installing {requirement}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", requirement])
        print("✅ All Python dependencies installed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def main():
    """Main installation function"""
    print("🚀 Starting StoryMaker installation...")
    
    # Create necessary directories
    directories = ["static/input", "static/mask", "static/results", "models", "checkpoints", "templates"]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {directory}")
    
    # Install Python dependencies
    if not install_python_dependencies():
        print("❌ Failed to install Python dependencies")
        return False
    
    # Setup InsightFace models
    if not setup_insightface_models():
        print("❌ Failed to setup InsightFace models")
        return False
    
    # Download StoryMaker checkpoints
    if not download_storymaker_checkpoints():
        print("⚠️  Some checkpoints are missing. Please download them manually.")
    
    print("🎉 Installation completed!")
    print("\n📋 Next steps:")
    print("1. Download the required checkpoints (mask.bin) if not already done")
    print("2. Run: uvicorn app:app --host 0.0.0.0 --port 7860")
    print("3. Open http://localhost:7860 in your browser")
    
    return True

if __name__ == "__main__":
    main()
