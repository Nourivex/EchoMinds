export interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
  isTyping?: boolean;
}

export interface Character {
  id: string;
  name: string;
  avatar?: string;
  description?: string;
}
