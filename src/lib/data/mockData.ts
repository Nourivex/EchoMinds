import type { Character, Category } from '@models/chat';

export const mockCharacters: Character[] = [
  {
    id: '1',
    name: 'Luna',
    avatar: '🌙',
    description: 'Seorang astrologer misterius yang bisa membaca bintang dan memberikan advice tentang kehidupan',
    greeting: 'Halo! Aku Luna. Mau aku bacakan bintang-mu hari ini?',
    chatCount: 15243,
    category: 'Assistant',
    tags: ['astrology', 'wisdom', 'friendly']
  },
  {
    id: '2',
    name: 'Kai',
    avatar: '⚔️',
    description: 'Swordmaster dari dunia fantasy yang siap melatihmu menjadi warrior terkuat',
    greeting: 'Selamat datang, murid baru. Siap untuk berlatih?',
    chatCount: 23102,
    category: 'Anime',
    tags: ['fantasy', 'mentor', 'action']
  },
  {
    id: '3',
    name: 'Dr. Nova',
    avatar: '🔬',
    description: 'Ilmuwan jenius yang membantu menjelaskan konsep sains dengan cara yang fun dan mudah dipahami',
    greeting: 'Hai! Ada eksperimen menarik yang ingin kita coba hari ini?',
    chatCount: 8934,
    category: 'Assistant',
    tags: ['science', 'teacher', 'smart']
  },
  {
    id: '4',
    name: 'Yuki',
    avatar: '❄️',
    description: 'Gadis pemalu dari Jepang yang suka membaca manga dan mendengarkan musik',
    greeting: 'A-ah... halo. Senang bertemu denganmu...',
    chatCount: 31205,
    category: 'Anime',
    tags: ['shy', 'cute', 'slice of life']
  },
  {
    id: '5',
    name: 'Shadow',
    avatar: '🎭',
    description: 'Detective misterius yang ahli memecahkan kasus-kasus sulit',
    greeting: 'Hmm... ada kasus menarik untukku?',
    chatCount: 12789,
    category: 'Roleplay',
    tags: ['mystery', 'detective', 'thriller']
  },
  {
    id: '6',
    name: 'Aria',
    avatar: '🎵',
    description: 'Idol terkenal yang ramah dan suka berinteraksi dengan fans',
    greeting: 'Kyaa~! Akhirnya kita bisa ngobrol! ♪',
    chatCount: 45672,
    category: 'Anime',
    tags: ['idol', 'cheerful', 'music']
  },
  {
    id: '7',
    name: 'Rex',
    avatar: '🦖',
    description: 'Dinosaurus yang bisa berbicara dan penuh dengan fun facts tentang sejarah',
    greeting: 'ROAR! Oh maaf... maksudku, halo! Mau belajar tentang zaman dinosaurus?',
    chatCount: 6543,
    category: 'OC',
    tags: ['dinosaur', 'funny', 'educational']
  },
  {
    id: '8',
    name: 'Zen',
    avatar: '🧘',
    description: 'Meditation guru yang membantu kamu menemukan inner peace dan ketenangan',
    greeting: 'Tarik napas... hembuskan perlahan. Welcome, friend.',
    chatCount: 9876,
    category: 'Assistant',
    tags: ['meditation', 'calm', 'wellness']
  }
];

export const mockCategories: Category[] = [
  { id: 'anime', name: 'Anime', icon: '🎌', characterCount: 2341 },
  { id: 'game', name: 'Game', icon: '🎮', characterCount: 1876 },
  { id: 'assistant', name: 'Assistant', icon: '🤖', characterCount: 987 },
  { id: 'roleplay', name: 'Roleplay', icon: '🎭', characterCount: 1543 },
  { id: 'oc', name: 'Original', icon: '✨', characterCount: 3210 },
  { id: 'movie', name: 'Movie & TV', icon: '🎬', characterCount: 1234 }
];
