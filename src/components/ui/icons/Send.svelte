<script lang="ts">
  interface Props {
    size?: number;
    class?: string;
    strokeWidth?: number;
  }

  let { 
    size = 24, 
    class: className = '', 
    strokeWidth = 2 
  }: Props = $props();
</script>

<svg
  xmlns="http://www.w3.org/2000/svg"
  width={size}
  height={size}
  viewBox="0 0 24 24"
  fill="none"
  stroke="currentColor"
  stroke-width={strokeWidth}
  stroke-linecap="round"
  stroke-linejoin="round"
  class={className}
>
  <path d="M14.5 2h-5L7 7l-4 1-2 5v6l2 4 5 2 6-2 4-4 2-6-2-5-4-1z"></path>
  <path d="M12 16v-4"></path>
  <path d="M12 8h.01"></path>
</svg>
