#!/bin/bash
# 🔴💀 RICK'S ULTIMATE AUTONOMOUS RED TEAM ARSENAL — INSTALL SCRIPT
# Run from the red-team-arsenal directory: chmod +x scripts/install_tools.sh && ./scripts/install_tools.sh

set -e

echo ""
echo "██████╗ ███████╗██████╗     ████████╗███████╗ █████╗ ███╗   ███╗"
echo "██╔══██╗██╔════╝██╔══██╗    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║"
echo "██████╔╝█████╗  ██║  ██║       ██║   █████╗  ███████║██╔████╔██║"
echo "██╔══██╗██╔══╝  ██║  ██║       ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║"
echo "██║  ██║███████╗██████╔╝       ██║   ███████╗██║  ██║██║ ╚═╝ ██║"
echo "╚═╝  ╚═╝╚══════╝╚═════╝        ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝"
echo ""
echo "🔴💀 Ultimate Autonomous Red Team Arsenal — Setup Script"
echo "   Rick Jefferson / RJ Business Solutions"
echo ""

# ── DETECT OS ─────────────────────────────────────────────────────────────────
OS="$(uname -s)"
echo "📌 Detected OS: $OS"

# ── PYTHON ENV ────────────────────────────────────────────────────────────────
echo ""
echo "🐍 Setting up Python environment..."

if ! command -v python3 &>/dev/null; then
  echo "❌ Python3 not found. Please install Python 3.11+"
  exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "   Python: $PYTHON_VERSION"

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel --quiet

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip install \
  openai anthropic huggingface-hub transformers sentence-transformers \
  langchain langchain-community langgraph pydantic \
  fastapi uvicorn httpx aiohttp websockets requests \
  tavily-python apify-client kaggle scholarly feedparser \
  numpy pandas chromadb \
  cloudflare boto3 \
  pyrit \
  python-dotenv rich typer loguru pyyaml jinja2 markdown \
  pytest pytest-asyncio \
  --quiet

echo "✅ Python dependencies installed"

# ── NODE / DASHBOARD ──────────────────────────────────────────────────────────
echo ""
echo "⚛️  Setting up React dashboard..."

if ! command -v node &>/dev/null; then
  echo "⚠️  Node.js not found. Install from https://nodejs.org to use the dashboard."
else
  cd dashboard
  npm install --quiet
  cd ..
  echo "✅ Dashboard dependencies installed"
fi

# ── CLOUDFLARE ────────────────────────────────────────────────────────────────
echo ""
echo "☁️  Setting up Cloudflare..."

if command -v node &>/dev/null; then
  cd cloudflare
  npm install -g wrangler --quiet 2>/dev/null || echo "   (wrangler already installed)"
  cd ..
  echo "✅ Wrangler ready"
fi

# ── RED TEAM TOOLS (Docker-based — requires Docker) ──────────────────────────
echo ""
echo "🐳 Checking Docker for red team tools..."

if command -v docker &>/dev/null; then
  echo "✅ Docker available. Red team tools will run in containers."
  echo ""
  echo "   To pull PentAGI (Gold Standard) run:"
  echo "   docker pull ghcr.io/vxcontrol/pentagi:latest"
  echo ""
  echo "   To clone and install CAI, ARACNE, Strix (requires Linux VM or Docker):"
  echo "   See RED_TEAM_TOOLS_SETUP.md for Docker container instructions"
else
  echo "⚠️  Docker not found."
  echo "   Install Docker from https://docs.docker.com/desktop/mac/"
  echo "   Or set AGENT_EXECUTION_MODE=llm in .env to use LLM-only mode"
fi

# ── DIRECTORIES ───────────────────────────────────────────────────────────────
echo ""
echo "📁 Creating runtime directories..."
mkdir -p sessions reports logs
echo "✅ Runtime directories created"

# ── KAGGLE ────────────────────────────────────────────────────────────────────
echo ""
echo "📊 Configuring Kaggle API..."
mkdir -p ~/.kaggle
if [ -f .env ]; then
  KAGGLE_USER=$(grep KAGGLE_USERNAME .env | cut -d= -f2)
  KAGGLE_KEY=$(grep KAGGLE_KEY .env | cut -d= -f2)
  if [ -n "$KAGGLE_USER" ] && [ -n "$KAGGLE_KEY" ]; then
    echo "{\"username\":\"$KAGGLE_USER\",\"key\":\"$KAGGLE_KEY\"}" > ~/.kaggle/kaggle.json
    chmod 600 ~/.kaggle/kaggle.json
    echo "✅ Kaggle credentials configured"
  fi
fi

# ── DONE ──────────────────────────────────────────────────────────────────────
echo ""
echo "════════════════════════════════════════════════════════════"
echo "✅ INSTALLATION COMPLETE — 🔴💀 Red Team Arsenal Ready"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "🚀 QUICK START:"
echo ""
echo "  # Activate venv (always do this first)"
echo "  source .venv/bin/activate"
echo ""
echo "  # Run a mission via CLI"
echo "  python main.py run \"Research SQL injection techniques and explain the attack chain\" --cost mid"
echo ""
echo "  # Start the API server"
echo "  python main.py serve"
echo ""
echo "  # Start the dashboard (in a second terminal)"
echo "  cd dashboard && npm run dev"
echo "  # Then open http://localhost:3000"
echo ""
echo "  # List all agents"
echo "  python main.py agents"
echo ""
echo "  # List all models"
echo "  python main.py models"
echo ""
echo "  # Search academic papers"
echo "  python main.py research \"autonomous penetration testing LLM\""
echo ""
echo "☁️  CLOUDFLARE:"
echo "  cd cloudflare && npx wrangler deploy"
echo ""
echo "  Create R2 bucket: npx wrangler r2 bucket create red-team-reports"
echo "  Create KV: npx wrangler kv:namespace create red-team-sessions"
echo ""
echo "🔑 All API keys are pre-configured in .env"
echo ""
