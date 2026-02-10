# REST API Endpoints

EchoMinds Backend menyediakan RESTful API untuk komunikasi frontend-backend.

**Base URL:** `http://localhost:8000`

---

## Authentication

🚧 **Coming Soon** - Saat ini tidak ada authentication (local development only).

Future: JWT Bearer token authentication.

```http
Authorization: Bearer <token>
```

---

## Health & Status

### GET `/api/health`

Check backend health dan LLM availability.

**Request:**
```http
GET /api/health HTTP/1.1
Host: localhost:8000
```

**Response `200 OK`:**
```json
{
  "status": "healthy",
  "llm_provider": "ollama",
  "model_loaded": "llama3.2:3b",
  "available_models": [
    "llama3.2:3b",
    "mistral:7b"
  ],
  "gpu_available": false,
  "uptime_seconds": 3600.5
}
```

**Response `503 Service Unavailable`:**
```json
{
  "detail": "LLM service not available"
}
```

---

### GET `/api/status`

Get detailed system status dengan resource usage.

**Request:**
```http
GET /api/status HTTP/1.1
Host: localhost:8000
```

**Response `200 OK`:**
```json
{
  "status": "running",
  "llm_provider": "ollama",
  "model_loaded": "llama3.2:3b",
  "gpu_available": false,
  "cpu_usage": 45.2,
  "memory_usage": 62.8,
  "uptime_seconds": 3600.5
}
```

**Fields:**
- `status`: `"running"` | `"error"` | `"initializing"`
- `cpu_usage`: CPU usage percentage (0-100)
- `memory_usage`: RAM usage percentage (0-100)
- `uptime_seconds`: Seconds since backend started

---

## Chat

### POST `/api/chat`

Send message dan receive AI response dengan RAG context.

**Request:**
```http
POST /api/chat HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "message": "Hello, how are you?",
  "userId": "lycus",
  "characterId": "luna",
  "conversationId": "optional-conversation-id"
}
```

**Request Body Schema:**
```typescript
interface ChatMessage {
  message: string;          // User message (max 2000 chars)
  userId: string;           // User identifier
  characterId: string;      // Character ID (luna, kai, etc.)
  conversationId?: string;  // Optional conversation tracking
}
```

**Response `200 OK`:**
```json
{
  "reply": "Hello Lycus! I'm doing wonderfully, thank you for asking! How can I help you today? 💜",
  "characterName": "Luna",
  "conversationId": "conv_123456",
  "context": [
    {
      "content": "Previous relevant message from context...",
      "role": "user",
      "timestamp": "2026-02-10T12:30:00Z",
      "relevance": 0.85
    },
    {
      "content": "Another relevant message...",
      "role": "assistant",
      "timestamp": "2026-02-10T12:31:00Z",
      "relevance": 0.78
    }
  ],
  "metadata": {
    "responseTime": 1.234,
    "tokenCount": 42,
    "model": "llama3.2:3b"
  }
}
```

**Response Body Schema:**
```typescript
interface ChatResponse {
  reply: string;                    // AI generated response
  characterName: string;            // Character name
  conversationId: string;           // Conversation ID
  context: ContextMessage[];        // RAG retrieved context
  metadata: {
    responseTime: number;           // Seconds
    tokenCount: number;             // Tokens generated
    model: string;                  // Model used
  };
}

interface ContextMessage {
  content: string;
  role: 'user' | 'assistant';
  timestamp: string;                // ISO 8601 format
  relevance: number;                // 0-1 similarity score
}
```

**Error Responses:**

`400 Bad Request`:
```json
{
  "detail": "Message cannot be empty"
}
```

