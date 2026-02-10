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
  description: string;
  greeting?: string;
  chatCount?: number;
  category?: string;
  tags?: string[];
}

export interface Category {
  id: string;
  name: string;
  icon: string;
  characterCount?: number;
}
