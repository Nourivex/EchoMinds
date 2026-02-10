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

<div class="flex flex-col h-full bg-slate-900">
  <!-- Chat Messages Area -->
  <div
    bind:this={chatContainerRef}
    class="flex-1 overflow-y-auto px-4 py-6 space-y-2 scroll-smooth"
  >
    {#each messages as message (message.id)}
      <ChatMessage {message} />
    {/each}

    {#if isAssistantTyping}
      <ChatMessage 
        message={{
          id: 'typing',
          content: '',
          role: 'assistant',
          timestamp: new Date(),
          isTyping: true
        }} 
      />
    {/if}
  </div>

  <!-- Input Bar (Sticky Bottom) -->
  <InputBar onSend={handleSendMessage} disabled={isAssistantTyping} />
</div>
