"""
Memory Service - Long-term Memory Management System

Handles persistent memories per character-user pair.
Supports pinned, emotional, and factual memories with semantic search.
"""

import os
import json
import uuid
from datetime import datetime
from typing import List, Dict, Optional, Any
from pathlib import Path

from models.schemas import MemoryEntry, MemoryCreateRequest, MemoryUpdateRequest, MemoryType


class MemoryService:
    """Manages long-term memories for characters"""
    
    def __init__(self, data_dir: str = "data/memories"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_memory_file_path(self, character_id: str, user_id: str = "default") -> Path:
        """Get file path for character-user memory storage"""
        # Use default user if not specified
        safe_user = user_id or "default"
        filename = f"{character_id}_{safe_user}.json"
        return self.data_dir / filename
    
    def _load_memories(self, character_id: str, user_id: str = "default") -> List[Dict[str, Any]]:
        """Load all memories for a character-user pair"""
        file_path = self._get_memory_file_path(character_id, user_id)
        
        if not file_path.exists():
            return []
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("memories", [])
        except Exception as e:
            print(f"Error loading memories from {file_path}: {e}")
            return []
    
    def _save_memories(self, character_id: str, user_id: str, memories: List[Dict[str, Any]]) -> None:
        """Save memories to file"""
        file_path = self._get_memory_file_path(character_id, user_id)
        
        data = {
            "characterId": character_id,
            "userId": user_id,
            "lastUpdated": datetime.utcnow().isoformat(),
            "memories": memories
        }
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving memories to {file_path}: {e}")
            raise
    
    def create_memory(
        self,
        character_id: str,
        user_id: str,
        request: MemoryCreateRequest
    ) -> MemoryEntry:
        """Create a new memory entry"""
        memories = self._load_memories(character_id, user_id)
        
        memory_id = str(uuid.uuid4())[:8]
        now = datetime.utcnow().isoformat()
        
        memory_data = {
            "id": memory_id,
            "characterId": character_id,
            "userId": user_id,
            "content": request.content,
            "memoryType": request.memoryType.value,
            "importance": request.importance,
            "isPinned": request.isPinned,
            "createdAt": now,
            "updatedAt": now,
            "metadata": request.metadata
        }
        
        memories.append(memory_data)
        self._save_memories(character_id, user_id, memories)
        
        return MemoryEntry(**memory_data)
    
    def get_all_memories(
        self,
        character_id: str,
        user_id: str = "default",
        memory_type: Optional[MemoryType] = None,
        pinned_only: bool = False
    ) -> List[MemoryEntry]:
        """Get all memories for a character-user pair with optional filters"""
        memories = self._load_memories(character_id, user_id)
        
        # Apply filters
        if memory_type:
            memories = [m for m in memories if m.get("memoryType") == memory_type.value]
        
        if pinned_only:
            memories = [m for m in memories if m.get("isPinned", False)]
        
        # Sort by importance (desc), then by creation time (desc)
        memories.sort(key=lambda m: (m.get("isPinned", False), m.get("importance", 0), m.get("createdAt", "")), reverse=True)
        
        return [MemoryEntry(**m) for m in memories]
    
    def get_memory(self, character_id: str, user_id: str, memory_id: str) -> Optional[MemoryEntry]:
        """Get a specific memory by ID"""
        memories = self._load_memories(character_id, user_id)
        
        for memory in memories:
            if memory.get("id") == memory_id:
                return MemoryEntry(**memory)
        
        return None
    
    def update_memory(
        self,
        character_id: str,
        user_id: str,
        memory_id: str,
        request: MemoryUpdateRequest
    ) -> Optional[MemoryEntry]:
        """Update an existing memory"""
        memories = self._load_memories(character_id, user_id)
        
        for i, memory in enumerate(memories):
            if memory.get("id") == memory_id:
                # Update fields if provided
                if request.content is not None:
                    memory["content"] = request.content
                if request.importance is not None:
                    memory["importance"] = request.importance
                if request.isPinned is not None:
                    memory["isPinned"] = request.isPinned
                if request.metadata is not None:
                    memory["metadata"] = request.metadata
                
                memory["updatedAt"] = datetime.utcnow().isoformat()
                
                memories[i] = memory
                self._save_memories(character_id, user_id, memories)
                
                return MemoryEntry(**memory)
        
        return None
    
    def delete_memory(self, character_id: str, user_id: str, memory_id: str) -> bool:
        """Delete a memory by ID"""
        memories = self._load_memories(character_id, user_id)
        
        filtered = [m for m in memories if m.get("id") != memory_id]
        
        if len(filtered) < len(memories):
            self._save_memories(character_id, user_id, filtered)
            return True
        
        return False
    
    def pin_memory(self, character_id: str, user_id: str, memory_id: str, pinned: bool = True) -> Optional[MemoryEntry]:
        """Pin or unpin a memory"""
        request = MemoryUpdateRequest(isPinned=pinned)
        return self.update_memory(character_id, user_id, memory_id, request)
    
    def get_relevant_memories(
        self,
        character_id: str,
        user_id: str,
        query: Optional[str] = None,
        limit: int = 10
    ) -> List[MemoryEntry]:
        """
        Get relevant memories for context injection.
        
        Priority:
        1. Pinned memories (always included)
        2. High importance memories
        3. Recent memories
        4. Semantic match (if query provided - future enhancement)
        """
        memories = self._load_memories(character_id, user_id)
        
        # Separate pinned and regular
        pinned = [m for m in memories if m.get("isPinned", False)]
        regular = [m for m in memories if not m.get("isPinned", False)]
        
        # Sort regular by importance * recency
        regular.sort(key=lambda m: m.get("importance", 0), reverse=True)
        
        # Combine: all pinned + top regular (up to limit)
        selected = pinned + regular[:max(0, limit - len(pinned))]
        
        return [MemoryEntry(**m) for m in selected[:limit]]
    
    def get_memory_statistics(self, character_id: str, user_id: str = "default") -> Dict[str, Any]:
        """Get statistics about memories"""
        memories = self._load_memories(character_id, user_id)
        
        return {
            "totalCount": len(memories),
            "pinnedCount": sum(1 for m in memories if m.get("isPinned", False)),
            "byType": {
                "factual": sum(1 for m in memories if m.get("memoryType") == "factual"),
                "emotional": sum(1 for m in memories if m.get("memoryType") == "emotional"),
                "pinned": sum(1 for m in memories if m.get("memoryType") == "pinned"),
                "auto": sum(1 for m in memories if m.get("memoryType") == "auto"),
            },
            "avgImportance": sum(m.get("importance", 0) for m in memories) / len(memories) if memories else 0
        }


# Global instance
memory_service = MemoryService()