`422 Unprocessable Entity`:
```json
{
  "detail": [
    {
      "loc": ["body", "message"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

`500 Internal Server Error`:
```json
{
  "detail": "LLM generation failed: timeout"
}
```

---

## Configuration

### GET `/api/config`

Get current model configuration.

**Request:**
```http
GET /api/config HTTP/1.1
Host: localhost:8000
```

**Response `200 OK`:**
```json
{
  "model_name": "llama3.2:3b",
  "cpu_threads": 4,
  "gpu_layers": 0,
  "temperature": 0.8,
  "context_length": 4096,
  "max_tokens": 512
}
```

---

### PUT `/api/config`

Update model configuration (runtime).

**Request:**
```http
PUT /api/config HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "model_name": "mistral:7b",
  "cpu_threads": 8,
  "gpu_layers": -1,
  "temperature": 0.7,
  "context_length": 8192,
  "max_tokens": 1024
}
```

**Request Body Schema:**
```typescript
interface ModelConfigUpdate {
  model_name?: string;      // Optional: Switch model
  cpu_threads?: number;     // 1-32
  gpu_layers?: number;      // -1 (all GPU), 0 (CPU), >0 (partial)
  temperature?: number;     // 0.0-2.0
  context_length?: number;  // 512-32768
  max_tokens?: number;      // 1-4096
}
```

**Response `200 OK`:**
```json
{
  "model_name": "mistral:7b",
  "cpu_threads": 8,
  "gpu_layers": -1,
  "temperature": 0.7,
  "context_length": 8192,
  "max_tokens": 1024
}
```

**Error Responses:**

`400 Bad Request`:
```json
{
  "detail": "Model 'nonexistent:model' not found"
}
```

`422 Unprocessable Entity`:
```json
{
  "detail": "temperature must be between 0.0 and 2.0"
}
```

---

## Models

### GET `/api/models`

List available LLM models.

**Request:**
```http
GET /api/models HTTP/1.1
Host: localhost:8000
```

**Response `200 OK`:**
```json
{
  "models": [
    {
      "name": "llama3.2:3b",
      "size": "2.0GB",
      "parameter_count": "3B",
      "quantization": "Q4_0",
      "loaded": true
    },
    {
      "name": "mistral:7b",
      "size": "4.1GB",
      "parameter_count": "7B",
      "quantization": "Q4_0",
      "loaded": false
    }
  ]
}
```

---

## Characters

### GET `/api/characters`

List all available characters.

**Request:**
```http
GET /api/characters HTTP/1.1
Host: localhost:8000
```

**Response `200 OK`:**
```json
{
  "characters": [
    {
      "id": "luna",
      "name": "Luna",
      "avatar": "👱‍♀️",
      "description": "Free spirit dengan creative energy tak terbatas",
      "personality": "Playful, imaginative, encouraging",
      "greeting": "Hey there! ✨ Ready for an adventure?",
      "chatCount": 1523,
      "emotionalHooks": ["creativity", "adventure", "positivity"]
    },
    {
      "id": "kai",
      "name": "Kai",
      "avatar": "🧑‍💼",
      "description": "Problem solver yang analytical dan straightforward",
      "personality": "Logical, direct, supportive",
      "greeting": "Hi. What can I help you with today?",
      "chatCount": 892,
      "emotionalHooks": ["logic", "problem-solving", "clarity"]
    }
  ]
}
```

---

### GET `/api/characters/:id`

Get specific character details.

**Request:**
```http
GET /api/characters/luna HTTP/1.1
Host: localhost:8000
```

**Response `200 OK`:**
```json
{
  "id": "luna",
  "name": "Luna",
  "avatar": "👱‍♀️",
  "description": "Free spirit dengan creative energy tak terbatas",
  "personality": "Playful, imaginative, encouraging",
  "greeting": "Hey there! ✨ Ready for an adventure?",
  "systemPrompt": "You are Luna, a creative and playful AI companion...",
  "exampleDialogues": [
    {
      "user": "I'm feeling stuck on my project",
      "assistant": "Oh no! Let's brainstorm together! What if we..."
    }
  ],
  "emotionalHooks": ["creativity", "adventure", "positivity"],
  "chatCount": 1523
}
```

**Error `404 Not Found`:**
```json
{
  "detail": "Character 'unknown' not found"
}
```

---

## Conversations

### GET `/api/conversations/:characterId/:userId`

Get conversation history.

**Request:**
```http
GET /api/conversations/luna/lycus?limit=50&offset=0 HTTP/1.1
Host: localhost:8000
```

**Query Parameters:**
- `limit`: Number of messages (default: 50, max: 200)
- `offset`: Pagination offset (default: 0)

**Response `200 OK`:**
```json
{
  "messages": [
    {
      "id": "msg_123",
      "role": "user",
      "content": "Hello!",
      "timestamp": "2026-02-10T12:00:00Z"
    },
    {
      "id": "msg_124",
      "role": "assistant",
      "content": "Hey there! ✨",
      "timestamp": "2026-02-10T12:00:05Z"
    }
  ],
  "total": 156,
  "hasMore": true
}
```

---

### DELETE `/api/conversations/:characterId/:userId`

Clear conversation history untuk specific character-user pair.

**Request:**
```http
DELETE /api/conversations/luna/lycus HTTP/1.1
Host: localhost:8000
```

**Response `200 OK`:**
```json
{
  "message": "Conversation cleared successfully",
  "deletedCount": 156
}
```

---

## Embeddings (Internal)

### POST `/api/embed`

Generate text embeddings (untuk testing/debugging).

**Request:**
```http
POST /api/embed HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "text": "Hello world",
  "model": "all-MiniLM-L6-v2"
}
```

**Response `200 OK`:**
```json
{
  "embedding": [0.123, -0.456, 0.789, ...],  // 384-dim vector
  "dimension": 384,
  "model": "all-MiniLM-L6-v2"
}
```

---

## Error Responses

All errors follow consistent format:

```typescript
interface ErrorResponse {
  detail: string | ValidationError[];
}

