<script lang="ts">
  import { updateBasic, companionForm } from '@stores/companionForm';
  
  const avatarOptions = ['🤖', '👨', '👩', '🧑', '👦', '👧', '🧒', '👶', '🦸', '🦹', '🧙', '🧚', '🧛', '🧜', '🧝', '🧞'];
  
  const categoryOptions = [
    { id: 'supportive', label: 'Supportive', icon: '💙' },
    { id: 'creative', label: 'Creative', icon: '🎨' },
    { id: 'professional', label: 'Professional', icon: '💼' },
    { id: 'mindfulness', label: 'Mindfulness', icon: '🧘' },
    { id: 'adventure', label: 'Adventure', icon: '⚡' }
  ];

  let form = $companionForm.basic;
</script>

<div class="space-y-6">
  <div class="text-center mb-6">
    <h2 class="text-2xl font-bold text-slate-900 dark:text-slate-100 mb-2">
      <span class="text-3xl mr-2">🎭</span> Basic Identity
    </h2>
    <p class="text-sm text-slate-600 dark:text-slate-400">
      Buat identitas dasar karakter kamu
    </p>
  </div>

  <!-- Avatar Selection -->
  <div>
    <label class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">
      Choose Avatar *
    </label>
    <div class="grid grid-cols-8 gap-2">
      {#each avatarOptions as avatar}
        <button
          type="button"
          onclick={() => updateBasic({ avatar })}
          class="w-full aspect-square text-2xl rounded-xl border-2 transition-all {
            form.avatar === avatar
              ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20 scale-110 shadow-lg'
              : 'border-gray-200 dark:border-slate-700 hover:border-purple-300 dark:hover:border-purple-600 hover:scale-105'
          }"
        >
          {avatar}
        </button>
      {/each}
    </div>
  </div>

  <!-- Name -->
  <div>
    <label for="name" class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">
      Character Name *
    </label>
    <input
      id="name"
      type="text"
      value={form.name}
      oninput={(e) => updateBasic({ name: e.currentTarget.value })}
      placeholder="e.g., Luna, Kai, Nova..."
      class="w-full px-4 py-3 bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 outline-none transition-all"
    />
  </div>

  <!-- Description -->
  <div>
    <label for="description" class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">
      Short Description *
    </label>
    <input
      id="description"
      type="text"
      value={form.description}
      oninput={(e) => updateBasic({ description: e.currentTarget.value })}
      placeholder="One-line tagline (e.g., 'Your creative companion')"
      class="w-full px-4 py-3 bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 outline-none transition-all"
    />
  </div>

  <!-- Category -->
  <div>
    <label class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">
      Category *
    </label>
    <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
      {#each categoryOptions as cat}
        <button
          type="button"
          onclick={() => updateBasic({ category: cat.id })}
          class="flex items-center gap-2 p-3 rounded-xl border-2 transition-all {
            form.category === cat.id
              ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20 shadow-md'
              : 'border-gray-200 dark:border-slate-700 hover:border-purple-300 dark:hover:border-purple-600'
          }"
        >
          <span class="text-xl">{cat.icon}</span>
          <span class="text-sm font-medium text-slate-700 dark:text-slate-300">{cat.label}</span>
        </button>
      {/each}
    </div>
  </div>
</div>
