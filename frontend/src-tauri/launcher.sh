#!/bin/bash
set -e

cd "$(dirname "$0")/../.."

# Kill any process using port 8000
if lsof -ti:8000 &> /dev/null; then
  echo "Killing process on port 8000..."
  lsof -ti:8000 | xargs kill -9
fi

# Check for uvicorn
if ! command -v uvicorn &> /dev/null; then
  echo "❌ uvicorn not found. Please install it in your venv (pip install uvicorn)"; exit 1
fi
# Check for ollama
if ! command -v ollama &> /dev/null; then
  echo "❌ ollama not found. Please install it (brew install ollama or https://ollama.com/download)"; exit 1
fi

# Start Ollama if not running
if ! pgrep -x "ollama" > /dev/null; then
  echo "Starting Ollama..."
  ollama serve &
  sleep 2
fi

# Pull Gemma model if not present
if ! ollama list | grep -q gemma; then
  echo "Pulling Gemma model..."
  ollama pull gemma
fi

# Activate venv
source venv/bin/activate

# Start backend from project root
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Wait for backend to be ready
for i in {1..30}; do
  STATUS=$(curl -s http://localhost:8000/api/status || true)
  if [[ "$STATUS" == *"ready"* ]]; then
    echo "Backend is ready!"
    break
  fi
  echo "Waiting for backend... ($i)"
  sleep 2
done

if ! kill -0 $BACKEND_PID 2>/dev/null; then
  echo "Backend failed to start."
  exit 1
fi

wait $BACKEND_PID 