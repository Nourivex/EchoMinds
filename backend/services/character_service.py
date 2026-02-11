"""Character service for loading and managing character profiles."""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from functools import lru_cache
from uuid import uuid4

from models.schemas import CharacterProfile, CharacterCreateRequest
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
    
    def create_character(self, request: CharacterCreateRequest) -> CharacterProfile:
        """Create new character from request data.
        
        This method constructs a character with advanced settings:
        - Separated personality traits and background lore
        - Language-specific system prompts
        - Relationship dynamics (friend, partner, mentor, custom)
        - Emotional tone configuration
        
        Args:
            request: Character creation request data
            
        Returns:
            Created CharacterProfile
            
        Raises:
            ValueError: If character with same name already exists
        """
        # Check if character with this name already exists
        existing = [c for c in self._character_cache.values() if c.name.lower() == request.name.lower()]
        if existing:
            raise ValueError(f"Character with name '{request.name}' already exists")
        
        # Generate unique ID
        character_id = str(uuid4())[:8]
        
        # Build default greeting if not provided
        greeting_templates = {
            "friend": f"Hey! I'm {request.name}. What's up?",
            "partner": f"Hi there... I'm {request.name}. Nice to finally meet you.",
            "mentor": f"Greetings, I am {request.name}. How may I guide you today?",
            "rival": f"So you're the one I've heard about. I'm {request.name}. Let's see what you've got."
        }
        default_greeting = greeting_templates.get(request.relationshipType, f"Hello! I'm {request.name}.")
        
        # Build language-aware system prompt
        system_prompt = self._build_advanced_system_prompt(request)
        
        # Construct character profile
        character = CharacterProfile(
            id=character_id,
            name=request.name,
            avatar=request.avatar,
            description=request.description,
            personality=request.personality,
            greeting=request.greeting or default_greeting,
            systemPrompt=request.systemPromptOverride or system_prompt,
            exampleDialogues=[]  # Can be populated later
        )
        
        # Save to disk and cache
        self.save_character(character)
        
        logger.info(f"Created character: {character.name} (ID: {character_id}) with relationship: {request.relationshipType}")
        return character
    
    def _build_advanced_system_prompt(self, request: CharacterCreateRequest) -> str:
        """Build advanced system prompt based on character settings.
        
        Incorporates:
        - Language constraints (force ID or EN)
        - Relationship dynamics
        - Emotional tone
        - Conversation style
        - Background lore
        """
        prompt_parts = []
        
        # Core identity
        prompt_parts.append(f"You are {request.name}.")
        prompt_parts.append(f"{request.description}")
        
        # Personality traits
        prompt_parts.append(f"\nPersonality: {request.personality}")
        
        # Background/Lore (if provided)
        if request.background:
            prompt_parts.append(f"\nBackground: {request.background}")
        
        # Language enforcement
        language_instruction = {
            "id": "You MUST respond exclusively in Bahasa Indonesia. Always use Indonesian language for all responses.",
            "en": "You MUST respond exclusively in English. Always use English language for all responses."
        }
        prompt_parts.append(f"\n{language_instruction.get(request.language, language_instruction['id'])}")
        
        # Relationship dynamics
        relationship_instructions = {
            "friend": "Your relationship with the user is that of close friends. Be supportive, loyal, and share mutual trust.",
            "partner": "Your relationship with the user is romantic. Show care, affection, and emotional intimacy while respecting boundaries.",
            "mentor": "Your relationship is that of a mentor guiding a student. Share wisdom, encourage growth, and provide patient guidance.",
            "rival": "You are rivals with the user. Show competitiveness, challenge them, but maintain mutual respect."
        }
        relationship_text = relationship_instructions.get(request.relationshipType, f"Your relationship with the user is: {request.relationshipType}")
        prompt_parts.append(f"\n{relationship_text}")
        
        # Emotional tone
        tone_instructions = {
            "warm": "Your tone is warm and comforting. Express care and empathy.",
            "neutral": "Maintain a balanced, neutral tone. Be informative and clear.",
            "playful": "Your tone is playful and energetic. Use humor and keep things fun.",
            "mysterious": "Your tone is mysterious and intriguing. Speak with subtle depth."
        }
        prompt_parts.append(tone_instructions.get(request.emotionalTone, ""))
        
        # Conversation style
        style_instructions = {
            "friendly": "Keep your responses warm and conversational.",
            "professional": "Maintain professionalism and clarity in communication.",
            "playful": "Be fun, use playful language, and keep energy high.",
            "mysterious": "Speak with intrigue, leave subtle hints, be thought-provoking.",
            "wise": "Share wisdom calmly, encourage reflection, be patient."
        }
        prompt_parts.append(style_instructions.get(request.conversationStyle, ""))
        
        # Final instruction
        prompt_parts.append(f"\nStay in character as {request.name}. Be consistent with your personality, relationship, and tone.")
        
        return "\n".join(filter(None, prompt_parts))
    
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
