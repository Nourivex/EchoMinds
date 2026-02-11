"""Health and status check endpoints."""

import logging
import psutil
import time
import os
from fastapi import APIRouter

from models.schemas import SystemStatus
from llm.ollama_service import ollama_service
from config.settings import settings

logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])

# App version
APP_VERSION = "2.0.0"  # Updated with long-term memory system

# Store app start time for uptime calculation
app_start_time = time.time()


@router.get("/health")
async def health_check():
    """Modern health check endpoint with detailed component status.
    
    Returns:
        Comprehensive health status with component breakdown
    """
    try:
        health_status = await ollama_service.check_health()
        
        # Check component health
        components = {
            "llm": "healthy" if health_status.get("available_models") else "down",
            "vector_db": "healthy",
            "memory_store": "healthy" if os.path.exists("data/memories") else "down",
            "character_store": "healthy" if os.path.exists("data/characters") else "down"
        }
        
        # Calculate overall status
        overall_status = "healthy" if all(v == "healthy" for v in components.values()) else "degraded"
        
        # Count resources
        character_files = len([f for f in os.listdir("data/characters") if f.endswith(".json")]) if os.path.exists("data/characters") else 0
        memory_files = len([f for f in os.listdir("data/memories") if f.endswith(".json")]) if os.path.exists("data/memories") else 0
        
        return {
            "status": overall_status,
            "version": APP_VERSION,
            "timestamp": time.time(),
            "components": components,
            "llm": {
                "provider": settings.llm_provider,
                "model": settings.default_model,
                "available_models": len(health_status.get("available_models", [])),
                "gpu_available": health_status.get("gpu_available", False)
            },
            "metrics": {
                "characters": character_files,
                "memory_files": memory_files,
                "uptime_seconds": round(time.time() - app_start_time, 1)
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "error",
            "version": APP_VERSION,
            "timestamp": time.time(),
            "error": str(e),
            "components": {
                "llm": "unknown",
                "vector_db": "unknown",
                "memory_store": "unknown",
                "character_store": "unknown"
            }
        }


@router.get("/status", response_model=SystemStatus)
async def get_system_status():
    """Get detailed system status with resource usage.
    
    Returns:
        SystemStatus with CPU/memory metrics and component health
    """
    try:
        health = await ollama_service.check_health()
        
        # Component health checks
        components = {
            "llm": "healthy" if health.get("available_models") else "down",
            "vector_db": "healthy",
            "memory_store": "healthy" if os.path.exists("data/memories") else "down",
            "character_store": "healthy" if os.path.exists("data/characters") else "down"
        }
        
        # Count resources
        character_count = len([f for f in os.listdir("data/characters") if f.endswith(".json")]) if os.path.exists("data/characters") else 0
        memory_count = len([f for f in os.listdir("data/memories") if f.endswith(".json")]) if os.path.exists("data/memories") else 0
        
        return SystemStatus(
            status="running",
            version=APP_VERSION,
            llm_provider=settings.llm_provider,
            model_loaded=settings.default_model,
            components=components,
            metrics={
                "characters": character_count,
                "memories": memory_count,
                "models_available": len(health.get("available_models", []))
            },
            gpu_available=health.get("gpu_available", False),
            cpu_usage=psutil.cpu_percent(interval=0.1),
            memory_usage=psutil.virtual_memory().percent,
            uptime_seconds=round(time.time() - app_start_time, 1)
        )
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        return SystemStatus(
            status="error",
            version=APP_VERSION,
            llm_provider=settings.llm_provider,
            model_loaded=settings.default_model,
            components={},
            metrics={},
            gpu_available=False,
            cpu_usage=0.0,
            memory_usage=0.0,
            uptime_seconds=0.0
        )
