<script lang="ts">
  import SendIcon from '@components/ui/icons/Send.svelte';

  interface Props {
    onSend: (message: string) => void;
    disabled?: boolean;
  }

  let { onSend, disabled = false }: Props = $props();

  let inputValue = $state('');
  let textareaRef = $state<HTMLTextAreaElement | null>(null);

  function handleSubmit(e: Event) {
    e.preventDefault();
    const trimmed = inputValue.trim();
    if (trimmed && !disabled) {
      onSend(trimmed);
      inputValue = '';
      // Reset textarea height
      if (textareaRef) {
        textareaRef.style.height = 'auto';
      }
    }
  }

  function handleInput() {
    // Auto-resize textarea
    if (textareaRef) {
      textareaRef.style.height = 'auto';
      textareaRef.style.height = `${Math.min(textareaRef.scrollHeight, 120)}px`;
    }
  }

  function handleKeyDown(e: KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  }
</script>

<form
  onsubmit={handleSubmit}
  class="sticky bottom-0 left-0 right-0 bg-slate-900 border-t border-slate-700 px-4 py-3 safe-area-inset"
>
  <div class="flex items-end gap-2 max-w-4xl mx-auto">
    <textarea
      bind:this={textareaRef}
      bind:value={inputValue}
      oninput={handleInput}
      onkeydown={handleKeyDown}
      placeholder="Ketik pesan..."
      rows="1"
      class="flex-1 bg-slate-800 text-slate-100 rounded-2xl px-4 py-3 resize-none outline-none focus:ring-2 focus:ring-blue-500 placeholder-slate-500 max-h-[120px] overflow-y-auto"
      {disabled}
    ></textarea>
    
    <button
      type="submit"
      disabled={disabled || !inputValue.trim()}
      class="flex-shrink-0 w-12 h-12 rounded-full bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 disabled:cursor-not-allowed flex items-center justify-center transition-colors"
      aria-label="Kirim pesan"
    >
      <SendIcon size={20} class="text-white" />
    </button>
  </div>
</form>
