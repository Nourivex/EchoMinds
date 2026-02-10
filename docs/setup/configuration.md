# Configuration Guide

Panduan lengkap konfigurasi EchoMinds untuk berbagai skenario penggunaan.

---

## Configuration Files

### Frontend Configuration

#### `vite.config.ts`
```typescript
export default defineConfig({
  server: {
    port: 5173,
    host: true,  // Expose ke network
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    minify: 'esbuild'
  }
})
```

#### `tailwind.config.js`
```javascript
export default {
  darkMode: 'class',  // Support light/dark theme
  content: [
    './index.html',
    './src/**/*.{svelte,js,ts}'
  ],
  theme: {
    extend: {
      // Custom colors, fonts, dll
    }
  }
}
```

---

### Backend Configuration

#### `backend/.env`

Semua konfigurasi backend melalui environment variables:

```bash
#==========================================
# API Configuration
#==========================================
API_HOST=localhost
API_PORT=8000
API_RELOAD=true
DEBUG=true

#==========================================
# CORS (Cross-Origin Resource Sharing)
#==========================================
# Comma-separated list for multiple origins
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]

#==========================================
# LLM Provider Configuration
#==========================================
# Options: ollama, llamacpp
LLM_PROVIDER=ollama

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_MODEL=llama3.2:3b

# Llama.cpp Configuration (if using llamacpp)
# LLAMACPP_MODEL_PATH=/path/to/model.gguf
# LLAMACPP_N_CTX=4096

#==========================================
# Resource Allocation
#==========================================
# CPU threads untuk inference (recommended: jumlah core - 1)
CPU_THREADS=4

# GPU layers 
# -1 = Use all GPU (if available)
#  0 = CPU only (recommended untuk testing)
# >0 = Specific number of layers to GPU
GPU_LAYERS=0

# Context window size (tokens)
# Larger = more memory, better long conversations
# Common values: 2048, 4096, 8192, 16384
CONTEXT_LENGTH=4096

# Max tokens per response
MAX_TOKENS=512

# Temperature (0.0 - 2.0)
# Lower = more focused, Higher = more creative
TEMPERATURE=0.8

#==========================================
# Vector Database (ChromaDB)
#==========================================
VECTOR_DB_PATH=../data/vectorstore
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Collection naming prefix
COLLECTION_PREFIX=echominds

#==========================================
# Data Storage
#==========================================
CHARACTER_DATA_PATH=../data/characters
CONVERSATION_DATA_PATH=../data/conversations

#==========================================
# Logging
#==========================================
LOG_LEVEL=INFO
LOG_FILE=../logs/echominds.log
```

---

## Configuration Profiles

### Development (Default)
```bash
# backend/.env
DEBUG=true
API_RELOAD=true
LOG_LEVEL=DEBUG
GPU_LAYERS=0
CPU_THREADS=4
CORS_ORIGINS=["http://localhost:5173"]
```

**Karakteristik:**
- Auto-reload on code changes
- Verbose logging
- CPU-only (faster startup)
- Permissive CORS

---

### Production
```bash
# backend/.env
DEBUG=false
API_RELOAD=false
LOG_LEVEL=WARNING
GPU_LAYERS=-1
CPU_THREADS=8
CORS_ORIGINS=["https://yourdomain.com"]
```

**Karakteristik:**
- No auto-reload
- Minimal logging
- GPU acceleration enabled
- Strict CORS
- More CPU threads

**Additional production settings:**
```bash
# Use production ASGI server
pip install gunicorn

# Run with gunicorn
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

---

### Testing
```bash
# backend/.env.test
DEBUG=false
LOG_LEVEL=ERROR
VECTOR_DB_PATH=../data/test_vectorstore
CHARACTER_DATA_PATH=../data/test_characters
CONVERSATION_DATA_PATH=../data/test_conversations
```

**Karakteristik:**
- Isolated data directories
- Minimal logging
- Consistent configuration

---

## LLM Provider Configurations

### Ollama (Recommended)

**Advantages:**
- Easy installation
- Model management via CLI
- Built-in model pulling
- Good performance

**Configuration:**
```bash
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_MODEL=llama3.2:3b
```

**Available models:**
```bash
# List installed models
ollama list

