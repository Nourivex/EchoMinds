<script lang="ts">
  import { Heart } from '@lucide/svelte';
  import { updateRelationship, companionForm } from '@stores/companionForm';
  import OptionCard from '../ui/OptionCard.svelte';
  
  const relationshipOptions = [
    { id: 'friend', label: 'Friend', description: 'Supportive companion' },
    { id: 'partner', label: 'Partner', description: 'Romantic connection' },
    { id: 'mentor', label: 'Mentor', description: 'Wise guide' },
    { id: 'rival', label: 'Rival', description: 'Competitive edge' },
    { id: 'custom', label: 'Custom', description: 'Define your own' }
  ];
  
  const roleOptions = [
    { id: 'kakak', label: 'Kakak', desc: 'Protective, responsible' },
    { id: 'adik', label: 'Adik', desc: 'Playful, looks up' },
    { id: 'senior', label: 'Senior', desc: 'Experienced' },
    { id: 'junior', label: 'Junior', desc: 'Learning' },
    { id: 'equal', label: 'Equal', desc: 'Balanced' },
    { id: 'custom', label: 'Custom', desc: 'Your own' }
  ];
  
  const addressOptions = [
    { id: 'kamu', label: 'Kamu', context: 'Casual' },
    { id: 'mas', label: 'Mas', context: 'Respectful (M)' },
    { id: 'mbak', label: 'Mbak', context: 'Respectful (F)' },
    { id: 'kakak', label: 'Kakak', context: 'Older sibling' },
    { id: 'adik', label: 'Adik', context: 'Younger' },
    { id: 'sayang', label: 'Sayang', context: 'Endearing' }
  ];
  
  const ageOptions = [
    { id: 'older', label: 'Older', desc: 'More experienced' },
    { id: 'younger', label: 'Younger', desc: 'Youthful energy' },
    { id: 'same', label: 'Same Age', desc: 'Equal generation' }
  ];
  
  const authorityOptions = [
    { id: 'higher', label: 'Higher', desc: 'Guides you' },
    { id: 'equal', label: 'Equal', desc: 'Mutual respect' },
    { id: 'lower', label: 'Lower', desc: 'Seeks advice' }
  ];

  const toneOptions = [
    { id: 'warm', label: 'Warm', emoji: '💖' },
    { id: 'neutral', label: 'Neutral', emoji: '😌' },
    { id: 'playful', label: 'Playful', emoji: '😄' },
    { id: 'mysterious', label: 'Mysterious', emoji: '🌙' }
  ];

  let form = $companionForm.relationship;
</script>

