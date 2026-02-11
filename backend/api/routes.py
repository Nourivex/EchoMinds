"""Main API router - aggregates all route modules."""

from fastapi import APIRouter

# Import all route modules
from api.routes_health import router as health_router
from api.routes_chat import router as chat_router
from api.routes_characters import router as characters_router
from api.routes_memories import router as memories_router
from api.routes_models import router as models_router

# Create main router
router = APIRouter(prefix="/api")

# Include all sub-routers
router.include_router(health_router)
router.include_router(chat_router)
router.include_router(characters_router)
router.include_router(memories_router)
router.include_router(models_router)
