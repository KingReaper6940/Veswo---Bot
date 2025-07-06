#!/bin/bash
set -e

# Clean Tauri and Node build artifacts
echo "[Clean] Removing old build artifacts..."
cd frontend
rm -rf node_modules src-tauri/target dist

echo "[Clean] Installing Node dependencies..."
npm install

echo "[Clean] Running Tauri build..."
npm run tauri:build

echo "[Clean] Build complete! Check src-tauri/target/release/bundle/macos/ for the .app and src-tauri/target/release/bundle/dmg/ for the DMG." 