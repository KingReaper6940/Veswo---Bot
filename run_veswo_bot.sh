#!/bin/bash

# Veswo Bot Launcher Script
# This script removes quarantine attributes and launches Veswo Bot

APP_PATH="./frontend/src-tauri/target/release/bundle/macos/veswo1-bot.app"

echo "🚀 Launching Veswo Bot..."

# Check if app exists
if [ ! -d "$APP_PATH" ]; then
    echo "❌ App not found at $APP_PATH"
    echo "Please run 'npm run tauri build' in the frontend directory first."
    exit 1
fi

# Remove quarantine attributes
echo "🔓 Removing quarantine attributes..."
xattr -dr com.apple.quarantine "$APP_PATH" 2>/dev/null
xattr -dr com.apple.provenance "$APP_PATH" 2>/dev/null

# Launch the app
echo "🎯 Launching Veswo Bot..."
open "$APP_PATH"

echo "✅ Veswo Bot should now be running!"
echo "💡 If you see a security warning, right-click the app and select 'Open'" 