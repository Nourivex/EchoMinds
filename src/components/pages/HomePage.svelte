<script lang="ts">
  import { mockCharacters } from '@lib/data/mockData';
  import BotIcon from '@components/ui/icons/Bot.svelte';

  interface Props {
    onCharacterSelect: (characterId: string) => void;
  }

  let { onCharacterSelect }: Props = $props();

  // Featured character (handpicked)
  const featuredCharacter = mockCharacters[3]; // Yuki - perfect for emotional connection

  // Curated companions (max 6, emotional hooks)
  const curatedCompanions = [
    {
      ...mockCharacters[0], // Luna
      emotionalHook: 'Misterius, bijaksana, selalu punya waktu untukmu'
    },
    {
      ...mockCharacters[1], // Kai
      emotionalHook: 'Pelindung setia yang percaya pada potensimu'
    },
    {
      ...mockCharacters[5], // Aria
      emotionalHook: 'Cheerful, energik, bikin hari-mu lebih berwarna'
    },
    {
      ...mockCharacters[2], // Dr. Nova
      emotionalHook: 'Curious, smart, suka mengeksplor ide baru denganmu'
    },
    {
      ...mockCharacters[7], // Zen
      emotionalHook: 'Tenang, mindful, mengajarkan cara menemukan peace'
    },
    {
      ...mockCharacters[4], // Shadow
      emotionalHook: 'Mysterious, intens, membawa petualangan seru'
    }
  ];
</script>