<div class="space-y-6">
  <div class="text-center mb-6">
    <h2 class="text-2xl font-bold text-slate-900 dark:text-slate-100 mb-2 flex items-center justify-center gap-2">
      <Heart size={28} />
      Relationship Dynamics
    </h2>
    <p class="text-sm text-slate-600 dark:text-slate-400">
      Bangun hubungan yang personal dan konsisten dengan 7 layers
    </p>
  </div>

  <!-- User Identity (Most Important) -->
  <div class="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/10 dark:to-purple-900/10 border-2 border-blue-300 dark:border-blue-700 rounded-xl p-5 space-y-4">
    <div class="flex items-start gap-3">
      <span class="text-2xl">👤</span>
      <div class="flex-1">
        <h4 class="text-sm font-bold text-slate-900 dark:text-slate-100 mb-1">
          User Identity <span class="text-red-500">* CRITICAL</span>
        </h4>
        <p class="text-xs text-slate-600 dark:text-slate-400 mb-4">
          Ini yang bikin character <strong>tahu siapa kamu</strong> baginya — tanpa ini, percakapan jadi generik!
        </p>
        
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <!-- User Name -->
          <div>
            <label for="userName" class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-2">
              Nama Kamu *
            </label>
            <input
              type="text"
              id="userName"
              value={form.userName}
              oninput={(e) => updateRelationship({ userName: e.currentTarget.value })}
              placeholder="e.g., Lycus, Kak Budi, Sarah"
              class="w-full px-3 py-2 bg-white dark:bg-slate-900 border border-blue-300 dark:border-blue-700 rounded-lg text-sm text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-blue-500 outline-none"
            />
          </div>
          
          <!-- Preferred Address -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-2">
              Cara Panggil *
            </label>
            <select
              value={form.preferredAddress}
              onchange={(e) => updateRelationship({ preferredAddress: e.currentTarget.value })}
              class="w-full px-3 py-2 bg-white dark:bg-slate-900 border border-blue-300 dark:border-blue-700 rounded-lg text-sm text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-blue-500 outline-none"
            >
              {#each addressOptions as addr}
                <option value={addr.id}>{addr.label} ({addr.context})</option>
              {/each}
            </select>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Relationship Type -->
  <div>
    <label class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">
      Relationship Type *
    </label>
    <div class="grid grid-cols-2 gap-3">
      {#each relationshipOptions as rel}
        <button
          type="button"
          onclick={() => updateRelationship({ type: rel.id })}
          class="flex flex-col gap-1 p-3 rounded-xl border-2 transition-all text-left {
            form.type === rel.id
              ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20 shadow-md'
              : 'border-gray-200 dark:border-slate-700 hover:border-purple-300'
          }"
        >
          <span class="text-sm font-semibold text-slate-900 dark:text-slate-100">{rel.label}</span>
          <span class="text-xs text-slate-500 dark:text-slate-400">{rel.description}</span>
        </button>
      {/each}
    </div>
    
    {#if form.type === 'custom'}
      <input
        type="text"
        value={form.customType || ''}
        oninput={(e) => updateRelationship({ customType: e.currentTarget.value })}
        placeholder="e.g., Childhood friend, Mysterious ally..."
        class="w-full mt-3 px-4 py-3 bg-white dark:bg-slate-900 border border-purple-300 dark:border-purple-700 rounded-lg text-sm text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-purple-500 outline-none"
      />
    {/if}
  </div>

  <!-- Relationship Role -->
  <div>
    <label class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">
      Social Role *
    </label>
    <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
      {#each roleOptions as role}
        <button
          type="button"
          onclick={() => updateRelationship({ role: role.id })}
          class="flex flex-col gap-1 p-3 rounded-xl border-2 transition-all text-left {
            form.role === role.id
              ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20'
              : 'border-gray-200 dark:border-slate-700 hover:border-purple-300'
          }"
        >
          <span class="text-sm font-semibold text-slate-900 dark:text-slate-100">{role.label}</span>
          <span class="text-xs text-slate-500 dark:text-slate-400">{role.desc}</span>
        </button>
      {/each}
    </div>
    
    {#if form.role === 'custom'}
      <input
        type="text"
        value={form.customRole || ''}
        oninput={(e) => updateRelationship({ customRole: e.currentTarget.value })}
        placeholder="e.g., Sepupu, Guru, Tetangga..."
        class="w-full mt-3 px-4 py-3 bg-white dark:bg-slate-900 border border-purple-300 dark:border-purple-700 rounded-lg text-sm text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-purple-500 outline-none"
      />
    {/if}
  </div>

  <!-- Relationship Label (Optional) -->
  <div>
    <label for="label" class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">
      Relationship Label <span class="text-xs text-slate-500">(Opsional)</span>
    </label>
    <input
      type="text"
      id="label"
      value={form.label}
      oninput={(e) => updateRelationship({ label: e.currentTarget.value })}
      placeholder="e.g., 'adik kandung', 'sahabat sejak kecil'"
      class="w-full px-4 py-3 bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-purple-500 outline-none"
    />
  </div>

  <!-- Age & Authority -->
  <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
    <!-- Age Relation -->
    <div>
      <label class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">
        Age Relation *
      </label>
      <div class="space-y-2">
        {#each ageOptions as age}
          <button
            type="button"
            onclick={() => updateRelationship({ ageRelation: age.id })}
            class="w-full flex justify-between items-center p-3 rounded-lg border-2 transition-all {
              form.ageRelation === age.id
                ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20'
                : 'border-gray-200 dark:border-slate-700 hover:border-purple-300'
            }"
          >
            <div class="text-left">
              <div class="text-sm font-semibold text-slate-900 dark:text-slate-100">{age.label}</div>
              <div class="text-xs text-slate-500 dark:text-slate-400">{age.desc}</div>
            </div>
            {#if form.ageRelation === age.id}
              <svg class="w-5 h-5 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
              </svg>
            {/if}
          </button>
        {/each}
      </div>
    </div>
    
    <!-- Authority Level -->
    <div>
      <label class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">
        Authority Level *
      </label>
      <div class="space-y-2">
        {#each authorityOptions as auth}
          <button
            type="button"
            onclick={() => updateRelationship({ authorityLevel: auth.id })}
            class="w-full flex justify-between items-center p-3 rounded-lg border-2 transition-all {
              form.authorityLevel === auth.id
                ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20'
                : 'border-gray-200 dark:border-slate-700 hover:border-purple-300'
            }"
          >
            <div class="text-left">
              <div class="text-sm font-semibold text-slate-900 dark:text-slate-100">{auth.label}</div>
              <div class="text-xs text-slate-500 dark:text-slate-400">{auth.desc}</div>
            </div>
            {#if form.authorityLevel === auth.id}
              <svg class="w-5 h-5 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
              </svg>
            {/if}
          </button>
        {/each}
      </div>
    </div>
  </div>

  <!-- Emotional Tone -->
  <div>
    <label class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">
      Emotional Tone *
    </label>
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
      {#each toneOptions as tone}
        <OptionCard
          label={tone.label}
          emoji={tone.emoji}
          selected={form.emotionalTone === tone.id}
          onclick={() => updateRelationship({ emotionalTone: tone.id })}
        />
      {/each}
    </div>
  </div>
</div>
