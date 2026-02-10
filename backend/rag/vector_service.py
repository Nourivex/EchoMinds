"""
RAG Service dengan ChromaDB untuk per-character memory
"""
import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional
import logging
from sentence_transformers import SentenceTransformer
from ..config.settings import settings
import uuid

logger = logging.getLogger(__name__)


class RAGService:
    """Service untuk Retrieval-Augmented Generation"""
    
    def __init__(self):
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=str(settings.vector_db_path),
            settings=ChromaSettings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Initialize embedding model
        logger.info(f"Loading embedding model: {settings.embedding_model}")
        self.embedding_model = SentenceTransformer(settings.embedding_model)
        
        logger.info("RAG Service initialized")
    
    def _get_collection_name(self, character_id: str, user_id: str) -> str:
        """Generate collection name per character-user pair"""
        return f"{settings.collection_prefix}{character_id}_{user_id}"
    
    def _get_or_create_collection(self, collection_name: str):
        """Get or create ChromaDB collection"""
        try:
            collection = self.client.get_collection(name=collection_name)
        except Exception:
            collection = self.client.create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
        return collection
    
    def _generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text"""
        embedding = self.embedding_model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    
    async def store_conversation(
        self,
        character_id: str,
        user_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Store conversation message in vector DB"""
        try:
            collection_name = self._get_collection_name(character_id, user_id)
            collection = self._get_or_create_collection(collection_name)
            
            # Generate unique ID
            doc_id = str(uuid.uuid4())
            
            # Generate embedding
            embedding = self._generate_embedding(content)
            
            # Prepare metadata
            doc_metadata = {
                "character_id": character_id,
                "user_id": user_id,
                "role": role,
                **(metadata or {})
            }
            
            # Store in ChromaDB
            collection.add(
                ids=[doc_id],
                embeddings=[embedding],
                documents=[content],
                metadatas=[doc_metadata]
            )
            
            logger.debug(f"Stored conversation: {doc_id}")
            return doc_id
            
        except Exception as e:
            logger.error(f"Failed to store conversation: {e}")
            raise RuntimeError(f"Store conversation error: {str(e)}")
    
    async def retrieve_context(
        self,
        character_id: str,
        user_id: str,
        query: str,
        top_k: int = 5,
        min_relevance: float = 0.3
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant context from conversation history"""
        try:
            collection_name = self._get_collection_name(character_id, user_id)
            collection = self._get_or_create_collection(collection_name)
            
            # Get collection count
            count = collection.count()
            if count == 0:
                return []
            
            # Generate query embedding
            query_embedding = self._generate_embedding(query)
            
            # Search similar documents
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=min(top_k, count)
            )
            
            # Process results
            contexts = []
            if results["documents"] and results["documents"][0]:
                for i, doc in enumerate(results["documents"][0]):
                    distance = results["distances"][0][i] if results["distances"] else 1.0
                    relevance = 1 - distance  # Convert distance to similarity
                    
                    if relevance >= min_relevance:
                        contexts.append({
                            "content": doc,
                            "relevance": relevance,
                            "metadata": results["metadatas"][0][i] if results["metadatas"] else {}
                        })
            
            logger.debug(f"Retrieved {len(contexts)} context documents")
            return contexts
            
        except Exception as e:
            logger.error(f"Failed to retrieve context: {e}")
            return []
    
    async def get_recent_messages(
        self,
        character_id: str,
        user_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get recent messages from conversation"""
        try:
            collection_name = self._get_collection_name(character_id, user_id)
            collection = self._get_or_create_collection(collection_name)
            
            count = collection.count()
            if count == 0:
                return []
            
            # Get all documents (ChromaDB doesn't support sorting by timestamp directly)
            results = collection.get(
                limit=min(limit * 2, count),  # Get more to filter
                include=["documents", "metadatas"]
            )
            
            # Convert to list and sort by timestamp (if available)
            messages = []
            if results["documents"]:
                for i, doc in enumerate(results["documents"]):
                    metadata = results["metadatas"][i] if results["metadatas"] else {}
                    messages.append({
                        "content": doc,
                        "role": metadata.get("role", "unknown"),
                        "metadata": metadata
                    })
            
            # Return most recent
            return messages[-limit:] if len(messages) > limit else messages
            
        except Exception as e:
            logger.error(f"Failed to get recent messages: {e}")
            return []
    
    async def clear_conversation(self, character_id: str, user_id: str) -> bool:
        """Clear conversation history for character-user pair"""
        try:
            collection_name = self._get_collection_name(character_id, user_id)
            self.client.delete_collection(name=collection_name)
            logger.info(f"Cleared conversation: {collection_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to clear conversation: {e}")
            return False


# Global service instance
rag_service = RAGService()
