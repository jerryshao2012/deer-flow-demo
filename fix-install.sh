#!/bin/bash

# Fix the deerflow module import issue

set -e

echo "🔧 Fixing DeerFlow installation..."

# Navigate to backend directory
cd "$(dirname "$0")/deer-flow/backend"

echo "📦 Running uv sync to install dependencies..."
uv sync

echo "✅ Installation complete!"
echo ""
echo "Now try running start.sh again:"
echo "  cd .. && ./start.sh"
