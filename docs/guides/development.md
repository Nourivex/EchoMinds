# Development Guide

Panduan lengkap untuk development EchoMinds.

---

## Prerequisites

- Node.js 20+ & npm
- Python 3.11+
- Git
- VS Code (recommended) atau editor favorit
- Ollama atau Llama.cpp

---

## Initial Setup

### 1. Clone & Install

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
pip install-r requirements.txt
cd ..
```

### 2. Environment Configuration

```bash
# Copy environment template
cp backend/.env.example backend/.env

# Edit dengan konfigurasi lokal
# Minimal config untuk development:
DEBUG=true
LLM_PROVIDER=ollama
CPU_THREADS=4
GPU_LAYERS=0
```

### 3. Start Development Servers

```bash
# Terminal 1: Frontend
npm run dev
# Access: http://localhost:5173

# Terminal 2: Backend
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
# API: http://localhost:8000/docs

# Terminal 3: Ollama (if needed)
ollama serve
```

---

## Project Structure Deep Dive

### Frontend Structure

```
src/
├── components/
│   ├── chat/
│   │   ├── ChatInterface.svelte      # Main chat UI
│   │   └── InputBar.svelte           # Message input
│   ├── layouts/
│   │   ├── Sidebar.svelte            # Navigation sidebar
│   │   ├── Topbar.svelte             # Top navigation
│   │   └── Footer.svelte             # Footer (future)
│   ├── pages/
│   │   ├── HomePage.svelte           # Landing page
│   │   ├── MyChatsPage.svelte        # Chat history
│   │   ├── ExplorePage.svelte        # Character discovery
│   │   ├── CreatePage.svelte         # Character creation
│   │   └── SettingsPage.svelte       # App settings
│   └── ui/                           # Reusable UI components
│       ├── Button.svelte
│       ├── Input.svelte
│       └── Card.svelte
├── lib/
│   ├── data/
│   │   ├── mockCharacters.ts         # Character data (temp)
│   │   └── mockCategories.ts         # Category data (temp)
│   └── utils/
│       ├── formatters.ts             # Date, number formatting
│       └── validators.ts             # Input validation
├── models/
│   ├── Character.ts                  # Character interface
│   ├── Message.ts                    # Message types
│   └── User.ts                       # User interface
├── services/
│   └── api.ts                        # Backend API client
├── stores/
│   ├── router.ts                     # Client-side routing
│   ├── theme.ts                      # Theme state
│   └── user.ts                       # User state
├── App.svelte                        # Root component
└── main.ts                           # Entry point
```

### Backend Structure

```
backend/
├── api/
│   └── routes.py                     # FastAPI routes
├── config/
│   └── settings.py                   # Configuration
├── llm/
│   ├── ollama_service.py             # Ollama integration
│   └── llamacpp_service.py           # Llama.cpp (future)
├── models/
│   └── schemas.py                    # Pydantic models
├── rag/
│   └── vector_service.py             # ChromaDB RAG
├── services/
│   ├── chat_service.py               # Chat orchestrator
│   └── character_service.py          # Character management
└── main.py                           # FastAPI app
```

---

## Development Workflow

### Adding a New Feature

#### Example: Add "Export Conversation" Feature

**1. Plan the Feature**
- Where: Settings page or chat interface?
- Format: JSON? Markdown? PDF?
- Backend support needed? Yes
- API endpoint: `GET /api/conversations/:id/export`

**2. Backend Implementation**

```python
# backend/api/routes.py
@router.get("/conversations/{character_id}/{user_id}/export")
async def export_conversation(
    character_id: str,
    user_id: str,
    format: str = Query("json", regex="^(json|markdown)$")
):
    """Export conversation history."""
    messages = await rag_service.get_all_messages(
        character_id=character_id,
        user_id=user_id
    )
    
    if format == "json":
        return {"messages": messages}
    elif format == "markdown":
        md = generate_markdown(messages)
        return PlainTextResponse(md)
```

**3. Frontend Service**

```typescript
// src/services/api.ts
export async function exportConversation(
  characterId: string,
  userId: string,
  format: 'json' | 'markdown' = 'json'
): Promise<Blob> {
  const response = await fetch(
    `${BASE_URL}/api/conversations/${characterId}/${userId}/export?format=${format}`
  );
  return response.blob();
}
```

**4. UI Component**

```svelte
<!-- src/components/pages/SettingsPage.svelte -->
<script lang="ts">
import { Download } from '@lucide/svelte';
import { exportConversation } from '$services/api';

async function handleExport() {
  const blob = await exportConversation('luna', 'lycus', 'json');
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'conversation-luna.json';
  a.click();
}
</script>

