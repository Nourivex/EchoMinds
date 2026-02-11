<script lang="ts">
  import { onMount } from 'svelte';
  import type { Character } from '@models/chat';
  import type { Message } from '@lib/types/message';
  import ChatMessage from '@components/ui/ChatMessage.svelte';
  import InputBar from './InputBar.svelte';
  import MessageActions from './MessageActions.svelte';
  import ActionPart from './message-parts/ActionPart.svelte';
  import DialoguePart from './message-parts/DialoguePart.svelte';
  import ThoughtPart from './message-parts/ThoughtPart.svelte';
  import TranslationToggle from './message-parts/TranslationToggle.svelte';
  import { sendMessage, APIError } from '@services/api';

  interface Props {
    character?: Character | null;
  }

  let { character }: Props = $props();

  // State menggunakan Svelte 5 Runes
  let messages = $state<Message[]>([]);
  let conversationId = $state<string | undefined>(undefined);
  let isAssistantTyping = $state(false);
  let chatContainerRef = $state<HTMLDivElement | null>(null);
  let errorMessage = $state<string | null>(null);

  function scrollToBottom(smooth = true) {
    if (chatContainerRef) {
      chatContainerRef.scrollTo({
        top: chatContainerRef.scrollHeight,
        behavior: smooth ? 'smooth' : 'instant'
      });
    }
  }

  async function handleSendMessage(content: string) {
    if (!character) {
      errorMessage = 'Please select a character first';
      setTimeout(() => errorMessage = null, 3000);
      return;
    }

    // Clear previous error
    errorMessage = null;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      role: 'user',
      timestamp: new Date()
    };
    
    messages = [...messages, userMessage];
    setTimeout(() => scrollToBottom(), 50);

    // Show typing indicator
    isAssistantTyping = true;

    try {
      // Call backend API
      const response = await sendMessage(
        content,
        'lycus', // TODO: Get from user auth
        character.id,
        conversationId
      );

      // Store conversation ID
      if (!conversationId) {
        conversationId = response.conversationId;
      }

      // Add assistant response with structured content
      const assistantMessage: Message = {
        id: response.conversationId + '_' + Date.now(),
        content: response.reply,
        role: 'assistant',
        timestamp: new Date(),
        structured: response.structured  // Include structured content
      };

      messages = [...messages, assistantMessage];
      setTimeout(() => scrollToBottom(), 50);

    } catch (error) {
      console.error('Failed to send message:', error);
      
      // Show user-friendly error
      if (error instanceof APIError) {
        errorMessage = `Failed to get response: ${error.message}`;
      } else {
        errorMessage = 'Connection error. Please check if backend is running.';
      }

      // Add error message to chat
      const errorMsg: Message = {
        id: 'error_' + Date.now(),
        content: '❌ Sorry, I encountered an error. Please try again.',
        role: 'assistant',
        timestamp: new Date()
      };
      messages = [...messages, errorMsg];

      // Clear error after 5 seconds
      setTimeout(() => errorMessage = null, 5000);
    } finally {
      isAssistantTyping = false;
    }
  }

  function handleDeleteMessage(messageId: string) {
    messages = messages.filter(m => m.id !== messageId);
  }

  async function handleRegenerateResponse(messageId: string) {
    // Find the message to regenerate
    const messageIndex = messages.findIndex(m => m.id === messageId);
    if (messageIndex === -1 || messageIndex === 0) return;
    
    // Get the user message before this assistant message
    const userMessage = messages[messageIndex - 1];
    if (!userMessage || userMessage.role !== 'user') return;
    
    // Remove the old assistant message
    messages = messages.slice(0, messageIndex);
    
    // Regenerate
    isAssistantTyping = true;
    
    try {
      const response = await sendMessage(
        userMessage.content,
        'lycus',
        character!.id,
        conversationId
      );
      
      const newAssistantMessage: Message = {
        id: response.conversationId + '_' + Date.now(),
        content: response.reply,
        role: 'assistant',
        timestamp: new Date()
      };
      
      messages = [...messages, newAssistantMessage];
      setTimeout(() => scrollToBottom(), 50);
    } catch (error) {
      console.error('Failed to regenerate:', error);
      errorMessage = 'Failed to regenerate response';
      setTimeout(() => errorMessage = null, 3000);
    } finally {
      isAssistantTyping = false;
    }
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
      // Reset conversation ID on character change
      conversationId = undefined;
      errorMessage = null;
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
          <div class="flex gap-3 items-start animate-in fade-in slide-in-from-bottom-2 duration-300 group">
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
                  <!-- Render structured message if available -->
                  {#if message.structured && (message.structured.dialogue || message.structured.action || message.structured.thought)}
                    <div class="space-y-2">
                      {#if message.structured.action}
                        <ActionPart text={message.structured.action} />
                      {/if}
                      
                      {#if message.structured.dialogue}
                        <DialoguePart text={message.structured.dialogue} />
                      {/if}
                      
                      {#if message.structured.thought}
                        <ThoughtPart text={message.structured.thought} />
                      {/if}
                      
                      <!-- Translation toggle -->
                      <TranslationToggle structured={message.structured} />
                    </div>
                  {:else}
                    <!-- Fallback to raw content -->
                    <p class="text-[15px] leading-relaxed text-slate-800 dark:text-slate-100 whitespace-pre-wrap break-words">
                      {message.content}
                    </p>
                  {/if}
                  
                  <div class="flex items-center justify-between gap-2 mt-2">
                    <span class="text-xs text-slate-400 dark:text-slate-500" title={message.timestamp.toLocaleString('id-ID')}>
                      {message.timestamp.toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' })}
                    </span>
                    <MessageActions
                      messageId={message.id}
                      content={message.content}
                      isAssistant={true}
                      onRegenerate={() => handleRegenerateResponse(message.id)}
                      onDelete={() => handleDeleteMessage(message.id)}
                    />
                  </div>
                {/if}
              </div>
            </div>
          </div>
        {:else}
          <!-- User Message -->
          <div class="flex justify-end animate-in fade-in slide-in-from-bottom-2 duration-300 group">
            <div class="max-w-[85%] sm:max-w-[75%]">
              <div class="bg-gradient-to-br from-purple-600 to-blue-600 text-white rounded-2xl rounded-br-sm px-4 py-3 shadow-md">
                <p class="text-[15px] leading-relaxed whitespace-pre-wrap break-words">
                  {message.content}
                </p>
                <div class="flex items-center justify-between gap-2 mt-2">
                  <span class="text-xs text-purple-100" title={message.timestamp.toLocaleString('id-ID')}>
                    {message.timestamp.toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' })}
                  </span>
                  <div class="opacity-80">
                    <MessageActions
                      messageId={message.id}
                      content={message.content}
                      isAssistant={false}
                      onDelete={() => handleDeleteMessage(message.id)}
                    />
                  </div>
                </div>
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

  <!-- Error Toast Notification -->
  {#if errorMessage}
    <div class="absolute bottom-20 left-1/2 transform -translate-x-1/2 bg-red-500 text-white px-4 py-2 rounded-lg shadow-lg animate-in fade-in slide-in-from-bottom-4 duration-300 z-50">
      <p class="text-sm font-medium">{errorMessage}</p>
    </div>
  {/if}
</div>
