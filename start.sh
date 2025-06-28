#!/bin/bash

# Veswo Assistant Startup Script
# This script ensures both backend and frontend are running correctly

set -e

echo "🚀 Starting Veswo Assistant..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

# Function to cleanup on exit
cleanup() {
    print_status "Shutting down Veswo Assistant..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Setup Python environment
print_status "Setting up Python environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Created virtual environment"
fi

source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
print_success "Python dependencies installed"

# Start backend
print_status "Starting backend server..."
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Test backend connection
print_status "Testing backend connection..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    print_success "Backend server is running on http://localhost:8000"
else
    print_warning "Backend health check failed, but continuing..."
fi

# Test a simple API call
if curl -s -X POST http://localhost:8000/api/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "test"}' > /dev/null 2>&1; then
    print_success "Backend API is responding correctly"
else
    print_error "Backend API is not responding"
    exit 1
fi

# Setup frontend
print_status "Setting up frontend..."
cd frontend
npm install > /dev/null 2>&1
print_success "Frontend dependencies installed"

# Start frontend
print_status "Starting frontend development server..."
npm run tauri dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

print_success "Veswo Assistant started successfully!"
echo ""
print_status "Services running:"
echo "  🔧 Backend API: http://localhost:8000"
echo "  📱 Frontend: http://localhost:1420"
echo "  📚 API Docs: http://localhost:8000/docs"
echo ""
print_status "Logs:"
echo "  📄 Backend: tail -f backend.log"
echo "  📄 Frontend: tail -f frontend.log"
echo ""
print_status "Press Ctrl+C to stop all services"

# Wait for user to stop
wait 