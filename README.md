# EchoMinds - Your Personal AI Companion 💜

<div align="center">

**Mobile-first AI companion platform dengan local LLM dan RAG memory**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9-blue)](https://www.typescriptlang.org/)
[![Svelte 5](https://img.shields.io/badge/Svelte-5.45-orange)](https://svelte.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)](https://fastapi.tiangolo.com/)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue)](https://www.python.org/)

[Features](#-features) • [Installation](#-quick-start) • [Documentation](docs/) • [Contributing](CONTRIBUTING.md)

</div>

---

## 🌟 Features

### ✨ **Emotion-First Design**
- 🎨 **Candy.AI-inspired UI** - Beautiful, connection-focused interface
- 🌓 **Dark/Light Mode** - Seamless theme switching dengan localStorage persistence
- 📱 **Mobile-First** - Responsive design dengan auto-collapsing sidebar
- ✨ **Smooth Animations** - Polished micro-interactions

### 💬 **Advanced Chat System**
- 🤖 **Local LLM** - Ollama/Llama.cpp integration untuk privacy
- 🧠 **RAG Memory** - Per-character vector database dengan ChromaDB
- 👥 **Multiple Characters** - Setiap karakter punya personality & memory unik
- 💾 **Persistent Conversations** - Chat history tersimpan per user-character pair

### ⚙️ **Customizable Performance**
- 🔧 **CPU/GPU Control** - Atur resource allocation (CPU threads, GPU layers)
- 🎛️ **Model Switching** - Ganti model LLM secara dynamic
- 📊 **Resource Monitoring** - Real-time CPU/memory usage tracking
- 🚀 **Optimized Inference** - Context caching & efficient batching

### 🎭 **Character System**
- ✍️ **Custom Characters** - Create your own AI companions
- 📝 **Rich Personalities** - System prompts, example dialogues, emotional hooks
- 🔍 **Explore & Discover** - Browse curated character collection
- 💾 **Character Memory** - Each character remembers your conversations uniquely

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** 20+ & npm
- **Python** 3.11+
- **Ollama** (atau Llama.cpp)

### Installation

```bash
# Clone repository
git clone https://github.com/Nourivex/EchoMinds.git
cd EchoMinds

# Install frontend dependencies
npm install

# Install backend dependencies
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cd ..

# Setup configuration
cp backend/.env.example backend/.env
# Edit backend/.env sesuai kebutuhan

# Install & start Ollama (if using Ollama)
# Download from: https://ollama.ai
ollama pull llama3.2:3b
```

### Running Development

```bash
# Terminal 1: Frontend (Vite dev server)
npm run dev
# Access: http://localhost:5173

# Terminal 2: Backend (FastAPI server)
cd backend
uvicorn main:app --reload --port 8000
# API: http://localhost:8000

# Terminal 3: Ollama (if not running as service)
ollama serve
```

---

## 📚 Documentation

### Setup & Configuration
- [📦 Installation Guide](docs/setup/installation.md)
- [⚙️ Configuration Options](docs/setup/configuration.md)

### Architecture
- [🏗️ System Overview](docs/architecture/overview.md)
- [🎨 Frontend Architecture](docs/architecture/frontend.md)
- [⚡ Backend Architecture](docs/architecture/backend.md)

### API Reference
- [📡 REST API Endpoints](docs/api/endpoints.md)
- [📋 Request/Response Models](docs/api/models.md)

### Features
- [💬 Chat System](docs/features/chat.md)
- [🧠 RAG & Memory](docs/features/rag.md)
- [🎭 Character Creation](docs/features/characters.md)
- [🎨 Theme System](docs/features/theming.md)

### Development
- [🛠️ Development Guide](docs/guides/development.md)
- [🚀 Deployment Guide](docs/guides/deployment.md)
- [🧪 Testing Guide](docs/guides/testing.md)
- [🤝 Contributing](CONTRIBUTING.md)

---

## 🛠️ Tech Stack

### Frontend
- **Framework:** Svelte 5 (Runes mode)
- **Build Tool:** Vite 7.3
- **Language:** TypeScript 5.9 (strict mode)
- **Styling:** Tailwind CSS 3.4
- **Icons:** @lucide/svelte
- **State Management:** Svelte Stores

### Backend
- **Framework:** FastAPI 0.115
- **LLM Runtime:** Ollama / Llama.cpp
- **Vector DB:** ChromaDB 0.5
- **Embeddings:** sentence-transformers
- **Validation:** Pydantic 2.10
- **Server:** Uvicorn

### Infrastructure
- **Local LLM:** Ollama (recommended) atau Llama.cpp
- **Storage:** File-based (conversations, characters)
- **Vector Store:** ChromaDB (persistent)

---

## 📁 Project Structure

```
EchoMinds/
├── src/                      # Frontend source
│   ├── components/          
│   │   ├── chat/            # Chat interface components
│   │   ├── layouts/         # Sidebar, Topbar
│   │   ├── pages/           # Route pages
│   │   └── ui/              # Reusable UI components
│   ├── lib/                 
│   │   ├── data/            # Mock data & constants
│   │   └── utils/           # Utility functions
│   ├── models/              # TypeScript interfaces
│   ├── services/            # API service layer
│   ├── stores/              # Svelte stores (router, theme)
│   └── App.svelte           # Root component
│
├── backend/                 # Backend source
│   ├── api/                 # FastAPI routes
│   ├── llm/                 # LLM services (Ollama, Llama.cpp)
│   ├── rag/                 # RAG & vector DB
│   ├── models/              # Pydantic models
│   ├── services/            # Business logic
│   ├── config/              # Configuration
│   └── main.py              # FastAPI app entry
│
├── data/                    # Runtime data (gitignored)
│   ├── characters/          # Character profiles
│   ├── conversations/       # Chat history
│   └── vectorstore/         # ChromaDB embeddings
│
├── docs/                    # Documentation
│   ├── setup/
│   ├── architecture/
│   ├── api/
│   ├── features/
│   └── guides/
│
└── tests/                   # Test suites
    ├── frontend/
    └── backend/
```

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) untuk guidelines.

### Development Workflow
1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Code Style
- **Frontend:** ESLint + Prettier
- **Backend:** Black + isort + mypy
- **Commits:** Conventional Commits format

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Svelte Team** - Amazing framework
- **Ollama** - Easy local LLM deployment
- **ChromaDB** - Powerful vector database
- **Tailwind CSS** - Utility-first styling
- **Candy.AI** - UI/UX inspiration

---

## 📞 Contact & Support

- **Issues:** [GitHub Issues](https://github.com/Nourivex/EchoMinds/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Nourivex/EchoMinds/discussions)
- **Email:** support@echominds.dev

---

<div align="center">

**Made with 💜 by Lycus**

[⬆ Back to Top](#echominds---your-personal-ai-companion-)

</div>