# Pull new model
ollama pull llama3.2:3b      # Small, fast (2GB)
ollama pull mistral:7b       # Balanced (4GB)
ollama pull llama3:8b        # Better quality (5GB)
ollama pull mixtral:8x7b     # High quality (26GB)

# Remove model
ollama rm llama3.2:3b
```

**Model switching in runtime:**
```bash
# Via API
curl -X POST http://localhost:8000/api/config \
  -H "Content-Type: application/json" \
  -d '{"model_name":"mistral:7b"}'
```

---

### Llama.cpp

**Advantages:**
- More control over quantization
- Better for custom models
- Lower memory usage with quantization

**Configuration:**
```bash
LLM_PROVIDER=llamacpp
LLAMACPP_MODEL_PATH=/path/to/model.gguf
LLAMACPP_N_CTX=4096
```

**Quantization formats:**
- `Q4_0`: 4-bit (smallest, fastest, lower quality)
- `Q5_0`: 5-bit (balanced)
- `Q8_0`: 8-bit (good quality)
- `F16`: 16-bit float (best quality, largest)

**Example dengan custom model:**
```bash
# Download GGUF model
wget https://huggingface.co/.../model-Q4_0.gguf

# Update .env
LLAMACPP_MODEL_PATH=./models/model-Q4_0.gguf
LLAMACPP_N_CTX=4096
GPU_LAYERS=35  # Adjust based on GPU VRAM
```

---

## Resource Allocation Tuning

### CPU-Only Configuration

**Optimal untuk:**
- Development
- Testing
- Machines tanpa GPU
- Balanced performance

```bash
CPU_THREADS=4          # Use 50-75% of available cores
GPU_LAYERS=0           # No GPU
CONTEXT_LENGTH=2048    # Smaller context untuk speed
MAX_TOKENS=256         # Shorter responses
```

**Performance tips:**
- Set `CPU_THREADS` to core count - 1
- Use smaller models (3B parameters)
- Reduce context length
- Consider model quantization

---

### GPU-Accelerated Configuration

**Optimal untuk:**
- Production deployment
- Faster inference
- Longer context windows
- Higher quality models

```bash
CPU_THREADS=2          # Fewer CPU threads
GPU_LAYERS=-1          # All layers to GPU
CONTEXT_LENGTH=8192    # Larger context
MAX_TOKENS=1024        # Longer responses
```

**GPU VRAM requirements:**
- 3B model (Q4): ~2GB VRAM
- 7B model (Q4): ~4GB VRAM
- 13B model (Q4): ~8GB VRAM
- 33B model (Q4): ~20GB VRAM

**Monitoring GPU:**
```bash
# NVIDIA
nvidia-smi -l 1

# Check VRAM usage
nvidia-smi --query-gpu=memory.used --format=csv
```

---

### Hybrid Configuration (CPU + GPU)

**Optimal untuk:**
- Limited VRAM
- Balancing performance

```bash
CPU_THREADS=4
GPU_LAYERS=20          # Partial GPU offload
CONTEXT_LENGTH=4096
```

**Finding optimal GPU_LAYERS:**
1. Start with `GPU_LAYERS=0` (CPU only)
2. Incrementally increase by 5
3. Monitor VRAM usage with `nvidia-smi`
4. Find sweet spot before OOM errors

---

## RAG & Vector Database Configuration

### ChromaDB Settings

```bash
VECTOR_DB_PATH=../data/vectorstore
EMBEDDING_MODEL=all-MiniLM-L6-v2
COLLECTION_PREFIX=echominds
```

**Embedding model options:**
```bash
# Fast, lightweight (default)
EMBEDDING_MODEL=all-MiniLM-L6-v2        # 384 dim, 80MB

# Better quality
EMBEDDING_MODEL=all-mpnet-base-v2       # 768 dim, 420MB

# Multilingual
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2
```

**Performance tuning:**
```python
# In backend/rag/vector_service.py

# Batch size untuk embedding generation
BATCH_SIZE = 32  # Increase for more RAM, decrease for less

