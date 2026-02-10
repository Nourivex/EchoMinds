# Installation Guide

## System Requirements

### Minimum
- **OS:** Windows 10/11, macOS 11+, Linux (Ubuntu 20.04+)
- **RAM:** 8GB (16GB recommended)
- **Storage:** 10GB free space
- **CPU:** 4 cores (8 recommended untuk performa optimal)
- **GPU:** Optional (NVIDIA dengan CUDA 11+ untuk accelerasi)

### Software
- **Node.js:** 20.0.0 atau lebih baru
- **npm:** 10.0.0 atau lebih baru
- **Python:** 3.11 atau lebih baru
- **pip:** 23.0 atau lebih baru
- **Git:** 2.40 atau lebih baru

---

## Installation Methods

### Method 1: Automated Setup (Recommended)

#### Windows
```powershell
# Download installer script
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/Nourivex/EchoMinds/main/scripts/install.ps1" -OutFile "install.ps1"

# Run installer
.\install.ps1

# Follow interactive prompts
```

#### macOS/Linux
```bash
# Download installer script
curl -O https://raw.githubusercontent.com/Nourivex/EchoMinds/main/scripts/install.sh

# Make executable
chmod +x install.sh

# Run installer
./install.sh

# Follow interactive prompts
```

---

### Method 2: Manual Setup

#### Step 1: Clone Repository

```bash
# Via HTTPS
git clone https://github.com/Nourivex/EchoMinds.git

# Atau via SSH
git clone git@github.com:Nourivex/EchoMinds.git

# Navigate to directory
cd EchoMinds
```

#### Step 2: Install Node.js Dependencies

```bash
# Check Node.js version
node --version  # Should be 20.0.0+

# Install frontend dependencies
npm install

# Verify installation
npm list --depth=0
```

**Expected packages:**
- `svelte@^5.45.2`
- `vite@^7.3.1`
- `typescript@^5.9.3`
- `tailwindcss@^3.4.16`
- `@lucide/svelte@^0.563.1`

#### Step 3: Install Python Dependencies

##### Windows
```powershell
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

##### macOS/Linux
```bash
# Navigate to backend
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

**Expected packages:**
- `fastapi==0.115.0`
- `ollama==0.4.5`
- `chromadb==0.5.23`
- `sentence-transformers==3.3.1`
- `pydantic==2.10.4`
- `uvicorn==0.34.0`

#### Step 4: Install Ollama (LLM Runtime)

##### Windows
```powershell
# Download Ollama installer
# Visit: https://ollama.ai/download/windows
# Run installer: OllamaSetup.exe

# Verify installation
ollama --version

# Pull default model
ollama pull llama3.2:3b
```

##### macOS
```bash
# Using brew
brew install ollama

# Or download from: https://ollama.ai/download/mac
# Run: Ollama.app

# Verify installation
ollama --version

# Pull default model
ollama pull llama3.2:3b
```

##### Linux
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Verify installation
ollama --version

# Pull default model
ollama pull llama3.2:3b
```

#### Step 5: Configure Environment

```bash
# Navigate to backend directory
cd backend

# Copy environment template
cp .env.example .env

# Edit configuration
# Windows: notepad .env
# macOS: open -e .env
# Linux: nano .env
```

**Minimal configuration (.env):**
```bash
# API Configuration
API_HOST=localhost
API_PORT=8000
DEBUG=true

# LLM Provider (ollama or llamacpp)
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_MODEL=llama3.2:3b

# Resource Allocation
CPU_THREADS=4           # Number of CPU threads
GPU_LAYERS=0            # 0 = CPU only, -1 = all GPU
CONTEXT_LENGTH=4096     # Context window size
MAX_TOKENS=512          # Max response tokens

# Vector Database
VECTOR_DB_PATH=../data/vectorstore
EMBEDDING_MODEL=all-MiniLM-L6-v2

# CORS (untuk development)
CORS_ORIGINS=["http://localhost:5173"]
```

#### Step 6: Initialize Database Directories

```bash
# Return to project root
cd ..

# Create data directories
mkdir -p data/vectorstore
mkdir -p data/conversations
mkdir -p data/characters

# Copy example character
cp backend/data/characters/example.json data/characters/luna.json
```

---

## Verification

### Test Frontend
```bash
# From project root
npm run dev

