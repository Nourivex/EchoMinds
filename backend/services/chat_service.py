"""Chat service orchestrating LLM, RAG, and character management."""

import logging
import time
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from models.schemas import (
    ChatMessage,
    ChatResponse,
    ConversationMessage,
    ContextMessage
)
from services.character_service import character_service
from llm.ollama_service import ollama_service
from rag.vector_service import rag_service
from config.settings import settings

logger = logging.getLogger(__name__)


class ChatService:
    """Service for processing chat messages with RAG and LLM."""
    
    async def process_message(
        self,
        character_id: str,
        user_id: str,
        message: str,
        conversation_id: Optional[str] = None
    ) -> ChatResponse:
        """Process user message and generate AI response.
        
        Steps:
        1. Validate input
        2. Load character profile
        3. Retrieve RAG context
        4. Get recent conversation history
        5. Build prompt
        6. Generate LLM response
        7. Store conversation
        8. Return response
        
        Args:
            character_id: Character identifier
            user_id: User identifier
            message: User message text
            conversation_id: Optional conversation tracking ID
            
        Returns:
            ChatResponse with AI reply and context
            
        Raises:
            ValueError: If input validation fails
            Exception: If LLM generation fails
        """
        start_time = time.time()
        
        # 1. Validate input
        if not message or not message.strip():
            raise ValueError("Message cannot be empty")
        
        if len(message) > 2000:
            raise ValueError("Message too long (max 2000 characters)")
        
        # 2. Load character profile
        character = character_service.get_character(character_id)
        if not character:
            raise ValueError(f"Character not found: {character_id}")
        
        logger.info(
            f"Processing message for {character.name} "
            f"from user {user_id}: {message[:50]}..."
        )
        
        try:
            # 3. Retrieve RAG context
            context_messages = await rag_service.retrieve_context(
                character_id=character_id,
                user_id=user_id,
                query=message,
                top_k=5
            )
            
            logger.debug(f"Retrieved {len(context_messages)} context messages")
            
            # 4. Get recent conversation history
            history = await rag_service.get_recent_messages(
                character_id=character_id,
                user_id=user_id,
                limit=6  # Last 3 exchanges (6 messages)
            )
            
            logger.debug(f"Retrieved {len(history)} recent messages")
            
            # 5. Build prompt
            system_prompt = self._build_system_prompt(
                character_id=character_id,
                context_messages=context_messages
            )
            
            # 6. Generate LLM response
            ai_response = await ollama_service.generate(
                prompt=message,
                system_prompt=system_prompt,
                conversation_history=[
                    {"role": msg["role"], "content": msg["content"]} 
                    for msg in history
                ],
                temperature=settings.temperature,
                max_tokens=settings.max_tokens
            )
            
            response_time = time.time() - start_time
            logger.info(f"Generated response in {response_time:.2f}s")
            
            # Generate conversation ID if not provided
            conv_id = conversation_id or str(uuid4())
            
            # 7. Store conversation in vector DB (user message + assistant response)
            await rag_service.store_conversation(
                character_id=character_id,
                user_id=user_id,
                role="user",
                content=message,
                metadata={"conversation_id": conv_id, "timestamp": datetime.now().isoformat()}
            )
            
            await rag_service.store_conversation(
                character_id=character_id,
                user_id=user_id,
                role="assistant",
                content=ai_response,
                metadata={"conversation_id": conv_id, "timestamp": datetime.now().isoformat()}
            )
            
            # 8. Return response
            return ChatResponse(
                reply=ai_response,
                characterName=character.name,
                conversationId=conversation_id or str(uuid4()),
                context=[
                    ContextMessage(
                        content=msg.content,
                        role=msg.role,
                        timestamp=msg.timestamp,
                        relevance=msg.metadata.get("relevance", 0.0)
                    )
                    for msg in context_messages
                ],
                metadata={
                    "responseTime": round(response_time, 3),
                    "tokenCount": len(ai_response.split()),  # Approximate
                    "model": settings.default_model,
                    "contextUsed": len(context_messages)
                }
            )
            
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            raise Exception(f"Failed to generate response: {str(e)}")
    
    def _build_system_prompt(
        self,
        character_id: str,
        context_messages: List[ConversationMessage]
    ) -> str:
        """Build system prompt with character personality and context.
        
        Args:
            character_id: Character identifier
            context_messages: RAG retrieved context
            
        Returns:
            Complete system prompt string
        """
        # Get base system prompt with character personality
        context_text = None
        
        if context_messages:
            context_parts = []
            for msg in context_messages[:3]:  # Top 3 most relevant
                role_label = "User" if msg.role == "user" else "You"
                relevance = msg.metadata.get("relevance", 0)
                context_parts.append(
                    f"{role_label}: {msg.content[:200]} "
                    f"(relevance: {relevance:.2f})"
                )
            context_text = "\n".join(context_parts)
        
        return character_service.build_system_prompt(
            character_id=character_id,
            context=context_text
        )
    
    def _build_message_history(
        self,
        system_prompt: str,
        history: List[ConversationMessage],
        current_message: str
    ) -> List[dict]:
        """Build message list for LLM API.
        
        Args:
            system_prompt: System prompt with character personality
            history: Recent conversation history
            current_message: Current user message
            
        Returns:
            List of message dicts for LLM API
        """
        messages = [
            {"role": "system", "content": system_prompt}
        ]
       
        # Add conversation history (handle both dict and object types)
        for msg in history:
            if isinstance(msg, dict):
                messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
            else:
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": current_message
        })
        
        return messages
    
    async def clear_conversation(
        self,
        character_id: str,
        user_id: str
    ) -> int:
        """Clear conversation history for specific character-user pair.
        
        Args:
            character_id: Character identifier
            user_id: User identifier
            
        Returns:
            Number of messages deleted
        """
        try:
            await rag_service.clear_conversation(
                character_id=character_id,
                user_id=user_id
            )
            logger.info(f"Cleared conversation: {character_id}/{user_id}")
            return 1  # ChromaDB doesn't return count
        except Exception as e:
            logger.error(f"Failed to clear conversation: {e}")
            raise


# Global chat service instance
chat_service = ChatService()