# Number of results to retrieve
TOP_K = 5  # More results = more context, slower

# Minimum similarity threshold
SIMILARITY_THRESHOLD = 0.3  # Higher = stricter matching
```

---

### Memory Management

**Per-character isolation:**
```bash
# Collections named: echominds_{characterId}_{userId}
# Example: echominds_luna_lycus
```

**Clear old conversations:**
```bash
# Via API
curl -X DELETE http://localhost:8000/api/conversations/luna/lycus
```

**Disk usage monitoring:**
```bash
# Check ChromaDB size
du -sh data/vectorstore/

# Typical sizes:
# - 100 messages: ~5-10MB
# - 1000 messages: ~50-100MB
# - 10000 messages: ~500MB-1GB
```

---

## Advanced Configuration

### Custom Character Profiles

Create JSON files in `data/characters/`:

```json
{
  "id": "custom_ai",
  "name": "Custom AI",
  "avatar": "🤖",
  "description": "Your custom AI companion",
  "personality": "Helpful, technical, and detail-oriented",
  "greeting": "Hello! I'm your custom AI assistant.",
  "systemPrompt": "You are a helpful AI assistant specialized in...",
  "exampleDialogues": [
    {
      "user": "How do I configure this?",
      "assistant": "Let me help you with the configuration..."
    }
  ],
  "emotionalHooks": ["technical", "problem-solving", "efficiency"],
  "chatCount": 0
}
```

**Load custom character:**
```bash
# Restart backend to detect new characters
# Or trigger hot-reload via API (future feature)
```

---

### CORS Configuration

**Single origin:**
```bash
CORS_ORIGINS=["http://localhost:5173"]
```

**Multiple origins:**
```bash
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000","https://yourdomain.com"]
```

**All origins (⚠️ Development only):**
```bash
CORS_ORIGINS=["*"]
```

---

### Logging Configuration

```bash
# Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL=INFO

# Log file location
LOG_FILE=../logs/echominds.log
```

**Log rotation (production):**
```python
# Add to backend/config/logging.py
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    'logs/echominds.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
```

---

## Environment-Specific Configs

### Docker Configuration

```dockerfile
# Dockerfile
ENV API_HOST=0.0.0.0
ENV API_PORT=8000
ENV OLLAMA_BASE_URL=http://ollama:11434
ENV VECTOR_DB_PATH=/app/data/vectorstore
```

### Cloud Deployment

**AWS/GCP/Azure:**
```bash
# Use environment variables from cloud service
# Example (AWS ECS):
API_HOST=0.0.0.0
OLLAMA_BASE_URL=http://internal-llm-service:11434
VECTOR_DB_PATH=/mnt/efs/vectorstore
```

---

## Configuration Validation

Test your configuration:

```bash
# Check backend config
cd backend
python -c "from config.settings import settings; print(settings.model_dump())"

# Verify LLM connection
curl http://localhost:8000/api/health

# Test embedding generation
curl -X POST http://localhost:8000/api/embed \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello world"}'
```

---

## Troubleshooting Configuration Issues

### Issue: "Model not found"
```bash
# Check available models
ollama list

# Pull missing model
ollama pull llama3.2:3b

# Verify DEFAULT_MODEL matches
echo $DEFAULT_MODEL
```

### Issue: "CORS error"
```bash
# Check CORS_ORIGINS includes frontend URL
# Must be exact match including protocol and port
CORS_ORIGINS=["http://localhost:5173"]  # ✅
CORS_ORIGINS=["localhost:5173"]          # ❌ (missing http://)
```

### Issue: "Out of memory"
```bash
# Reduce resource usage:
CONTEXT_LENGTH=2048   # From 4096
MAX_TOKENS=256        # From 512
GPU_LAYERS=0          # Use CPU only

# Or use smaller model:
DEFAULT_MODEL=llama3.2:3b  # Instead of llama3:8b
```

---

## Next Steps

- [Development Guide](../guides/development.md)
- [API Documentation](../api/endpoints.md)
- [Deployment Guide](../guides/deployment.md)

---

**Configuration complete!** Your EchoMinds instance is ready to use.
