<script lang="ts">
  import Sidebar from '@components/layouts/Sidebar.svelte';
  import Topbar from '@components/layouts/Topbar.svelte';
  import HomePage from '@components/pages/HomePage.svelte';
  import MyChatsPage from '@components/pages/MyChatsPage.svelte';
  import ExplorePage from '@components/pages/ExplorePage.svelte';
  import CreatePage from '@components/pages/CreatePage.svelte';
  import SettingsPage from '@components/pages/SettingsPage.svelte';
  import ChatInterface from '@components/chat/ChatInterface.svelte';
  import { router } from '@stores/router';
  import { mockCharacters } from '@lib/data/mockData';
  import { ArrowLeft } from '@lucide/svelte';

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

<div class="flex h-screen w-full bg-gray-50 dark:bg-slate-900">
  {#if routerState.currentRoute === 'chat'}
    <!-- Chat Interface (fullscreen, no sidebar) -->
    <div class="flex flex-col w-full h-full">
      <!-- Chat Topbar dengan Back Button -->
      <header class="sticky top-0 z-50 bg-white/95 dark:bg-slate-800/95 backdrop-blur-sm border-b border-gray-200 dark:border-slate-700 px-6 py-3">
        <div class="flex items-center gap-4">
          <button
            onclick={handleBackToHome}
            class="p-2 hover:bg-gray-100 dark:hover:bg-slate-700 rounded-lg transition-colors text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-slate-100"
            aria-label="Back to home"
          >
            <ArrowLeft size={24} />
          </button>
          
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center text-2xl">
              {selectedCharacter?.avatar || '🤖'}
            </div>
            <div>
              <h2 class="text-lg font-semibold text-slate-900 dark:text-slate-100">{selectedCharacter?.name || 'Chat'}</h2>
              <p class="text-xs text-slate-600 dark:text-slate-400">Online</p>
            </div>
          </div>
        </div>
      </header>
      
      <ChatInterface character={selectedCharacter} />
    </div>
  {:else}
    <!-- All other routes dengan Sidebar -->
    <Sidebar>
      <Topbar />
      
      {#if routerState.currentRoute === 'home'}
        <HomePage onCharacterSelect={handleCharacterSelect} />
      {:else if routerState.currentRoute === 'my-chats'}
        <MyChatsPage />
      {:else if routerState.currentRoute === 'explore'}
        <ExplorePage />
      {:else if routerState.currentRoute === 'create'}
        <CreatePage />
      {:else if routerState.currentRoute === 'settings'}
        <SettingsPage />
      {/if}
    </Sidebar>
  {/if}
</div>
