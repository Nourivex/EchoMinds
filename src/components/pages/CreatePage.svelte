<script lang="ts">
  import { Sparkles, Image, Wand2 } from '@lucide/svelte';

  let characterName = $state('');
  let characterPersonality = $state('');
  let characterVoice = $state('friendly');
  let selectedAvatar = $state('🤖');

  const avatarOptions = ['🤖', '👨', '👩', '🧑', '👦', '👧', '🧒', '👶', '🦸', '🦹', '🧙', '🧚', '🧛', '🧜', '🧝', '🧞'];
  const voiceOptions = [
    { id: 'friendly', label: 'Friendly & Warm', icon: '😊' },
    { id: 'professional', label: 'Professional', icon: '💼' },
    { id: 'playful', label: 'Playful & Fun', icon: '🎮' },
    { id: 'mysterious', label: 'Mysterious', icon: '🎭' },
    { id: 'wise', label: 'Wise & Calm', icon: '🧘' }
  ];

  function handleCreate() {
    console.log('Creating character:', { characterName, characterPersonality, characterVoice, selectedAvatar });
    alert('Character creation coming soon! 🎉');
  }
</script>

<div class="h-full overflow-y-auto bg-gradient-to-b from-gray-50 to-white dark:from-slate-950 dark:to-slate-900 px-4 sm:px-6 py-8 pb-16">
  <div class="max-w-3xl mx-auto">
    <!-- Header -->
    <div class="mb-8 text-center">
      <div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-purple-500 to-blue-500 rounded-2xl mb-4">
        <Wand2 size={32} class="text-white" />
      </div>
      <h1 class="text-3xl sm:text-4xl font-bold text-slate-900 dark:text-slate-100 mb-2">Create Your Companion</h1>
      <p class="text-slate-600 dark:text-slate-400">Design a unique AI companion just for you</p>
    </div>

    <!-- Form -->
    <div class="bg-white dark:bg-slate-800/50 rounded-3xl border border-gray-200 dark:border-slate-700 p-6 sm:p-8 space-y-6">
      <!-- Avatar Selection -->
      <div>
        <label class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">
          Choose Avatar
        </label>
        <div class="grid grid-cols-8 gap-2">
          {#each avatarOptions as avatar}
            <button
              type="button"
              onclick={() => selectedAvatar = avatar}
              class="w-full aspect-square text-2xl rounded-xl border-2 transition-all {selectedAvatar === avatar ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20 scale-110' : 'border-gray-200 dark:border-slate-700 hover:border-purple-300 dark:hover:border-purple-600'}"
            >
              {avatar}
            </button>
          {/each}
        </div>
      </div>

      <!-- Name -->
      <div>
        <label for="name" class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">
          Character Name *
        </label>
        <input
          id="name"
          type="text"
          bind:value={characterName}
          placeholder="e.g., Luna, Kai, Nova..."
          class="w-full px-4 py-3 bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 outline-none transition-all"
        />
      </div>

      <!-- Personality -->
      <div>
        <label for="personality" class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">
          Personality & Background *
        </label>
        <textarea
          id="personality"
          bind:value={characterPersonality}
          placeholder="Describe their personality, interests, and background. Be as detailed as you like..."
          rows="5"
          class="w-full px-4 py-3 bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 outline-none transition-all resize-none"
        ></textarea>
      </div>

      <!-- Voice/Tone -->
      <div>
        <label class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">
          Conversation Style
        </label>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {#each voiceOptions as voice}
            <button
              type="button"
              onclick={() => characterVoice = voice.id}
              class="flex items-center gap-3 p-4 rounded-xl border-2 transition-all text-left {characterVoice === voice.id ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20' : 'border-gray-200 dark:border-slate-700 hover:border-purple-300 dark:hover:border-purple-600'}"
            >
              <span class="text-2xl">{voice.icon}</span>
              <span class="text-sm font-medium text-slate-700 dark:text-slate-300">{voice.label}</span>
            </button>
          {/each}
        </div>
      </div>

      <!-- Create Button -->
      <button
        onclick={handleCreate}
        disabled={!characterName.trim() || !characterPersonality.trim()}
        class="w-full py-4 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 disabled:from-slate-600 disabled:to-slate-600 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl disabled:shadow-none transition-all disabled:cursor-not-allowed flex items-center justify-center gap-2"
      >
        <Sparkles size={20} />
        <span>Create Companion</span>
      </button>
    </div>
  </div>
</div>
