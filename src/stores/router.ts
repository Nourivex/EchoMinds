import { writable } from 'svelte/store';

export type Route = 'home' | 'chat' | 'my-chats' | 'explore' | 'create' | 'settings';

export interface RouterState {
  currentRoute: Route;
  selectedCharacterId: string | null;
}

function createRouter() {
  const { subscribe, update } = writable<RouterState>({
    currentRoute: 'home',
    selectedCharacterId: null
  });

  return {
    subscribe,
    navigateToChat: (characterId: string) => {
      update(state => ({
        ...state,
        currentRoute: 'chat',
        selectedCharacterId: characterId
      }));
    },
    navigateToHome: () => {
      update(state => ({
        ...state,
        currentRoute: 'home',
        selectedCharacterId: null
      }));
    },
    navigateToMyChats: () => {
      update(state => ({
        ...state,
        currentRoute: 'my-chats',
        selectedCharacterId: null
      }));
    },
    navigateToExplore: () => {
      update(state => ({
        ...state,
        currentRoute: 'explore',
        selectedCharacterId: null
      }));
    },
    navigateToCreate: () => {
      update(state => ({
        ...state,
        currentRoute: 'create',
        selectedCharacterId: null
      }));
    },
    navigateToSettings: () => {
      update(state => ({
        ...state,
        currentRoute: 'settings',
        selectedCharacterId: null
      }));
    }
  };
}

export const router = createRouter();
