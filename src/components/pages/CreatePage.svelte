<script lang="ts">
  import { Sparkles, Wand2, AlertCircle, Globe, Heart, MessageCircle } from '@lucide/svelte';
  import { router } from '@stores/router';

  // Core fields
  let characterName = $state('');
  let characterAvatar = $state('🤖');
  let characterDescription = $state('');
  
  // Personality & Background (separated as per your design)
  let characterPersonality = $state('');
  let characterBackground = $state('');
  
  // Language settings
  let primaryLanguage = $state('id'); // id | en
  let conversationStyle = $state('friendly');
  
  // Relationship settings
  let relationshipType = $state('friend'); // friend | partner | mentor | etc
  let emotionalTone = $state('warm'); // warm | neutral | playful | mysterious
  
  // Category
  let selectedCategory = $state('supportive');
  
  // UI State
  let isCreating = $state(false);
  let error = $state<string | null>(null);

  const avatarOptions = ['🤖', '👨', '👩', '🧑', '👦', '👧', '🧒', '👶', '🦸', '🦹', '🧙', '🧚', '🧛', '🧜', '🧝', '🧞'];
  
  const languageOptions = [
    { id: 'id', label: 'Bahasa Indonesia', flag: '🇮🇩' },
    { id: 'en', label: 'English', flag: '🇺🇸' }
  ];

  const styleOptions = [
    { id: 'friendly', label: 'Friendly & Warm', icon: '😊' },
    { id: 'professional', label: 'Professional', icon: '💼' },
    { id: 'playful', label: 'Playful & Fun', icon: '🎮' },
    { id: 'mysterious', label: 'Mysterious', icon: '🎭' },
    { id: 'wise', label: 'Wise & Calm', icon: '🧘' }
  ];

  const relationshipOptions = [
    { id: 'friend', label: 'Friend', description: 'Supportive companion' },
    { id: 'partner', label: 'Partner', description: 'Romantic connection' },
    { id: 'mentor', label: 'Mentor', description: 'Wise guide' },
    { id: 'rival', label: 'Rival', description: 'Competitive edge' }
  ];

  const toneOptions = [
    { id: 'warm', label: 'Warm', emoji: '💖' },
    { id: 'neutral', label: 'Neutral', emoji: '😌' },
    { id: 'playful', label: 'Playful', emoji: '😄' },
    { id: 'mysterious', label: 'Mysterious', emoji: '🌙' }
  ];

  const categoryOptions = [
    { id: 'supportive', label: 'Supportive', icon: '💙' },
    { id: 'creative', label: 'Creative', icon: '🎨' },
    { id: 'professional', label: 'Professional', icon: '💼' },
    { id: 'mindfulness', label: 'Mindfulness', icon: '🧘' },
    { id: 'adventure', label: 'Adventure', icon: '⚡' }
  ];

  async function handleCreate() {
    try {
      isCreating = true;
      error = null;

      // Construct character payload
      const characterData = {
        name: characterName,
        avatar: characterAvatar,
        description: characterDescription,
        personality: characterPersonality,
        background: characterBackground,
        language: primaryLanguage,
        conversationStyle,
        relationshipType,
        emotionalTone,
        category: selectedCategory
      };

      // TODO: POST to /api/characters with characterData
      console.log('Creating character:', characterData);
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      alert(`✨ Character "${characterName}" akan dibuat dengan:\n- Language: ${primaryLanguage}\n- Relationship: ${relationshipType}\n- Tone: ${emotionalTone}\n\n⚠️ Backend endpoint akan segera diimplementasikan!`);
      
      // Reset form
      resetForm();
      
    } catch (err) {
      error = err instanceof Error ? err.message : 'Gagal membuat character';
      console.error('Failed to create character:', err);
    } finally {
      isCreating = false;
    }
  }

  function resetForm() {
    characterName = '';
    characterAvatar = '🤖';
    characterDescription = '';
    characterPersonality = '';
    characterBackground = '';
    primaryLanguage = 'id';
    conversationStyle = 'friendly';
    relationshipType = 'friend';
    emotionalTone = 'warm';
    selectedCategory = 'supportive';
  }
