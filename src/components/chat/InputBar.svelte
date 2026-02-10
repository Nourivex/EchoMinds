<script lang="ts">
  import { Send, Paperclip, Smile } from '@lucide/svelte';

  interface Props {
    onSend: (message: string) => void;
    disabled?: boolean;
    characterName?: string;
  }

  let { onSend, disabled = false, characterName = 'AI' }: Props = $props();

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
  class="sticky bottom-0 left-0 right-0 bg-white/95 dark:bg-slate-900/95 backdrop-blur-sm border-t border-gray-200 dark:border-slate-800 px-3 sm:px-4 py-3 sm:py-4"
>
  <div class="max-w-4xl mx-auto">
    <div class="flex items-end gap-2 bg-gray-50 dark:bg-slate-800/50 rounded-2xl p-2 border border-gray-200 dark:border-slate-700 focus-within:ring-2 focus-within:ring-purple-500/50 focus-within:border-purple-500 dark:focus-within:border-purple-500 transition-all">
      <!-- Action Buttons Left -->
      <div class="flex items-center gap-1 pb-2">
        <button
          type="button"
          class="p-1.5 hover:bg-gray-200 dark:hover:bg-slate-700 rounded-lg text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300 transition-colors"
          title="Attach file"
        >
          <Paperclip size={18} />
        </button>
        <button
          type="button"
          class="p-1.5 hover:bg-gray-200 dark:hover:bg-slate-700 rounded-lg text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300 transition-colors"
          title="Add emoji"
        >
          <Smile size={18} />
        </button>
      </div>

      <!-- Textarea -->
      <textarea
        bind:this={textareaRef}
        bind:value={inputValue}
        oninput={handleInput}
        onkeydown={handleKeyDown}
        placeholder={`Message ${characterName}...`}
        rows="1"
        class="flex-1 bg-transparent text-slate-900 dark:text-slate-100 px-2 py-2 resize-none outline-none placeholder-slate-400 dark:placeholder-slate-500 max-h-[120px] overflow-y-auto"
        {disabled}
      ></textarea>
      
      <!-- Send Button -->
      <button
        type="submit"
        disabled={disabled || !inputValue.trim()}
        class="flex-shrink-0 w-10 h-10 sm:w-11 sm:h-11 rounded-xl bg-gradient-to-br from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 disabled:from-slate-600 disabled:to-slate-600 disabled:cursor-not-allowed flex items-center justify-center transition-all hover:scale-105 active:scale-95 shadow-lg disabled:shadow-none"
        aria-label="Send message"
      >
        <Send size={18} class="text-white" />
      </button>
    </div>
  </div>
</form>
