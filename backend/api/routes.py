"""FastAPI routes for EchoMinds backend."""

import logging
import psutil
import time
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from models.schemas import (
    ChatMessage,
    ChatResponse,
    ModelConfig,
    ModelConfigUpdate,
    SystemStatus,
    CharacterProfile,
    CharacterCreateRequest,
    ErrorResponse
)
from services.chat_service import chat_service
from services.character_service import character_service
from llm.ollama_service import ollama_service
from config.settings import settings

logger = logging.getLogger(__name__)

# Create API router
router = APIRouter(prefix="/api", tags=["api"])

# Store app start time for uptime calculation
app_start_time = time.time()


@router.get("/health")
async def health_check():
    """Health check endpoint.
    
    Returns:
        Health status with LLM availability
    """
    try:
        health_status = await ollama_service.check_health()
        return {
            "status": "healthy",
            "llm_provider": settings.llm_provider,
            "model_loaded": settings.default_model,
            "available_models": health_status.get("available_models", []),
            "gpu_available": health_status.get("gpu_available", False),
            "uptime_seconds": round(time.time() - app_start_time, 1)
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail="LLM service not available"
        )


@router.get("/status", response_model=SystemStatus)
async def get_system_status():
    """Get detailed system status with resource usage.
    
    Returns:
        SystemStatus with CPU/memory metrics
    """
    try:
        health = await ollama_service.check_health()
        
        return SystemStatus(
            status="running",
            llm_provider=settings.llm_provider,
            model_loaded=settings.default_model,
            gpu_available=health.get("gpu_available", False),
            cpu_usage=psutil.cpu_percent(interval=0.1),
            memory_usage=psutil.virtual_memory().percent,
            uptime_seconds=round(time.time() - app_start_time, 1)
        )
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        return SystemStatus(
            status="error",
            llm_provider=settings.llm_provider,
            model_loaded=settings.default_model,
            gpu_available=False,
            cpu_usage=0.0,
            memory_usage=0.0,
            uptime_seconds=0.0
        )


@router.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Process chat message and return AI response.
    
    Args:
        message: ChatMessage with user input
        
    Returns:
        ChatResponse with AI reply and context
        
    Raises:
        HTTPException: If validation or generation fails
    """
    try:
        response = await chat_service.process_message(
            character_id=message.characterId,
            user_id=message.userId,
            message=message.message,
            conversation_id=message.conversationId
        )
        return response
        
    except ValueError as e:
        logger.warning(f"Invalid chat request: {e}")
        raise HTTPException(status_code=400, detail=str(e))
        
    except Exception as e:
        logger.error(f"Chat processing failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate response: {str(e)}"
        )


@router.get("/config", response_model=ModelConfig)
async def get_config():
    """Get current model configuration.
    
    Returns:
        ModelConfig with current settings
    """
    return ModelConfig(
        model_name=settings.default_model,
        cpu_threads=settings.cpu_threads,
        gpu_layers=settings.gpu_layers,
        temperature=settings.temperature,
        context_length=settings.context_length,
        max_tokens=settings.max_tokens
    )


@router.put("/config", response_model=ModelConfig)
async def update_config(config: ModelConfigUpdate):
    """Update model configuration at runtime.
    
    Args:
        config: ModelConfigUpdate with new settings
        
    Returns:
        Updated ModelConfig
        
    Raises:
        HTTPException: If model not found or validation fails
    """
    try:
        # Update settings
        if config.model_name is not None:
            # Verify model exists
            health = await ollama_service.check_health()
            available_models = health.get("models", [])
            
            if config.model_name not in available_models:
                # Try to pull model
                logger.info(f"Pulling model: {config.model_name}")
                await ollama_service.pull_model(config.model_name)
            
            settings.default_model = config.model_name
        
        if config.cpu_threads is not None:
            settings.cpu_threads = config.cpu_threads
        
        if config.gpu_layers is not None:
            settings.gpu_layers = config.gpu_layers
        
        if config.temperature is not None:
            settings.temperature = config.temperature
        
        if config.context_length is not None:
            settings.context_length = config.context_length
        
        if config.max_tokens is not None:
            settings.max_tokens = config.max_tokens
        
        logger.info(f"Configuration updated: {config.model_dump(exclude_none=True)}")
        
        return ModelConfig(
            model_name=settings.default_model,
            cpu_threads=settings.cpu_threads,
            gpu_layers=settings.gpu_layers,
            temperature=settings.temperature,
            context_length=settings.context_length,
            max_tokens=settings.max_tokens
        )
        
    except Exception as e:
        logger.error(f"Config update failed: {e}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("/models")
async def list_models():
    """List available LLM models.
    
    Returns:
        Dictionary with models list
    """
    try:
        models = await ollama_service.get_model_info()
        return {"models": models}
    except Exception as e:
        logger.error(f"Failed to list models: {e}")
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve models"
        )


@router.get("/characters", response_model=List[CharacterProfile])
async def list_characters():
    """List all available characters.
    
    Returns:
        List of character profiles
    """
    try:
        characters = character_service.get_all_characters()
        return characters
    except Exception as e:
        logger.error(f"Failed to list characters: {e}")
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve characters"
        )


@router.post("/characters", response_model=CharacterProfile, status_code=201)
async def create_character(request: CharacterCreateRequest):
    """Create new AI character with advanced settings.
    
    This endpoint supports:
    - Separated personality traits and background lore
    - Language selection (ID/EN) with enforcement
    - Relationship dynamics (friend, partner, mentor, custom)
    - Emotional tone and conversation style
    - Category tagging
    
    Args:
        request: Character creation request with all settings
        
    Returns:
        Created CharacterProfile
        
    Raises:
        HTTPException: If character creation fails
    """
    try:
        character = character_service.create_character(request)
        logger.info(f"Character created via API: {character.name} (ID: {character.id})")
        return character
    except ValueError as e:
        # Character with same name exists
        logger.warning(f"Character creation failed: {e}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to create character: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Could not create character: {str(e)}"
        )


@router.get("/characters/{character_id}", response_model=CharacterProfile)
async def get_character(character_id: str):
    """Get specific character by ID.
    
    Args:
        character_id: Character identifier
        
    Returns:
        CharacterProfile
        
    Raises:
        HTTPException: If character not found
    """
    character = character_service.get_character(character_id)
    if not character:
        raise HTTPException(
            status_code=404,
            detail=f"Character not found: {character_id}"
        )
    return character


@router.delete("/conversations/{character_id}/{user_id}")
async def clear_conversation(character_id: str, user_id: str):
    """Clear conversation history for character-user pair.
    
    Args:
        character_id: Character identifier
        user_id: User identifier
        
    Returns:
        Success message with count
    """
    try:
        count = await chat_service.clear_conversation(
            character_id=character_id,
            user_id=user_id
        )
        return {
            "message": "Conversation cleared successfully",
            "deletedCount": count
        }
    except Exception as e:
        logger.error(f"Failed to clear conversation: {e}")
        raise HTTPException(
            status_code=500,
            detail="Could not clear conversation"
        )


@router.post("/embed")
async def generate_embedding(text: str = Query(..., min_length=1)):
    """Generate text embedding (for testing/debugging).
    
    Args:
        text: Text to embed
        
    Returns:
        Embedding vector and metadata
    """
    try:
        embedding = await ollama_service.generate_embedding(text)
        return {
            "embedding": embedding,
            "dimension": len(embedding),
            "model": settings.embedding_model
        }
    except Exception as e:
        logger.error(f"Embedding generation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="Could not generate embedding"
        )
