<script lang="ts">
  import { Sparkles, Wand2, AlertCircle, Globe, Heart, MessageCircle } from '@lucide/svelte';
  import { router } from '@stores/router';
  import { createCharacter } from '@services/api';

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
  let relationshipType = $state('friend'); // friend | partner | mentor | custom
  let relationshipRole = $state('equal'); // kakak | adik | senior | junior | equal | custom
  let customRole = $state(''); // For custom role
  let relationshipLabel = $state(''); // Custom label (e.g., "kakak angkat", "teman masa kecil")
  let customRelationship = $state(''); // For custom relationship type
  let emotionalTone = $state('warm'); // warm | neutral | playful | mysterious
  
  // User identity awareness (CRITICAL for relationship context)
  let userName = $state(''); // How character addresses user (e.g., "Lycus", "Kak Lycus")
  let preferredAddress = $state('kamu'); // kamu | mas | mbak | sayang | kakak | adik
  
  // Relative positioning
  let ageRelation = $state('same'); // older | younger | same
  let authorityLevel = $state('equal'); // higher | equal | lower
  
  // Category
  let selectedCategory = $state('supportive');
  
  // UI State
  let isCreating = $state(false);
  let error = $state<string | null>(null);
  let backendAvailable = $state(false);
  let successMessage = $state<string | null>(null);

  // Check if backend character creation endpoint is available
  async function checkBackendAvailability() {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/characters`, {
        method: 'OPTIONS'
      });
      backendAvailable = response.ok || response.status === 405; // 405 means endpoint exists but POST not implemented yet
    } catch {
      backendAvailable = false;
    }
  }

  // Check on mount
  $effect(() => {
    checkBackendAvailability();
  });

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
    { id: 'rival', label: 'Rival', description: 'Competitive edge' },
    { id: 'custom', label: 'Custom', description: 'Define your own' }
  ];
  
  const roleOptions = [
    { id: 'kakak', label: 'Kakak (Older Sibling)', desc: 'Protective, responsible' },
    { id: 'adik', label: 'Adik (Younger Sibling)', desc: 'Playful, looks up to you' },
    { id: 'senior', label: 'Senior', desc: 'Experienced, mentoring' },
    { id: 'junior', label: 'Junior', desc: 'Learning, respectful' },
    { id: 'equal', label: 'Equal', desc: 'Same level, balanced' },
    { id: 'custom', label: 'Custom', desc: 'Your own dynamic' }
  ];
  
  const addressOptions = [
    { id: 'kamu', label: 'Kamu', context: 'Casual, equal' },
    { id: 'mas', label: 'Mas', context: 'Respectful (male)' },
    { id: 'mbak', label: 'Mbak', context: 'Respectful (female)' },
    { id: 'kakak', label: 'Kakak', context: 'Older sibling' },
    { id: 'adik', label: 'Adik', context: 'Younger sibling' },
    { id: 'sayang', label: 'Sayang', context: 'Endearing/romantic' }
  ];
  
  const ageOptions = [
    { id: 'older', label: 'Older', desc: 'More experienced, mature' },
    { id: 'younger', label: 'Younger', desc: 'Youthful, energetic' },
    { id: 'same', label: 'Same Age', desc: 'Equal generation' }
  ];
  
  const authorityOptions = [
    { id: 'higher', label: 'Higher', desc: 'Commands respect, guides you' },
    { id: 'equal', label: 'Equal', desc: 'Balanced, mutual respect' },
    { id: 'lower', label: 'Lower', desc: 'Looks up to you, seeks advice' }
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
      successMessage = null;

      // Construct character payload with all advanced fields
      const characterData = {
        name: characterName,
        avatar: characterAvatar,
        description: characterDescription,
        personality: characterPersonality,
        background: characterBackground,
        language: primaryLanguage,
        conversationStyle,
        relationshipType: relationshipType === 'custom' ? customRelationship : relationshipType,
        relationshipRole: relationshipRole === 'custom' ? customRole : relationshipRole,
        relationshipLabel,
        userName: userName || characterName, // Fallback to characterName
        preferredAddress,
        ageRelation,
        authorityLevel,
        emotionalTone,
        category: selectedCategory
      };

      // Call backend API to create character
      const createdCharacter = await createCharacter(characterData);
      
      successMessage = `✨ ${createdCharacter.name} has been created successfully!`;
      
      // Reset form after 3 seconds
      setTimeout(() => {
        resetForm();
        successMessage = null;
      }, 3000);
      
    } catch (err) {
      if (err instanceof Error) {
        error = err.message;
      } else {
        error = 'Gagal membuat character. Coba lagi.';
      }
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
    relationshipRole = 'equal';
    customRole = '';
    relationshipLabel = '';
    customRelationship = '';
    userName = '';
    preferredAddress = 'kamu';
    ageRelation = 'same';
    authorityLevel = 'equal';
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
      
      {#if successMessage}
        <!-- Success Alert -->
        <div class="flex items-center gap-3 p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-xl animate-fade-in">
          <Sparkles size={20} class="text-green-600 dark:text-green-400 flex-shrink-0" />
          <p class="text-sm text-green-700 dark:text-green-300 font-medium">{successMessage}</p>
        </div>
      {/if}

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
          <div class="grid grid-cols-2 gap-3 mb-3">
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
          
          {#if relationshipType === 'custom'}
            <div class="bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-800 rounded-xl p-4 space-y-3">
              <p class="text-xs text-slate-600 dark:text-slate-400">
                💡 <strong>Tip:</strong> Jelaskan hubungan yang kamu inginkan, misalnya: "Childhood best friend", "Mysterious ally", "Caring sibling", dll.
              </p>
              <input
                type="text"
                bind:value={customRelationship}
                placeholder="e.g., Childhood best friend, Mysterious ally..."
                class="w-full px-4 py-3 bg-white dark:bg-slate-900 border border-purple-300 dark:border-purple-700 rounded-lg text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 outline-none transition-all"
              />
            </div>
          {/if}
        </div>

        <!-- User Identity (NEW - Critical for context) -->
        <div class="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/10 dark:to-purple-900/10 border border-blue-200 dark:border-blue-800 rounded-xl p-5 space-y-4">
          <div class="flex items-start gap-3">
            <span class="text-2xl">👤</span>
            <div class="flex-1">
              <h4 class="text-sm font-bold text-slate-900 dark:text-slate-100 mb-1">User Identity Awareness</h4>
              <p class="text-xs text-slate-600 dark:text-slate-400 mb-4">
                Biar character tahu siapa kamu baginya — ini <strong>penting banget</strong> supaya percakapan lebih personal!
              </p>
              
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <!-- User Name -->
                <div>
                  <label for="userName" class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-2">
                    Nama Kamu (Untuk Character) *
                  </label>
                  <input
                    type="text"
                    id="userName"
                    bind:value={userName}
                    placeholder="e.g., Lycus, Kak Budi, Sarah"
                    class="w-full px-3 py-2 bg-white dark:bg-slate-900 border border-blue-300 dark:border-blue-700 rounded-lg text-sm text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                  />
                </div>
                
                <!-- Preferred Address -->
                <div>
                  <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-2">
                    Cara Panggil Kamu *
                  </label>
                  <select
                    bind:value={preferredAddress}
                    class="w-full px-3 py-2 bg-white dark:bg-slate-900 border border-blue-300 dark:border-blue-700 rounded-lg text-sm text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                  >
                    {#each addressOptions as addr}
                      <option value={addr.id}>{addr.label} ({addr.context})</option>
                    {/each}
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Relationship Role (NEW) -->
        <div>
          <label class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">
            Social Role (Hubungan Sosial) *
          </label>
          <div class="grid grid-cols-2 gap-3 mb-3">
            {#each roleOptions as role}
              <button
                type="button"
                onclick={() => relationshipRole = role.id}
                class="flex flex-col gap-1 p-3 rounded-xl border-2 transition-all text-left {relationshipRole === role.id ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20' : 'border-gray-200 dark:border-slate-700 hover:border-purple-300 dark:hover:border-purple-600'}"
              >
                <span class="text-sm font-semibold text-slate-900 dark:text-slate-100">{role.label}</span>
                <span class="text-xs text-slate-500 dark:text-slate-400">{role.desc}</span>
              </button>
            {/each}
          </div>
          
          {#if relationshipRole === 'custom'}
            <input
              type="text"
              bind:value={customRole}
              placeholder="e.g., Sepupu, Guru privat, Tetangga dekat..."
              class="w-full px-4 py-3 bg-white dark:bg-slate-900 border border-purple-300 dark:border-purple-700 rounded-lg text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 outline-none transition-all"
            />
          {/if}
        </div>

        <!-- Relationship Label (NEW - Optional) -->
        <div>
          <label for="relationshipLabel" class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">
            Relationship Label <span class="text-xs text-slate-500">(Opsional)</span>
          </label>
          <input
            type="text"
            id="relationshipLabel"
            bind:value={relationshipLabel}
            placeholder="e.g., 'adik kandung', 'sahabat sejak kecil', 'mantan kekasih'"
            class="w-full px-4 py-3 bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 outline-none transition-all"
          />
          <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Nama spesifik untuk hubungan kalian (misal: "adik kandung" bukan cuma "adik")
          </p>
        </div>

        <!-- Age & Authority (NEW - Side by side) -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <!-- Age Relation -->
          <div>
            <label class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">
              Age Relation *
            </label>
            <div class="space-y-2">
              {#each ageOptions as age}
                <button
                  type="button"
                  onclick={() => ageRelation = age.id}
                  class="w-full flex flex-col gap-1 p-3 rounded-lg border-2 transition-all text-left {ageRelation === age.id ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20' : 'border-gray-200 dark:border-slate-700 hover:border-purple-300 dark:hover:border-purple-600'}"
                >
                  <span class="text-sm font-semibold text-slate-900 dark:text-slate-100">{age.label}</span>
                  <span class="text-xs text-slate-500 dark:text-slate-400">{age.desc}</span>
                </button>
              {/each}
            </div>
          </div>
          
          <!-- Authority Level -->
          <div>
            <label class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">
              Authority Level *
            </label>
            <div class="space-y-2">
              {#each authorityOptions as auth}
                <button
                  type="button"
                  onclick={() => authorityLevel = auth.id}
                  class="w-full flex flex-col gap-1 p-3 rounded-lg border-2 transition-all text-left {authorityLevel === auth.id ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20' : 'border-gray-200 dark:border-slate-700 hover:border-purple-300 dark:hover:border-purple-600'}"
                >
                  <span class="text-sm font-semibold text-slate-900 dark:text-slate-100">{auth.label}</span>
                  <span class="text-xs text-slate-500 dark:text-slate-400">{auth.desc}</span>
                </button>
              {/each}
            </div>
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
        disabled={!characterName.trim() || !characterDescription.trim() || !characterPersonality.trim() || !userName.trim() || (relationshipType === 'custom' && !customRelationship.trim()) || (relationshipRole === 'custom' && !customRole.trim()) || isCreating}
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

      <!-- Smart Status Note -->
      {#if !backendAvailable}
        <p class="text-xs text-center text-slate-500 dark:text-slate-400">
          ⚠️ Backend endpoint sedang dalam development. Form siap digunakan saat backend aktif.
        </p>
      {:else}
        <p class="text-xs text-center text-green-600 dark:text-green-400">
          ✅ Connected to backend • Ready to create characters
        </p>
      {/if}
    </div>
  </div>
</div>
