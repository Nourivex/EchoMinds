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


class MemoryType(str, Enum):
    """Memory entry types"""
    FACTUAL = "factual"        # Facts about user or relationship
    EMOTIONAL = "emotional"    # Emotional moments (hurt, happy, etc)
    PINNED = "pinned"          # User-pinned important memories
    AUTO = "auto"              # Auto-generated from conversations


# ============ API Request Models ============

class ChatMessage(BaseModel):
    """Single chat message"""
    message: str = Field(..., min_length=1, max_length=4000, description="User message content")
    userId: str = Field(..., min_length=1, description="Unique user identifier")
    characterId: str = Field(..., description="Character ID to chat with")
    conversationId: Optional[str] = Field(None, description="Conversation ID for continuity")


class ModelConfigUpdate(BaseModel):
    """Model configuration update request"""
    model: Optional[str] = Field(None, description="Model name (e.g., llama3.2:3b)")
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0, description="Sampling temperature")
    max_tokens: Optional[int] = Field(None, ge=50, le=4096, description="Max generation tokens")
    # Advanced options (optional)
    cpu_threads: Optional[int] = Field(None, ge=1, le=32, description="Number of CPU threads")
    gpu_layers: Optional[int] = Field(None, ge=-1, le=100, description="GPU layers (-1 = all)")
    context_length: Optional[int] = Field(None, ge=512, le=32768, description="Context window size")


class CharacterCreateRequest(BaseModel):
    """Character creation request with advanced relationship settings"""
    # Core Identity
    name: str = Field(..., min_length=1, max_length=50, description="Character name")
    avatar: str = Field(..., min_length=1, max_length=10, description="Character avatar emoji")
    description: str = Field(..., min_length=10, max_length=200, description="Short description")
    personality: str = Field(..., min_length=10, max_length=1000, description="Personality traits")
    background: Optional[str] = Field(None, max_length=2000, description="Character background/lore")
    
    # Communication Settings
    language: str = Field(default="id", description="Primary language (id/en)")
    conversationStyle: str = Field(default="friendly", description="Conversation style")
    emotionalTone: str = Field(default="warm", description="Emotional tone")
    category: str = Field(default="supportive", description="Character category")
    
    # Relationship System (Advanced)
    relationshipType: str = Field(default="friend", description="Emotional relationship (friend/partner/mentor/rival)")
    relationshipRole: Optional[str] = Field(None, description="Social role (kakak/adik/senior/equal/custom)")
    relationshipLabel: Optional[str] = Field(None, description="Custom relationship name (e.g., 'kakak angkat')")
    
    # User Identity Awareness
    userName: Optional[str] = Field(None, description="How character addresses user")
    preferredAddress: Optional[str] = Field(None, description="Formal address (kamu/mas/mbak/sayang)")
    
    # Relative Positioning
    ageRelation: Optional[str] = Field(default="same", description="Age relative to user (older/younger/same)")
    authorityLevel: Optional[str] = Field(default="equal", description="Authority (higher/equal/lower)")
    
    # Advanced Overrides
    greeting: Optional[str] = Field(None, description="Custom greeting message")
    systemPromptOverride: Optional[str] = Field(None, description="Custom system prompt (advanced)")


class MemoryCreateRequest(BaseModel):
    """Request to create a memory entry"""
    content: str = Field(..., min_length=1, max_length=500, description="Memory content")
    memoryType: MemoryType = Field(default=MemoryType.FACTUAL, description="Type of memory")
    importance: float = Field(default=0.5, ge=0.0, le=1.0, description="Importance score (0-1)")
    isPinned: bool = Field(default=False, description="Whether memory is pinned")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class MemoryUpdateRequest(BaseModel):
    """Request to update a memory entry"""
    content: Optional[str] = Field(None, min_length=1, max_length=500)
    importance: Optional[float] = Field(None, ge=0.0, le=1.0)
    isPinned: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None


# ============ API Response Models ============

class ContextMessage(BaseModel):
    """Context message from RAG retrieval"""
    content: str = Field(..., description="Message content")
    role: ChatRole = Field(..., description="Message role")
    timestamp: str = Field(..., description="Message timestamp (ISO 8601)")
    relevance: float = Field(..., ge=0.0, le=1.0, description="Relevance score")


class StructuredMessageContent(BaseModel):
    """Structured message content for immersive chat"""
    dialogue: Optional[str] = Field(None, description="Spoken dialogue (in quotes)")
    action: Optional[str] = Field(None, description="Physical action or narration (in asterisks)")
    thought: Optional[str] = Field(None, description="Internal thought (in parentheses)")
    emotion: Optional[str] = Field(None, description="Emotional state or expression")
    
    # Translation (optional)
    translation: Optional[Dict[str, str]] = Field(
        None,
        description="Translations for dialogue, action, thought"
    )
    
    # Legacy support
    raw_content: Optional[str] = Field(None, description="Original unstructured message")


class ChatResponse(BaseModel):
    """Chat response with context"""
    reply: str = Field(..., description="AI-generated reply (legacy)")
    characterName: str = Field(..., description="Character name")
    conversationId: str = Field(..., description="Conversation ID")
    context: List[ContextMessage] = Field(default_factory=list, description="Retrieved context messages")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata (tokens, latency, etc.)"
    )
    
    # New structured content (optional, for immersive mode)
    structured: Optional[StructuredMessageContent] = Field(
        None,
        description="Structured message parts (dialogue, action, thought)"
    )


class SystemStatus(BaseModel):
    """System status response"""
    status: str = Field(..., description="Overall system status")
    version: str = Field(..., description="Application version")
    llm_provider: str = Field(..., description="Active LLM provider")
    model_loaded: str = Field(..., description="Currently loaded model")
    
    # Component Health
    components: Dict[str, str] = Field(..., description="Component status (healthy/degraded/down)")
    
    # Metrics
    metrics: Dict[str, int] = Field(..., description="System metrics (characters, memories, etc)")
    
    # Resource Usage
    gpu_available: bool = Field(..., description="GPU availability")
    cpu_usage: float = Field(..., ge=0, le=100, description="CPU usage percentage")
    memory_usage: float = Field(..., ge=0, le=100, description="Memory usage percentage")
    uptime_seconds: float = Field(..., description="Server uptime")


class MemoryEntry(BaseModel):
    """Memory entry response"""
    id: str = Field(..., description="Unique memory ID")
    characterId: str = Field(..., description="Character this memory belongs to")
    userId: str = Field(..., description="User this memory is about")
    content: str = Field(..., description="Memory content")
    memoryType: MemoryType = Field(..., description="Type of memory")
    importance: float = Field(..., ge=0.0, le=1.0, description="Importance score")
    isPinned: bool = Field(..., description="Whether pinned by user")
    createdAt: str = Field(..., description="Creation timestamp (ISO 8601)")
    updatedAt: str = Field(..., description="Last update timestamp (ISO 8601)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


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
