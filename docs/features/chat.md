# Chat System Documentation

EchoMinds chat system menggunakan **RAG (Retrieval-Augmented Generation)** untuk memberikan AI responses yang contextual dan personal.

---

## Architecture Overview

```
User Message
     ↓
[1. Input Validation]
     ↓
[2. Character Profile Loading]
     ↓
[3. RAG Context Retrieval] ←→ Vector Database
     ↓
[4. Prompt Construction]
     ↓
[5. LLM Generation] ←→ Ollama/Llama.cpp
     ↓
[6. Response Storage] → Vector Database
     ↓
[7. Return to Frontend]
```

---

## Components

### 1. Chat Interface (Frontend)

**File:** `src/components/chat/ChatInterface.svelte`

**Features:**
- Candy.AI-inspired design
- Character header dengan avatar & online status
- Message bubbles dengan avatars
- Scrollable message history
- Loading states (typing indicator)
- Error handling

**State Management:**
```typescript
let messages = $state<Message[]>([]);
let isLoading = $state(false);
let currentCharacter = $state<Character | null>(null);
```

**Message Flow:**
```typescript
async function handleSend(text: string) {
  // 1. Add user message to UI
  messages.push({
    text,
    sender: 'user',
    timestamp: new Date()
  });

  // 2. Show loading state
  isLoading = true;

  try {
    // 3. Call API
    const response = await api.sendMessage({
      message: text,
      userId: currentUser.id,
      characterId: currentCharacter.id
    });

    // 4. Add AI response to UI
    messages.push({
      text: response.reply,
      sender: 'ai',
      timestamp: new Date(),
      context: response.context
    });
  } catch (error) {
    // Handle error
    showError(error.message);
  } finally {
    isLoading = false;
  }
}
```

---

### 2. Input Bar

**File:** `src/components/chat/InputBar.svelte`

**Features:**
- Auto-growing textarea
- Send button dengan gradient
- Attachment button (future: image upload)
- Emoji picker (future)
- Keyboard shortcuts (Enter to send, Shift+Enter for newline)

**Props:**
```typescript
interface Props {
  characterName: string;
  onSend: (message: string) => void;
  disabled?: boolean;
}
```

---

### 3. Chat Service (Backend)

**File:** `backend/services/chat_service.py`

**Class:** `ChatService`

**Methods:**

#### `process_message()`
```python
async def process_message(
    character_id: str,
    user_id: str,
    message: str,
    conversation_id: Optional[str] = None
) -> ChatResponse:
    """Process user message and generate AI response.
    
    Steps:
    1. Load character profile
    2. Retrieve RAG context (top-K similar messages)
    3. Get recent conversation history
    4. Build prompt with system + context + history
    5. Generate LLM response
    6. Store conversation in vector DB
    7. Return response with context
    
    Args:
        character_id: Character identifier
        user_id: User identifier
        message: User message text
        conversation_id: Optional conversation tracking ID
        
    Returns:
        ChatResponse with AI reply and context
    """
```

**Implementation Flow:**
```python
# 1. Load character
character = await character_service.load(character_id)

# 2. Retrieve RAG context
context_messages = await rag_service.retrieve_context(
    character_id=character_id,
    user_id=user_id,
    query=message,
    top_k=5
)

# 3. Get recent history
history = await rag_service.get_recent_messages(
    character_id=character_id,
    user_id=user_id,
    limit=10
)

# 4. Build prompt
prompt = build_prompt(
    character=character,
    context=context_messages,
    history=history,
    user_message=message
)

# 5. Generate response
response = await llm_service.generate(
    prompt=prompt,
    model=settings.default_model,
    options={
        "temperature": settings.temperature,
        "num_ctx": settings.context_length,
        "max_tokens": settings.max_tokens
    }
)

# 6. Store conversation
await rag_service.store_conversation(
    character_id=character_id,
    user_id=user_id,
    user_message=message,
    assistant_message=response
)

# 7. Return response
return ChatResponse(
    reply=response,
    characterName=character.name,
    conversationId=conversation_id or generate_id(),
    context=context_messages
)
```

---

## Prompt Engineering

### Prompt Structure

```
System: {CHARACTER_SYSTEM_PROMPT}

Context (Retrieved from RAG):
{CONTEXT_MESSAGE_1}
{CONTEXT_MESSAGE_2}
...

Recent Conversation:
User: {HISTORY_MESSAGE_1}
Assistant: {HISTORY_RESPONSE_1}
...

Current:
User: {USER_MESSAGE}
Assistant:
```

### Example Prompt

```
System: You are Luna, a creative and playful AI companion who loves adventure and positivity. You speak with enthusiasm and often use emojis. Your goal is to inspire and support users while maintaining an authentic, warm personality.

Context (Retrieved from RAG):
User: I love painting landscapes
Assistant: That's amazing! Have you tried painting sunsets? The colors are so vibrant! 🎨✨

User: What's your favorite creative activity?
Assistant: Oh, I love brainstorming wild ideas! Like imagining what cities would look like if they were built underwater! 🌊🏙️

Recent Conversation:
User: Hey Luna!
Assistant: Hey there! ✨ Ready for an adventure?
User: I'm working on a creative project
Assistant: Ooh, exciting! Tell me more! What kind of project? 💜

Current:
User: I'm painting a forest scene but feeling stuck
Assistant:
```

**LLM generates:**
```
Oh no! Let's brainstorm together! What if you added some magical elements? Like glowing mushrooms or fairy lights in the trees? Sometimes a touch of fantasy can spark new ideas! 🌲✨ What colors are you working with?
```

