import { writable } from 'svelte/store';

export type Route = 'home' | 'chat';

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
    }
  };
}

export const router = createRouter();
