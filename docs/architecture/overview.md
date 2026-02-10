# System Architecture Overview

EchoMinds menggunakan arsitektur **client-server** dengan **local-first approach**, di mana semua data processing (LLM inference & RAG) terjadi di local machine untuk privacy maksimal.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER DEVICE                          │
│                                                             │
│  ┌─────────────────────┐         ┌────────────────────┐   │
│  │   Frontend (Web)    │◄───────►│  Backend (FastAPI)  │   │
│  │                     │  HTTP/  │                     │   │
│  │  - Svelte 5 UI      │  REST   │  - Chat Service     │   │
│  │  - Theme System     │  API    │  - LLM Service      │   │
│  │  - Router           │         │  - RAG Service      │   │
│  │  - State Management │         │  - Character Mgmt   │   │
│  └─────────────────────┘         └─────────┬───────┬──┘   │
│                                             │       │      │
│                          ┌──────────────────┘       │      │
│                          │                          │      │
│                  ┌───────▼───────┐        ┌─────────▼────┐│
│                  │     Ollama    │        │   ChromaDB   ││
│                  │   (LLM Runtime)│       │ (Vector DB)  ││
│                  │                │        │              ││
│                  │ - Model Storage│        │ - Embeddings ││
│                  │ - Inference    │        │ - Similarity ││
│                  │ - GPU/CPU Mgmt │        │   Search     ││
│                  └────────────────┘        └──────────────┘│
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Layers

### 1. Presentation Layer (Frontend)

**Technology:** Svelte 5 + TypeScript + Vite

**Responsibilities:**
- User interface rendering
- User interaction handling
- Client-side routing
- Theme management (light/dark)
- State management (Svelte stores)
- API communication

**Key Components:**
- `App.svelte` - Root component, routing orchestration
- `Sidebar.svelte` - Navigation dengan mobile responsive
- `ChatInterface.svelte` - Main chat UI
- Pages: Home, MyChats, Explore, Create, Settings

**Data Flow:**
```
User Input → UI Component → API Service → Backend
                                ↓
Frontend Store ← UI Update ←────┘
```

---

### 2. API Layer (Backend Routes)

**Technology:** FastAPI

**Responsibilities:**
- HTTP request handling
- Input validation (Pydantic)
- Error handling
- CORS management
- Request routing

**Endpoints:**
```
POST   /api/chat              # Send message, get AI response
GET    /api/status            # System health & resource usage
GET    /api/config            # Current model configuration
PUT    /api/config            # Update model configuration
GET    /api/models            # List available LLM models
GET    /api/characters        # List characters
DELETE /api/conversations/:id # Clear conversation history
```

---

### 3. Business Logic Layer (Services)

**Technology:** Python async services

#### Chat Service Orchestrator
```python
class ChatService:
    async def process_message(
        character_id: str,
        user_id: str, 
        message: str
    ) -> ChatResponse:
        # 1. Load character profile
        # 2. Retrieve RAG context from vector DB
        # 3. Build prompt with system + context + history
        # 4. Generate LLM response
        # 5. Store conversation in vector DB
        # 6. Return response
```

**Dependencies:**
- `LLMService` (Ollama/Llama.cpp)
- `RAGService` (ChromaDB)
- `CharacterService` (Profile management)

---

### 4. LLM Integration Layer

**Technology:** Ollama Python client / Llama.cpp bindings

**Responsibilities:**
- Model loading & switching
- Inference execution
- Resource allocation (CPU/GPU)
- Embedding generation
- Health monitoring

**Key Operations:**
```python
# Text generation
response = await ollama_service.generate(
    prompt=prompt,
    model=model_name,
    options={
        "temperature": 0.8,
        "num_ctx": 4096,
        "num_predict": 512,
        "num_thread": 4,
        "num_gpu": 0
    }
)

# Embedding generation
embedding = await ollama_service.generate_embedding(
    text=message,
    model="all-MiniLM-L6-v2"
)
```

---

### 5. Data Persistence Layer

#### Vector Database (ChromaDB)

**Purpose:** Semantic memory untuk RAG

**Schema:**
```python
Collection: "echominds_{characterId}_{userId}"
Documents: [
    {
        "id": "uuid",
        "embedding": [0.123, 0.456, ...],  # 384-dim vector
        "metadata": {
            "role": "user" | "assistant",
            "timestamp": "2026-02-10T12:34:56",
            "character_id": "luna",
            "user_id": "lycus"
        },
        "document": "Actual message text"
    }
]
```

