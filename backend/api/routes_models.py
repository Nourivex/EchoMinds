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
        provider=settings.llm_provider,
        model_name=settings.default_model,
        cpu_threads=settings.cpu_threads,
        gpu_layers=settings.gpu_layers,
        temperature=settings.temperature,
        context_length=settings.context_length,
        max_tokens=settings.max_tokens
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
        
    if config.cpu_threads is not None:
        settings.cpu_threads = config.cpu_threads
        
    if config.gpu_layers is not None:
        settings.gpu_layers = config.gpu_layers
        
    if config.context_length is not None:
        settings.context_length = config.context_length
    
    logger.info(f"Updated config: model={settings.default_model}, temp={settings.temperature}")
    
    return ModelConfig(
        provider=settings.llm_provider,
        model_name=settings.default_model,
        cpu_threads=settings.cpu_threads,
        gpu_layers=settings.gpu_layers,
        temperature=settings.temperature,
        context_length=settings.context_length,
        max_tokens=settings.max_tokens
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
