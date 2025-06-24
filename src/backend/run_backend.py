#!/usr/bin/env python3
"""
Run the FastAPI backend server
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import uvicorn
    
    print("Starting GenAI Document Assistant Backend...")
    print("Backend will be available at: http://localhost:8000")
    print("API docs available at: http://localhost:8000/docs")
    
    # Import the app here to avoid import issues
    from api import app
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
