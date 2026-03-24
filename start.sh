#!/bin/bash

# Quick Start Script for DeerFlow Hello World Demo
# This script helps you start the demo quickly after initial setup

set -e

echo "🦌 ================================================"
echo "   DEERFLOW HELLO WORLD - QUICK START"
echo "=============================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if deer-flow directory exists
if [ ! -d "deer-flow" ]; then
    echo -e "${RED}❌ deer-flow directory not found!${NC}"
    echo "💡 Please run ./setup.sh first to complete initial setup"
    exit 1
fi

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo -e "${YELLOW}⚠️  Ollama server is not running${NC}"
    echo "🚀 Starting Ollama server in background..."
    ollama serve &
    sleep 3
    
    if pgrep -x "ollama" > /dev/null; then
        echo -e "${GREEN}✅ Ollama server started${NC}"
    else
        echo -e "${RED}❌ Failed to start Ollama server${NC}"
        echo "💡 Please start it manually: ollama serve"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Ollama server is running${NC}"
fi

# Check if GLM-4-Flash model exists
if ! ollama list | grep -q "glm-4.7-flash"; then
    echo -e "${RED}❌ GLM-4-Flash model not found!${NC}"
    echo "💡 Please pull the model first:"
    echo "   ollama pull glm-4.7-flash:latest"
    exit 1
else
    echo -e "${GREEN}✅ GLM-4-Flash model found${NC}"
fi

# Navigate to deer-flow directory
cd deer-flow

# Check if .env exists and has Tavily key
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ .env file not found!${NC}"
    echo "💡 Please run ./setup.sh or copy .env.example to .env"
    cd ..
    exit 1
fi

TAVILY_KEY=$(grep "^TAVILY_API_KEY=" .env | cut -d '=' -f 2)
if [ "$TAVILY_KEY" = "your-tavily-api-key-here" ] || [ -z "$TAVILY_KEY" ]; then
    echo -e "${YELLOW}⚠️  Tavily API key not configured!${NC}"
    echo "💡 Edit deer-flow/.env and add your Tavily API key"
    echo "   Get one at: https://app.tavily.com"
    echo ""
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        cd ..
        exit 1
    fi
fi

# Check if config.yaml exists
if [ ! -f "config.yaml" ]; then
    echo -e "${RED}❌ config.yaml not found!${NC}"
    echo "💡 Copying from parent directory..."
    cp ../config.yaml .
    echo -e "${GREEN}✅ config.yaml copied${NC}"
fi

echo ""
echo "=============================================="
echo "   🚀 STARTING DEERFLOW"
echo "=============================================="
echo ""
echo "📍 Working Directory: $(pwd)"
echo "🤖 Model: GLM-4-Flash (Ollama Local)"
echo "🔍 Search Engine: Tavily API"
echo "🌐 Web UI: http://localhost:2026"
echo ""
echo -e "${YELLOW}⏳ Starting development server...${NC}"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start DeerFlow
make dev
