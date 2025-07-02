#!/bin/bash

# veswo1-bot Startup Script
# This script starts both the backend and frontend with proper GPT-2 initialization

echo "🚀 Starting veswo1-bot with GPT-2..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if a port is in use
port_in_use() {
    lsof -i :$1 >/dev/null 2>&1
}

# Check prerequisites
echo -e "${BLUE}📋 Checking prerequisites...${NC}"

# Check Python
if ! command_exists python3; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

# Check Node.js
if ! command_exists node; then
    echo -e "${RED}❌ Node.js is not installed. Please install Node.js 16 or higher.${NC}"
    exit 1
fi

# Check Rust
if ! command_exists cargo; then
    echo -e "${RED}❌ Rust is not installed. Please install Rust.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ All prerequisites are installed${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${BLUE}🔧 Activating virtual environment...${NC}"
source venv/bin/activate

# Install Python dependencies
echo -e "${BLUE}📦 Installing Python dependencies...${NC}"
pip install -r requirements.txt

# Check if frontend dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${YELLOW}📦 Installing frontend dependencies...${NC}"
    cd frontend
    npm install
    cd ..
fi

# Kill any existing processes on ports 8000 and 1420
echo -e "${BLUE}🧹 Cleaning up existing processes...${NC}"
if port_in_use 8000; then
    echo -e "${YELLOW}⚠️  Port 8000 is in use. Killing existing process...${NC}"
    lsof -ti:8000 | xargs kill -9
fi

if port_in_use 1420; then
    echo -e "${YELLOW}⚠️  Port 1420 is in use. Killing existing process...${NC}"
    lsof -ti:1420 | xargs kill -9
fi

# Start backend in background
echo -e "${BLUE}🔧 Starting backend server...${NC}"
cd backend
source ../venv/bin/activate
echo -e "${YELLOW}🔄 Initializing GPT-2 model (this may take a few minutes on first run)...${NC}"
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# Wait for backend to be ready
echo -e "${BLUE}⏳ Waiting for backend to initialize...${NC}"
for i in {1..60}; do
    if curl -s http://localhost:8000/health >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Backend is ready!${NC}"
        break
    fi
    if [ $i -eq 60 ]; then
        echo -e "${RED}❌ Backend failed to start within 60 seconds${NC}"
        kill $BACKEND_PID 2>/dev/null
        exit 1
    fi
    echo -n "."
    sleep 1
done

# Check GPT-2 status
echo -e "${BLUE}🧠 Checking GPT-2 model status...${NC}"
GPT2_READY=false
for i in {1..30}; do
    STATUS_RESPONSE=$(curl -s http://localhost:8000/api/status 2>/dev/null)
    if echo "$STATUS_RESPONSE" | grep -q '"gpt2_ready":true'; then
        echo -e "${GREEN}✅ GPT-2 model is ready!${NC}"
        GPT2_READY=true
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${RED}❌ GPT-2 model failed to initialize within 30 seconds${NC}"
        echo -e "${YELLOW}⚠️  The app will start but GPT-2 may not be fully ready${NC}"
    fi
    echo -n "."
    sleep 2
done

# Start frontend
echo -e "${BLUE}🎨 Starting frontend...${NC}"
cd frontend
npm run tauri dev &
FRONTEND_PID=$!
cd ..

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down veswo1-bot...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}✅ veswo1-bot stopped${NC}"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

echo -e "${GREEN}🎉 veswo1-bot is starting!${NC}"
echo -e "${BLUE}📱 Frontend will open automatically${NC}"
echo -e "${BLUE}🌐 Backend API: http://localhost:8000${NC}"
echo -e "${BLUE}🧠 GPT-2 Status: $([ "$GPT2_READY" = true ] && echo "Ready" || echo "Initializing")${NC}"
echo -e "${YELLOW}💡 Press Ctrl+C to stop the application${NC}"

# Wait for processes
wait 