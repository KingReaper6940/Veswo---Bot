#!/bin/bash

# Veswo Assistant Launcher
# This script is used by the packaged Tauri app to start the backend

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(dirname "$SCRIPT_DIR")"

echo "🚀 Starting Veswo Assistant..."

# Check if we're in development mode or packaged mode
if [ -d "$APP_DIR/backend" ]; then
    # Development mode - backend is in the project directory
    BACKEND_DIR="$APP_DIR/backend"
    VENV_DIR="$APP_DIR/venv"
    echo "📁 Development mode detected"
else
    # Packaged mode - backend is in the app bundle
    BACKEND_DIR="$APP_DIR/Contents/Resources/backend"
    VENV_DIR="$APP_DIR/Contents/Resources/venv"
    echo "📦 Packaged mode detected"
fi

echo "🔧 Backend directory: $BACKEND_DIR"
echo "🐍 Virtual environment: $VENV_DIR"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if backend directory exists
if [ ! -d "$BACKEND_DIR" ]; then
    echo "❌ Backend directory not found at: $BACKEND_DIR"
    exit 1
fi

# Activate virtual environment if it exists
if [ -d "$VENV_DIR" ]; then
    echo "🐍 Activating virtual environment..."
    source "$VENV_DIR/bin/activate"
else
    echo "⚠️  Virtual environment not found. Using system Python."
fi

# Install dependencies if requirements.txt exists
if [ -f "$BACKEND_DIR/requirements.txt" ]; then
    echo "📦 Installing Python dependencies..."
    pip install -r "$BACKEND_DIR/requirements.txt" --quiet
fi

# Kill any existing backend processes
echo "🔄 Checking for existing backend processes..."
pkill -f "uvicorn main:app" || true
sleep 2

# Start the backend server
echo "🚀 Starting backend server..."
cd "$BACKEND_DIR"
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

echo "✅ Backend server started with PID: $BACKEND_PID"
echo "🌐 Server running at: http://localhost:8000"

# Wait for the backend to be ready
echo "⏳ Waiting for backend to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:8000/api/status > /dev/null 2>&1; then
        echo "✅ Backend is ready!"
        break
    fi
    echo "⏳ Waiting... ($i/30)"
    sleep 2
done

# Keep the script running to maintain the backend process
echo "🔄 Backend server is running. Press Ctrl+C to stop."
wait $BACKEND_PID 