<script lang="ts">
  import { mockCharacters } from '@lib/data/mockData';
  import { router } from '@stores/router';
  import { MessageSquare, Clock } from '@lucide/svelte';

  // Mock chat history
  const chatHistory = mockCharacters.slice(0, 5).map((char, idx) => ({
    character: char,
    lastMessage: 'Hey! How are you doing today?',
    timestamp: new Date(Date.now() - idx * 3600000), // Hours ago
    unread: idx < 2 ? Math.floor(Math.random() * 3) + 1 : 0
  }));
</script>

<div class="h-full overflow-y-auto bg-gradient-to-b from-gray-50 to-white dark:from-slate-950 dark:to-slate-900 px-4 sm:px-6 py-8 pb-20">
  <div class="max-w-4xl mx-auto">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl sm:text-4xl font-bold text-slate-900 dark:text-slate-100 mb-2">My Chats</h1>
      <p class="text-slate-600 dark:text-slate-400">Continue your conversations</p>
    </div>

    <!-- Chat List -->
    {#if chatHistory.length > 0}
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
