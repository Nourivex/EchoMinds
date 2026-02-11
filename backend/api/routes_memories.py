"""Memory management endpoints."""

import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Path

from models.schemas import MemoryEntry, MemoryCreateRequest, MemoryUpdateRequest, MemoryType
from services.memory_service import memory_service
from services.character_service import character_service

logger = logging.getLogger(__name__)

router = APIRouter(tags=["memories"])


@router.post("/memories/{character_id}/{user_id}", response_model=MemoryEntry, status_code=201)
async def create_memory(
    character_id: str = Path(..., description="Character ID"),
    user_id: str = Path(..., description="User ID"),
    request: MemoryCreateRequest = None
):
    """Create a new memory entry for a character-user relationship.
    
    Args:
        character_id: Character identifier
        user_id: User identifier
        request: Memory creation request
        
    Returns:
        Created MemoryEntry
    """
    try:
        # Verify character exists
        character = character_service.get_character(character_id)
        if not character:
            raise HTTPException(status_code=404, detail=f"Character not found: {character_id}")
        
        memory = memory_service.create_memory(character_id, user_id, request)
        logger.info(f"Created memory {memory.id} for {character_id}/{user_id}")
        return memory
        
    except Exception as e:
        logger.error(f"Failed to create memory: {e}")
        raise HTTPException(status_code=500, detail=f"Could not create memory: {str(e)}")


@router.get("/memories/{character_id}/{user_id}", response_model=List[MemoryEntry])
async def get_memories(
    character_id: str = Path(..., description="Character ID"),
    user_id: str = Path(..., description="User ID"),
    memory_type: Optional[MemoryType] = Query(None, description="Filter by memory type"),
    pinned_only: bool = Query(False, description="Only return pinned memories")
):
    """Get all memories for a character-user relationship.
    
    Args:
        character_id: Character identifier
        user_id: User identifier
        memory_type: Optional filter by type
        pinned_only: Only return pinned memories
        
    Returns:
        List of MemoryEntry
    """
    try:
        memories = memory_service.get_all_memories(
            character_id=character_id,
            user_id=user_id,
            memory_type=memory_type,
            pinned_only=pinned_only
        )
        return memories
        
    except Exception as e:
        logger.error(f"Failed to retrieve memories: {e}")
        raise HTTPException(status_code=500, detail=f"Could not retrieve memories: {str(e)}")


@router.get("/memories/{character_id}/{user_id}/stats")
async def get_memory_stats(
    character_id: str = Path(..., description="Character ID"),
    user_id: str = Path(..., description="User ID")
):
    """Get memory statistics for a character-user relationship.
    
    Args:
        character_id: Character identifier
        user_id: User identifier
        
    Returns:
        Memory statistics
    """
    try:
        stats = memory_service.get_memory_statistics(character_id, user_id)
        return stats
        
    except Exception as e:
        logger.error(f"Failed to retrieve memory stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/memories/{character_id}/{user_id}/{memory_id}", response_model=MemoryEntry)
async def get_memory(
    character_id: str = Path(..., description="Character ID"),
    user_id: str = Path(..., description="User ID"),
    memory_id: str = Path(..., description="Memory ID")
):
    """Get a specific memory by ID.
    
    Args:
        character_id: Character identifier
        user_id: User identifier
        memory_id: Memory identifier
        
    Returns:
        MemoryEntry
    """
    memory = memory_service.get_memory(character_id, user_id, memory_id)
    if not memory:
        raise HTTPException(
            status_code=404,
            detail=f"Memory not found: {memory_id}"
        )
    return memory


@router.put("/memories/{character_id}/{user_id}/{memory_id}", response_model=MemoryEntry)
async def update_memory(
    character_id: str = Path(..., description="Character ID"),
    user_id: str = Path(..., description="User ID"),
    memory_id: str = Path(..., description="Memory ID"),
    request: MemoryUpdateRequest = None
):
    """Update an existing memory.
    
    Args:
        character_id: Character identifier
        user_id: User identifier
        memory_id: Memory identifier
        request: Memory update request
        
    Returns:
        Updated MemoryEntry
    """
    memory = memory_service.update_memory(character_id, user_id, memory_id, request)
    if not memory:
        raise HTTPException(
            status_code=404,
            detail=f"Memory not found: {memory_id}"
        )
    logger.info(f"Updated memory {memory_id} for {character_id}/{user_id}")
    return memory


@router.delete("/memories/{character_id}/{user_id}/{memory_id}", status_code=204)
async def delete_memory(
    character_id: str = Path(..., description="Character ID"),
    user_id: str = Path(..., description="User ID"),
    memory_id: str = Path(..., description="Memory ID")
):
    """Delete a memory by ID.
    
    Args:
        character_id: Character identifier
        user_id: User identifier
        memory_id: Memory identifier
        
    Returns:
        No content on success
    """
    success = memory_service.delete_memory(character_id, user_id, memory_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Memory not found: {memory_id}"
        )
    logger.info(f"Deleted memory {memory_id} for {character_id}/{user_id}")
    return None


@router.post("/memories/{character_id}/{user_id}/{memory_id}/pin", response_model=MemoryEntry)
async def pin_memory(
    character_id: str = Path(..., description="Character ID"),
    user_id: str = Path(..., description="User ID"),
    memory_id: str = Path(..., description="Memory ID"),
    pinned: bool = Query(True, description="Pin (true) or unpin (false)")
):
    """Pin or unpin a memory.
    
    Pinned memories are always included in chat context.
    
    Args:
        character_id: Character identifier
        user_id: User identifier
        memory_id: Memory identifier
        pinned: Whether to pin or unpin
        
    Returns:
        Updated MemoryEntry
    """
    memory = memory_service.pin_memory(character_id, user_id, memory_id, pinned)
    if not memory:
        raise HTTPException(
            status_code=404,
            detail=f"Memory not found: {memory_id}"
        )
    
    action = "Pinned" if pinned else "Unpinned"
    logger.info(f"{action} memory {memory_id} for {character_id}/{user_id}")
    return memory
