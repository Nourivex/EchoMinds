<script lang="ts">
  import type { Character } from '@models/chat';
  import UsersIcon from '@components/ui/icons/Users.svelte';

  interface Props {
    character: Character;
    onclick?: () => void;
  }

  let { character, onclick }: Props = $props();

  function formatChatCount(count?: number): string {
    if (!count) return '0';
    if (count >= 1000000) return `${(count / 1000000).toFixed(1)}M`;
    if (count >= 1000) return `${(count / 1000).toFixed(1)}K`;
    return count.toString();
  }
</script>

<button
  class="group w-full bg-slate-800 hover:bg-slate-750 rounded-xl p-4 transition-all duration-200 hover:scale-[1.02] hover:shadow-lg hover:shadow-blue-500/10 text-left"
  onclick={onclick}
>
  <!-- Character Avatar -->
  <div class="flex items-start gap-3 mb-3">
    <div class="flex-shrink-0 w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-2xl shadow-lg">
      {character.avatar || '👤'}
    </div>
    
    <div class="flex-1 min-w-0">
      <h3 class="font-semibold text-slate-100 text-base mb-1 group-hover:text-blue-400 transition-colors">
        {character.name}
      </h3>
      
      {#if character.category}
        <span class="inline-block px-2 py-0.5 text-xs rounded-full bg-slate-700 text-slate-300">
          {character.category}
        </span>
      {/if}
    </div>
  </div>

  <!-- Description -->
  <p class="text-sm text-slate-400 line-clamp-2 mb-3 leading-relaxed">
    {character.description}
  </p>

  <!-- Stats -->
  <div class="flex items-center gap-2 text-xs text-slate-500">
    <UsersIcon size={14} />
    <span>{formatChatCount(character.chatCount)} chats</span>
  </div>
</button>