**Operations:**
- `add()` - Store new conversation message
- `query()` - Semantic search untuk context retrieval
- `delete()` - Clear conversation history

#### File Storage

**Character Profiles:**
```
data/characters/
├── luna.json
├── kai.json
└── aria.json
```

**Conversation Backups (Future):**
```
data/conversations/
└── {userId}/
    └── {characterId}/
        └── YYYY-MM-DD.json
```

---

## Data Flow Diagrams

### Chat Message Flow

```
┌──────┐                                                   ┌────────┐
│ User │                                                   │Frontend│
└───┬──┘                                                   └───┬────┘
    │                                                          │
    │ 1. Types message + clicks send                          │
    │─────────────────────────────────────────────────────────►│
    │                                                          │
    │                                                   ┌──────▼──────┐
    │                                                   │ InputBar    │
    │                                                   │  component  │
    │                                                   └──────┬──────┘
    │                                                          │
    │                                                          │ 2. Emit onSend event
    │                                                          ▼
    │                                                   ┌──────────────┐
    │                                                   │ChatInterface │
    │                                                   │  component   │
    │                                                   └──────┬───────┘
    │                                                          │
    │                                                          │ 3. Call API service
    │                                                          ▼
    │                                                   ┌──────────────┐
    │                                                   │  api.ts      │
    │                                                   │  service     │
    │                                                   └──────┬───────┘
    │                                                          │
    │                                                          │ 4. HTTP POST /api/chat
    │                                                          │    {message, userId, characterId}
    │                                  ┌───────────────────────┘
    │                                  │
    │                           ┌──────▼──────┐
    │                           │  FastAPI    │
    │                           │   Routes    │
    │                           └──────┬──────┘
    │                                  │
    │                                  │ 5. Validate request (Pydantic)
    │                                  ▼
    │                           ┌─────────────┐
    │                           │ChatService  │
    │                           │  .process() │
    │                           └──────┬──────┘
    │                                  │
    │          ┌───────────────────────┼───────────────────────┐
    │          │ 6a. Load character    │ 6b. Retrieve context  │
    │          │     profile           │      from RAG         │
    │          ▼                       ▼                       │
    │   ┌─────────────┐        ┌──────────────┐              │
    │   │ Character   │        │  RAG Service │              │
    │   │   Service   │        │              │              │
    │   └─────────────┘        └──────┬───────┘              │
    │                                  │                       │
    │                                  │ Query ChromaDB        │
    │                                  ▼                       │
    │                          ┌──────────────┐               │
    │                          │  ChromaDB    │               │
    │                          │ Semantic     │               │
    │                          │  Search      │               │
    │                          └──────┬───────┘               │
    │                                  │                       │
    │                                  │ Returns top-K docs    │
    │          ┌───────────────────────┘                       │
    │          │                                               │
    │          │ 7. Build prompt:                             │
    │          │    System + Context + History + User msg     │
    │          ▼                                               │
    │   ┌─────────────┐                                       │
    │   │ LLM Service │                                       │
    │   │  (Ollama)   │                                       │
    │   └──────┬──────┘                                       │
    │          │                                               │
    │          │ 8. Generate response                         │
    │          ▼                                               │
    │   ┌─────────────┐                                       │
    │   │   Ollama    │                                       │
    │   │   Runtime   │                                       │
    │   └──────┬──────┘                                       │
    │          │                                               │
    │          │ Returns AI text                              │
    │          └───────────────────────┐                      │
    │                                  │                      │
    │                                  │ 9. Store conversation│
    │                                  ▼                      │
    │                          ┌──────────────┐              │
    │                          │  RAG Service │              │
    │                          │ .store()     │              │
    │                          └──────┬───────┘              │
    │                                  │                      │
    │                                  │ Add to ChromaDB      │
    │                                  ▼                      │
    │                          ┌──────────────┐              │
    │                          │  ChromaDB    │              │
    │                          └──────┬───────┘              │
    │                                  │                      │
    │          ┌───────────────────────┘                      │
    │          │                                              │
    │          │ 10. Return ChatResponse                     │
    │          ▼                                              │
    │   ┌─────────────┐                                      │
    │   │  FastAPI    │                                      │
    │   │   Routes    │                                      │
    │   └──────┬──────┘                                      │
    │          │                                              │
    │          │ 11. JSON response                           │
    │          │     {reply, context, metadata}              │
    │          └────────────────────────┐                    │
    │                                   │                    │
    │                            ┌──────▼──────┐            │
    │                            │  Frontend   │            │
    │                            │   api.ts    │            │
    │                            └──────┬──────┘            │
    │                                   │                    │
    │                                   │ 12. Update UI      │
    │                                   ▼                    │
    │                            ┌─────────────┐            │
    │                            │ChatInterface│            │
    │                            │ - Add msg   │            │
    │◄───────────────────────────┤ - Scroll    │            │
    │ 13. Display AI response    │             │            │
    │                            └─────────────┘            │
    │                                                         │
```

