#!/bin/bash

echo "🚀 Setting up StoryMaker Dynamic Image Generator..."

# Step 1: Clone the GitHub repository
echo "📥 Cloning StoryMaker repository..."
git clone https://github.com/RedAIGC/StoryMaker.git
cd StoryMaker

# Step 2: Create Python virtual environment
echo "🐍 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Step 3: Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Step 4: Install core dependencies
echo "📚 Installing core dependencies..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install opencv-python
pip install numpy
pip install Pillow
pip install transformers
pip install diffusers
pip install insightface
pip install accelerate
pip install fastapi
pip install uvicorn
pip install python-multipart
pip install jinja2
pip install aiofiles

# Step 5: Create directory structure
echo "🧱 Creating directory structure..."
mkdir -p static/input static/mask static/results
mkdir -p models checkpoints templates

# Step 6: Download InsightFace models
echo "🤖 Downloading InsightFace models..."
python3 -c "
import insightface
app = insightface.app.FaceAnalysis(name='buffalo_l')
app.prepare(ctx_id=0, det_size=(640, 640))
print('InsightFace models downloaded successfully!')
"

# Step 7: Create requirements.txt
echo "📝 Creating requirements.txt..."
cat > requirements.txt << EOF
torch>=2.0.0
torchvision>=0.15.0
torchaudio>=2.0.0
opencv-python>=4.8.0
numpy>=1.24.0
Pillow>=10.0.0
transformers>=4.30.0
diffusers>=0.20.0
insightface>=0.7.3
accelerate>=0.20.0
fastapi>=0.100.0
uvicorn>=0.23.0
python-multipart>=0.0.6
jinja2>=3.1.0
aiofiles>=23.0.0
safetensors>=0.3.0
xformers>=0.0.20
EOF

echo "✅ Setup complete! Run 'uvicorn app:app --host 0.0.0.0 --port 7860' to start the server."
