/**
 * Structured message types for immersive chat
 */

export interface StructuredMessageContent {
  dialogue?: string;          // Spoken text in quotes
  action?: string;            // Physical actions in *asterisks*
  thought?: string;           // Internal thoughts in (parentheses)
  emotion?: string;           // Emotional state
  translation?: {
    dialogue?: string;
    action?: string;
    thought?: string;
  };
  raw_content?: string;       // Original message (fallback)
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;             // Legacy flat text
  timestamp: Date;
  structured?: StructuredMessageContent;  // New structured content
}

export interface ChatResponse {
  reply: string;               // Legacy
  characterName: string;
  conversationId: string;
  context: Array<{
    content: string;
    role: string;
    timestamp: string;
    relevance: number;
  }>;
  metadata: {
    responseTime: number;
    tokenCount: number;
    model: string;
    contextUsed: number;
  };
  structured?: StructuredMessageContent;  // New structured content
}
