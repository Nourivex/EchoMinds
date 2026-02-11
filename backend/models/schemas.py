"""
Pydantic models untuk API requests dan responses
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class LLMProvider(str, Enum):
    """Supported LLM providers"""
    OLLAMA = "ollama"
    LLAMACPP = "llamacpp"


class ChatRole(str, Enum):
    """Chat message roles"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


# ============ API Request Models ============

class ChatMessage(BaseModel):
    """Single chat message"""
    message: str = Field(..., min_length=1, max_length=4000, description="User message content")
    userId: str = Field(..., min_length=1, description="Unique user identifier")
    characterId: str = Field(..., description="Character ID to chat with")
    conversationId: Optional[str] = Field(None, description="Conversation ID for continuity")


class ModelConfigUpdate(BaseModel):
    """Model configuration update request"""
    model_name: Optional[str] = Field(None, description="Model name (e.g., llama3.2:3b)")
    cpu_threads: Optional[int] = Field(None, ge=1, le=32, description="Number of CPU threads")
    gpu_layers: Optional[int] = Field(None, ge=-1, le=100, description="GPU layers (-1 = all)")
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0, description="Sampling temperature")
    context_length: Optional[int] = Field(None, ge=512, le=32768, description="Context window size")
    max_tokens: Optional[int] = Field(None, ge=50, le=4096, description="Max generation tokens")


class CharacterCreateRequest(BaseModel):
    """Character creation request"""
    name: str = Field(..., min_length=1, max_length=50, description="Character name")
    avatar: str = Field(..., min_length=1, max_length=10, description="Character avatar emoji")
    description: str = Field(..., min_length=10, max_length=200, description="Short description")
    personality: str = Field(..., min_length=10, max_length=1000, description="Personality traits")
    background: Optional[str] = Field(None, max_length=2000, description="Character background/lore")
    language: str = Field(default="id", description="Primary language (id/en)")
    conversationStyle: str = Field(default="friendly", description="Conversation style")
    relationshipType: str = Field(default="friend", description="Relationship type with user")
    emotionalTone: str = Field(default="warm", description="Emotional tone")
    category: str = Field(default="supportive", description="Character category")
    greeting: Optional[str] = Field(None, description="Custom greeting message")
    systemPromptOverride: Optional[str] = Field(None, description="Custom system prompt (advanced)")


# ============ API Response Models ============

class ContextMessage(BaseModel):
    """Context message from RAG retrieval"""
    content: str = Field(..., description="Message content")
    role: ChatRole = Field(..., description="Message role")
    timestamp: str = Field(..., description="Message timestamp (ISO 8601)")
    relevance: float = Field(..., ge=0.0, le=1.0, description="Relevance score")


class ChatResponse(BaseModel):
    """Chat API response"""
    reply: str = Field(..., description="AI-generated response")
    characterName: str = Field(..., description="Character name")
    conversationId: str = Field(..., description="Conversation ID")
    context: List[ContextMessage] = Field(default_factory=list, description="Retrieved context messages")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata (tokens, latency, etc.)"
    )


class SystemStatus(BaseModel):
    """System status response"""
    status: str = Field(..., description="Overall system status")
    llm_provider: str = Field(..., description="Active LLM provider")
    model_loaded: str = Field(..., description="Currently loaded model")
    gpu_available: bool = Field(..., description="GPU availability")
    cpu_usage: float = Field(..., ge=0, le=100, description="CPU usage percentage")
    memory_usage: float = Field(..., ge=0, le=100, description="Memory usage percentage")
    uptime_seconds: float = Field(..., description="Server uptime")


class ModelConfig(BaseModel):
    """Current model configuration"""
    provider: str
    model_name: str
    cpu_threads: int
    gpu_layers: int
    temperature: float
    context_length: int
    max_tokens: int
    gpu_memory_used: Optional[float] = None  # GB
    cpu_memory_used: Optional[float] = None  # GB


class CharacterProfile(BaseModel):
    """Character profile data"""
    id: str
    name: str
    avatar: str
    description: str
    personality: str
    greeting: str
    systemPrompt: str
    exampleDialogues: List[Dict[str, str]] = Field(default_factory=list)


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    code: str = Field(..., description="Error code")


# ============ Internal Data Models ============

class ConversationMessage(BaseModel):
    """Internal conversation message storage"""
    id: str
    role: ChatRole
    content: str
    timestamp: datetime
    characterId: str
    userId: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class VectorDocument(BaseModel):
    """Document for vector storage"""
    id: str
    content: str
    metadata: Dict[str, Any]
    embedding: Optional[List[float]] = None
