"""Message parser service untuk structured messages."""

import re
import logging
from typing import Optional, Dict
from models.schemas import StructuredMessageContent

logger = logging.getLogger(__name__)


def parse_structured_message(raw_content: str) -> StructuredMessageContent:
    """Parse raw message into structured components.
    
    Format conventions:
    - Dialogue: Text in "quotes"
    - Action: Text in *asterisks*
    - Thought: Text in (parentheses)
    
    Args:
        raw_content: Raw message string from LLM
        
    Returns:
        StructuredMessageContent with parsed components
        
    Example:
        Input:  *Aiko duduk di lantai* "Kakak! Halo!" (senang sekali)
        Output: action="Aiko duduk di lantai", dialogue="Kakak! Halo!", thought="senang sekali"
    """
    try:
        # Extract actions (between *asterisks*)
        action_matches = re.findall(r'\*([^*]+)\*', raw_content)
        actions = [a.strip() for a in action_matches if a.strip()]
        
        # Extract dialogue (between "quotes")
        dialogue_matches = re.findall(r'"([^"]+)"', raw_content)
        dialogues = [d.strip() for d in dialogue_matches if d.strip()]
        
        # Extract thoughts (between (parentheses))
        thought_matches = re.findall(r'\(([^)]+)\)', raw_content)
        thoughts = [t.strip() for t in thought_matches if t.strip()]
        
        # Extract remaining text (emotion/narration not in special markers)
        # Remove parsed parts to find remaining content
        remaining = raw_content
        for match in re.finditer(r'\*[^*]+\*|"[^"]+"|\\([^)]+\\)', remaining):
            remaining = remaining.replace(match.group(0), '')
        remaining = remaining.strip()
        
        # Build structured content
        structured = StructuredMessageContent(
            dialogue=' '.join(dialogues) if dialogues else None,
            action=' '.join(actions) if actions else None,
            thought=' '.join(thoughts) if thoughts else None,
            emotion=remaining if remaining and len(remaining) > 0 else None,
            raw_content=raw_content
        )
        
        # If nothing was parsed, treat entire message as dialogue
        if not any([structured.dialogue, structured.action, structured.thought]):
            structured.dialogue = raw_content.strip('"')
        
        logger.debug(f"Parsed message: dialogue={bool(structured.dialogue)}, "
                    f"action={bool(structured.action)}, thought={bool(structured.thought)}")
        
        return structured
        
    except Exception as e:
        logger.error(f"Failed to parse message: {e}")
        # Fallback: treat entire message as dialogue
        return StructuredMessageContent(
            dialogue=raw_content,
            raw_content=raw_content
        )


def format_structured_prompt_instructions() -> str:
    """Generate formatting instructions for system prompt.
    
    Returns:
        Formatted instructions string to append to system prompt
    """
    return """
[Response Formatting Guidelines]
Format your responses using these conventions to create immersive narrative:

1. **Dialogue** (what you say):
   - Use double quotes: "Kakak! Halo juga!"
   - Keep natural and conversational

2. **Action** (what you do):
   - Use asterisks: *duduk di lantai sambil memainkan boneka*
   - Describe physical actions, gestures, movements
   - Keep vivid but concise

3. **Thought** (inner feelings):
   - Use parentheses: (senang sekali kakak datang)
   - Express internal emotions, not spoken aloud
   - Optional, use sparingly for depth

Example responses:
*Aiko sedang bermain boneka di kamarnya. Mendengar suara pintu, dia menoleh.*

"Kakak! Halo juga! Kakak lagi apa nih?"

*Ia tersenyum lebar, menunjukkan bonekanya.*

(semoga kakak tidak pergi lagi seperti kemarin...)

IMPORTANT: Mix these elements naturally. Not every response needs all three types.
Keep authentic to the character and situation.
"""


def enhance_system_prompt_with_formatting(base_prompt: str) -> str:
    """Add formatting instructions to existing system prompt.
    
    Args:
        base_prompt: Original character system prompt
        
    Returns:
        Enhanced prompt with formatting guidelines
    """
    formatting_instructions = format_structured_prompt_instructions()
    return f"{base_prompt}\n\n{formatting_instructions}"