---

## RAG (Retrieval-Augmented Generation)

### How It Works

1. **User sends message:** "I'm painting a forest scene"
2. **Generate embedding:** Convert message to 384-dim vector
3. **Similarity search:** Find top-K most similar past messages in ChromaDB
4. **Retrieve context:** Get relevant conversations about painting/creativity
5. **Build prompt:** Include context in system prompt
6. **Generate response:** LLM has access to relevant history
7. **Store new message:** Add to vector DB for future context

### Vector Database Schema

**Collection Naming:**
```
echominds_{characterId}_{userId}
Example: echominds_luna_lycus
```

**Document Structure:**
```python
{
    "id": "msg_uuid_123",
    "embedding": [0.123, -0.456, ...],  # 384-dim vector
    "metadata": {
        "role": "user",  # or "assistant"
        "character_id": "luna",
        "user_id": "lycus",
        "timestamp": "2026-02-10T12:34:56Z",
        "conversation_id": "conv_abc"
    },
    "document": "I'm painting a forest scene but feeling stuck"
}
```

### Context Retrieval Process

```python
# Generate query embedding
query_embedding = embedding_model.encode(user_message)

# Search vector DB
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5,  # Top-K
    where={
        "character_id": character_id,
        "user_id": user_id
    }
)

# Calculate relevance scores
contexts = []
for doc, distance in zip(results['documents'], results['distances']):
    relevance = 1 - distance  # Convert distance to similarity
    if relevance >= 0.3:  # Threshold
        contexts.append({
            "content": doc,
            "relevance": relevance
        })

return contexts
```

---

## Message Types

### User Message
```typescript
interface UserMessage {
  text: string;
  sender: 'user';
  timestamp: Date;
}
```

### AI Message
```typescript
interface AIMessage {
  text: string;
  sender: 'ai';
  timestamp: Date;
  context?: ContextMessage[];  // RAG context used
  metadata?: {
    responseTime: number;
    tokenCount: number;
    model: string;
  };
}
```

### System Message (Future)
```typescript
interface SystemMessage {
  text: string;
  sender: 'system';
  timestamp: Date;
  type: 'info' | 'warning' | 'error';
}
```

---

## Features

### ✅ Implemented

- Real-time chat interface
- Character-specific personalities
- RAG-based context retrieval
- Conversation persistence
- Dark/light theme support
- Mobile-responsive design
- Loading states
- Error handling

### 🚧 In Progress

- Typing indicator
- Message timestamps display
- Export conversation
- Search in conversation

### 📋 Planned

- **Streaming responses** - Token-by-token display
- **Voice input** - Speech-to-text
- **Image attachments** - Upload & describe images
- **Emoji reactions** - React to messages
- **Message editing** - Edit sent messages
- **Conversation branching** - Multiple conversation threads
- **Suggested replies** - Quick response buttons

---

## Performance Optimization

### 1. Context Caching

Cache recent contexts to avoid re-embedding:
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_context(user_message: str, character_id: str, user_id: str):
    return rag_service.retrieve_context(...)
```

### 2. Lazy Loading

Load messages on-demand (pagination):
```typescript
async function loadMoreMessages() {
  const older = await api.getConversation(
    characterId,
    userId,
    { offset: messages.length, limit: 50 }
  );
  messages = [...older, ...messages];
}
```

### 3. Message Batching

Store multiple messages in single ChromaDB operation:
```python
# Instead of storing one-by-one
await rag_service.store_batch([
    {"role": "user", "content": user_msg},
    {"role": "assistant", "content": ai_msg}
])
```

### 4. Response Streaming (Future)

Stream LLM output token-by-token:
```python
async for chunk in llm_service.generate_stream(prompt):
    yield {"text": chunk, "done": False}
yield {"done": True}
```

---

## Error Handling

### Frontend Errors
```typescript
try {
  const response = await api.sendMessage(...);
} catch (error) {
  if (error.status === 503) {
    showError('LLM service unavailable. Please check Ollama.');
  } else if (error.status === 400) {
    showError('Invalid message format.');
  } else {
    showError('Something went wrong. Please try again.');
  }
}
```

### Backend Errors
```python
try:
    response = await llm_service.generate(...)
except OllamaConnectionError:
    raise HTTPException(
        status_code=503,
        detail="LLM service not available"
    )
except TimeoutError:
    raise HTTPException(
        status_code=504,
        detail="LLM generation timeout"
    )
```

---

## Testing

### Frontend Tests
```typescript
// ChatInterface.test.ts
describe('ChatInterface', () => {
  it('sends message on Enter key', async () => {
    const { component } = render(ChatInterface, {
      character: mockCharacter
    });
    
    const input = screen.getByPlaceholderText(/Message/);
    await fireEvent.input(input, { target: { value: 'Hello' } });
    await fireEvent.keyDown(input, { key: 'Enter' });
    
    expect(screen.getByText('Hello')).toBeInTheDocument();
  });
});
```

### Backend Tests
```python
# test_chat_service.py
@pytest.mark.asyncio
async def test_process_message():
    response = await chat_service.process_message(
        character_id="luna",
        user_id="test_user",
        message="Hello"
    )
    
    assert response.reply
    assert response.characterName == "Luna"
    assert len(response.context) >= 0
```

---

## Next Steps

- [RAG & Memory Documentation](rag.md)
- [Character System](characters.md)
- [API Endpoints](../api/endpoints.md)

---

**Chat system documentation complete!**