interface ValidationError {
  loc: string[];        // Field location
  msg: string;          // Error message
  type: string;         // Error type
}
```

### HTTP Status Codes

- `200 OK` - Success
- `400 Bad Request` - Invalid input
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - LLM service down

---

## Rate Limiting

🚧 **Coming Soon**

Future: Rate limiting per user/IP.
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1707652800
```

---

## Websocket API (Future)

Streaming LLM responses via WebSocket:

```javascript
const ws = new WebSocket('ws://localhost:8000/api/ws/chat');

ws.send(JSON.stringify({
  message: 'Tell me a story',
  userId: 'lycus',
  characterId: 'luna'
}));

ws.onmessage = (event) => {
  const chunk = JSON.parse(event.data);
  console.log(chunk.text);  // Streaming token
};
```

---

## OpenAPI Documentation

Interactive API docs available at:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

---

## Example Usage

### JavaScript/TypeScript

```typescript
// api.ts
const BASE_URL = 'http://localhost:8000';

async function sendMessage(
  message: string,
  userId: string,
  characterId: string
): Promise<ChatResponse> {
  const response = await fetch(`${BASE_URL}/api/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ message, userId, characterId })
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }

  return response.json();
}

// Usage
const response = await sendMessage(
  'Hello!',
  'lycus',
  'luna'
);
console.log(response.reply);
```

### Python

```python
import requests

BASE_URL = 'http://localhost:8000'

def send_message(message: str, user_id: str, character_id: str):
    response = requests.post(
        f'{BASE_URL}/api/chat',
        json={
            'message': message,
            'userId': user_id,
            'characterId': character_id
        }
    )
    response.raise_for_status()
    return response.json()

# Usage
response = send_message('Hello!', 'lycus', 'luna')
print(response['reply'])
```

### cURL

```bash
# Send chat message
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello!",
    "userId": "lycus",
    "characterId": "luna"
  }'

# Get system status
curl http://localhost:8000/api/status

# Update config
curl -X PUT http://localhost:8000/api/config \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 0.9,
    "max_tokens": 1024
  }'
```

---

## Next Steps

- [Request/Response Models](models.md)
- [Frontend API Service](../guides/development.md#api-service)
- [Backend Implementation](../architecture/backend.md)

---

**API documentation complete!**
