<script lang="ts">
  import { Copy, RotateCw, Trash2 } from '@lucide/svelte';
  
  interface Props {
    messageId: string;
    content: string;
    onCopy?: () => void;
    onRegenerate?: () => void;
    onDelete?: () => void;
    isAssistant?: boolean;
  }
  
  let { messageId, content, onCopy, onRegenerate, onDelete, isAssistant = false }: Props = $props();
  
  let copySuccess = $state(false);
  
  function handleCopy() {
    navigator.clipboard.writeText(content);
    copySuccess = true;
    onCopy?.();
    setTimeout(() => copySuccess = false, 2000);
  }
  
  function handleRegenerate() {
    onRegenerate?.();
  }
  
  function handleDelete() {
    onDelete?.();
  }
</script>

<div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
  <!-- Copy Button -->
  <button
    type="button"
    onclick={handleCopy}
    class="p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-200"
    title={copySuccess ? 'Copied!' : 'Copy message'}
  >
    {#if copySuccess}
      <svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
      </svg>
    {:else}
      <Copy size={16} />
    {/if}
  </button>
  
  <!-- Regenerate Button (only for assistant messages) -->
  {#if isAssistant && onRegenerate}
    <button
      type="button"
      onclick={handleRegenerate}
      class="p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors text-slate-500 dark:text-slate-400 hover:text-purple-600 dark:hover:text-purple-400"
      title="Regenerate response"
    >
      <RotateCw size={16} />
    </button>
  {/if}
  
  <!-- Delete Button -->
  {#if onDelete}
    <button
      type="button"
      onclick={handleDelete}
      class="p-1.5 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors text-slate-500 dark:text-slate-400 hover:text-red-600 dark:hover:text-red-400"
      title="Delete message"
    >
      <Trash2 size={16} />
    </button>
  {/if}
</div>
