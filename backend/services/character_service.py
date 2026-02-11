"""Character service for loading and managing character profiles."""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from functools import lru_cache

from models.schemas import CharacterProfile
from config.settings import settings

logger = logging.getLogger(__name__)


class CharacterService:
    """Service for managing AI character profiles."""
    
    def __init__(self):
        """Initialize character service and load profiles."""
        self.characters_dir = Path(settings.character_data_path)
        self._character_cache: Dict[str, CharacterProfile] = {}
        self._load_all_characters()
    
    def _load_all_characters(self) -> None:
        """Load all character profiles from JSON files."""
        if not self.characters_dir.exists():
            logger.warning(f"Characters directory not found: {self.characters_dir}")
            self.characters_dir.mkdir(parents=True, exist_ok=True)
            return
        
        for json_file in self.characters_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    character = CharacterProfile(**data)
                    self._character_cache[character.id] = character
                    logger.info(f"Loaded character: {character.name} ({character.id})")
            except Exception as e:
                logger.error(f"Failed to load character from {json_file}: {e}")
    
    def get_character(self, character_id: str) -> Optional[CharacterProfile]:
        """Get character by ID.
        
        Args:
            character_id: Character identifier
            
        Returns:
            CharacterProfile if found, None otherwise
        """
        return self._character_cache.get(character_id)
    
    def get_all_characters(self) -> List[CharacterProfile]:
        """Get all loaded characters.
        
        Returns:
            List of all character profiles
        """
        return list(self._character_cache.values())
    
    def reload_characters(self) -> None:
        """Reload all character profiles from disk."""
        logger.info("Reloading character profiles...")
        self._character_cache.clear()
        self._load_all_characters()
    
    def save_character(self, character: CharacterProfile) -> None:
        """Save character profile to disk.
        
        Args:
            character: Character profile to save
            
        Raises:
            IOError: If file write fails
        """
        file_path = self.characters_dir / f"{character.id}.json"
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(
                    character.model_dump(exclude_none=True),
                    f,
                    indent=2,
                    ensure_ascii=False
                )
            
            # Update cache
            self._character_cache[character.id] = character
            logger.info(f"Saved character: {character.name} ({character.id})")
            
        except Exception as e:
            logger.error(f"Failed to save character {character.id}: {e}")
            raise IOError(f"Could not save character: {e}")
    
    def delete_character(self, character_id: str) -> bool:
        """Delete character profile.
        
        Args:
            character_id: Character identifier
            
        Returns:
            True if deleted, False if not found
        """
        if character_id not in self._character_cache:
            return False
        
        file_path = self.characters_dir / f"{character_id}.json"
        
        try:
            if file_path.exists():
                file_path.unlink()
            
            del self._character_cache[character_id]
            logger.info(f"Deleted character: {character_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete character {character_id}: {e}")
            return False
    
    @lru_cache(maxsize=100)
    def build_system_prompt(
        self,
        character_id: str,
        context: Optional[str] = None
    ) -> str:
        """Build system prompt for LLM with character personality.
        
        Args:
            character_id: Character identifier
            context: Optional RAG context to include
            
        Returns:
            Complete system prompt string
            
        Raises:
            ValueError: If character not found
        """
        character = self.get_character(character_id)
        if not character:
            raise ValueError(f"Character not found: {character_id}")
        
        prompt_parts = [
            f"You are {character.name}.",
            f"Personality: {character.personality}",
        ]
        
        if character.systemPrompt:
            prompt_parts.append(f"\n{character.systemPrompt}")
        
        if character.exampleDialogues:
            prompt_parts.append("\nExample dialogues:")
            for example in character.exampleDialogues[:3]:  # Limit to 3 examples
                prompt_parts.append(f"User: {example.get('user', '')}")
                prompt_parts.append(f"Assistant: {example.get('assistant', '')}")
        
        if context:
            prompt_parts.append(f"\nRelevant context from previous conversations:")
            prompt_parts.append(context)
        
        prompt_parts.append(
            f"\nSpeak as {character.name} would speak. "
            f"Stay in character and provide helpful, engaging responses."
        )
        
        return "\n".join(prompt_parts)


# Global character service instance
character_service = CharacterService()
