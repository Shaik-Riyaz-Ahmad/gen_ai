#!/bin/bash

echo "🔧 Setting up GenAI Document Assistant..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip is not installed. Please install pip first."
    exit 1
fi

# Use pip3 if available, otherwise pip
PIP_CMD="pip"
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
fi

echo "📦 Installing Python dependencies..."
$PIP_CMD install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your Gemini API key!"
    echo "   Get your API key from: https://makersuite.google.com/app/apikey"
fi

# Create uploads directory
mkdir -p uploads

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your Gemini API key"
echo "2. Run: ./start.sh to start the application"
echo ""
echo "📚 Get your Gemini API key:"
echo "   Visit: https://makersuite.google.com/app/apikey"
