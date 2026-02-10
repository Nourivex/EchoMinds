<script lang="ts">
  import { onMount } from 'svelte';
  import type { Message, Character } from '@models/chat';
  import ChatMessage from '@components/ui/ChatMessage.svelte';
  import InputBar from './InputBar.svelte';

  interface Props {
    character?: Character | null;
  }

  let { character }: Props = $props();

  // Mock state menggunakan Svelte 5 Runes
  let messages = $state<Message[]>([]);

  let isAssistantTyping = $state(false);
  let chatContainerRef = $state<HTMLDivElement | null>(null);

  function scrollToBottom(smooth = true) {
    if (chatContainerRef) {
      chatContainerRef.scrollTo({
        top: chatContainerRef.scrollHeight,
        behavior: smooth ? 'smooth' : 'instant'
      });
    }
  }

  async function handleSendMessage(content: string) {
    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      role: 'user',
      timestamp: new Date()
    };
    
    messages = [...messages, userMessage];
    
    // Scroll after adding message
    setTimeout(() => scrollToBottom(), 50);

    // Simulate assistant typing
    isAssistantTyping = true;

    // Mock AI response delay
    await new Promise(resolve => setTimeout(resolve, 1500));

    const characterName = character?.name || 'EchoMinds';
    const assistantMessage: Message = {
      id: (Date.now() + 1).toString(),
      content: `Kamu bilang: "${content}". Ini adalah response mock dari ${characterName}.`,
      role: 'assistant',
      timestamp: new Date()
    };

    messages = [...messages, assistantMessage];
    isAssistantTyping = false;

    setTimeout(() => scrollToBottom(), 50);
  }

  onMount(() => {
    scrollToBottom(false);
  });

  // Watch messages length for auto-scroll
  $effect(() => {
    if (messages.length > 0) {
      setTimeout(() => scrollToBottom(), 100);
    }
  });

  // Reset messages when character changes
  $effect(() => {
    if (character) {
      const initialGreeting = character.greeting || 'Halo! Ada yang bisa kubantu?';
      messages = [
        {
          id: '1',
          content: initialGreeting,
          role: 'assistant',
          timestamp: new Date()
        }
      ];
      setTimeout(() => scrollToBottom(false), 100);
    }
  });
</script>

<div class="flex flex-col h-full bg-gradient-to-b from-gray-50 to-white dark:from-slate-950 dark:to-slate-900">
  <!-- Character Header Card - Candy.AI Style -->
  {#if character}
    <div class="px-4 py-4 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm border-b border-gray-200 dark:border-slate-800">
      <div class="flex items-center gap-4 max-w-4xl mx-auto">
        <!-- Character Avatar -->
        <div class="relative">
          <div class="w-14 h-14 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 p-0.5 shadow-lg">
            <div class="w-full h-full rounded-full bg-white dark:bg-slate-800 flex items-center justify-center text-3xl">
              {character.avatar}
            </div>
          </div>
          <div class="absolute bottom-0 right-0 w-4 h-4 bg-green-500 rounded-full border-2 border-white dark:border-slate-900"></div>
        </div>
        
        <!-- Character Info -->
        <div class="flex-1 min-w-0">
          <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-100">{character.name}</h3>
          <p class="text-sm text-slate-500 dark:text-slate-400 truncate">{character.description}</p>
        </div>
      </div>
    </div>
  {/if}

  <!-- Chat Messages Area -->
  <div
    bind:this={chatContainerRef}
    class="flex-1 overflow-y-auto px-3 sm:px-4 py-6 scroll-smooth"
  >
    <div class="max-w-4xl mx-auto space-y-6">
      {#each messages as message (message.id)}
        {#if message.role === 'assistant'}
          <!-- AI Message dengan Avatar (Candy.AI Style) -->
          <div class="flex gap-3 items-start animate-in fade-in slide-in-from-bottom-2 duration-300">
            <div class="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 p-0.5 shadow-md flex-shrink-0">
              <div class="w-full h-full rounded-full bg-white dark:bg-slate-800 flex items-center justify-center text-xl">
                {character?.avatar || '🤖'}
              </div>
            </div>
            
            <div class="flex-1 max-w-[85%] sm:max-w-[75%]">
              <div class="bg-white dark:bg-slate-800 rounded-2xl rounded-tl-sm px-4 py-3 shadow-sm border border-gray-100 dark:border-slate-700">
                {#if message.isTyping}
                  <div class="flex gap-1.5 py-1">
                    <span class="w-2 h-2 bg-slate-400 dark:bg-slate-500 rounded-full animate-bounce" style="animation-delay: 0ms;"></span>
                    <span class="w-2 h-2 bg-slate-400 dark:bg-slate-500 rounded-full animate-bounce" style="animation-delay: 150ms;"></span>
                    <span class="w-2 h-2 bg-slate-400 dark:bg-slate-500 rounded-full animate-bounce" style="animation-delay: 300ms;"></span>
                  </div>
                {:else}
                  <p class="text-[15px] leading-relaxed text-slate-800 dark:text-slate-100 whitespace-pre-wrap break-words">
                    {message.content}
                  </p>
                  <span class="text-xs text-slate-400 dark:text-slate-500 mt-1.5 block">
                    {message.timestamp.toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' })}
                  </span>
                {/if}
              </div>
            </div>
          </div>
        {:else}
          <!-- User Message -->
          <div class="flex justify-end animate-in fade-in slide-in-from-bottom-2 duration-300">
            <div class="max-w-[85%] sm:max-w-[75%]">
              <div class="bg-gradient-to-br from-purple-600 to-blue-600 text-white rounded-2xl rounded-br-sm px-4 py-3 shadow-md">
                <p class="text-[15px] leading-relaxed whitespace-pre-wrap break-words">
                  {message.content}
                </p>
                <span class="text-xs text-purple-100 mt-1.5 block text-right">
                  {message.timestamp.toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>
            </div>
          </div>
        {/if}
      {/each}

      {#if isAssistantTyping}
        <!-- Typing Indicator dengan Avatar -->
        <div class="flex gap-3 items-start">
          <div class="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 p-0.5 shadow-md flex-shrink-0">
            <div class="w-full h-full rounded-full bg-white dark:bg-slate-800 flex items-center justify-center text-xl">
              {character?.avatar || '🤖'}
            </div>
          </div>
          
          <div class="bg-white dark:bg-slate-800 rounded-2xl rounded-tl-sm px-4 py-3 shadow-sm border border-gray-100 dark:border-slate-700">
            <div class="flex gap-1.5 py-1">
              <span class="w-2 h-2 bg-slate-400 dark:bg-slate-500 rounded-full animate-bounce" style="animation-delay: 0ms;"></span>
              <span class="w-2 h-2 bg-slate-400 dark:bg-slate-500 rounded-full animate-bounce" style="animation-delay: 150ms;"></span>
              <span class="w-2 h-2 bg-slate-400 dark:bg-slate-500 rounded-full animate-bounce" style="animation-delay: 300ms;"></span>
            </div>
          </div>
        </div>
      {/if}
    </div>
  </div>

  <!-- Input Bar (Sticky Bottom) -->
  <InputBar onSend={handleSendMessage} disabled={isAssistantTyping} characterName={character?.name} />
</div>
