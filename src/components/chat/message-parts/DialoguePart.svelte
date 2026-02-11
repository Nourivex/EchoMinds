<script lang="ts">
  interface Props {
    text: string;
  }

  let { text }: Props = $props();
</script>

<!-- Dialogue (normal text, quoted) -->
<div class="text-base text-slate-900 dark:text-slate-100 leading-relaxed mb-2">
  "{text}"
</div>
