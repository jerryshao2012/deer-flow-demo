#!/bin/bash

# DeerFlow Hello World Demo - Quick Start Script
# This script automates the initial setup process

set -e  # Exit on error

echo "🦌 ================================================"
echo "   DEERFLOW HELLO WORLD - QUICK START"
echo "=============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check if Ollama is installed
echo "📦 Step 1: Checking Ollama installation..."
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✅ Ollama is installed${NC}"
    ollama --version
else
    echo -e "${RED}❌ Ollama is not installed${NC}"
    echo "💡 Please install Ollama from: https://ollama.com"
    echo "   Or run: brew install ollama (macOS)"
    exit 1
fi

# Step 1b: Check if Nginx is installed
echo "📦 Step 1b: Checking Nginx installation..."
if command -v nginx &> /dev/null; then
    echo -e "${GREEN}✅ Nginx is installed${NC}"
else
    echo -e "${YELLOW}⚠️  Nginx is not installed${NC}"
    echo "📥 Installing nginx..."
    if command -v brew &> /dev/null; then
        brew install nginx
    else
        echo -e "${RED}❌ brew not found, please install nginx manually${NC}"
        exit 1
    fi
fi

# Step 2: Check if GLM-4-Flash model is available
echo ""
echo "📦 Step 2: Checking GLM-4-Flash model..."
if ollama list | grep -q "glm-4.7-flash"; then
    echo -e "${GREEN}✅ GLM-4-Flash model found${NC}"
else
    echo -e "${YELLOW}⚠️  GLM-4-Flash model not found${NC}"
    echo "💡 Do you want to pull it now? (This will download ~19GB)"
    read -p "Continue? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "📥 Pulling glm-4.7-flash:latest..."
        ollama pull glm-4.7-flash:latest
    else
        echo "Skipping model download. You can pull it later with: ollama pull glm-4.7-flash:latest"
    fi
fi

# Step 3: Check Python version
echo ""
echo "📦 Step 3: Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python $python_version detected"

# Step 4: Clone DeerFlow repository
echo ""
echo "📦 Step 4: Setting up DeerFlow repository..."
if [ -d "deer-flow" ]; then
    echo -e "${YELLOW}⚠️  deer-flow directory already exists${NC}"
    read -p "Do you want to re-clone it? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf deer-flow
        git clone https://github.com/bytedance/deer-flow.git
        echo -e "${GREEN}✅ DeerFlow repository cloned${NC}"
    fi
else
    git clone https://github.com/bytedance/deer-flow.git
    echo -e "${GREEN}✅ DeerFlow repository cloned${NC}"
fi

# Step 5: Install dependencies
echo ""
echo "📦 Step 5: Installing dependencies..."
cd deer-flow

if command -v uv &> /dev/null; then
    echo -e "${GREEN}✅ uv is installed${NC}"
else
    echo -e "${YELLOW}⚠️  uv is not installed${NC}"
    echo "📥 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

echo "🔧 Installing Python dependencies..."
uv sync

echo "🔧 Installing Frontend dependencies..."
if command -v pnpm &> /dev/null; then
    (cd deer-flow/frontend && pnpm install)
elif command -v npm &> /dev/null; then
    (cd deer-flow/frontend && npm install)
else
    echo -e "${YELLOW}⚠️  Neither pnpm nor npm found, skipping frontend dependency installation${NC}"
fi

# Step 6: Copy configuration files
echo ""
echo "📦 Step 6: Copying configuration files..."
cd ..

if [ -f "config.yaml" ]; then
    cp config.yaml deer-flow/
    echo -e "${GREEN}✅ config.yaml copied${NC}"
else
    echo -e "${RED}❌ config.yaml not found in current directory${NC}"
    exit 1
fi

if [ -f ".env.example" ]; then
    cp .env.example deer-flow/.env
    echo -e "${GREEN}✅ .env file created${NC}"
else
    echo -e "${RED}❌ .env.example not found in current directory${NC}"
    exit 1
fi

# Step 7: Prompt for Tavily API key
echo ""
echo "📦 Step 7: Configuring Tavily API key..."
echo -e "${YELLOW}⚠️  You need a Tavily API key for web search functionality${NC}"
echo "💡 Get your free API key at: https://app.tavily.com"
echo ""
read -p "Enter your Tavily API key (or press Enter to skip): " TAVILY_KEY

if [ -n "$TAVILY_KEY" ]; then
    # Update .env file with the provided key
    sed -i.bak "s|your-tavily-api-key-here|$TAVILY_KEY|g" deer-flow/.env
    echo -e "${GREEN}✅ Tavily API key configured${NC}"
else
    echo -e "${YELLOW}⚠️  Skipping Tavily API key configuration${NC}"
    echo "💡 You can add it later by editing deer-flow/.env"
fi

# Cleanup backup file
rm -f deer-flow/.env.bak

# Step 8: Start Ollama server
echo ""
echo "📦 Step 8: Starting Ollama server..."
if pgrep -x "ollama" > /dev/null; then
    echo -e "${GREEN}✅ Ollama server is already running${NC}"
else
    echo "🚀 Starting Ollama server in background..."
    ollama serve &
    sleep 3
    if pgrep -x "ollama" > /dev/null; then
        echo -e "${GREEN}✅ Ollama server started${NC}"
    else
        echo -e "${RED}❌ Failed to start Ollama server${NC}"
        echo "💡 Please start it manually with: ollama serve"
    fi
fi

# Final instructions
echo ""
echo "=============================================="
echo "   🎉 SETUP COMPLETE!"
echo "=============================================="
echo ""
echo "📚 Next Steps:"
echo ""
echo "1️⃣  Start DeerFlow:"
echo -e "   ${YELLOW}cd deer-flow && make dev${NC}"
echo ""
echo "2️⃣  Open your browser:"
echo -e "   ${YELLOW}http://localhost:2026${NC}"
echo ""
echo "3️⃣  Try your first research query:"
echo -e "   ${YELLOW}\"Research recent breakthroughs in quantum computing\"${NC}"
echo ""
echo "4️⃣  Run the hello world demo script:"
echo -e "   ${YELLOW}cd .. && python hello_world.py${NC}"
echo ""
echo "=============================================="
echo ""
echo -e "${GREEN}✨ Happy researching! ✨${NC}"
echo ""
