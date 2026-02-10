<script lang="ts">
  import { Home, MessageSquare, Compass, PlusCircle, Settings, ChevronLeft, ChevronRight } from '@lucide/svelte';
  import { router } from '@stores/router';
  import type { ComponentType } from 'svelte';

  interface Props {
    children?: import('svelte').Snippet;
  }

  let { children }: Props = $props();

  let isExpanded = $state(false);
  let isMobile = $state(false);

  // Detect mobile viewport
  $effect(() => {
    if (typeof window !== 'undefined') {
      const checkMobile = () => {
        const mobile = window.innerWidth < 768;
        isMobile = mobile;
        // Auto-collapse on mobile
        if (mobile) {
          isExpanded = false;
        }
      };
      
      checkMobile();
      window.addEventListener('resize', checkMobile);
      
      return () => window.removeEventListener('resize', checkMobile);
    }
  });

  interface MenuItem {
    icon: ComponentType;
    label: string;
    action: () => void;
  }

  const menuItems: MenuItem[] = [
    { icon: Home, label: 'Home', action: () => router.navigateToHome() },
    { icon: MessageSquare, label: 'My Chats', action: () => router.navigateToMyChats() },
    { icon: Compass, label: 'Explore', action: () => router.navigateToExplore() },
    { icon: PlusCircle, label: 'Create', action: () => router.navigateToCreate() },
    { icon: Settings, label: 'Settings', action: () => router.navigateToSettings() }
  ];

  function toggleSidebar() {
    isExpanded = !isExpanded;
  }
</script>

<aside 
  class="fixed left-0 top-0 h-full bg-white/95 dark:bg-slate-900/95 backdrop-blur-sm border-r border-gray-200 dark:border-slate-800 transition-all duration-300 z-40 {isExpanded ? 'w-56' : 'w-16'}"
>
  <!-- Toggle Button -->
  <button
    onclick={toggleSidebar}
    class="absolute -right-3 top-20 w-6 h-6 bg-white dark:bg-slate-800 hover:bg-gray-100 dark:hover:bg-slate-700 rounded-full flex items-center justify-center text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 transition-all shadow-lg border border-gray-300 dark:border-slate-700"
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
        class="group relative flex items-center gap-3 px-3 py-3 rounded-lg hover:bg-gray-100 dark:hover:bg-slate-800 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 transition-all"
        title={item.label}
      >
        <item.icon size={20} class="flex-shrink-0" />
        
        {#if isExpanded}
          <span class="text-sm font-medium whitespace-nowrap">{item.label}</span>
        {:else}
          <!-- Tooltip for collapsed state -->
          <div class="absolute left-full ml-2 px-2 py-1 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap shadow-lg border border-gray-200 dark:border-slate-700">
            {item.label}
          </div>
        {/if}
      </button>
    {/each}
  </nav>
</aside>

<!-- Content Area dengan proper spacing - LAYOUT responsibility -->
<div class="w-full h-full {isExpanded ? 'pl-56' : 'pl-16'} transition-all duration-300">
  <div class="h-full flex flex-col">
    {#if children}
      {@render children()}
    {/if}
  </div>
</div>
