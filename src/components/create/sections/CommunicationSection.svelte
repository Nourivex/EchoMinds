<script lang="ts">
  import { Globe } from '@lucide/svelte';
  import { updateCommunication, companionForm } from '@stores/companionForm';
  import OptionCard from '../ui/OptionCard.svelte';
  
  const languageOptions = [
    { id: 'id', label: 'Bahasa Indonesia', flag: '🇮🇩' },
    { id: 'en', label: 'English', flag: '🇺🇸' }
  ];

  const styleOptions = [
    // Friendly & Casual
    { id: 'friendly', label: 'Friendly & Warm', icon: '😊', category: 'casual' },
    { id: 'playful', label: 'Playful & Fun', icon: '🎮', category: 'casual' },
    { id: 'teasing', label: 'Teasing & Flirty', icon: '😏', category: 'casual' },
    { id: 'cute', label: 'Cute & Adorable', icon: '🥰', category: 'casual' },
    { id: 'energetic', label: 'Energetic & Bubbly', icon: '✨', category: 'casual' },
    
    // Intimate & Romantic
    { id: 'romantic', label: 'Romantic & Sweet', icon: '💕', category: 'intimate' },
    { id: 'seductive', label: 'Seductive & Alluring', icon: '🌹', category: 'intimate' },
    { id: 'dominant', label: 'Dominant & Assertive', icon: '👑', category: 'intimate' },
    { id: 'submissive', label: 'Submissive & Obedient', icon: '🎀', category: 'intimate' },
    { id: 'sensual', label: 'Sensual & Passionate', icon: '🔥', category: 'intimate' },
    
    // Intelligent & Formal
    { id: 'professional', label: 'Professional', icon: '💼', category: 'formal' },
    { id: 'wise', label: 'Wise & Calm', icon: '🧘', category: 'formal' },
    { id: 'intellectual', label: 'Intellectual', icon: '📚', category: 'formal' },
    { id: 'mentor', label: 'Mentoring & Guiding', icon: '🎓', category: 'formal' },
    
    // Unique Personalities
    { id: 'mysterious', label: 'Mysterious', icon: '🎭', category: 'unique' },
    { id: 'tsundere', label: 'Tsundere', icon: '😤', category: 'unique' },
    { id: 'yandere', label: 'Yandere', icon: '🔪', category: 'unique' },
    { id: 'kuudere', label: 'Kuudere (Cool)', icon: '❄️', category: 'unique' },
    { id: 'dandere', label: 'Dandere (Shy)', icon: '🌸', category: 'unique' },
    
    // Dark & Edge
    { id: 'sadistic', label: 'Sadistic', icon: '😈', category: 'dark' },
    { id: 'possessive', label: 'Possessive', icon: '⛓️', category: 'dark' },
    { id: 'manipulative', label: 'Manipulative', icon: '🎭', category: 'dark' },
    
    // Other
    { id: 'sarcastic', label: 'Sarcastic & Witty', icon: '😎', category: 'other' },
    { id: 'caring', label: 'Caring & Nurturing', icon: '🤗', category: 'other' },
    { id: 'shy', label: 'Shy & Reserved', icon: '😳', category: 'other' }
  ];

  // Helper function to toggle style selection (max 3)
  function toggleStyle(styleId: string) {
    const currentStyles = $companionForm.communication.styles;
    
    if (currentStyles.includes(styleId)) {
      // Remove if already selected
      updateCommunication({ styles: currentStyles.filter(s => s !== styleId) });
    } else if (currentStyles.length < 3) {
      // Add if under limit
      updateCommunication({ styles: [...currentStyles, styleId] });
    }
    // Ignore if already at max (3)
  }
</script>

<div class="space-y-6">
  <div class="text-center mb-6">
    <h2 class="text-2xl font-bold text-slate-900 dark:text-slate-100 mb-2 flex items-center justify-center gap-2">
      <Globe size={28} />
      Communication Settings
    </h2>
    <p class="text-sm text-slate-600 dark:text-slate-400">
      Bahasa dan gaya komunikasi karakter
    </p>
  </div>

  <!-- Primary Language -->
  <div>
    <label class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">
      Primary Language *
    </label>
    <div class="grid grid-cols-2 gap-3">
      {#each languageOptions as lang}
        <OptionCard
          label={lang.label}
          emoji={lang.flag}
          selected={$companionForm.communication.language === lang.id}
          onclick={() => updateCommunication({ language: lang.id })}
        />
      {/each}
    </div>
  </div>

  <!-- Conversation Style -->
  <div>
    <div class="flex items-center justify-between mb-3">
      <label class="block text-sm font-semibold text-slate-700 dark:text-slate-300">
        Conversation Styles * <span class="text-xs text-slate-500">(Pilih 1-3)</span>
      </label>
      <div class="text-xs font-medium text-purple-600 dark:text-purple-400">
        {$companionForm.communication.styles.length} / 3 selected
      </div>
    </div>
    
    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2">
      {#each styleOptions as style}
        <button
          type="button"
          onclick={() => toggleStyle(style.id)}
          disabled={!$companionForm.communication.styles.includes(style.id) && $companionForm.communication.styles.length >= 3}
          class="flex flex-col items-center gap-1 p-2.5 rounded-lg border-2 transition-all text-center {
            $companionForm.communication.styles.includes(style.id)
              ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20 shadow-md'
              : 'border-gray-200 dark:border-slate-700 hover:border-purple-300 disabled:opacity-40 disabled:cursor-not-allowed'
          }"
        >
          <span class="text-xl">{style.icon}</span>
          <span class="text-xs font-medium text-slate-700 dark:text-slate-300 leading-tight">{style.label}</span>
          {#if $companionForm.communication.styles.includes(style.id)}
            <svg class="w-4 h-4 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
          {/if}
        </button>
      {/each}
    </div>
    
    <p class="text-xs text-slate-500 dark:text-slate-400 mt-3">
      💡 Kombinasi style menciptakan personality yang unik. Misalnya: Friendly + Teasing + Playful = Cheerful teman yang suka bercanda
    </p>
  </div>
</div>
