<script lang="ts">
  interface Props {
    label: string;
    description?: string;
    icon?: string;
    emoji?: string;
    selected: boolean;
    onclick?: () => void;
  }

  let { label, description, icon, emoji, selected, onclick }: Props = $props();
</script>

<button
  type="button"
  {onclick}
  class="flex items-center gap-3 p-4 rounded-xl border-2 transition-all text-left w-full {
    selected
      ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20 shadow-md'
      : 'border-gray-200 dark:border-slate-700 hover:border-purple-300 dark:hover:border-purple-600 hover:shadow-sm'
  }"
>
  {#if emoji}
    <span class="text-2xl flex-shrink-0">{emoji}</span>
  {/if}
  {#if icon}
    <span class="text-xl flex-shrink-0">{icon}</span>
  {/if}
  <div class="flex-1 min-w-0">
    <div class="text-sm font-semibold text-slate-900 dark:text-slate-100">{label}</div>
    {#if description}
      <div class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">{description}</div>
    {/if}
  </div>
  {#if selected}
    <svg class="w-5 h-5 text-purple-600 dark:text-purple-400 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
    </svg>
  {/if}
</button>
