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
  <path d="M8 2v4"></path>
  <path d="M16 2v4"></path>
  <rect width="18" height="18" x="3" y="4" rx="2"></rect>
  <path d="M3 10h18"></path>
</svg>
