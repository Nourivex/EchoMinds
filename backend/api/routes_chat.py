"""Chat endpoints."""

import logging
from fastapi import APIRouter, HTTPException

from models.schemas import ChatMessage, ChatResponse
from services.chat_service import chat_service

logger = logging.getLogger(__name__)

router = APIRouter(tags=["chat"])


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


@router.delete("/conversations/{character_id}/{user_id}")
async def clear_conversation(character_id: str, user_id: str):
    """Clear conversation history for character-user pair.
    
    Args:
        character_id: Character identifier
        user_id: User identifier
        
    Returns:
        Success message
    """
    try:
        from rag.vector_service import rag_service
        await rag_service.clear_conversation(character_id, user_id)
        return {"message": "Conversation cleared successfully"}
        
    except Exception as e:
        logger.error(f"Failed to clear conversation: {e}")
        raise HTTPException(
            status_code=500,
            detail="Could not clear conversation"
        )
