<script lang="ts">
  interface Props {
    text: string;
  }

  let { text }: Props = $props();
</script>

<!-- Action/Narration (italic, muted) -->
<div class="text-sm text-slate-500 dark:text-slate-400 italic leading-relaxed mb-2">
  *{text}*
</div>
