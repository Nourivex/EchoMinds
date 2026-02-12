<script lang="ts">
  import { updateRelationship, companionForm } from '@stores/companionForm';
  
  // SIMPLIFIED: Only 5 main relationship types
  const relationshipOptions = [
    { id: 'friend', label: 'Friend', icon: '🤝', desc: 'Casual buddy' },
    { id: 'partner', label: 'Romantic Partner', icon: '💕', desc: 'Love interest' },
    { id: 'mentor', label: 'Mentor', icon: '🎓', desc: 'Guides you' },
    { id: 'student', label: 'Student', icon: '📚', desc: 'Learns from you' },
    { id: 'rival', label: 'Rival', icon: '⚔️', desc: 'Competitive' }
  ];

  // SIMPLIFIED: Only 3 addressing styles
  const addressOptions = [
    { id: 'casual', label: 'Casual (Kamu)', example: 'Hey, kamu lagi ngapain?' },
    { id: 'respectful', label: 'Respectful (Mas/Mbak)', example: 'Mas, boleh tanya sesuatu?' },
    { id: 'intimate', label: 'Intimate (Sayang)', example: 'Sayang, aku kangen...' }
  ];

  // Auto-set userName based on relationship (using $effect for Svelte 5)
  $effect(() => {
    if ($companionForm.relationship.type && !$companionForm.relationship.userName) {
      updateRelationship({ userName: 'You' });
    }
  });

</script>

<div class="space-y-6">
  <div class="text-center mb-6">
    <h2 class="text-2xl font-bold text-slate-900 dark:text-slate-100 mb-2">
      <span class="text-3xl mr-2">💕</span> Relationship
    </h2>
    <p class="text-sm text-slate-600 dark:text-slate-400">
      Bagaimana karakter ini berhubungan dengan kamu?
    </p>
  </div>

  <!-- Relationship Type -->
  <div>
    <label class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">
      Relationship Type *
    </label>
    <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
      {#each relationshipOptions as rel}
        <button
          type="button"
          onclick={() => updateRelationship({ type: rel.id })}
          class="flex flex-col items-center gap-2 p-4 rounded-xl border-2 transition-all {
            $companionForm.relationship.type === rel.id
              ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20 shadow-md ring-2 ring-purple-200'
              : 'border-gray-200 dark:border-slate-700 hover:border-purple-300 dark:hover:border-purple-600'
          }"
        >
          <span class="text-3xl">{rel.icon}</span>
          <div class="text-center">
            <div class="text-sm font-medium text-slate-700 dark:text-slate-300">{rel.label}</div>
            <div class="text-xs text-slate-500 dark:text-slate-500">{rel.desc}</div>
          </div>
        </button>
      {/each}
    </div>
  </div>

  <!-- Addressing Style -->
  <div>
    <label class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">
      How Should They Address You? *
    </label>
    <div class="space-y-2">
      {#each addressOptions as addr}
        <button
          type="button"
          onclick={() => updateRelationship({ preferredAddress: addr.id })}
          class="w-full text-left p-4 rounded-xl border-2 transition-all {
            $companionForm.relationship.preferredAddress === addr.id
              ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20 shadow-md'
              : 'border-gray-200 dark:border-slate-700 hover:border-purple-300 dark:hover:border-purple-600'
          }"
        >
          <div class="font-medium text-slate-700 dark:text-slate-300">{addr.label}</div>
          <div class="text-sm text-slate-500 dark:text-slate-500 mt-1 italic">"{addr.example}"</div>
        </button>
      {/each}
    </div>
  </div>

  <!-- Your Name (What character calls you) -->
  <div>
    <label for="userName" class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">
      Your Name *
    </label>
    <input
      id="userName"
      type="text"
      value={$companionForm.relationship.userName}
      oninput={(e) => updateRelationship({ userName: e.currentTarget.value })}
      placeholder="How should they call you? (e.g., Alex, Budi...)"
      class="w-full px-4 py-3 bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 outline-none transition-all"
    />
  </div>

  <!-- Optional: Custom Label -->
  <div>
    <label for="relationshipLabel" class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">
      Custom Relationship Label <span class="text-xs text-slate-500">(Optional)</span>
    </label>
    <input
      id="relationshipLabel"
      type="text"
      value={$companionForm.relationship.label || ''}
      oninput={(e) => updateRelationship({ label: e.currentTarget.value })}
      placeholder="e.g., 'Kakak angkat', 'Best friend', 'Teman sejati'..."
      class="w-full px-4 py-3 bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 outline-none transition-all"
    />
    <p class="text-xs text-slate-500 dark:text-slate-500 mt-2">
      💡 Tip: Kamu bisa custom label seperti "Kakak yang baik hati" atau "Teman curhat"
    </p>
  </div>
</div>