# Expected output:
# VITE v7.3.1  ready in xxx ms
# ➜  Local:   http://localhost:5173/
# ➜  Network: use --host to expose

# Open browser: http://localhost:5173
# Should see homepage with dark theme
```

### Test Backend
```bash
# From project root
cd backend

# Activate venv (if not active)
# Windows: .\venv\Scripts\Activate.ps1
# macOS/Linux: source venv/bin/activate

# Start server
uvicorn main:app --reload --port 8000

# Expected output:
# INFO:     Uvicorn running on http://localhost:8000
# INFO:     Application startup complete

# In new terminal, test health endpoint:
curl http://localhost:8000/api/health

# Expected response:
# {"status":"healthy","llm":"ollama","model":"llama3.2:3b"}
```

### Test Ollama
```bash
# Check if Ollama is running
curl http://localhost:11434/api/version

# Test model inference
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:3b",
  "prompt": "Hello, how are you?",
  "stream": false
}'

# Should return JSON with response
```

---

## Troubleshooting

### Issue: "Node.js version too old"
```bash
# Update Node.js via nvm (recommended)
# Install nvm: https://github.com/nvm-sh/nvm

nvm install 20
nvm use 20
node --version  # Should be 20.x.x
```

### Issue: "Python not found"
```bash
# Windows: Install from python.org
# macOS: brew install python@3.11
# Linux: sudo apt install python3.11

# Verify
python3 --version  # Should be 3.11+
```

### Issue: "npm install fails"
```bash
# Clear cache
npm cache clean --force

# Delete node_modules
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

### Issue: "pip install fails"
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v

# If specific package fails, install separately:
pip install chromadb==0.5.23
```

### Issue: "Ollama connection refused"
```bash
# Start Ollama service
# Windows: Check system tray, right-click Ollama icon
# macOS: Open Ollama.app
# Linux: systemctl start ollama

# Verify service
ollama list  # Should show installed models

# If port conflict, change port in .env:
OLLAMA_BASE_URL=http://localhost:11435
```

### Issue: "ChromaDB initialization error"
```bash
# Ensure directory exists and is writable
mkdir -p data/vectorstore
chmod 755 data/vectorstore

# Clear existing database (if corrupted)
rm -rf data/vectorstore/*

# Restart backend
```

### Issue: "CORS error in browser console"
```bash
# Check backend/.env CORS_ORIGINS:
CORS_ORIGINS=["http://localhost:5173"]

# If using different port, update accordingly
# Restart backend after changes
```

---

## GPU Acceleration (Optional)

### NVIDIA GPU (CUDA)

#### Windows/Linux
```bash
# Check CUDA availability
nvidia-smi

# Install CUDA toolkit (if not installed)
# Visit: https://developer.nvidia.com/cuda-downloads

# Install PyTorch with CUDA support
pip install torch --index-url https://download.pytorch.org/whl/cu118

# Update .env for GPU usage:
GPU_LAYERS=-1  # Use all GPU layers
```

#### Verify GPU Usage
```bash
# Start backend
cd backend
python -c "import torch; print(torch.cuda.is_available())"
# Should print: True

# Monitor GPU during inference
nvidia-smi -l 1  # Refresh every second
```

### Apple Silicon (Metal)

```bash
# PyTorch with MPS (Metal Performance Shaders)
pip install torch torchvision

# Verify Metal support
python -c "import torch; print(torch.backends.mps.is_available())"
# Should print: True
```

---

## Next Steps

1. ✅ **Verify all services running**
   - Frontend: http://localhost:5173
   - Backend: http://localhost:8000
   - Ollama: http://localhost:11434

2. 📖 **Read Configuration Guide**
   - [Configuration Options](configuration.md)

3. 🎨 **Explore the UI**
   - Create a character
   - Start a conversation
   - Toggle theme (light/dark)

4. 🛠️ **Development Setup**
   - [Development Guide](../guides/development.md)

5. 🧪 **Run Tests**
   - [Testing Guide](../guides/testing.md)

---

## Getting Help

- **Documentation:** [docs/](../README.md)
- **Issues:** [GitHub Issues](https://github.com/Nourivex/EchoMinds/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Nourivex/EchoMinds/discussions)

---

**Installation complete! 🎉** Enjoy using EchoMinds!