<button onclick={handleExport}>
  <Download size={16} />
  Export Conversation
</button>
```

**5. Testing**

```typescript
// tests/frontend/ExportFeature.test.ts
describe('Export Conversation', () => {
  it('downloads JSON file', async () => {
    const blob = await exportConversation('luna', 'lycus');
    expect(blob.type).toBe('application/json');
  });
});
```

```python
# tests/backend/test_export.py
def test_export_conversation():
    response = client.get("/api/conversations/luna/lycus/export")
    assert response.status_code == 200
    assert "messages" in response.json()
```

**6. Documentation**

Update:
- `docs/api/endpoints.md` - Add endpoint documentation
- `docs/features/chat.md` - Mention export feature
- `CHANGELOG.md` - Add to unreleased section

**7. Commit**

```bash
git add .
git commit -m "feat(chat): add conversation export (JSON/Markdown)"
```

---

## Code Style & Standards

### Frontend (TypeScript/Svelte)

**Naming Conventions:**
```typescript
// Components: PascalCase
ChatInterface.svelte
InputBar.svelte

// Utilities: camelCase
formatDate.ts
validateInput.ts

// Constants: UPPER_SNAKE_CASE
const API_BASE_URL = 'http://localhost:8000';
const MAX_MESSAGE_LENGTH = 2000;
```

**Svelte 5 Runes:**
```typescript
// ✅ Use Runes
let count = $state(0);
let doubled = $derived(count * 2);

// ❌ Avoid old Svelte syntax
let count = 0;
$: doubled = count * 2;
```

**Props & Types:**
```typescript
// ✅ Explicit interface
interface Props {
  message: string;
  onSend: (text: string) => void;
  disabled?: boolean;
}

let { message, onSend, disabled = false }: Props = $props();

// ❌ Implicit any
let { message, onSend } = $props();
```

**Imports:**
```typescript
// ✅ Absolute imports with alias
import { ChatInterface } from '$components/chat';
import { api } from '$services/api';

// ❌ Relative imports (avoid when possible)
import { ChatInterface } from '../../components/chat/ChatInterface.svelte';
```

---

### Backend (Python)

**Type Hints:**
```python
# ✅ Always use type hints
async def process_message(
    character_id: str,
    user_id: str,
    message: str
) -> ChatResponse:
    pass

# ❌ No type hints
async def process_message(character_id, user_id, message):
    pass
```

**Docstrings:**
```python
# ✅ Google-style docstrings
async def retrieve_context(
    character_id: str,
    user_id: str,
    query: str,
    top_k: int = 5
) -> List[ContextMessage]:
    """Retrieve relevant context from vector database.
    
    Args:
        character_id: Character identifier
        user_id: User identifier
        query: Search query text
        top_k: Number of results to return
        
    Returns:
        List of context messages sorted by relevance
        
    Raises:
        VectorDBError: If database query fails
    """
```

**Error Handling:**
```python
# ✅ Specific exceptions
try:
    response = await ollama.generate(prompt)
except OllamaConnectionError as e:
    logger.error(f"Ollama connection failed: {e}")
    raise HTTPException(status_code=503, detail="LLM unavailable")

# ❌ Bare except
try:
    response = await ollama.generate(prompt)
except:
    pass
```

---

## Testing

### Frontend Tests (Vitest)

```bash
# Run all tests
npm run test

# Watch mode
npm run test:watch

# Coverage
npm run test:coverage
```

**Example Test:**
```typescript
// src/components/chat/InputBar.test.ts
import { render, fireEvent, screen } from '@testing-library/svelte';
import InputBar from './InputBar.svelte';

describe('InputBar', () => {
  it('calls onSend when Enter is pressed', async () => {
    const onSend = vi.fn();
    render(InputBar, {
      characterName: 'Luna',
      onSend
    });
    
    const input = screen.getByPlaceholderText(/Message Luna/);
    await fireEvent.input(input, { target: { value: 'Test' } });
    await fireEvent.keyDown(input, { key: 'Enter' });
    
    expect(onSend).toHaveBeenCalledWith('Test');
  });
  
  it('does not send empty messages', async () => {
    const onSend = vi.fn();
    render(InputBar, { characterName: 'Luna', onSend });
    
    const input = screen.getByPlaceholderText(/Message Luna/);
    await fireEvent.keyDown(input, { key: 'Enter' });
    
    expect(onSend).not.toHaveBeenCalled();
  });
});
```

---

### Backend Tests (Pytest)

```bash
# Run all tests
cd backend
pytest

# Specific file
pytest tests/test_chat_service.py

# With coverage
pytest --cov=backend --cov-report=html
```

**Example Test:**
```python
# tests/test_chat_service.py
import pytest
from services.chat_service import ChatService

