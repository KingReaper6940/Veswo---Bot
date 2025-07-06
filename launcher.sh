#!/bin/bash

# veswo1-bot Launcher (Robust DMG Edition)
# This script is used by the packaged Tauri app to start the backend and install all dependencies if needed

set -e

# Helper function for colored output
echo_info() { echo -e "\033[1;34m[INFO]\033[0m $1"; }
echo_warn() { echo -e "\033[1;33m[WARN]\033[0m $1"; }
echo_error() { echo -e "\033[1;31m[ERROR]\033[0m $1"; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(dirname "$SCRIPT_DIR")"

# Detect mode
echo_info "Starting veswo1-bot..."
if [ -d "$APP_DIR/backend" ]; then
    BACKEND_DIR="$APP_DIR/backend"
    VENV_DIR="$APP_DIR/venv"
    echo_info "Development mode detected"
else
    BACKEND_DIR="$APP_DIR/Contents/Resources/backend"
    VENV_DIR="$APP_DIR/Contents/Resources/venv"
    echo_info "Packaged mode detected"
fi

echo_info "Backend directory: $BACKEND_DIR"
echo_info "Virtual environment: $VENV_DIR"

# 1. Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo_error "Python 3 is not installed."
    echo_info "Please install Python 3.8 or higher from: https://www.python.org/downloads/macos/"
    osascript -e 'display dialog "Python 3 is required. Please install it from https://www.python.org/downloads/macos/ and relaunch the app." with title "veswo1-bot: Python Required" buttons {"OK"}' || true
    exit 1
fi

# 2. Check backend directory
if [ ! -d "$BACKEND_DIR" ]; then
    echo_error "Backend directory not found at: $BACKEND_DIR"
    osascript -e 'display dialog "Backend directory not found. Please reinstall the app or contact support." with title "veswo1-bot: Error" buttons {"OK"}' || true
    exit 1
fi

# 3. Create or activate virtual environment
echo_info "Checking Python virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    echo_info "Creating virtual environment..."
    python3 -m venv "$VENV_DIR" || { echo_error "Failed to create virtual environment."; exit 1; }
fi
source "$VENV_DIR/bin/activate"
echo_info "Virtual environment activated."

# 4. Install Python dependencies
echo_info "Installing Python dependencies..."
if [ -f "$BACKEND_DIR/requirements.txt" ]; then
    pip install --upgrade pip --quiet
    pip install -r "$BACKEND_DIR/requirements.txt" --quiet || { echo_error "Failed to install Python dependencies."; exit 1; }
    echo_info "Python dependencies installed."
else
    echo_warn "requirements.txt not found. Skipping Python dependencies."
fi

# 5. Kill any existing backend processes
echo_info "Checking for existing backend processes..."
pkill -f "uvicorn main:app" || true
sleep 2

# 6. Check for Homebrew
if ! command -v brew &> /dev/null; then
    echo_warn "Homebrew is not installed."
    echo_info "Please install Homebrew from: https://brew.sh/"
    osascript -e 'display dialog "Homebrew is required to install Ollama. Please install it from https://brew.sh/ and relaunch the app." with title "veswo1-bot: Homebrew Required" buttons {"OK"}' || true
    exit 1
fi

# 7. Check for Ollama
if ! command -v ollama &> /dev/null; then
    echo_warn "Ollama is not installed. Attempting to install via Homebrew..."
    brew install ollama || {
        echo_error "Failed to install Ollama via Homebrew."
        echo_info "You can also download Ollama directly from: https://ollama.com/download"
        osascript -e 'display dialog "Ollama is required. Please install it from https://ollama.com/download and relaunch the app." with title "veswo1-bot: Ollama Required" buttons {"OK"}' || true
        exit 1
    }
else
    echo_info "Ollama is already installed."
fi

# 8. Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo_info "Starting Ollama server..."
    ollama serve &
    OLLAMA_PID=$!
    sleep 5
else
    echo_info "Ollama is already running."
fi

# 9. Check if Gemma model is pulled
echo_info "Checking for Gemma model..."
if ! ollama list | grep -q "gemma"; then
    echo_info "Pulling Gemma model (this may take a while)..."
    ollama pull gemma || { echo_error "Failed to pull Gemma model."; exit 1; }
else
    echo_info "Gemma model is already available."
fi

# 10. Wait for Ollama to be ready
OLLAMA_READY=0
echo_info "Waiting for Ollama server to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo_info "Ollama server is ready!"
        OLLAMA_READY=1
        break
    fi
    echo_info "Waiting for Ollama server... ($i/30)"
    sleep 2
done
if [ $OLLAMA_READY -eq 0 ]; then
    echo_error "Ollama server did not become ready in time."
    exit 1
fi

# 11. Start the backend server
echo_info "Starting backend server..."
cd "$BACKEND_DIR"
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

echo_info "Backend server started with PID: $BACKEND_PID"
echo_info "Server running at: http://localhost:8000"

echo_info "Waiting for backend to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:8000/api/status > /dev/null 2>&1; then
        echo_info "Backend is ready!"
        break
    fi
    echo_info "Waiting... ($i/30)"
    sleep 2
done

echo_info "Backend server is running. Press Ctrl+C to stop."
wait $BACKEND_PID 