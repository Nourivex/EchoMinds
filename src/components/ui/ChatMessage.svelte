<script lang="ts">
  import type { Message } from '@models/chat';
  import { cn } from '@lib/utils/cn';

  interface Props {
    message: Message;
  }

  let { message }: Props = $props();

  const isUser = $derived(message.role === 'user');
  const formattedTime = $derived(
    message.timestamp.toLocaleTimeString('id-ID', {
      hour: '2-digit',
      minute: '2-digit'
    })
  );
</script>

<div
  class={cn(
    'flex w-full mb-4 animate-in fade-in slide-in-from-bottom-2 duration-300',
    isUser ? 'justify-end' : 'justify-start'
  )}
>
  <div
    class={cn(
      'max-w-[85%] sm:max-w-[70%] rounded-2xl px-4 py-3 shadow-sm',
      isUser
        ? 'bg-blue-600 text-white rounded-br-md'
        : 'bg-slate-800 text-slate-100 rounded-bl-md'
    )}
  >
    {#if message.isTyping}
      <div class="flex gap-1 py-1">
        <span class="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style="animation-delay: 0ms;"></span>
        <span class="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style="animation-delay: 150ms;"></span>
        <span class="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style="animation-delay: 300ms;"></span>
      </div>
    {:else}
      <p class="text-[15px] leading-relaxed whitespace-pre-wrap break-words">
        {message.content}
      </p>
      <span class={cn(
        'text-xs mt-1 block',
        isUser ? 'text-blue-100' : 'text-slate-400'
      )}>
        {formattedTime}
      </span>
    {/if}
  </div>
</div>
