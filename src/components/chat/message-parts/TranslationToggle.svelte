<script lang="ts">
  import { Globe } from '@lucide/svelte';
  import type { StructuredMessageContent } from '@lib/types/message';

  interface Props {
    structured?: StructuredMessageContent;
  }

  let { structured }: Props = $props();
  
  let showTranslation = $state(false);
  
  const hasTranslation = $derived(
    structured?.translation && 
    (structured.translation.dialogue || structured.translation.action || structured.translation.thought)
  );
</script>

{#if hasTranslation}
  <div class="mt-3 border-t border-slate-200 dark:border-slate-700 pt-2">
    <button
      onclick={() => showTranslation = !showTranslation}
      class="flex items-center gap-1.5 text-xs text-purple-600 dark:text-purple-400 hover:text-purple-700 dark:hover:text-purple-300 transition-colors"
    >
      <Globe size={14} />
      <span>{showTranslation ? 'Hide' : 'Show'} translation</span>
    </button>
    
    {#if showTranslation}
      <div class="mt-2 p-2.5 bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-800 rounded-lg space-y-1">
        {#if structured?.translation?.dialogue}
          <div class="text-sm text-purple-900 dark:text-purple-100">
            {structured.translation.dialogue}
          </div>
        {/if}
        
        {#if structured?.translation?.action}
          <div class="text-xs text-purple-700 dark:text-purple-300 italic">
            {structured.translation.action}
          </div>
        {/if}
        
        {#if structured?.translation?.thought}
          <div class="text-xs text-purple-600 dark:text-purple-400">
            ({structured.translation.thought})
          </div>
        {/if}
      </div>
    {/if}
  </div>
{/if}