</script>

<div class="h-full overflow-y-auto bg-gradient-to-b from-gray-50 to-white dark:from-slate-950 dark:to-slate-900 px-4 sm:px-6 py-8 pb-20">
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
    <div class="bg-white dark:bg-slate-800/50 rounded-3xl border border-gray-200 dark:border-slate-700 p-6 sm:p-8 space-y-8">
      
      {#if error}
        <!-- Error Alert -->
        <div class="flex items-center gap-3 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl">
          <AlertCircle size={20} class="text-red-600 dark:text-red-400 flex-shrink-0" />
          <p class="text-sm text-red-700 dark:text-red-300">{error}</p>
        </div>
      {/if}

      <!-- Section 1: Basic Identity -->
      <div class="space-y-6">
        <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-100 flex items-center gap-2">
          <span class="text-2xl">🎭</span> Basic Identity
        </h3>

        <!-- Avatar Selection -->
        <div>
          <label class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">
            Choose Avatar *
          </label>
          <div class="grid grid-cols-8 gap-2">
            {#each avatarOptions as avatar}
              <button
                type="button"
                onclick={() => characterAvatar = avatar}
                class="w-full aspect-square text-2xl rounded-xl border-2 transition-all {characterAvatar === avatar ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20 scale-110' : 'border-gray-200 dark:border-slate-700 hover:border-purple-300 dark:hover:border-purple-600'}"
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

        <!-- Description (Short) -->
        <div>
          <label for="description" class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">
            Short Description *
          </label>
          <input
            id="description"
            type="text"
            bind:value={characterDescription}
            placeholder="One-line tagline (e.g., 'Your creative companion')"
            class="w-full px-4 py-3 bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 outline-none transition-all"
          />
        </div>

        <!-- Category -->
        <div>
          <label class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">
            Category *
          </label>
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
            {#each categoryOptions as cat}
              <button
                type="button"
                onclick={() => selectedCategory = cat.id}
                class="flex items-center gap-2 p-3 rounded-xl border-2 transition-all {selectedCategory === cat.id ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20' : 'border-gray-200 dark:border-slate-700 hover:border-purple-300 dark:hover:border-purple-600'}"
              >
                <span class="text-xl">{cat.icon}</span>
                <span class="text-sm font-medium text-slate-700 dark:text-slate-300">{cat.label}</span>
              </button>
            {/each}
          </div>
        </div>
      </div>

      <!-- Divider -->
      <div class="border-t border-gray-200 dark:border-slate-700"></div>

      <!-- Section 2: Personality & Background -->
      <div class="space-y-6">
        <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-100 flex items-center gap-2">
          <span class="text-2xl">🧠</span> Personality & Background
        </h3>

        <!-- Personality (Traits) -->
        <div>
          <label for="personality" class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">
            Personality Traits *
          </label>
          <textarea
            id="personality"
            bind:value={characterPersonality}
            placeholder="e.g., Calm, empathetic, curious, loves deep conversations..."
            rows="3"
            class="w-full px-4 py-3 bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 outline-none transition-all resize-none"
          ></textarea>
        </div>

        <!-- Background (Lore) -->
        <div>
          <label for="background" class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">
            Background & Lore
          </label>
          <textarea
            id="background"
            bind:value={characterBackground}
            placeholder="Their story, profession, where they come from... (optional but makes them richer)"
            rows="3"
            class="w-full px-4 py-3 bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 outline-none transition-all resize-none"
          ></textarea>
        </div>
      </div>

      <!-- Divider -->
      <div class="border-t border-gray-200 dark:border-slate-700"></div>

      <!-- Section 3: Communication Style -->
      <div class="space-y-6">
        <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-100 flex items-center gap-2">
          <Globe size={24} />
          Communication Settings
        </h3>

        <!-- Primary Language -->
        <div>
          <label class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">
            Primary Language *
          </label>
          <div class="grid grid-cols-2 gap-3">
            {#each languageOptions as lang}
              <button
                type="button"
                onclick={() => primaryLanguage = lang.id}
                class="flex items-center gap-3 p-4 rounded-xl border-2 transition-all {primaryLanguage === lang.id ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20' : 'border-gray-200 dark:border-slate-700 hover:border-purple-300 dark:hover:border-purple-600'}"
              >
                <span class="text-2xl">{lang.flag}</span>
                <span class="text-sm font-medium text-slate-700 dark:text-slate-300">{lang.label}</span>
              </button>
            {/each}
          </div>
        </div>

        <!-- Conversation Style -->
        <div>
          <label class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">
            Conversation Style *
          </label>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {#each styleOptions as style}
              <button
                type="button"
                onclick={() => conversationStyle = style.id}
                class="flex items-center gap-3 p-4 rounded-xl border-2 transition-all text-left {conversationStyle === style.id ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20' : 'border-gray-200 dark:border-slate-700 hover:border-purple-300 dark:hover:border-purple-600'}"
              >
                <span class="text-2xl">{style.icon}</span>
                <span class="text-sm font-medium text-slate-700 dark:text-slate-300">{style.label}</span>
              </button>
            {/each}
          </div>
        </div>
      </div>

      <!-- Divider -->
      <div class="border-t border-gray-200 dark:border-slate-700"></div>

      <!-- Section 4: Relationship Dynamics -->
      <div class="space-y-6">
        <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-100 flex items-center gap-2">
          <Heart size={24} />
          Relationship Dynamics
        </h3>

        <!-- Relationship Type -->
        <div>
          <label class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">
            Relationship Type *
          </label>
          <div class="grid grid-cols-2 gap-3">
            {#each relationshipOptions as rel}
              <button
                type="button"
                onclick={() => relationshipType = rel.id}
                class="flex flex-col gap-1 p-4 rounded-xl border-2 transition-all text-left {relationshipType === rel.id ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20' : 'border-gray-200 dark:border-slate-700 hover:border-purple-300 dark:hover:border-purple-600'}"
              >
                <span class="text-sm font-semibold text-slate-900 dark:text-slate-100">{rel.label}</span>
                <span class="text-xs text-slate-500 dark:text-slate-400">{rel.description}</span>
              </button>
            {/each}
          </div>
        </div>

        <!-- Emotional Tone -->
        <div>
          <label class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">
            Emotional Tone *
          </label>
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {#each toneOptions as tone}
              <button
                type="button"
                onclick={() => emotionalTone = tone.id}
                class="flex items-center gap-2 p-3 rounded-xl border-2 transition-all {emotionalTone === tone.id ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20' : 'border-gray-200 dark:border-slate-700 hover:border-purple-300 dark:hover:border-purple-600'}"
              >
                <span class="text-xl">{tone.emoji}</span>
                <span class="text-sm font-medium text-slate-700 dark:text-slate-300">{tone.label}</span>
              </button>
            {/each}
          </div>
        </div>
      </div>

      <!-- Create Button -->
      <button
        onclick={handleCreate}
        disabled={!characterName.trim() || !characterDescription.trim() || !characterPersonality.trim() || isCreating}
        class="w-full py-4 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 disabled:from-slate-600 disabled:to-slate-600 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl disabled:shadow-none transition-all disabled:cursor-not-allowed flex items-center justify-center gap-2"
      >
        {#if isCreating}
          <div class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
          <span>Creating Character...</span>
        {:else}
          <Sparkles size={20} />
          <span>Create My Companion</span>
        {/if}
      </button>

      <!-- Note -->
      <p class="text-xs text-center text-slate-500 dark:text-slate-400">
        ⚠️ Form siap! Backend endpoint akan diimplementasikan sesuai design lengkap
      </p>
    </div>
  </div>
</div>
