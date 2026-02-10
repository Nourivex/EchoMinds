<script lang="ts">
  import { Home, MessageSquare, Compass, PlusCircle, Settings, ChevronLeft, ChevronRight } from '@lucide/svelte';
  import { router } from '@stores/router';
  import type { ComponentType } from 'svelte';

  interface Props {
    children?: import('svelte').Snippet;
  }

  let { children }: Props = $props();

  let isExpanded = $state(false);

  interface MenuItem {
    icon: ComponentType;
    label: string;
    action: () => void;
  }

  const menuItems: MenuItem[] = [
    { icon: Home, label: 'Home', action: () => router.navigateToHome() },
    { icon: MessageSquare, label: 'My Chats', action: () => {} },
    { icon: Compass, label: 'Explore', action: () => {} },
    { icon: PlusCircle, label: 'Create', action: () => {} },
    { icon: Settings, label: 'Settings', action: () => {} }
  ];

  function toggleSidebar() {
    isExpanded = !isExpanded;
  }
</script>

<aside 
  class="fixed left-0 top-0 h-full bg-slate-900/95 backdrop-blur-sm border-r border-slate-800 transition-all duration-300 z-40 {isExpanded ? 'w-56' : 'w-16'}"
>
  <!-- Toggle Button -->
  <button
    onclick={toggleSidebar}
    class="absolute -right-3 top-20 w-6 h-6 bg-slate-800 hover:bg-slate-700 rounded-full flex items-center justify-center text-slate-400 hover:text-slate-200 transition-all shadow-lg border border-slate-700"
    aria-label={isExpanded ? 'Collapse sidebar' : 'Expand sidebar'}
  >
    {#if isExpanded}
      <ChevronLeft size={14} />
    {:else}
      <ChevronRight size={14} />
    {/if}
  </button>

  <!-- Menu Items -->
  <nav class="flex flex-col gap-2 p-3 mt-20">
    {#each menuItems as item}
      <button
        onclick={item.action}
        class="group relative flex items-center gap-3 px-3 py-3 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-slate-100 transition-all"
        title={item.label}
      >
        <item.icon size={20} class="flex-shrink-0" />
        
        {#if isExpanded}
          <span class="text-sm font-medium whitespace-nowrap">{item.label}</span>
        {:else}
          <!-- Tooltip for collapsed state -->
          <div class="absolute left-full ml-2 px-2 py-1 bg-slate-800 text-slate-100 text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap">
            {item.label}
          </div>
        {/if}
      </button>
    {/each}
  </nav>
</aside>

<!-- Spacer untuk konten utama -->
<div class="{isExpanded ? 'ml-56' : 'ml-16'} transition-all duration-300">
  {#if children}
    {@render children()}
  {/if}
</div>
