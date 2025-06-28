#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Error: .env file not found"
    exit 1
fi

# Run the application
cd backend
python main.py

# Deactivate virtual environment if it was activated
if [ -n "$VIRTUAL_ENV" ]; then
    deactivate
fi 

# Run the Tkinter app
python app.py

curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

cd frontend/src-tauri
cargo build

cd ..
npm install
npm run tauri dev 