/**
 * Smart Character Generator
 * 
 * Generates personality traits and background lore using LLM based on character identity.
 */

const API_URL = 'http://localhost:8000/api';

interface CharacterIdentity {
  name: string;
  gender: 'Male' | 'Female';
  race: string;
  category: string;
  description: string;
}

interface GenerationResult {
  personality: string;
  background: string;
}

/**
 * Generate smart personality traits based on character identity
 */
export async function generatePersonality(identity: CharacterIdentity): Promise<string> {
  try {
    const prompt = `Based on this character profile:
- Name: ${identity.name}
- Gender: ${identity.gender}
- Race: ${identity.race}
- Category: ${identity.category}
- Description: ${identity.description}

Generate 3-5 personality traits that would fit this character naturally. 
Format: comma-separated traits (e.g., "friendly, creative, curious, empathetic").
Keep it concise and relevant.`;

    const response = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: prompt,
        userId: 'system-generator',
        characterId: 'system',
        conversationId: `gen-${Date.now()}`
      })
    });

    if (!response.ok) {
      throw new Error('Failed to generate personality');
    }

    const data = await response.json();
    const traits = data.response.trim();
    
    return traits;
  } catch (error) {
    console.error('Error generating personality:', error);
    // Fallback to basic traits
    return `${identity.category}, friendly, thoughtful`;
  }
}

/**
 * Generate smart background story based on character identity
 */
export async function generateBackground(identity: CharacterIdentity, personality: string): Promise<string> {
  try {
    const prompt = `Based on this character:
- Name: ${identity.name}
- Gender: ${identity.gender}
- Race: ${identity.race}
- Category: ${identity.category}
- Description: ${identity.description}
- Personality: ${personality}

Write a short background story (2-3 sentences) that explains who this character is and their background.
Make it natural and consistent with the traits. Keep it under 150 words.`;

    const response = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: prompt,
        userId: 'system-generator',
        characterId: 'system',
        conversationId: `gen-${Date.now()}`
      })
    });

    if (!response.ok) {
      throw new Error('Failed to generate background');
    }

    const data = await response.json();
    const background = data.response.trim();
    
    return background;
  } catch (error) {
    console.error('Error generating background:', error);
    // Fallback to basic background
    return `${identity.name} is a ${identity.race.toLowerCase()} ${identity.gender.toLowerCase()} with a ${identity.category} nature. They enjoy meaningful conversations and connecting with others.`;
  }
}

/**
 * Generate both personality and background in one call (more efficient)
 */
export async function generateCharacterDetails(identity: CharacterIdentity): Promise<GenerationResult> {
  try {
    const prompt = `Create a character profile based on:
- Name: ${identity.name}
- Gender: ${identity.gender}
- Race: ${identity.race}
- Category: ${identity.category}
- Description: ${identity.description}

Generate TWO things:
1. PERSONALITY: 3-5 traits (comma-separated)
2. BACKGROUND: 2-3 sentence background story

Format your response exactly as:
PERSONALITY: [traits here]
BACKGROUND: [story here]`;

    const response = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: prompt,
        userId: 'system-generator',
        characterId: 'system',
        conversationId: `gen-${Date.now()}`
      })
    });

    if (!response.ok) {
      throw new Error('Failed to generate character details');
    }

    const data = await response.json();
    const text = data.response.trim();

    // Parse response
    const personalityMatch = text.match(/PERSONALITY:\s*(.+?)(?=\n|BACKGROUND:|$)/i);
    const backgroundMatch = text.match(/BACKGROUND:\s*(.+?)$/is);

    const personality = personalityMatch?.[1]?.trim() || `${identity.category}, friendly, thoughtful`;
    const background = backgroundMatch?.[1]?.trim() || `${identity.name} is a ${identity.race.toLowerCase()} ${identity.gender.toLowerCase()} with a warm personality.`;

    return { personality, background };
  } catch (error) {
    console.error('Error generating character details:', error);
    // Fallback
    return {
      personality: `${identity.category}, friendly, thoughtful, empathetic`,
      background: `${identity.name} is a ${identity.race.toLowerCase()} ${identity.gender.toLowerCase()} with a ${identity.category} nature. They enjoy meaningful conversations and connecting with others.`
    };
  }
}
