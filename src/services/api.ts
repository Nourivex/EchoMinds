/**
 * TypeScript API service for backend communication
 */

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * API Client for EchoMinds backend
 */
export class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public data?: any
  ) {
    super(message);
    this.name = 'APIError';
  }
}

/**
 * Generic fetch wrapper with error handling
 */
async function fetchAPI<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${BASE_URL}${endpoint}`;
  
  const defaultHeaders: HeadersInit = {
    'Content-Type': 'application/json',
  };

  const config: RequestInit = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  };

  try {
    const response = await fetch(url, config);

    // Handle non-JSON responses
    const contentType = response.headers.get('content-type');
    const isJSON = contentType?.includes('application/json');

    if (!response.ok) {
      const errorData = isJSON ? await response.json() : await response.text();
      throw new APIError(
        errorData.detail || errorData || 'API request failed',
        response.status,
        errorData
      );
    }

    if (isJSON) {
      return await response.json();
    } else {
      return (await response.text()) as unknown as T;
    }
  } catch (error) {
    if (error instanceof APIError) {
      throw error;
    }
    
    // Network or other errors
    throw new APIError(
      `Network error: ${(error as Error).message}`,
      0,
      error
    );
  }
}

// ==================== Types ====================

export interface ChatMessage {
  message: string;
  userId: string;
  characterId: string;
  conversationId?: string;
}

export interface ContextMessage {
  content: string;
  role: 'user' | 'assistant';
  timestamp: string;
  relevance: number;
}

export interface ChatResponse {
  reply: string;
  characterName: string;
  conversationId: string;
  context: ContextMessage[];
  metadata: {
    responseTime: number;
    tokenCount: number;
    model: string;
  };
}

export interface ModelConfig {
  model_name: string;
  cpu_threads: number;
  gpu_layers: number;
  temperature: number;
  context_length: number;
  max_tokens: number;
}

export interface SystemStatus {
  status: string;
  llm_provider: string;
  model_loaded: string;
  gpu_available: boolean;
  cpu_usage: number;
  memory_usage: number;
  uptime_seconds: number;
}

export interface Character {
  id: string;
  name: string;
  avatar: string;
  description: string;
  personality: string;
  greeting: string;
  systemPrompt?: string;
  exampleDialogues?: Array<{
    user: string;
    assistant: string;
  }>;
  emotionalHooks?: string[];
  chatCount: number;
}

// ==================== API Functions ====================

/**
 * Health Check
 */
export async function checkHealth() {
  return fetchAPI('/api/health');
}

/**
 * Get system status with resource usage
 */
export async function getSystemStatus(): Promise<SystemStatus> {
  return fetchAPI<SystemStatus>('/api/status');
}

/**
 * Send chat message and get AI response
 */
export async function sendMessage(
  message: string,
  userId: string,
  characterId: string,
  conversationId?: string
): Promise<ChatResponse> {
  return fetchAPI<ChatResponse>('/api/chat', {
    method: 'POST',
    body: JSON.stringify({
      message,
      userId,
      characterId,
      conversationId,
    }),
  });
}

/**
 * Get current model configuration
 */
export async function getModelConfig(): Promise<ModelConfig> {
  return fetchAPI<ModelConfig>('/api/config');
}

/**
 * Update model configuration
 */
export async function updateModelConfig(
  config: Partial<ModelConfig>
): Promise<ModelConfig> {
  return fetchAPI<ModelConfig>('/api/config', {
    method: 'PUT',
    body: JSON.stringify(config),
  });
}

/**
 * List available LLM models
 */
export async function listModels(): Promise<{ models: any[] }> {
  return fetchAPI('/api/models');
}

/**
 * List all characters
 */
export async function listCharacters(): Promise<Character[]> {
  return fetchAPI<Character[]>('/api/characters');
}

/**
 * Create new character with advanced settings
 */
export async function createCharacter(characterData: {
  name: string;
  avatar: string;
  description: string;
  personality: string;
  background?: string;
  language: string;
  conversationStyle: string;
  relationshipType: string;
  emotionalTone: string;
  category: string;
  greeting?: string;
  systemPromptOverride?: string;
}): Promise<Character> {
  return fetchAPI<Character>('/api/characters', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(characterData),
  });
}

/**
 * Get specific character by ID
 */
export async function getCharacter(characterId: string): Promise<Character> {
  return fetchAPI<Character>(`/api/characters/${characterId}`);
}

/**
 * Clear conversation history
 */
export async function clearConversation(
  characterId: string,
  userId: string
): Promise<{ message: string; deletedCount: number }> {
  return fetchAPI(`/api/conversations/${characterId}/${userId}`, {
    method: 'DELETE',
  });
}

/**
 * Generate text embedding (for testing)
 */
export async function generateEmbedding(
  text: string
): Promise<{ embedding: number[]; dimension: number; model: string }> {
  return fetchAPI(`/api/embed?text=${encodeURIComponent(text)}`);
}

// ==================== Export default API object ====================

export default {
  checkHealth,
  getSystemStatus,
  sendMessage,
  getModelConfig,
  updateModelConfig,
  listModels,
  listCharacters,
  createCharacter,
  getCharacter,
  clearConversation,
  generateEmbedding,
};
