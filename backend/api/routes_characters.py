"""Character CRUD endpoints."""

import logging
from typing import List
from fastapi import APIRouter, HTTPException

from models.schemas import CharacterProfile, CharacterCreateRequest
from services.character_service import character_service

logger = logging.getLogger(__name__)

router = APIRouter(tags=["characters"])


@router.get("/characters", response_model=List[CharacterProfile])
async def list_characters():
    """Get list of all available characters.
    
    Returns:
        List of CharacterProfile objects
    """
    return character_service.get_all_characters()


@router.post("/characters", response_model=CharacterProfile, status_code=201)
async def create_character(request: CharacterCreateRequest):
    """Create a new character with advanced relationship settings.
    
    Args:
        request: Character creation request with all fields
        
    Returns:
        Created CharacterProfile
        
    Raises:
        HTTPException: If validation fails or name exists
    """
    try:
        character = character_service.create_character(request)
        logger.info(f"Created character: {character.name} ({character.id})")
        return character
        
    except ValueError as e:
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
