# 🎨 StoryMaker Dynamic Image Generator

A fully functional web application that transforms your photos into creative AI-generated story scenes using advanced Stable Diffusion XL technology.

## 🚀 Quick Start (Terminal Commands)

### Step 1: Clone and Setup
\`\`\`bash
# Clone the StoryMaker repository
git clone https://github.com/RedAIGC/StoryMaker.git
cd StoryMaker

# Make setup script executable
chmod +x scripts/setup.sh

# Run the setup script
./scripts/setup.sh
\`\`\`

### Step 2: Manual Installation (Alternative)
\`\`\`bash
# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Upgrade pip
pip install --upgrade pip

# Install PyTorch with CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install other dependencies
pip install opencv-python numpy Pillow transformers diffusers
pip install insightface accelerate fastapi uvicorn python-multipart
pip install jinja2 aiofiles safetensors xformers

# Create directory structure
mkdir -p static/input static/mask static/results
mkdir -p models checkpoints templates
\`\`\`

### Step 3: Download Models
\`\`\`bash
# Run the model installation script
python scripts/install_models.py

# Or manually download InsightFace models
python -c "
import insightface
app = insightface.app.FaceAnalysis(name='buffalo_l')
app.prepare(ctx_id=0, det_size=(640, 640))
print('InsightFace models downloaded!')
"
\`\`\`

### Step 4: Download StoryMaker Checkpoints
\`\`\`bash
# Create checkpoints directory
mkdir -p checkpoints

# Download mask.bin (replace URL with actual checkpoint URL)
# wget -O checkpoints/mask.bin [CHECKPOINT_URL]

# For now, you'll need to manually download:
# - mask.bin -> checkpoints/mask.bin
# - Any other required model files
\`\`\`

### Step 5: Run the Application
\`\`\`bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Start the FastAPI server
uvicorn app:app --host 0.0.0.0 --port 7860

# Or run with auto-reload for development
uvicorn app:app --host 0.0.0.0 --port 7860 --reload
\`\`\`

### Step 6: Access the Application
Open your browser and navigate to:
\`\`\`
http://localhost:7860
\`\`\`

## 🖥️ Terminal Commands Summary

\`\`\`bash
# Complete setup in one go
git clone https://github.com/RedAIGC/StoryMaker.git
cd StoryMaker
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python scripts/install_models.py
uvicorn app:app --host 0.0.0.0 --port 7860
\`\`\`

## 🎯 Features

- **🖼️ Image Upload**: Upload face images and optional mask images
- **✨ AI Generation**: Generate creative story scenes using SDXL
- **🎨 Customization**: Adjust prompts, negative prompts, and generation parameters
- **📱 Responsive UI**: Modern, mobile-friendly interface
- **📥 Download**: Download individual images or all at once
- **🖼️ Gallery**: View all previously generated images

## 🔧 Configuration

### Environment Variables
Create a \`.env\` file with:
\`\`\`
CUDA_VISIBLE_DEVICES=0  # GPU device to use
MODEL_CACHE_DIR=./models  # Model cache directory
\`\`\`

### Advanced Settings
- **Number of Images**: 1-8 images per generation
- **Guidance Scale**: 1-20 (controls adherence to prompt)
- **Inference Steps**: 10-50 (quality vs speed trade-off)

## 📚 Example Prompts

### Creative Scenes
- "a person reading a book under a cherry blossom tree in Kyoto"
- "a person exploring a neon-lit cyberpunk city"
- "a person sitting on Mars in a futuristic space suit"
- "a person standing near the Eiffel Tower during sunset, wearing a scarf"

### Fantasy & Adventure
- "a person in traditional Japanese attire walking through a misty forest"
- "a person as a medieval knight in an enchanted castle"
- "a person as a space explorer on an alien planet"

## 🛠️ Troubleshooting

### Common Issues

**CUDA Out of Memory**
\`\`\`bash
# Reduce image resolution or batch size
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
\`\`\`

**Missing Models**
\`\`\`bash
# Re-run model installation
python scripts/install_models.py
\`\`\`

**Port Already in Use**
\`\`\`bash
# Use a different port
uvicorn app:app --host 0.0.0.0 --port 8000
\`\`\`

### Logs and Debugging
\`\`\`bash
# Run with verbose logging
uvicorn app:app --host 0.0.0.0 --port 7860 --log-level debug

# Check GPU availability
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
\`\`\`

## 🚀 Deployment

### Local Development
\`\`\`bash
uvicorn app:app --host 127.0.0.1 --port 7860 --reload
\`\`\`

### Production
\`\`\`bash
uvicorn app:app --host 0.0.0.0 --port 7860 --workers 1
\`\`\`

### Docker (Optional)
\`\`\`bash
# Build Docker image
docker build -t storymaker .

# Run container
docker run -p 7860:7860 --gpus all storymaker
\`\`\`

## 📋 Requirements

- **Python**: 3.8+
- **GPU**: CUDA-compatible GPU (recommended)
- **Memory**: 8GB+ RAM, 6GB+ VRAM
- **Storage**: 10GB+ for models and checkpoints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section
2. Review the logs for error messages
3. Open an issue on GitHub
4. Join our community discussions

---

**Happy Story Making! 🎨✨**
\`\`\`
