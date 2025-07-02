#!/bin/bash

# veswo1-bot Build Script
# This script builds the complete application package

set -e

echo "🚀 Building veswo1-bot..."

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
if [ ! -f "start.sh" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Make sure all scripts are executable
chmod +x start.sh
chmod +x launcher.sh
chmod +x run.sh
chmod +x dev.sh

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🐍 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🐍 Activating virtual environment..."
source venv/bin/activate

# Install backend dependencies
echo "📦 Installing backend dependencies..."
pip install -r requirements.txt

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install

# Build the Tauri application
echo "🔨 Building Tauri application..."
npm run tauri build

echo "✅ Build completed!"
echo ""
echo "📦 Your application has been built and is ready to run."
echo "🎯 To launch the application:"
echo "   - Double-click the .app file in frontend/src-tauri/target/release/bundle/macos/"
echo "   - Or run: ./start.sh (for development)"
echo ""
echo "📁 Build artifacts are in: frontend/src-tauri/target/release/bundle/"

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
    print_success "🎉 veswo1-bot is ready for distribution!"
    
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