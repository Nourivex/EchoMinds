<script lang="ts">
  import BotIcon from '@components/ui/icons/Bot.svelte';
  import MenuIcon from '@components/ui/icons/Menu.svelte';

  interface Props {
    children?: import('svelte').Snippet;
  }

  let { children }: Props = $props();
</script>

<div class="flex flex-col h-full bg-slate-900 text-slate-100">
  <!-- Header -->
  <header class="sticky top-0 z-50 bg-slate-800/95 backdrop-blur-sm border-b border-slate-700 px-4 py-3 safe-area-inset">
    <div class="flex items-center justify-between max-w-4xl mx-auto">
      <button
        class="p-2 hover:bg-slate-700 rounded-lg transition-colors"
        aria-label="Menu"
      >
        <MenuIcon size={24} class="text-slate-300" />
      </button>

      <div class="flex items-center gap-2">
        <BotIcon size={24} class="text-blue-500" />
        <h1 class="text-lg font-semibold">EchoMinds</h1>
      </div>

      <div class="w-10"></div> <!-- Spacer for symmetry -->
    </div>
  </header>

  <!-- Main Content -->
  <main class="flex-1 overflow-hidden">
    {#if children}
      {@render children()}
    {/if}
  </main>
</div>
