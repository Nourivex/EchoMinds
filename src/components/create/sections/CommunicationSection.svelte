<script lang="ts">
  import { Globe } from '@lucide/svelte';
  import { updateCommunication, companionForm } from '@stores/companionForm';
  import OptionCard from '../ui/OptionCard.svelte';
  
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

  let form = $companionForm.communication;
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
          selected={form.language === lang.id}
          onclick={() => updateCommunication({ language: lang.id })}
        />
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
        <OptionCard
          label={style.label}
          emoji={style.icon}
          selected={form.style === style.id}
          onclick={() => updateCommunication({ style: style.id })}
        />
      {/each}
    </div>
  </div>
</div>
