<script lang="ts">
  import { mockCharacters, mockCategories } from '@lib/data/mockData';
  import CharacterCard from '@components/ui/CharacterCard.svelte';
  import SearchIcon from '@components/ui/icons/Search.svelte';
  import FlameIcon from '@components/ui/icons/Flame.svelte';
  import StarIcon from '@components/ui/icons/Star.svelte';
  import PlusIcon from '@components/ui/icons/Plus.svelte';

  interface Props {
    onCharacterSelect: (characterId: string) => void;
  }

  let { onCharacterSelect }: Props = $props();

  let searchQuery = $state('');

  // Get trending characters (top 6 by chat count)
  const trendingCharacters = $derived(
    [...mockCharacters]
      .sort((a, b) => (b.chatCount || 0) - (a.chatCount || 0))
      .slice(0, 6)
  );

  // Get popular characters (next 6)
  const popularCharacters = $derived(
    [...mockCharacters]
      .sort((a, b) => (b.chatCount || 0) - (a.chatCount || 0))
      .slice(6)
  );
</script>

<div class="h-full overflow-y-auto bg-slate-900">
  <!-- Hero Section -->
  <section class="px-4 py-8 sm:py-12 bg-gradient-to-b from-slate-800 to-slate-900">
    <div class="max-w-4xl mx-auto text-center">
      <!-- Tagline -->
      <h1 class="text-3xl sm:text-4xl md:text-5xl font-bold text-slate-100 mb-4">
        Chat dengan <span class="bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">AI Companion</span> Favoritmu
      </h1>
      
      <p class="text-slate-400 text-base sm:text-lg mb-8 max-w-2xl mx-auto">
        Ribuan karakter AI menunggumu. Ngobrol, roleplay, atau cari teman curhat - semua ada di sini.
      </p>

      <!-- Search Bar -->
      <div class="relative max-w-2xl mx-auto">
        <div class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">
          <SearchIcon size={20} />
        </div>
        <input
          type="text"
          bind:value={searchQuery}
          placeholder="Cari karakter, tema, atau fandom..."
          class="w-full bg-slate-800 border border-slate-700 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 rounded-full px-12 py-4 text-slate-100 placeholder-slate-500 outline-none transition-all"
        />
      </div>

      <!-- Quick CTAs -->
      <div class="flex flex-wrap items-center justify-center gap-4 mt-8">
        <button class="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-full transition-colors shadow-lg shadow-blue-500/20">
          Mulai Ngobrol
        </button>
        <button class="px-6 py-3 bg-slate-800 hover:bg-slate-750 text-slate-100 font-medium rounded-full border border-slate-700 transition-colors">
          <div class="flex items-center gap-2">
            <PlusIcon size={18} />
            Buat Karakter
          </div>
        </button>
      </div>
    </div>
  </section>

  <!-- Trending Characters -->
  <section class="px-4 py-8">
    <div class="max-w-6xl mx-auto">
      <div class="flex items-center gap-2 mb-6">
        <FlameIcon size={24} class="text-orange-500" />
        <h2 class="text-2xl font-bold text-slate-100">Trending Now</h2>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {#each trendingCharacters as character (character.id)}
          <CharacterCard {character} onclick={() => onCharacterSelect(character.id)} />
        {/each}
      </div>
    </div>
  </section>

  <!-- Popular Characters -->
  <section class="px-4 py-8 bg-slate-900/50">
    <div class="max-w-6xl mx-auto">
      <div class="flex items-center gap-2 mb-6">
        <StarIcon size={24} class="text-yellow-500" />
        <h2 class="text-2xl font-bold text-slate-100">Popular</h2>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {#each popularCharacters as character (character.id)}
          <CharacterCard {character} onclick={() => onCharacterSelect(character.id)} />
        {/each}
      </div>
    </div>
  </section>

  <!-- Categories -->
  <section class="px-4 py-8">
    <div class="max-w-6xl mx-auto">
      <h2 class="text-2xl font-bold text-slate-100 mb-6">Explore Categories</h2>

      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-3">
        {#each mockCategories as category (category.id)}
          <button class="group bg-slate-800 hover:bg-slate-750 rounded-lg p-4 transition-all hover:scale-105">
            <div class="text-3xl mb-2">{category.icon}</div>
            <div class="text-sm font-medium text-slate-100 mb-1">{category.name}</div>
            <div class="text-xs text-slate-500">{category.characterCount}+ chars</div>
          </button>
        {/each}
      </div>
    </div>
  </section>

  <!-- Footer -->
  <footer class="px-4 py-8 border-t border-slate-800">
    <div class="max-w-6xl mx-auto">
      <div class="flex flex-wrap justify-center gap-6 text-sm text-slate-500 mb-4">
        <button class="hover:text-slate-300 transition-colors">About</button>
        <button class="hover:text-slate-300 transition-colors">Privacy</button>
        <button class="hover:text-slate-300 transition-colors">Terms</button>
        <button class="hover:text-slate-300 transition-colors">Help</button>
        <button class="hover:text-slate-300 transition-colors">Community</button>
      </div>
      <p class="text-center text-xs text-slate-600">
        © 2026 EchoMinds. Your Personal AI Companion Platform.
      </p>
    </div>
  </footer>
</div>
