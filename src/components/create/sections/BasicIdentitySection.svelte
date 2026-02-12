<script lang="ts">
  import { updateBasic, companionForm } from '@stores/companionForm';
  
  const avatarOptions = [
    '😊', '😎', '🥰', '😇', '🤗', '😏', '🤔', '😌', 
    '💫', '✨', '⭐', '🌟', '🔥', '💙', '💜', '💚',
    '🦋', '🌸', '🌺', '🌻', '🦄', '🐉', '🦊', '🐺',
    '👨', '👩', '🧑', '👨‍💼', '👩‍💼', '👨‍🎨', '👩‍🎨', '🧙'
  ];
  
  const raceOptions = [
    // Real-world races
    { id: 'asian', label: 'Asian', icon: '🌏' },
    { id: 'caucasian', label: 'Caucasian', icon: '🌍' },
    { id: 'african', label: 'African', icon: '🌍' },
    { id: 'hispanic', label: 'Hispanic', icon: '🌎' },
    { id: 'middle-eastern', label: 'Middle Eastern', icon: '🌍' },
    { id: 'indigenous', label: 'Indigenous', icon: '🌿' },
    { id: 'pacific-islander', label: 'Pacific Islander', icon: '🏝️' },
    { id: 'mixed', label: 'Mixed/Multiracial', icon: '🌈' },
    
    // Fantasy races
    { id: 'elf', label: 'Elf', icon: '🧝' },
    { id: 'dwarf', label: 'Dwarf', icon: '⚒️' },
    { id: 'vampire', label: 'Vampire', icon: '🧛' },
    { id: 'werewolf', label: 'Werewolf', icon: '🐺' },
    { id: 'fairy', label: 'Fairy', icon: '🧚' },
    { id: 'demon', label: 'Demon', icon: '😈' },
    { id: 'angel', label: 'Angel', icon: '😇' },
    { id: 'dragon', label: 'Dragon', icon: '🐉' },
    { id: 'mermaid', label: 'Mermaid', icon: '🧜' },
    { id: 'wizard', label: 'Wizard', icon: '🧙' },
    { id: 'android', label: 'Android', icon: '🤖' },
    { id: 'alien', label: 'Alien', icon: '👽' }
  ];
  
  const categoryOptions = [
    { id: 'supportive', label: 'Supportive', icon: '💙' },
    { id: 'creative', label: 'Creative', icon: '🎨' },
    { id: 'professional', label: 'Professional', icon: '💼' },
    { id: 'mindfulness', label: 'Mindfulness', icon: '🧘' },
    { id: 'adventure', label: 'Adventure', icon: '⚡' }
  ];

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

  <!-- STEP 1: GENDER (First Priority) -->
  <div>
    <label class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">
      Gender *
    </label>
    <div class="grid grid-cols-2 gap-3">
      <button
        type="button"
        onclick={() => updateBasic({ gender: 'Male' })}
        class="flex items-center justify-center gap-2 p-4 rounded-xl border-2 transition-all {
          $companionForm.basic.gender === 'Male'
            ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20 shadow-md ring-2 ring-blue-200'
            : 'border-gray-200 dark:border-slate-700 hover:border-blue-300 dark:hover:border-blue-600'
        }"
      >
        <span class="text-2xl">♂️</span>
        <span class="text-base font-medium text-slate-700 dark:text-slate-300">Male</span>
      </button>
      <button
        type="button"
        onclick={() => updateBasic({ gender: 'Female' })}
        class="flex items-center justify-center gap-2 p-4 rounded-xl border-2 transition-all {
          $companionForm.basic.gender === 'Female'
            ? 'border-pink-500 bg-pink-50 dark:bg-pink-900/20 shadow-md ring-2 ring-pink-200'
            : 'border-gray-200 dark:border-slate-700 hover:border-pink-300 dark:hover:border-pink-600'
        }"
      >
        <span class="text-2xl">♀️</span>
        <span class="text-base font-medium text-slate-700 dark:text-slate-300">Female</span>
      </button>
    </div>
  </div>

  <!-- STEP 2: RACE (Second Priority) -->
  <div>
    <label class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">
      Race/Ethnicity *
    </label>
    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2">
      {#each raceOptions as race}
        <button
          type="button"
          onclick={() => updateBasic({ race: race.id })}
          class="flex items-center gap-2 p-2.5 rounded-lg border-2 transition-all {
            $companionForm.basic.race === race.id
              ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20 shadow-md ring-2 ring-purple-200'
              : 'border-gray-200 dark:border-slate-700 hover:border-purple-300 dark:hover:border-purple-600'
          }"
        >
          <span class="text-lg">{race.icon}</span>
          <span class="text-xs font-medium text-slate-700 dark:text-slate-300">{race.label}</span>
        </button>
      {/each}
    </div>
  </div>

  <!-- STEP 3: Avatar Selection -->
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
            $companionForm.basic.avatar === avatar
              ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20 scale-110 shadow-lg'
              : 'border-gray-200 dark:border-slate-700 hover:border-purple-300 dark:hover:border-purple-600 hover:scale-105'
          }"
        >
          {avatar}
        </button>
      {/each}
    </div>
  </div>

  <!-- STEP 4: Name -->
  <div>
    <label for="name" class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">
      Character Name *
    </label>
    <input
      id="name"
      type="text"
      value={$companionForm.basic.name}
      oninput={(e) => updateBasic({ name: e.currentTarget.value })}
      placeholder="e.g., Luna, Kai, Nova..."
      class="w-full px-4 py-3 bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 outline-none transition-all"
    />
  </div>

  <!-- STEP 5: Description -->
  <div>
    <label for="description" class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">
      Short Description *
    </label>
    <input
      id="description"
      type="text"
      value={$companionForm.basic.description}
      oninput={(e) => updateBasic({ description: e.currentTarget.value })}
      placeholder="One-line tagline (e.g., 'Your creative companion')"
      class="w-full px-4 py-3 bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 outline-none transition-all"
    />
  </div>

  <!-- STEP 6: Category -->
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
            $companionForm.basic.category === cat.id
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
