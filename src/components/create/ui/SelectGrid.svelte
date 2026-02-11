<script lang="ts">
  interface GridItem {
    id: string;
    label: string;
    [key: string]: any;
  }

  interface Props {
    items: GridItem[];
    selectedId: string;
    columns?: number;
    onSelect: (id: string) => void;
    renderItem?: (item: GridItem, selected: boolean) => any;
  }

  let { items, selectedId, columns = 2, onSelect, renderItem }: Props = $props();
  
  const gridClass = $derived(`grid grid-cols-${columns} gap-3`);
</script>

<div class={gridClass}>
  {#each items as item}
    {@const selected = item.id === selectedId}
    
    {#if renderItem}
      {@render renderItem(item, selected)}
    {:else}
      <button
        type="button"
        onclick={() => onSelect(item.id)}
        class="flex items-center gap-2 p-3 rounded-xl border-2 transition-all {
          selected
            ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20'
            : 'border-gray-200 dark:border-slate-700 hover:border-purple-300 dark:hover:border-purple-600'
        }"
      >
        {#if item.icon}
          <span class="text-xl">{item.icon}</span>
        {/if}
        {#if item.emoji}
          <span class="text-xl">{item.emoji}</span>
        {/if}
        <span class="text-sm font-medium text-slate-700 dark:text-slate-300">{item.label}</span>
      </button>
    {/if}
  {/each}
</div>
