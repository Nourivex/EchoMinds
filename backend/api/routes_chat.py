"""Chat endpoints."""

import logging
from fastapi import APIRouter, HTTPException

from models.schemas import ChatMessage, ChatResponse
from services.chat_service import chat_service
from llm.ollama_service import ollama_service
from config.settings import settings
from uuid import uuid4
import time

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


@router.post("/enhance", response_model=ChatResponse)
async def enhance(message: ChatMessage):
    """Lightweight enhancer endpoint that reuses the chat pipeline but
    intended for short single-line description enhancements.

    This provides a dedicated route for the UI enhancer button and keeps
    semantics separate from general chat usage.
    """
    # If a valid characterId is provided and exists, reuse full chat pipeline
    try:
        if message.characterId:
            # Try to use existing character via chat_service
            try:
                return await chat_service.process_message(
                    character_id=message.characterId,
                    user_id=message.userId,
                    message=message.message,
                    conversation_id=message.conversationId,
                )
            except ValueError:
                # Fallthrough to generic enhancer when character not found
                logger.debug("Character not found for enhancer, using generic enhancer")

        # Generic enhancer: minimal system prompt for short description enhancement
        start = time.time()
        system_prompt = (
            "You are a professional creative writer. Given the user input, produce a single-line,"
            " compelling character description in Bahasa Indonesia (max 15 words). Return only the sentence."
        )

        ai_response = await ollama_service.generate(
            prompt=message.message,
            system_prompt=system_prompt,
            conversation_history=[],
            temperature=settings.temperature,
            max_tokens=80,
        )

        response_time = time.time() - start
        conv_id = message.conversationId or str(uuid4())

        return ChatResponse(
            reply=ai_response,
            characterName="Enhancer",
            conversationId=conv_id,
            context=[],
            metadata={
                "responseTime": round(response_time, 3),
                "model": settings.default_model,
            },
        )

    except Exception as e:
        logger.error(f"Enhance processing failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to enhance text: {str(e)}"
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
