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
  <path d="m15 18-6-6 6-6"></path>
</svg>
