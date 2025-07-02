#!/bin/bash

# veswo1-bot Development Script
# This script starts the development environment

set -e

echo "🚀 Starting veswo1-bot Development Environment..."

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
    print_status "Shutting down development environment..."
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
pip install --upgrade pip
pip install -r requirements.txt
print_success "Python dependencies installed"

# Start backend
print_status "Starting backend server..."
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 2

# Check if backend is running
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    print_warning "Backend health check failed, but continuing..."
else
    print_success "Backend server is running on http://localhost:8000"
fi

# Start frontend
print_status "Starting frontend development server..."
cd frontend
npm run tauri dev &
FRONTEND_PID=$!
cd ..

print_success "Development environment started!"
echo ""
print_status "Services running:"
echo "  🔧 Backend API: http://localhost:8000"
echo "  📱 Frontend: http://localhost:1420"
echo "  📚 API Docs: http://localhost:8000/docs"
echo ""
print_status "Press Ctrl+C to stop all services"

# Wait for user to stop
wait 