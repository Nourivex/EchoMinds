<script lang="ts">
  import { mockCharacters, mockCategories } from '@lib/data/mockData';
  import { router } from '@stores/router';
  import { Search, TrendingUp } from '@lucide/svelte';

  let searchQuery = $state('');
  let selectedCategory = $state<string | null>(null);

  const filteredCharacters = $derived(
    mockCharacters.filter(char => {
      const matchSearch = char.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         char.description.toLowerCase().includes(searchQuery.toLowerCase());
      const matchCategory = !selectedCategory || char.category === selectedCategory;
      return matchSearch && matchCategory;
    })
  );
</script>

<div class="h-full overflow-y-auto bg-gradient-to-b from-gray-50 to-white dark:from-slate-950 dark:to-slate-900 px-4 sm:px-6 py-8 pb-16">
  <div class="max-w-6xl mx-auto">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl sm:text-4xl font-bold text-slate-900 dark:text-slate-100 mb-2">Explore</h1>
      <p class="text-slate-600 dark:text-slate-400">Discover AI companions</p>
    </div>

    <!-- Search Bar -->
    <div class="mb-6">
      <div class="relative">
        <Search class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={20} />
        <input
          type="text"
          bind:value={searchQuery}
          placeholder="Search characters..."
          class="w-full pl-12 pr-4 py-3 bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 outline-none transition-all"
        />
      </div>
    </div>

    <!-- Category Filter -->
    <div class="mb-8 flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
      <button
        onclick={() => selectedCategory = null}
        class="px-4 py-2 rounded-full text-sm font-medium transition-all whitespace-nowrap {selectedCategory === null ? 'bg-purple-600 text-white' : 'bg-gray-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300 hover:bg-gray-300 dark:hover:bg-slate-600'}"
      >
        All
      </button>
      {#each mockCategories as category}
        <button
          onclick={() => selectedCategory = category.id}
          class="px-4 py-2 rounded-full text-sm font-medium transition-all whitespace-nowrap {selectedCategory === category.id ? 'bg-purple-600 text-white' : 'bg-gray-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300 hover:bg-gray-300 dark:hover:bg-slate-600'}"
        >
          {category.icon} {category.name}
        </button>
      {/each}
    </div>

    <!-- Characters Grid -->
    {#if filteredCharacters.length > 0}
      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
        {#each filteredCharacters as character}
          <button
            onclick={() => router.navigateToChat(character.id)}
            class="group bg-white dark:bg-slate-800/50 rounded-2xl p-4 border border-gray-200 dark:border-slate-700 hover:border-purple-300 dark:hover:border-purple-700 hover:shadow-xl transition-all"
          >
            <!-- Avatar -->
            <div class="mb-3 flex justify-center">
              <div class="w-20 h-20 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 p-0.5 group-hover:scale-110 transition-transform">
                <div class="w-full h-full rounded-full bg-white dark:bg-slate-800 flex items-center justify-center text-4xl">
                  {character.avatar}
                </div>
              </div>
            </div>

            <!-- Info -->
            <h3 class="font-semibold text-slate-900 dark:text-slate-100 mb-1 group-hover:text-purple-600 dark:group-hover:text-purple-400 transition-colors">
              {character.name}
            </h3>
            <p class="text-xs text-slate-500 dark:text-slate-400 line-clamp-2 mb-2">
              {character.description}
            </p>

            <!-- Stats -->
            <div class="flex items-center justify-center gap-1 text-xs text-slate-500">
              <TrendingUp size={12} />
              <span>{character.chatCount} chats</span>
            </div>
          </button>
        {/each}
      </div>
    {:else}
      <div class="text-center py-16">
        <div class="text-6xl mb-4">🔍</div>
        <h3 class="text-xl font-semibold text-slate-700 dark:text-slate-300 mb-2">No characters found</h3>
        <p class="text-slate-500 dark:text-slate-400">Try a different search or category</p>
      </div>
    {/if}
  </div>
</div>

<style>
  .scrollbar-hide::-webkit-scrollbar {
    display: none;
  }
  .scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }
</style>
