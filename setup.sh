#!/usr/bin/env bash
set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Market Calendar Bot - Initial Setup${NC}"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo -e "${RED}❌ uv not found. Please install it first:${NC}"
    echo "   https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
fi

echo -e "${GREEN}✓ uv found${NC}"

# Install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
uv sync
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${BLUE}Creating .env file from template...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created${NC}"
    echo -e "${BLUE}⚠️  Please update .env with your Telegram credentials${NC}"
fi

echo -e "${GREEN}✨ Setup complete!${NC}"
echo ""
echo "Next steps:"
echo "  1. Edit .env with your configuration"
echo "  2. Run: make run (to test locally)"
echo "  3. Or: uv run main.py"
echo ""
