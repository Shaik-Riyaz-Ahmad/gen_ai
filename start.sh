#!/bin/bash

echo "🚀 Starting GenAI Document Assistant..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Please copy .env.example to .env and add your Gemini API key."
    exit 1
fi

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Please run ./setup.sh first."
    exit 1
fi

# Start backend server in background
echo "📡 Starting backend server..."
cd src/backend
python run_backend.py &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 8

# Check if backend is running
if ! curl -s http://localhost:8000/health/ > /dev/null; then
    echo "❌ Backend failed to start. Please check the logs."
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo "✅ Backend started successfully!"

# Start frontend
echo "🎨 Starting frontend..."
cd ..
streamlit run app.py

# Cleanup when script exits
trap "echo '🛑 Shutting down servers...'; kill $BACKEND_PID 2>/dev/null" EXIT
