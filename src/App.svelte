<script lang="ts">
  import Sidebar from '@components/layouts/Sidebar.svelte';
  import Topbar from '@components/layouts/Topbar.svelte';
  import HomePage from '@components/pages/HomePage.svelte';
  import ChatInterface from '@components/chat/ChatInterface.svelte';
  import { router } from '@stores/router';
  import { mockCharacters } from '@lib/data/mockData';
  import {ArrowLeft} from '@lucide/svelte';

  let routerState = $state({ currentRoute: 'home', selectedCharacterId: null });

  router.subscribe(state => {
    routerState = state;
  });

  const selectedCharacter = $derived(
    routerState.selectedCharacterId
      ? mockCharacters.find(c => c.id === routerState.selectedCharacterId)
      : null
  );

  function handleCharacterSelect(characterId: string) {
    router.navigateToChat(characterId);
  }

  function handleBackToHome() {
    router.navigateToHome();
  }
</script>

<div class="flex h-screen bg-slate-900">
  {#if routerState.currentRoute === 'home'}
    <!-- Homepage dengan Sidebar -->
    <Sidebar>
      <Topbar />
      <HomePage onCharacterSelect={handleCharacterSelect} />
    </Sidebar>
  {:else if routerState.currentRoute === 'chat'}
    <!-- Chat Interface (fullscreen, no sidebar) -->
    <div class="flex flex-col w-full h-full">
      <!-- Chat Topbar dengan Back Button -->
      <header class="sticky top-0 z-50 bg-slate-800/95 backdrop-blur-sm border-b border-slate-700 px-6 py-3">
        <div class="flex items-center gap-4">
          <button
            onclick={handleBackToHome}
            class="p-2 hover:bg-slate-700 rounded-lg transition-colors text-slate-300 hover:text-slate-100"
            aria-label="Back to home"
          >
            <ArrowLeft size={24} />
          </button>
          
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center text-2xl">
              {selectedCharacter?.avatar || '🤖'}
            </div>
            <div>
              <h2 class="text-lg font-semibold text-slate-100">{selectedCharacter?.name || 'Chat'}</h2>
              <p class="text-xs text-slate-400">Online</p>
            </div>
          </div>
        </div>
      </header>
      
      <ChatInterface character={selectedCharacter} />
    </div>
  {/if}
</div>
