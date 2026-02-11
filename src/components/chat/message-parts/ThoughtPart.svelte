<script lang="ts">
  interface Props {
    text: string;
  }

  let { text }: Props = $props();
</script>

<!-- Thought (subtle, small, in parentheses) -->
<div class="text-sm text-slate-400 dark:text-slate-500 leading-relaxed">
  ({text})
</div>
