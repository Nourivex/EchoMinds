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
  <line x1="4" x2="20" y1="12" y2="12"></line>
  <line x1="4" x2="20" y1="6" y2="6"></line>
  <line x1="4" x2="20" y1="18" y2="18"></line>
</svg>