---

## Security Architecture

### 1. Local-First Design

**All data stays on device:**
- LLM inference runs locally (Ollama)
- Vector database stored locally (ChromaDB)
- Conversations never transmitted externally
- No external API calls (unless user configures)

### 2. Input Validation

**Backend:**
- Pydantic models untuk type safety
- String length limits
- SQL injection prevention (not applicable, no SQL)
- XSS prevention via sanitization

**Frontend:**
- Input validation sebelum API call
- Character limit enforcement
- Rate limiting (future)

### 3. CORS Policy

**Development:**
```python
CORS_ORIGINS = ["http://localhost:5173"]
```

**Production:**
```python
CORS_ORIGINS = ["https://yourdomain.com"]
```

### 4. Future Enhancements

- Authentication (JWT tokens)
- User management
- Role-based access control (RBAC)
- API rate limiting
- Content moderation

---

## Performance Architecture

### 1. Async Operations

**All I/O operations are async:**
```python
async def process_message(...):
    # Concurrent operations
    character, context = await asyncio.gather(
        character_service.load(character_id),
        rag_service.retrieve_context(...)
    )
    
    # Streaming LLM response (future)
    async for chunk in llm_service.generate_stream(...):
        yield chunk
```

### 2. Caching Strategy

**Model Cache:**
- Ollama caches loaded models in memory
- Switching models unloads previous

**Embedding Cache (Future):**
```python
# Cache frequently embedded texts
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_embedding(text: str) -> List[float]:
    return embedding_model.encode(text)
```

**Character Profile Cache:**
```python
# Load once, cache in memory
CHARACTER_CACHE = {}

async def load_character(char_id: str):
    if char_id not in CHARACTER_CACHE:
        CHARACTER_CACHE[char_id] = load_from_file(char_id)
    return CHARACTER_CACHE[char_id]
```

### 3. Resource Management

**CPU/GPU Allocation:**
- Configurable via environment variables
- Dynamic adjustment (future)
- Monitoring via `psutil`

**Memory Management:**
- Vector DB uses disk-based persistence
- LRU eviction for embeddings
- Context window limits prevent OOM

---

## Scalability Considerations

### Current: Single-User, Single-Device

**Limitations:**
- One user at a time
- No multi-device sync
- Local storage only

**Advantages:**
- Zero latency
- Complete privacy
- No server costs

### Future: Multi-User Server Deployment

**Architecture changes needed:**
1. **Authentication layer** - JWT, session management
2. **Database migration** - PostgreSQL untuk user data
3. **Distributed vector DB** - Qdrant/Weaviate cluster
4. **LLM serving** - vLLM atau Text Generation Inference
5. **Horizontal scaling** - Load balancer, multiple backend instances

**Estimated costs:**
- Small (10 users): 1x GPU server (~$500/mo)
- Medium (100 users): 3x GPU servers + DB (~$2000/mo)
- Large (1000 users): Kubernetes cluster (~$10k/mo)

---

## Technology Choices Rationale

### Why Svelte 5?
- ✅ Reactive by default (Runes API)
- ✅ Small bundle size (~5KB)
- ✅ Fast performance
- ✅ TypeScript integration
- ❌ Smaller ecosystem vs React

### Why FastAPI?
- ✅ Async/await native
- ✅ Automatic OpenAPI docs
- ✅ Pydantic validation
- ✅ Fast performance
- ❌ Less mature than Flask

### Why Ollama?
- ✅ Easy model management
- ✅ Good GPU support
- ✅ Active development
- ✅ One-command installation
- ❌ Less control vs llama.cpp

### Why ChromaDB?
- ✅ Simple API
- ✅ Built-in embeddings
- ✅ Good Python integration
- ✅ Disk persistence
- ❌ Not distributed (future limitation)

---

## Next Steps

- [Frontend Architecture Details](frontend.md)
- [Backend Architecture Details](backend.md)
- [API Documentation](../api/endpoints.md)

---

**Architecture documentation complete!**
