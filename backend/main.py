"""FastAPI main application for EchoMinds backend."""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config.settings import settings
from api.routes import router
from llm.ollama_service import ollama_service

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(settings.log_file) if settings.log_file else logging.NullHandler()
    ]
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events.
    
    Startup:
    - Check LLM service health
    - Warm up services
    
    Shutdown:
    - Cleanup resources
    """
    # Startup
    logger.info("=" * 50)
    logger.info("🚀 EchoMinds Backend Starting...")
    logger.info(f"Environment: {'DEBUG' if settings.debug else 'PRODUCTION'}")
    logger.info(f"LLM Provider: {settings.llm_provider}")
    logger.info(f"Default Model: {settings.default_model}")
    logger.info(f"CPU Threads: {settings.cpu_threads}")
    logger.info(f"GPU Layers: {settings.gpu_layers}")
    logger.info("=" * 50)
    
    try:
        # Check LLM service
        logger.info("Checking LLM service health...")
        health = await ollama_service.check_health()
        logger.info(f"✓ LLM service available with {len(health.get('models', []))} models")
        
        # Verify default model
        available_models = health.get('models', [])
        if settings.default_model not in available_models:
            logger.warning(
                f"Default model '{settings.default_model}' not found. "
                f"Available models: {', '.join(available_models)}"
            )
            if available_models:
                logger.info("Consider running: ollama pull {settings.default_model}")
        else:
            logger.info(f"✓ Default model '{settings.default_model}' ready")
        
    except Exception as e:
        logger.error(f"⚠️  LLM service check failed: {e}")
        logger.warning("Backend will start but chat functionality may not work")
    
    logger.info("✓ Backend startup complete")
    logger.info(f"API Docs: http://{settings.api_host}:{settings.api_port}/docs")
    
    yield  # Application running
    
    # Shutdown
    logger.info("Shutting down EchoMinds backend...")
    logger.info("✓ Cleanup complete")


# Create FastAPI application
app = FastAPI(
    title="EchoMinds API",
    description="Backend API for EchoMinds AI companion platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
logger.info(f"CORS Origins: {settings.cors_origins}")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle uncaught exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error" if not settings.debug else str(exc)
        }
    )


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "EchoMinds API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/api/health"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
        log_level=settings.log_level.lower()
    )
