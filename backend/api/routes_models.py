"""LLM model configuration endpoints."""

import logging
from typing import List
from fastapi import APIRouter, HTTPException, Query

from models.schemas import ModelConfig, ModelConfigUpdate
from llm.ollama_service import ollama_service
from config.settings import settings

logger = logging.getLogger(__name__)

router = APIRouter(tags=["models"])


@router.get("/models", response_model=List[str])
async def list_available_models():
    """Get list of available LLM models.
    
    Returns:
        List of model names
    """
    try:
        health = await ollama_service.check_health()
        return health.get("available_models", [])
        
    except Exception as e:
        logger.error(f"Failed to fetch models: {e}")
        raise HTTPException(
            status_code=503,
            detail="LLM service not available"
        )


@router.get("/config", response_model=ModelConfig)
async def get_model_config():
    """Get current model configuration.
    
    Returns:
        ModelConfig with current settings
    """
    return ModelConfig(
        model=settings.default_model,
        temperature=settings.temperature,
        max_tokens=settings.max_tokens,
        top_p=settings.top_p,
        top_k=settings.top_k,
        llm_provider=settings.llm_provider
    )


@router.put("/config", response_model=ModelConfig)
async def update_model_config(config: ModelConfigUpdate):
    """Update model configuration.
    
    Args:
        config: New configuration settings
        
    Returns:
        Updated ModelConfig
    """
    if config.model:
        settings.default_model = config.model
        
    if config.temperature is not None:
        settings.temperature = config.temperature
        
    if config.max_tokens is not None:
        settings.max_tokens = config.max_tokens
        
    if config.top_p is not None:
        settings.top_p = config.top_p
        
    if config.top_k is not None:
        settings.top_k = config.top_k
    
    logger.info(f"Updated config: model={settings.default_model}, temp={settings.temperature}")
    
    return ModelConfig(
        model=settings.default_model,
        temperature=settings.temperature,
        max_tokens=settings.max_tokens,
        top_p=settings.top_p,
        top_k=settings.top_k,
        llm_provider=settings.llm_provider
    )


@router.post("/embed")
async def generate_embedding(text: str = Query(..., min_length=1, max_length=5000)):
    """Generate text embedding.
    
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
