#!/bin/bash

# Veswo Assistant Build Script
# This script builds the application for distribution

set -e

echo "🚀 Building Veswo Assistant..."

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

# Check prerequisites
print_status "Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is required but not installed"
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    print_error "Node.js is required but not installed"
    exit 1
fi

# Check npm
if ! command -v npm &> /dev/null; then
    print_error "npm is required but not installed"
    exit 1
fi

# Check Rust
if ! command -v cargo &> /dev/null; then
    print_error "Rust is required but not installed"
    exit 1
fi

print_success "All prerequisites are installed"

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

# Setup frontend
print_status "Setting up frontend..."
cd frontend
npm install
print_success "Frontend dependencies installed"

# Build the application
print_status "Building Veswo Assistant..."
npm run tauri build

# Check if build was successful
if [ $? -eq 0 ]; then
    print_success "Build completed successfully!"
    
    # Show where the built files are
    echo ""
    print_status "Built files are located in:"
    echo "  📦 macOS: frontend/src-tauri/target/release/bundle/dmg/"
    echo "  📦 Windows: frontend/src-tauri/target/release/bundle/msi/"
    echo "  📦 Linux: frontend/src-tauri/target/release/bundle/appimage/"
    echo "  📦 Linux: frontend/src-tauri/target/release/bundle/deb/"
    
    echo ""
    print_success "🎉 Veswo Assistant is ready for distribution!"
    
    # Show file sizes
    echo ""
    print_status "Package sizes:"
    if [ -d "src-tauri/target/release/bundle/dmg" ]; then
        for file in src-tauri/target/release/bundle/dmg/*.dmg; do
            if [ -f "$file" ]; then
                size=$(du -h "$file" | cut -f1)
                echo "  📱 macOS: $(basename "$file") ($size)"
            fi
        done
    fi
    
    if [ -d "src-tauri/target/release/bundle/msi" ]; then
        for file in src-tauri/target/release/bundle/msi/*.msi; do
            if [ -f "$file" ]; then
                size=$(du -h "$file" | cut -f1)
                echo "  🪟 Windows: $(basename "$file") ($size)"
            fi
        done
    fi
    
    if [ -d "src-tauri/target/release/bundle/appimage" ]; then
        for file in src-tauri/target/release/bundle/appimage/*.AppImage; do
            if [ -f "$file" ]; then
                size=$(du -h "$file" | cut -f1)
                echo "  🐧 Linux: $(basename "$file") ($size)"
            fi
        done
    fi
    
else
    print_error "Build failed!"
    exit 1
fi

cd ..
print_success "Build script completed!" 