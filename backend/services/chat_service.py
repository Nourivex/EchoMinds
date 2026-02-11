"""Chat service orchestrating LLM, RAG, character management, and long-term memory."""

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
from services.memory_service import memory_service
from services.message_parser import (
    parse_structured_message,
    enhance_system_prompt_with_formatting
)
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
            # 3. Retrieve long-term memories
            memories = memory_service.get_relevant_memories(
                character_id=character_id,
                user_id=user_id,
                query=message,
                limit=8  # Top 8 relevant memories
            )
            
            logger.debug(f"Retrieved {len(memories)} long-term memories")
            
            # 4. Retrieve RAG context
            context_messages = await rag_service.retrieve_context(
                character_id=character_id,
                user_id=user_id,
                query=message,
                top_k=5
            )
            
            logger.debug(f"Retrieved {len(context_messages)} context messages")
            
            # 5. Get recent conversation history
            history = await rag_service.get_recent_messages(
                character_id=character_id,
                user_id=user_id,
                limit=6  # Last 3 exchanges (6 messages)
            )
            
            logger.debug(f"Retrieved {len(history)} recent messages")
            
            # 6. Build prompt with memories
            system_prompt = self._build_system_prompt(
                character_id=character_id,
                context_messages=context_messages,
                memories=memories
            )
            
            # 7. Generate LLM response
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
            
            # Parse structured message
            structured_content = parse_structured_message(ai_response)
            logger.debug(f"Parsed structured content: {structured_content.model_dump()}")
            
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
            
            # 9. Return response
            return ChatResponse(
                reply=ai_response,
                characterName=character.name,
                conversationId=conversation_id or str(uuid4()),
                context=[
                    ContextMessage(
                        content=msg.get("content", "") if isinstance(msg, dict) else msg.content,
                        role=msg.get("role", "user") if isinstance(msg, dict) else msg.role,
                        timestamp=msg.get("timestamp", "") if isinstance(msg, dict) else msg.timestamp,
                        relevance=msg.get("metadata", {}).get("relevance", 0.0) if isinstance(msg, dict) else msg.metadata.get("relevance", 0.0)
                    )
                    for msg in context_messages
                ],
                metadata={
                    "responseTime": round(response_time, 3),
                    "tokenCount": len(ai_response.split()),  # Approximate
                    "model": settings.default_model,
                    "contextUsed": len(context_messages)
                },
                structured=structured_content  # Add structured content
            )
            
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            raise Exception(f"Failed to generate response: {str(e)}")
    
    def _build_system_prompt(
        self,
        character_id: str,
        context_messages: List[ConversationMessage],
        memories: List = None
    ) -> str:
        """Build system prompt with character personality, context, and long-term memories.
        
        Args:
            character_id: Character identifier
            context_messages: RAG retrieved context
            memories: Long-term memory entries
            
        Returns:
            Complete system prompt string
        """
        # Get base system prompt with character personality
        context_text = None
        
        # 1. Inject long-term memories first (most important)
        memory_context = None
        if memories:
            memory_parts = ["=== LONG-TERM MEMORIES ==="]
            memory_parts.append("Things you remember about this user and your relationship:\n")
            
            for mem in memories:
                # Pinned memories get priority marker
                pin_marker = "📌 " if mem.isPinned else ""
                type_label = mem.memoryType.upper()
                
                memory_parts.append(f"{pin_marker}[{type_label}] {mem.content}")
            
            memory_context = "\n".join(memory_parts)
        
        # 2. Add conversation context (RAG)
        if context_messages:
            context_parts = ["=== RECENT CONTEXT ==="]
            for msg in context_messages[:3]:  # Top 3 most relevant
                msg_role = msg.get("role", "user") if isinstance(msg, dict) else msg.role
                msg_content = msg.get("content", "") if isinstance(msg, dict) else msg.content
                msg_metadata = msg.get("metadata", {}) if isinstance(msg, dict) else msg.metadata
                
                role_label = "User" if msg_role == "user" else "You"
                relevance = msg_metadata.get("relevance", 0)
                context_parts.append(
                    f"{role_label}: {msg_content[:200]} "
                    f"(relevance: {relevance:.2f})"
                )
            context_text = "\n".join(context_parts)
        
        # 3. Build complete prompt
        base_prompt = character_service.build_system_prompt(
            character_id=character_id,
            context=context_text
        )
        
        # Enhance with formatting instructions for structured messages
        base_prompt = enhance_system_prompt_with_formatting(base_prompt)
        
        # Inject memories at the top (after character identity)
        if memory_context:
            # Split base prompt to inject memories after character identity
            prompt_parts = base_prompt.split("\n\n", 1)
            if len(prompt_parts) == 2:
                return f"{prompt_parts[0]}\n\n{memory_context}\n\n{prompt_parts[1]}"
            else:
                return f"{base_prompt}\n\n{memory_context}"
        
        return base_prompt
    
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
