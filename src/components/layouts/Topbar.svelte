<script lang="ts">
  import { Sun, Moon, User } from '@lucide/svelte';
  import { theme, toggleTheme } from '@stores/theme';
  import BotIcon from '@components/ui/icons/Bot.svelte';

  interface Props {
    title?: string;
  }

  let { title = 'EchoMinds' }: Props = $props();

  let currentTheme = $state<'light' | 'dark'>('dark');

  theme.subscribe(value => {
    currentTheme = value;
  });
</script>

<header class="sticky top-0 z-50 bg-slate-800/95 dark:bg-slate-800/95 backdrop-blur-sm border-b border-slate-700 px-6 py-3">
  <div class="flex items-center justify-between max-w-7xl mx-auto">
    <!-- Logo & Title -->
    <div class="flex items-center gap-3">
      <BotIcon size={28} class="text-blue-500" />
      <h1 class="text-xl font-bold text-slate-100">{title}</h1>
    </div>

    <!-- Right Controls -->
    <div class="flex items-center gap-4">
      <!-- Theme Toggle -->
      <button
        onclick={toggleTheme}
        class="p-2.5 rounded-lg bg-slate-700/50 hover:bg-slate-700 text-slate-300 hover:text-slate-100 transition-all"
        aria-label="Toggle theme"
        title={currentTheme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
      >
        {#if currentTheme === 'dark'}
          <Sun size={20} />
        {:else}
          <Moon size={20} />
        {/if}
      </button>

      <!-- Profile Avatar -->
      <button
        class="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600 flex items-center justify-center text-white transition-all hover:scale-105 shadow-lg"
        aria-label="Profile"
        title="Your Profile"
      >
        <User size={20} />
      </button>
    </div>
  </div>
</header>