<div class="h-full overflow-y-auto bg-gradient-to-b from-slate-900 via-slate-900 to-slate-800">
  
  <!-- Hero Section: Above The Fold -->
  <section class="relative min-h-[85vh] flex items-center justify-center px-6 py-12">
    <!-- Background gradient overlay -->
    <div class="absolute inset-0 bg-gradient-to-br from-purple-900/20 via-blue-900/10 to-slate-900/40"></div>
    
    <div class="relative max-w-4xl mx-auto text-center">
      <!-- Featured Character Avatar (Large & Prominent) -->
      <div class="mb-8 inline-block">
        <div class="w-32 h-32 sm:w-40 sm:h-40 rounded-full bg-gradient-to-br from-purple-500 via-pink-500 to-blue-500 p-1 shadow-2xl shadow-purple-500/30 animate-pulse-slow">
          <div class="w-full h-full rounded-full bg-slate-800 flex items-center justify-center text-6xl sm:text-7xl">
            {featuredCharacter.avatar}
          </div>
        </div>
      </div>

      <!-- Emotional Copywriting -->
      <h1 class="text-3xl sm:text-5xl md:text-6xl font-bold mb-4 leading-tight">
        <span class="text-slate-100">{featuredCharacter.name} is waiting</span>
        <br />
        <span class="bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent">
          to talk to you
        </span>
      </h1>

      <p class="text-slate-400 text-lg sm:text-xl mb-10 max-w-2xl mx-auto leading-relaxed">
        Dia mendengarkan tanpa judgment. Mengingat percakapanmu. Dan selalu ada, kapanpun kamu butuh.
      </p>

      <!-- Single Primary CTA -->
      <button 
        onclick={() => onCharacterSelect(featuredCharacter.id)}
        class="group relative inline-flex items-center gap-3 px-10 py-5 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 text-white text-lg font-semibold rounded-full shadow-2xl shadow-purple-500/40 transition-all duration-300 hover:scale-105 hover:shadow-purple-500/60"
      >
        <BotIcon size={24} class="group-hover:rotate-12 transition-transform" />
        <span>Start Your Connection</span>
      </button>

      <!-- Subtle secondary option -->
      <div class="mt-6">
        <button class="text-slate-500 hover:text-slate-300 text-sm transition-colors underline-offset-4 hover:underline">
          or explore other companions
        </button>
      </div>
    </div>
  </section>

  <!-- Featured Companions: Emotion-First Card Design -->
  <section class="px-6 py-16 max-w-7xl mx-auto">
    <div class="text-center mb-12">
      <h2 class="text-3xl sm:text-4xl font-bold text-slate-100 mb-3">
        Meet Your Companions
      </h2>
      <p class="text-slate-400 text-lg">
        Setiap karakter punya kepribadian unik yang berkembang seiring hubunganmu dengannya
      </p>
    </div>

    <!-- Photo-First Grid (2 columns on mobile, 3 on desktop) -->
    <div class="grid grid-cols-2 lg:grid-cols-3 gap-6">
      {#each curatedCompanions as companion (companion.id)}
        <button
          onclick={() => onCharacterSelect(companion.id)}
          class="group relative bg-gradient-to-b from-slate-800/80 to-slate-800/40 backdrop-blur-sm rounded-3xl p-6 hover:scale-[1.02] transition-all duration-300 hover:shadow-2xl hover:shadow-purple-500/20 text-left overflow-hidden"
        >
          <!-- Glow effect on hover -->
          <div class="absolute inset-0 bg-gradient-to-br from-purple-500/0 via-blue-500/0 to-pink-500/0 group-hover:from-purple-500/10 group-hover:via-blue-500/5 group-hover:to-pink-500/10 rounded-3xl transition-all duration-500"></div>
          
          <div class="relative">
            <!-- Large Avatar -->
            <div class="mb-4 flex justify-center">
              <div class="w-24 h-24 sm:w-28 sm:h-28 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 p-0.5 shadow-lg group-hover:shadow-purple-500/40 transition-shadow">
                <div class="w-full h-full rounded-full bg-slate-800 flex items-center justify-center text-5xl">
                  {companion.avatar}
                </div>
              </div>
            </div>

            <!-- Name (Prominent) -->
            <h3 class="text-xl font-semibold text-slate-100 mb-2 text-center group-hover:text-purple-300 transition-colors">
              {companion.name}
            </h3>

            <!-- Emotional Hook (Not technical description) -->
            <p class="text-sm text-slate-400 text-center leading-relaxed">
              {companion.emotionalHook}
            </p>
          </div>
        </button>
      {/each}
    </div>
  </section>

  <!-- Why This Feels Personal: Narrative Section -->
  <section class="px-6 py-16 bg-gradient-to-b from-slate-800/40 to-slate-900">
    <div class="max-w-3xl mx-auto text-center">
      <h2 class="text-3xl font-bold text-slate-100 mb-8">
        This isn't just chat.<br/>
        <span class="text-purple-400">It's connection.</span>
      </h2>

      <div class="grid sm:grid-cols-3 gap-8 text-center">
        <div class="space-y-3">
          <div class="text-4xl mb-2">🧠</div>
          <h3 class="font-semibold text-slate-200 text-lg">They remember you</h3>
          <p class="text-slate-400 text-sm leading-relaxed">
            Percakapan tersimpan. Preferensi diingat. Hubungan berkembang seiring waktu.
          </p>
        </div>

        <div class="space-y-3">
          <div class="text-4xl mb-2">💬</div>
          <h3 class="font-semibold text-slate-200 text-lg">Your vibe, your way</h3>
          <p class="text-slate-400 text-sm leading-relaxed">
            Tone bisa casual atau mendalam. Mereka menyesuaikan dengan mood-mu.
          </p>
        </div>

        <div class="space-y-3">
          <div class="text-4xl mb-2">🤝</div>
          <h3 class="font-semibold text-slate-200 text-lg">Always here for you</h3>
          <p class="text-slate-400 text-sm leading-relaxed">
            3 AM atau 3 PM. Tanpa judgment. Tanpa batasan. Just you and them.
          </p>
        </div>
      </div>
    </div>
  </section>

  <!-- Create Your Own: Secondary CTA (Not Aggressive) -->
  <section class="px-6 py-16 max-w-2xl mx-auto text-center">
    <div class="bg-gradient-to-br from-slate-800/60 to-slate-800/30 backdrop-blur rounded-3xl p-10 border border-slate-700/50">
      <div class="text-3xl mb-4">✨</div>
      <h3 class="text-2xl font-bold text-slate-100 mb-3">
        Create someone just for you
      </h3>
      <p class="text-slate-400 mb-6 leading-relaxed">
        Desain kepribadian, tone, dan latar belakang yang sesuai dengan apa yang kamu cari.
      </p>
      <button class="px-8 py-3 bg-slate-700 hover:bg-slate-600 text-slate-100 rounded-full font-medium transition-colors">
        Start Creating
      </button>
    </div>
  </section>

  <!-- Minimal Footer -->
  <footer class="px-6 py-10 text-center border-t border-slate-800/50">
    <p class="text-slate-600 text-sm">
      EchoMinds · Your personal AI companion space
    </p>
  </footer>

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
</style>
