#!/bin/bash

echo "🚀 Starting StoryMaker with Fal AI Integration..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Creating template..."
    cat > .env << EOF
# Fal AI Configuration
FAL_API_KEY=your-fal-api-key-here

# Application Settings
APP_SECRET_KEY=storymaker-secret-key-2024
DEBUG=False
MAX_FILE_SIZE=10485760
GENERATION_TIMEOUT=300

# Model Settings
DEFAULT_MODEL=fal-ai/flux/schnell
IMAGE_WIDTH=1024
IMAGE_HEIGHT=1024
DEFAULT_STEPS=25
DEFAULT_GUIDANCE=7.5
EOF
    echo "📝 Please update the .env file with your actual Fal API key"
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p static/input static/mask static/results logs templates config services scripts

# Start the application
echo "🎨 Starting StoryMaker application..."
echo "🌐 Access the app at: http://localhost:7860"
echo "📊 Health check at: http://localhost:7860/health"
echo "🖼️  Gallery at: http://localhost:7860/gallery"

uvicorn app:app --host 0.0.0.0 --port 7860 --reload
