#!/bin/bash
# Storybook Web Application Setup Script

set -e

echo "🚀 Storybook Web Application Setup"
echo "===================================="
echo ""

# Check Node.js version
echo "📦 Checking Node.js version..."
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 20 ]; then
    echo "❌ Error: Node.js 20+ is required (you have $(node -v))"
    exit 1
fi
echo "✅ Node.js $(node -v) detected"
echo ""

# Check Python version
echo "🐍 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python $PYTHON_VERSION detected"
echo ""

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install
echo "✅ Node.js dependencies installed"
echo ""

# Setup Python environment
echo "🐍 Setting up Python environment..."
cd ..
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate
pip install -e . --quiet
echo "✅ Python environment ready"
echo ""

cd storybook-web

# Setup environment file
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  IMPORTANT: Edit .env and add your ANTHROPIC_API_KEY"
    echo ""
fi

# Check for API key
if ! grep -q "ANTHROPIC_API_KEY=sk-" .env 2>/dev/null; then
    echo "⚠️  WARNING: ANTHROPIC_API_KEY not configured in .env"
    echo ""
    echo "Please edit .env and add your API key:"
    echo "  ANTHROPIC_API_KEY=your_actual_key_here"
    echo ""
    echo "Get your API key from: https://console.anthropic.com"
    echo ""
fi

echo "✅ Setup complete!"
echo ""
echo "📖 Next steps:"
echo "   1. Edit .env and add your ANTHROPIC_API_KEY (if not done)"
echo "   2. Run: npm run dev"
echo "   3. Open: http://localhost:3000"
echo ""
echo "📚 Documentation:"
echo "   - ./README.md - Web app guide"
echo "   - ../WEB_APP_README.md - Complete architecture guide"
echo ""
echo "Happy writing! ✍️"
