#!/bin/bash

# Start the Python backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py &
BACKEND_PID=$!

# Start the Tauri frontend
cd ../frontend
npm install
npm run tauri dev &
FRONTEND_PID=$!

# Function to handle script termination
cleanup() {
    echo "Shutting down..."
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit 0
}

# Register the cleanup function for when the script receives a termination signal
trap cleanup SIGINT SIGTERM

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID 