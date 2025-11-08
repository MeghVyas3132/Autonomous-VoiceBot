#!/bin/bash

# Setup script for Offline VoiceBot

echo "🎤 Setting up Offline VoiceBot..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

echo "✓ Python $(python3 --version) found"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "✓ Virtual environment created"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo "✓ Dependencies installed"
echo ""

# Check for Vosk model
echo "🔍 Checking for Vosk model..."
VOSK_MODEL_PATH="$HOME/.vosk/model-en-us"

if [ -d "$VOSK_MODEL_PATH" ]; then
    echo "✓ Vosk model found at $VOSK_MODEL_PATH"
else
    echo "⚠️  Vosk model not found"
    echo ""
    echo "📥 To download the model, run:"
    echo "   mkdir -p ~/.vosk"
    echo "   wget https://alphacephei.com/vosk/models/model-en-us-0.22.zip"
    echo "   unzip model-en-us-0.22.zip"
    echo "   mv model-en-us-0.22 ~/.vosk/model-en-us"
    echo ""
    echo "Or download manually from: https://alphacephei.com/vosk/models"
fi

echo ""
echo "✨ Setup complete!"
echo ""
echo "🚀 To start VoiceBot, run:"
echo "   source venv/bin/activate"
echo "   python src/main.py"
echo ""