@pytest.fixture
async def chat_service():
    return ChatService()

@pytest.mark.asyncio
async def test_process_message(chat_service):
    """Test basic message processing."""
    response = await chat_service.process_message(
        character_id="luna",
        user_id="test_user",
        message="Hello!"
    )
    
    assert response.reply
    assert response.characterName == "Luna"
    assert isinstance(response.context, list)

@pytest.mark.asyncio
async def test_empty_message_rejected(chat_service):
    """Test that empty messages are rejected."""
    with pytest.raises(ValueError):
        await chat_service.process_message(
            character_id="luna",
            user_id="test_user",
            message=""
        )
```

---

## Debugging

### Frontend Debugging

**VS Code launch.json:**
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "chrome",
      "request": "launch",
      "name": "Debug Frontend",
      "url": "http://localhost:5173",
      "webRoot": "${workspaceFolder}/src"
    }
  ]
}
```

**Browser DevTools:**
- **Console:** Check for errors/warnings
- **Network:** Inspect API calls
- **React DevTools:** Inspect Svelte components (via extension)
- **Performance:** Profile render performance

### Backend Debugging

**VS Code launch.json:**
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Backend",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "main:app",
        "--reload",
        "--port",
        "8000"
      ],
      "cwd": "${workspaceFolder}/backend",
      "env": {
        "DEBUG": "true"
      }
    }
  ]
}
```

**Logging:**
```python
import logging

logger = logging.getLogger(__name__)

# Debug level logging
logger.debug(f"Processing message: {message[:50]}...")
logger.info(f"Generated response in {elapsed:.2f}s")
logger.warning(f"Context retrieval returned 0 results")
logger.error(f"LLM generation failed: {error}")
```

---

## Performance Profiling

### Frontend

```bash
# Build for production
npm run build

# Analyze bundle size
npm run build -- --analyze
```

**Lighthouse:**
```bash
# Install globally
npm install -g lighthouse

# Run audit
lighthouse http://localhost:5173 --view
```

### Backend

```python
# Add timing decorator
import time
from functools import wraps

def timing(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        elapsed = time.time() - start
        logger.info(f"{func.__name__} took {elapsed:.2f}s")
        return result
    return wrapper

@timing
async def process_message(...):
    pass
```

**cProfile:**
```bash
python -m cProfile -o output.prof main.py
python -m pstats output.prof
```

---

## Git Workflow

### Branch Strategy

```
main          # Production-ready code
├── develop   # Integration branch
├── feature/* # New features
├── fix/*     # Bug fixes
└── docs/*    # Documentation
```

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Build/config changes

**Examples:**
```bash
feat(chat): add streaming LLM responses
fix(theme): resolve localStorage persistence issue
docs(api): update endpoint documentation
refactor(rag): optimize context retrieval query
test(chat): add InputBar component tests
chore(deps): update Svelte to 5.45.2
```

---

## Common Tasks

### Add New Character

1. Create JSON file:
```bash
# data/characters/mycharacter.json
{
  "id": "mycharacter",
  "name": "My Character",
  "avatar": "🤖",
  "description": "Character description",
  "personality": "Friendly, helpful",
  "greeting": "Hello!",
  "systemPrompt": "You are...",
  "exampleDialogues": [],
  "emotionalHooks": [],
  "chatCount": 0
}
```

2. Restart backend to load new character

---

### Change LLM Model

```bash
# Pull new model
ollama pull mistral:7b

# Update .env
DEFAULT_MODEL=mistral:7b

# Or via API (runtime)
curl -X PUT http://localhost:8000/api/config \
  -H "Content-Type: application/json" \
  -d '{"model_name":"mistral:7b"}'
```

---

### Clear Vector Database

```bash
# Delete all vector data
rm -rf data/vectorstore/*

# Restart backend to reinitialize
```

---

## Troubleshooting

### "Cannot connect to backend"

1. Check backend is running: `curl http://localhost:8000/api/health`
2. Check CORS settings in `backend/.env`
3. Check frontend API base URL

### "Ollama connection refused"

1. Check Ollama is running: `ollama list`
2. Verify `OLLAMA_BASE_URL` in `.env`
3. Restart Ollama: `ollama serve`

### "Module not found" (Python)

1. Activate venv: `source venv/bin/activate`
2. Reinstall: `pip install -r requirements.txt`
3. Check Python path: `which python`

---

## Next Steps

- [Testing Guide](testing.md)
- [Deployment Guide](deployment.md)
- [Contributing Guidelines](../../CONTRIBUTING.md)

---

**Happy coding! 🚀**
