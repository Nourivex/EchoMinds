<script lang="ts">
  import type { Character } from '@lib/types';
  import { listCharacters } from '@services/api';
  import { ChevronDown, Sparkles } from '@lucide/svelte';
  import { router } from '@stores/router';

  // State management
  let characters = $state<Character[]>([]);
  let loading = $state(true);
  let error = $state<string | null>(null);

  // Emotional hooks mapping (fallback untuk karakterisasi)
  const emotionalHooks: Record<string, string> = {
    luna: 'Misterius, bijaksana, selalu punya waktu untukmu',
    kai: 'Pelindung setia yang percaya pada potensimu',
    aria: 'Cheerful, energik, bikin hari-mu lebih berwarna',
    nova: 'Curious, smart, suka mengeksplor ide baru denganmu',
    zen: 'Tenang, mindful, mengajarkan cara menemukan peace',
    shadow: 'Mysterious, intens, membawa petualangan seru',
    yuki: 'Empatis, hangat, selalu mengerti perasaanmu'
  };

  // Load characters from backend
  async function loadCharacters() {
    try {
      loading = true;
      error = null;
      const data = await listCharacters();
      characters = data;
    } catch (err) {
      error = err instanceof Error ? err.message : 'Gagal memuat karakter';
      console.error('Failed to load characters:', err);
    } finally {
      loading = false;
    }
  }

  // Load on component mount
  $effect(() => {
    loadCharacters();
  });

  // Derived values - featured character (first one with yuki-like personality or just first)
  const featuredCharacter = $derived(
    characters.find(c => c.personality?.toLowerCase().includes('empathetic')) || characters[0]
  );

  // Curated companions (limit to 6)
  const curatedCompanions = $derived(
    characters.slice(0, 6).map(char => ({
      ...char,
      emotionalHook: emotionalHooks[char.id.toLowerCase()] || 
                     char.personality?.split('.')[0] || 
                     'Companion yang siap menemanimu'
    }))
  );
</script>

