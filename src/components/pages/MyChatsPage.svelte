<script lang="ts">
  import type { Character } from '@lib/types';
  import { listCharacters } from '@services/api';
  import { router } from '@stores/router';
  import { MessageSquare, Clock, ArrowLeft } from '@lucide/svelte';
  import ChatInterface from '@components/chat/ChatInterface.svelte';

  // API State
  let characters = $state<Character[]>([]);
  let loading = $state(true);
  let error = $state<string | null>(null);

  // Router state
  let routerState = $state({ currentRoute: 'my-chats', selectedCharacterId: null });

  router.subscribe(state => {
    routerState = state;
  });

  // Selected character for chat
  const selectedCharacter = $derived(
    routerState.selectedCharacterId
      ? characters.find(c => c.id === routerState.selectedCharacterId)
      : null
  );

  // Load characters from backend
  async function loadCharacters() {
    try {
      loading = true;
      error = null;
      const data = await listCharacters();
      characters = data;
    } catch (err) {
      error = err instanceof Error ? err.message : 'Gagal memuat data';
      console.error('Failed to load characters:', err);
    } finally {
      loading = false;
    }
  }

  // Load on mount
  $effect(() => {
    loadCharacters();
  });

  // For now, display all available characters as potential chats
  // TODO: Add backend endpoint GET /api/conversations to fetch actual chat history
  const chatHistory = $derived(
    characters.map((char, idx) => ({
      character: char,
      lastMessage: 'Start a new conversation or continue where you left off',
      timestamp: new Date(Date.now() - idx * 3600000),
      unread: 0 // Real unread count from backend later
    }))
  );
</script>

{#if selectedCharacter}
  <!-- Chat View (fullscreen chat interface) -->
  <div class="flex flex-col h-full">
    <!-- Chat Header dengan Back Button -->
    <header class="sticky top-0 z-50 bg-white/95 dark:bg-slate-800/95 backdrop-blur-sm border-b border-gray-200 dark:border-slate-700 px-6 py-3">
      <div class="flex items-center gap-4">
        <button
          onclick={() => router.navigateToMyChats()}
          class="p-2 hover:bg-gray-100 dark:hover:bg-slate-700 rounded-lg transition-colors text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-slate-100"
          aria-label="Back to chats"
        >
          <ArrowLeft size={24} />
        </button>
        
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center text-2xl">
            {selectedCharacter.avatar || '🤖'}
          </div>
          <div>
            <h2 class="text-lg font-semibold text-slate-900 dark:text-slate-100">{selectedCharacter.name}</h2>
            <p class="text-xs text-slate-600 dark:text-slate-400">Online</p>
          </div>
        </div>
      </div>
    </header>
    
    <ChatInterface character={selectedCharacter} />
  </div>
{:else}
  <!-- Chat List View -->
  <div class="h-full overflow-y-auto bg-gradient-to-b from-gray-50 to-white dark:from-slate-950 dark:to-slate-900 px-4 sm:px-6 py-8 pb-20">
  <div class="max-w-4xl mx-auto">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl sm:text-4xl font-bold text-slate-900 dark:text-slate-100 mb-2">My Chats</h1>
      <p class="text-slate-600 dark:text-slate-400">Continue your conversations</p>
    </div>

    {#if loading}
      <!-- Loading State -->
      <div class="text-center py-16">
        <div class="w-16 h-16 border-4 border-purple-500/30 border-t-purple-500 rounded-full animate-spin mb-4 mx-auto"></div>
        <p class="text-slate-600 dark:text-slate-400">Loading chats...</p>
      </div>

    {:else if error}
      <!-- Error State -->
      <div class="text-center py-16">
        <div class="text-6xl mb-4">⚠️</div>
        <h3 class="text-xl font-semibold text-slate-700 dark:text-slate-300 mb-2">Failed to load chats</h3>
        <p class="text-slate-500 dark:text-slate-400 mb-4">{error}</p>
        <button 
          onclick={loadCharacters}
          class="px-6 py-3 bg-purple-600 hover:bg-purple-500 text-white rounded-full font-medium transition-colors"
        >
          Try Again
        </button>
      </div>

    {:else if chatHistory.length > 0}
      <!-- Chat List -->
      <div class="space-y-3">
        {#each chatHistory as chat}
          <button
            onclick={() => router.navigateToChat(chat.character.id)}
            class="w-full flex items-center gap-4 p-4 bg-white dark:bg-slate-800/50 rounded-2xl border border-gray-200 dark:border-slate-700 hover:border-purple-300 dark:hover:border-purple-700 hover:shadow-lg transition-all group"
          >
            <!-- Character Avatar -->
            <div class="relative flex-shrink-0">
              <div class="w-14 h-14 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 p-0.5">
                <div class="w-full h-full rounded-full bg-white dark:bg-slate-800 flex items-center justify-center text-3xl">
                  {chat.character.avatar}
                </div>
              </div>
              {#if chat.unread > 0}
                <div class="absolute -top-1 -right-1 w-6 h-6 bg-red-500 rounded-full flex items-center justify-center text-xs text-white font-bold">
                  {chat.unread}
                </div>
              {/if}
            </div>

            <!-- Chat Info -->
            <div class="flex-1 min-w-0 text-left">
              <div class="flex items-center justify-between mb-1">
                <h3 class="font-semibold text-slate-900 dark:text-slate-100 group-hover:text-purple-600 dark:group-hover:text-purple-400 transition-colors">
                  {chat.character.name}
                </h3>
                <span class="text-xs text-slate-500 dark:text-slate-500 flex items-center gap-1">
                  <Clock size={12} />
                  {new Intl.RelativeTimeFormat('id', { numeric: 'auto' }).format(
                    -Math.floor((Date.now() - chat.timestamp.getTime()) / 3600000),
                    'hour'
                  )}
                </span>
              </div>
              <p class="text-sm text-slate-600 dark:text-slate-400 truncate">
                {chat.lastMessage}
              </p>
            </div>

            <!-- Arrow Icon -->
            <div class="flex-shrink-0 text-slate-400 group-hover:text-purple-500 transition-colors">
              <MessageSquare size={20} />
            </div>
          </button>
        {/each}
      </div>
    {:else}
      <div class="text-center py-16">
        <div class="text-6xl mb-4">💬</div>
        <h3 class="text-xl font-semibold text-slate-700 dark:text-slate-300 mb-2">No chats yet</h3>
        <p class="text-slate-500 dark:text-slate-400">Start a conversation from the home page</p>
      </div>
    {/if}
  </div>
  </div>
{/if}
