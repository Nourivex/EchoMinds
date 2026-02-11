"""
Ollama LLM Service
Handles communication dengan Ollama server
"""
import asyncio
import ollama
from typing import List, Dict, Any, Optional, AsyncIterator
import logging
from config.settings import settings
from models.schemas import ChatRole

logger = logging.getLogger(__name__)


class OllamaService:
    """Service untuk manage Ollama LLM interactions"""
    
    def __init__(self):
        self.client = ollama.AsyncClient(host=settings.ollama_base_url)
        self.current_model = settings.default_model
        
    async def check_health(self) -> Dict[str, Any]:
        """Check Ollama server health"""
        try:
            response = await self.client.list()
            return {
                "status": "healthy",
                "available_models": [m.model for m in response.models],
                "current_model": self.current_model
            }
        except Exception as e:
            logger.error(f"Ollama health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> str:
        """Generate response from Ollama"""
        try:
            # Build messages
            messages = []
            
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            if conversation_history:
                messages.extend(conversation_history)
            
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Generate response
            response = await self.client.chat(
                model=self.current_model,
                messages=messages,
                options={
                    "temperature": temperature or settings.temperature,
                    "num_predict": max_tokens or settings.max_tokens,
                    "num_ctx": settings.context_length,
                    "num_thread": settings.cpu_threads,
                    "num_gpu": settings.gpu_layers
                },
                stream=stream
            )
            
            if stream:
                # Handle streaming response
                full_response = ""
                async for chunk in response:
                    if "message" in chunk and "content" in chunk["message"]:
                        full_response += chunk["message"]["content"]
                return full_response
            else:
                return response["message"]["content"]
                
        except Exception as e:
            logger.error(f"Ollama generate error: {e}")
            raise RuntimeError(f"Failed to generate response: {str(e)}")
    
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text"""
        try:
            response = await self.client.embeddings(
                model=self.current_model,
                prompt=text
            )
            return response["embedding"]
        except Exception as e:
            logger.error(f"Embedding generation error: {e}")
            raise RuntimeError(f"Failed to generate embedding: {str(e)}")
    
    async def pull_model(self, model_name: str) -> Dict[str, Any]:
        """Pull/download a model"""
        try:
            logger.info(f"Pulling model: {model_name}")
            response = await self.client.pull(model_name)
            return {"status": "success", "model": model_name, "details": response}
        except Exception as e:
            logger.error(f"Model pull error: {e}")
            raise RuntimeError(f"Failed to pull model: {str(e)}")
    
    async def switch_model(self, model_name: str) -> Dict[str, Any]:
        """Switch to different model"""
        try:
            # Check if model exists
            response = await self.client.list()
            available = [m.model for m in response.models]
            
            if model_name not in available:
                # Try to pull model
                await self.pull_model(model_name)
            
            self.current_model = model_name
            logger.info(f"Switched to model: {model_name}")
            
            return {
                "status": "success",
                "current_model": self.current_model
            }
        except Exception as e:
            logger.error(f"Model switch error: {e}")
            raise RuntimeError(f"Failed to switch model: {str(e)}")
    
    async def get_model_info(self) -> Dict[str, Any]:
        """Get current model information"""
        try:
            info = await self.client.show(self.current_model)
            return {
                "name": self.current_model,
                "details": info
            }
        except Exception as e:
            logger.error(f"Get model info error: {e}")
            return {
                "name": self.current_model,
                "error": str(e)
            }


# Global service instance
ollama_service = OllamaService()