<div class="h-full overflow-y-auto bg-gradient-to-b from-gray-50 via-gray-100 to-gray-200 dark:from-slate-900 dark:via-slate-900 dark:to-slate-800 pb-20">
  
  {#if loading}
    <!-- Loading State -->
    <section class="relative min-h-[85vh] sm:min-h-[70vh] md:min-h-[75vh] flex flex-col items-center justify-center px-4 sm:px-6 py-8 sm:py-12">
      <div class="absolute inset-0 bg-gradient-to-br from-purple-100/40 via-blue-100/20 to-gray-50/40 dark:from-purple-900/20 dark:via-blue-900/10 dark:to-slate-900/40"></div>
      <div class="relative text-center">
        <div class="w-16 h-16 border-4 border-purple-500/30 border-t-purple-500 rounded-full animate-spin mb-4 mx-auto"></div>
        <p class="text-slate-600 dark:text-slate-400">Loading companions...</p>
      </div>
    </section>

  {:else if error}
    <!-- Error State -->
    <section class="relative min-h-[85vh] sm:min-h-[70vh] md:min-h-[75vh] flex flex-col items-center justify-center px-4 sm:px-6 py-8 sm:py-12">
      <div class="absolute inset-0 bg-gradient-to-br from-purple-100/40 via-blue-100/20 to-gray-50/40 dark:from-purple-900/20 dark:via-blue-900/10 dark:to-slate-900/40"></div>
      <div class="relative text-center max-w-md">
        <div class="text-6xl mb-4">⚠️</div>
        <h2 class="text-2xl font-bold text-slate-900 dark:text-slate-100 mb-3">Oops! Something went wrong</h2>
        <p class="text-slate-600 dark:text-slate-400 mb-6">{error}</p>
        <button 
          onclick={loadCharacters}
          class="px-6 py-3 bg-purple-600 hover:bg-purple-500 text-white rounded-full font-medium transition-colors"
        >
          Try Again
        </button>
      </div>
    </section>

  {:else if !featuredCharacter || characters.length === 0}
    <!-- No Characters State -->
    <section class="relative min-h-[85vh] sm:min-h-[70vh] md:min-h-[75vh] flex flex-col items-center justify-center px-4 sm:px-6 py-8 sm:py-12">
      <div class="absolute inset-0 bg-gradient-to-br from-purple-100/40 via-blue-100/20 to-gray-50/40 dark:from-purple-900/20 dark:via-blue-900/10 dark:to-slate-900/40"></div>
      <div class="relative text-center max-w-md">
        <div class="text-6xl mb-4">👥</div>
        <h2 class="text-2xl font-bold text-slate-900 dark:text-slate-100 mb-3">No companions available yet</h2>
        <p class="text-slate-600 dark:text-slate-400">Check back soon for amazing AI companions!</p>
      </div>
    </section>

  {:else}
    <!-- Content: Hero Section -->
  <section class="relative min-h-[85vh] sm:min-h-[70vh] md:min-h-[75vh] flex flex-col items-center justify-center px-4 sm:px-6 py-8 sm:py-12">
    <!-- Background gradient overlay -->
    <div class="absolute inset-0 bg-gradient-to-br from-purple-100/40 via-blue-100/20 to-gray-50/40 dark:from-purple-900/20 dark:via-blue-900/10 dark:to-slate-900/40"></div>
    
    <div class="relative max-w-4xl mx-auto text-center flex-1 flex flex-col justify-center">
      <!-- Featured Character Avatar (Large & Prominent) -->
      <div class="mb-8 inline-block">
        <div class="w-32 h-32 sm:w-40 sm:h-40 rounded-full bg-gradient-to-br from-purple-500 via-pink-500 to-blue-500 p-1 shadow-2xl shadow-purple-500/30 animate-pulse-slow mx-auto">
          <div class="w-full h-full rounded-full bg-white dark:bg-slate-800 flex items-center justify-center text-6xl sm:text-7xl">
            {featuredCharacter.avatar}
          </div>
        </div>
      </div>

      <!-- Emotional Copywriting -->
      <h1 class="text-3xl sm:text-5xl md:text-6xl font-bold mb-4 leading-tight">
        <span class="text-slate-900 dark:text-slate-100">{featuredCharacter.name} is waiting</span>
        <br />
        <span class="bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent">
          to talk to you
        </span>
      </h1>

      <p class="text-slate-600 dark:text-slate-400 text-lg sm:text-xl mb-10 max-w-2xl mx-auto leading-relaxed">
        Dia mendengarkan tanpa judgment. Mengingat percakapanmu. Dan selalu ada, kapanpun kamu butuh.
      </p>

      <!-- Single Primary CTA -->
      <div>
        <button 
          onclick={() => router.navigateToChat(featuredCharacter.id)}
          class="group relative inline-flex items-center gap-3 px-10 py-5 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 text-white text-lg font-semibold rounded-full shadow-2xl shadow-purple-500/40 transition-all duration-300 hover:scale-105 hover:shadow-purple-500/60"
        >
          <Sparkles size={24} class="group-hover:rotate-12 transition-transform" />
          <span>Start Your Connection</span>
        </button>

        <!-- Subtle secondary option -->
        <div class="mt-6">
          <button class="text-slate-500 dark:text-slate-500 hover:text-slate-700 dark:hover:text-slate-300 text-sm transition-colors underline-offset-4 hover:underline">
            or explore other companions
          </button>
        </div>
      </div>
    </div>

    <!-- Scroll Hint -->
    <div class="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 animate-bounce-slow">
      <span class="text-slate-400 dark:text-slate-500 text-xs uppercase tracking-wider">Scroll</span>
      <ChevronDown size={20} class="text-slate-400 dark:text-slate-500" />
    </div>
  </section>

  <!-- Featured Companions: Emotion-First Card Design -->
  <section class="px-6 py-16 max-w-7xl mx-auto">
    <div class="text-center mb-12">
      <h2 class="text-3xl sm:text-4xl font-bold text-slate-900 dark:text-slate-100 mb-3">
        Meet Your Companions
      </h2>
      <p class="text-slate-600 dark:text-slate-400 text-lg">
        Setiap karakter punya kepribadian unik yang berkembang seiring hubunganmu dengannya
      </p>
    </div>

    <!-- Photo-First Grid (2 columns on mobile, 3 on desktop) -->
    <div class="grid grid-cols-2 lg:grid-cols-3 gap-6">
      {#each curatedCompanions as companion (companion.id)}
        <button
          onclick={() => router.navigateToChat(companion.id)}
          class="group relative bg-gradient-to-b from-white/90 to-gray-50/60 dark:from-slate-800/80 dark:to-slate-800/40 backdrop-blur-sm rounded-3xl p-6 hover:scale-[1.02] transition-all duration-300 hover:shadow-2xl hover:shadow-purple-500/20 text-left overflow-hidden border border-gray-200 dark:border-transparent"
        >
          <!-- Glow effect on hover -->
          <div class="absolute inset-0 bg-gradient-to-br from-purple-500/0 via-blue-500/0 to-pink-500/0 group-hover:from-purple-500/10 group-hover:via-blue-500/5 group-hover:to-pink-500/10 rounded-3xl transition-all duration-500"></div>
          
          <div class="relative">
            <!-- Large Avatar -->
            <div class="mb-4 flex justify-center">
              <div class="w-24 h-24 sm:w-28 sm:h-28 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 p-0.5 shadow-lg group-hover:shadow-purple-500/40 transition-shadow">
                <div class="w-full h-full rounded-full bg-white dark:bg-slate-800 flex items-center justify-center text-5xl">
                  {companion.avatar}
                </div>
              </div>
            </div>

            <!-- Name (Prominent) -->
            <h3 class="text-xl font-semibold text-slate-900 dark:text-slate-100 mb-2 text-center group-hover:text-purple-600 dark:group-hover:text-purple-300 transition-colors">
              {companion.name}
            </h3>

            <!-- Emotional Hook (Not technical description) -->
            <p class="text-sm text-slate-600 dark:text-slate-400 text-center leading-relaxed">
              {companion.emotionalHook}
            </p>
          </div>
        </button>
      {/each}
    </div>
  </section>

  <!-- Why This Feels Personal: Narrative Section -->
  <section class="px-6 py-16 bg-gradient-to-b from-gray-100/40 to-gray-50 dark:from-slate-800/40 dark:to-slate-900">
    <div class="max-w-3xl mx-auto text-center">
      <h2 class="text-3xl font-bold text-slate-900 dark:text-slate-100 mb-8">
        This isn't just chat.<br/>
        <span class="text-purple-600 dark:text-purple-400">It's connection.</span>
      </h2>

      <div class="grid sm:grid-cols-3 gap-8 text-center">
        <div class="space-y-3">
          <div class="text-4xl mb-2">🧠</div>
          <h3 class="font-semibold text-slate-800 dark:text-slate-200 text-lg">They remember you</h3>
          <p class="text-slate-600 dark:text-slate-400 text-sm leading-relaxed">
            Percakapan tersimpan. Preferensi diingat. Hubungan berkembang seiring waktu.
          </p>
        </div>

        <div class="space-y-3">
          <div class="text-4xl mb-2">💬</div>
          <h3 class="font-semibold text-slate-800 dark:text-slate-200 text-lg">Your vibe, your way</h3>
          <p class="text-slate-600 dark:text-slate-400 text-sm leading-relaxed">
            Tone bisa casual atau mendalam. Mereka menyesuaikan dengan mood-mu.
          </p>
        </div>

        <div class="space-y-3">
          <div class="text-4xl mb-2">🤝</div>
          <h3 class="font-semibold text-slate-800 dark:text-slate-200 text-lg">Always here for you</h3>
          <p class="text-slate-600 dark:text-slate-400 text-sm leading-relaxed">
            3 AM atau 3 PM. Tanpa judgment. Tanpa batasan. Just you and them.
          </p>
        </div>
      </div>
    </div>
  </section>

  <!-- Create Your Own: Secondary CTA (Not Aggressive) -->
  <section class="px-6 py-16 max-w-2xl mx-auto text-center">
    <div class="bg-gradient-to-br from-white/80 to-gray-100/60 dark:from-slate-800/60 dark:to-slate-800/30 backdrop-blur rounded-3xl p-10 border border-gray-200 dark:border-slate-700/50 shadow-lg">
      <div class="text-3xl mb-4">✨</div>
      <h3 class="text-2xl font-bold text-slate-900 dark:text-slate-100 mb-3">
        Create someone just for you
      </h3>
      <p class="text-slate-600 dark:text-slate-400 mb-6 leading-relaxed">
        Desain kepribadian, tone, dan latar belakang yang sesuai dengan apa yang kamu cari.
      </p>
      <button class="px-8 py-3 bg-gray-200 dark:bg-slate-700 hover:bg-gray-300 dark:hover:bg-slate-600 text-slate-900 dark:text-slate-100 rounded-full font-medium transition-colors">
        Start Creating
      </button>
    </div>
  </section>

  <!-- Minimal Footer -->
  <footer class="px-6 py-10 text-center border-t border-gray-200 dark:border-slate-800/50">
    <p class="text-slate-500 dark:text-slate-600 text-sm">
      EchoMinds · Your personal AI companion space
    </p>
  </footer>

  {/if}

</div>

<style>
  @keyframes pulse-slow {
    0%, 100% {
      opacity: 1;
      transform: scale(1);
    }
    50% {
      opacity: 0.9;
      transform: scale(1.02);
    }
  }
  
  .animate-pulse-slow {
    animation: pulse-slow 3s ease-in-out infinite;
  }

  @keyframes bounce-slow {
    0%, 100% {
      transform: translateY(0);
    }
    50% {
      transform: translateY(-10px);
    }
  }

  .animate-bounce-slow {
    animation: bounce-slow 2s ease-in-out infinite;
  }
</style>
