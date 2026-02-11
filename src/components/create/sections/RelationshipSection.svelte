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
    // Family
    { id: 'orang-tua', label: 'Orang Tua', desc: 'Parent, protective', category: 'family', compatibleTypes: ['mentor', 'friend', 'custom'] },
    { id: 'anak', label: 'Anak', desc: 'Child, dependent', category: 'family', compatibleTypes: ['friend', 'custom'] },
    { id: 'kakak', label: 'Kakak', desc: 'Older sibling', category: 'family', compatibleTypes: ['friend', 'mentor', 'rival', 'custom'] },
    { id: 'adik', label: 'Adik', desc: 'Younger sibling', category: 'family', compatibleTypes: ['friend', 'rival', 'custom'] },
    { id: 'sepupu', label: 'Sepupu', desc: 'Cousin', category: 'family', compatibleTypes: ['friend', 'rival', 'custom'] },
    
    // Social
    { id: 'sahabat', label: 'Sahabat', desc: 'Best friend', category: 'social', compatibleTypes: ['friend', 'custom'] },
    { id: 'teman', label: 'Teman', desc: 'Friend', category: 'social', compatibleTypes: ['friend', 'rival', 'custom'] },
    { id: 'tetangga', label: 'Tetangga', desc: 'Neighbor', category: 'social', compatibleTypes: ['friend', 'rival', 'custom'] },
    { id: 'kenalan', label: 'Kenalan', desc: 'Acquaintance', category: 'social', compatibleTypes: ['friend', 'rival', 'custom'] },
    
    // Academic/Professional
    { id: 'guru', label: 'Guru', desc: 'Teacher', category: 'academic', compatibleTypes: ['mentor', 'friend', 'custom'] },
    { id: 'murid', label: 'Murid', desc: 'Student', category: 'academic', compatibleTypes: ['friend', 'custom'] },
    { id: 'mentor', label: 'Mentor', desc: 'Guide', category: 'academic', compatibleTypes: ['mentor', 'friend', 'custom'] },
    { id: 'mentee', label: 'Mentee', desc: 'Learner', category: 'academic', compatibleTypes: ['friend', 'custom'] },
    { id: 'senior', label: 'Senior', desc: 'Experienced', category: 'academic', compatibleTypes: ['mentor', 'friend', 'rival', 'custom'] },
    { id: 'junior', label: 'Junior', desc: 'Learning', category: 'academic', compatibleTypes: ['friend', 'custom'] },
    { id: 'equal', label: 'Equal', desc: 'Balanced', category: 'academic', compatibleTypes: ['friend', 'rival', 'partner', 'custom'] },
    
    // Romantic
    { id: 'pacar', label: 'Pacar', desc: 'Boyfriend/Girlfriend', category: 'romantic', compatibleTypes: ['partner', 'friend', 'custom'] },
    { id: 'tunangan', label: 'Tunangan', desc: 'Fiancé(e)', category: 'romantic', compatibleTypes: ['partner', 'friend', 'custom'] },
    { id: 'suami-istri', label: 'Suami/Istri', desc: 'Spouse', category: 'romantic', compatibleTypes: ['partner', 'friend', 'custom'] },
    { id: 'gebetan', label: 'Gebetan', desc: 'Crush', category: 'romantic', compatibleTypes: ['friend', 'rival', 'partner', 'custom'] },
    
    // Other
    { id: 'rival', label: 'Rival', desc: 'Competitor', category: 'other', compatibleTypes: ['rival', 'friend', 'custom'] },
    { id: 'musuh', label: 'Musuh', desc: 'Enemy', category: 'other', compatibleTypes: ['rival', 'custom'] },
    { id: 'custom', label: 'Custom', desc: 'Your own', category: 'other', compatibleTypes: ['friend', 'partner', 'mentor', 'rival', 'custom'] }
  ];
  
  const addressOptions = [
    { id: 'kamu', label: 'Kamu', context: 'Casual', suitableFor: ['teman', 'sahabat', 'equal', 'pacar', 'gebetan', 'sepupu', 'kenalan'] },
    { id: 'mas', label: 'Mas', context: 'Respectful (M)', suitableFor: ['kakak', 'senior', 'guru', 'mentor', 'orang-tua', 'suami-istri', 'tetangga'] },
    { id: 'mbak', label: 'Mbak', context: 'Respectful (F)', suitableFor: ['kakak', 'senior', 'guru', 'mentor', 'orang-tua', 'suami-istri', 'tetangga'] },
    { id: 'kakak', label: 'Kakak', context: 'Older sibling', suitableFor: ['kakak', 'senior', 'mentor'] },
    { id: 'adik', label: 'Adik', context: 'Younger', suitableFor: ['adik', 'junior', 'murid', 'anak'] },
    { id: 'sayang', label: 'Sayang', context: 'Endearing', suitableFor: ['pacar', 'tunangan', 'suami-istri', 'anak', 'adik'] },
    { id: 'pak', label: 'Pak', context: 'Formal (M)', suitableFor: ['guru', 'orang-tua', 'mentor'] },
    { id: 'bu', label: 'Bu', context: 'Formal (F)', suitableFor: ['guru', 'orang-tua', 'mentor'] }
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

  // Smart label suggestions based on type + role
  const labelSuggestions = $derived.by(() => {
    const type = $companionForm.relationship.type;
    const role = $companionForm.relationship.role;
    const userName = $companionForm.relationship.userName;
    
    const map: Record<string, Record<string, string>> = {
      'friend': {
        'sahabat': `sahabat terbaik ${userName}`,
        'teman': `teman dekat ${userName}`,
        'kakak': `kakak yang supportive`,
        'adik': `adik yang ceria`,
        'sepupu': `sepupu kesayangan`,
        'default': `teman ${userName}`
      },
      'partner': {
        'pacar': `kekasih ${userName}`,
        'tunangan': `calon suami/istri ${userName}`,
        'suami-istri': `pasangan hidup ${userName}`,
        'gebetan': `gebetan ${userName}`,
        'equal': `partner hidup ${userName}`,
        'default': `partner ${userName}`
      },
      'mentor': {
        'orang-tua': `orang tua ${userName}`,
        'guru': `guru ${userName}`,
        'mentor': `mentor ${userName}`,
        'kakak': `kakak pembimbing`,
        'senior': `senior yang mengayomi`,
        'default': `mentor ${userName}`
      },
      'rival': {
        'rival': `rival utama ${userName}`,
        'musuh': `musuh bebuyutan ${userName}`,
        'teman': `teman sekaligus rival`,
        'kakak': `kakak yang kompetitif`,
        'default': `rival ${userName}`
      }
    };
    
    const typeMap = map[type] || map['friend'];
    return typeMap[role] || typeMap['default'] || '';
  });

  // Smart address suggestions
  const suggestedAddresses = $derived.by(() => {
    const role = $companionForm.relationship.role;
    return addressOptions.filter(addr => addr.suitableFor.includes(role));
  });

  // Check if type-role combination is compatible
  const isCompatibleCombination = $derived.by(() => {
    const type = $companionForm.relationship.type;
    const role = $companionForm.relationship.role;
    
    const roleData = roleOptions.find(r => r.id === role);
    if (!roleData) return true; // Custom always compatible
    
    return roleData.compatibleTypes.includes(type);
  });

  // Auto-update label when type or role changes
  $effect(() => {
    const currentLabel = $companionForm.relationship.label;
    const suggested = labelSuggestions;
    
    // Only auto-update if label is empty or matches old suggestion
    if (!currentLabel || currentLabel.includes('undefined')) {
      updateRelationship({ label: suggested });
    }
  });

  // Auto-select first suitable address when role changes
  $effect(() => {
    const suggested = suggestedAddresses;
    const currentAddress = $companionForm.relationship.preferredAddress;
    
    // Check if current address is suitable for role
    const isCurrentSuitable = suggested.some(addr => addr.id === currentAddress);
    
    if (!isCurrentSuitable && suggested.length > 0) {
      updateRelationship({ preferredAddress: suggested[0].id });
    }
  });
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
              value={$companionForm.relationship.userName}
              oninput={(e) => updateRelationship({ userName: e.currentTarget.value })}
              placeholder="e.g., Lycus, Kak Budi, Sarah"
              class="w-full px-3 py-2 bg-white dark:bg-slate-900 border border-blue-300 dark:border-blue-700 rounded-lg text-sm text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-blue-500 outline-none"
            />
          </div>
          
          <!-- Preferred Address -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-2">
              Cara Panggil * <span class="text-xs text-green-600">✨ Smart</span>
            </label>
            <select
              value={$companionForm.relationship.preferredAddress}
              onchange={(e) => updateRelationship({ preferredAddress: e.currentTarget.value })}
              class="w-full px-3 py-2 bg-white dark:bg-slate-900 border border-blue-300 dark:border-blue-700 rounded-lg text-sm text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-blue-500 outline-none"
            >
              <optgroup label="✨ Cocok untuk role ini">
                {#each suggestedAddresses as addr}
                  <option value={addr.id}>{addr.label} ({addr.context})</option>
                {/each}
              </optgroup>
              {#if suggestedAddresses.length < addressOptions.length}
                <optgroup label="Opsi lainnya">
                  {#each addressOptions.filter(a => !suggestedAddresses.includes(a)) as addr}
                    <option value={addr.id}>{addr.label} ({addr.context})</option>
                  {/each}
                </optgroup>
              {/if}
            </select>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">
              Auto-pilih yang cocok dengan role kamu
            </p>
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
            $companionForm.relationship.type === rel.id
              ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20 shadow-md'
              : 'border-gray-200 dark:border-slate-700 hover:border-purple-300'
          }"
        >
          <span class="text-sm font-semibold text-slate-900 dark:text-slate-100">{rel.label}</span>
          <span class="text-xs text-slate-500 dark:text-slate-400">{rel.description}</span>
        </button>
      {/each}
    </div>
    
    {#if $companionForm.relationship.type === 'custom'}
      <input
        type="text"
        value={$companionForm.relationship.customType || ''}
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
    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2">
      {#each roleOptions as role}
        <button
          type="button"
          onclick={() => updateRelationship({ role: role.id })}
          class="flex flex-col gap-0.5 p-2 rounded-lg border-2 transition-all text-left {
            $companionForm.relationship.role === role.id
              ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20 shadow-md'
              : 'border-gray-200 dark:border-slate-700 hover:border-purple-300'
          }"
        >
          <span class="text-xs font-bold text-slate-900 dark:text-slate-100">{role.label}</span>
          <span class="text-xs text-slate-500 dark:text-slate-400 leading-tight">{role.desc}</span>
        </button>
      {/each}
    </div>
    
    {#if $companionForm.relationship.role === 'custom'}
      <input
        type="text"
        value={$companionForm.relationship.customRole || ''}
        oninput={(e) => updateRelationship({ customRole: e.currentTarget.value })}
        placeholder="e.g., Bodyguard, Roommate, Pet..."
        class="w-full mt-3 px-4 py-3 bg-white dark:bg-slate-900 border border-purple-300 dark:border-purple-700 rounded-lg text-sm text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-purple-500 outline-none"
      />
    {/if}
  </div>

  <!-- Compatibility Warning -->
  {#if !isCompatibleCombination}
    <div class="bg-amber-50 dark:bg-amber-900/20 border border-amber-300 dark:border-amber-700 rounded-xl p-4 flex items-start gap-3">
      <svg class="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
      </svg>
      <div>
        <p class="text-sm font-semibold text-amber-900 dark:text-amber-100 mb-1">
          ⚠️ Kombinasi Tidak Biasa Terdeteksi
        </p>
        <p class="text-xs text-amber-700 dark:text-amber-300">
          <strong>Type "{$companionForm.relationship.type}"</strong> dengan <strong>Role "{$companionForm.relationship.role}"</strong> agak aneh. 
          Misalnya: "orang tua" sebagai "rival" 🤣<br/>
          <span class="text-xs mt-1 inline-block">💡 Pertimbangkan ubah salah satu atau gunakan "Custom" jika memang disengaja.</span>
        </p>
      </div>
    </div>
  {/if}

  <!-- Relationship Label (Optional) -->
  <div>
    <div class="flex items-center justify-between mb-2">
      <label for="label" class="block text-sm font-semibold text-slate-700 dark:text-slate-300">
        Relationship Label <span class="text-xs text-slate-500">(Opsional)</span> <span class="text-xs text-green-600">✨ Smart</span>
      </label>
      {#if labelSuggestions}
        <button
          type="button"
          onclick={() => updateRelationship({ label: labelSuggestions })}
          class="text-xs text-purple-600 dark:text-purple-400 hover:text-purple-700 dark:hover:text-purple-300 font-medium"
        >
          Gunakan saran
        </button>
      {/if}
    </div>
    <input
      type="text"
      id="label"
      value={$companionForm.relationship.label}
      oninput={(e) => updateRelationship({ label: e.currentTarget.value })}
      placeholder="e.g., 'adik kandung', 'sahabat sejak kecil'"
      class="w-full px-4 py-3 bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-purple-500 outline-none"
    />
    {#if labelSuggestions && labelSuggestions !== $companionForm.relationship.label}
      <p class="text-xs text-slate-500 dark:text-slate-400 mt-2">
        💡 Saran: <span class="text-purple-600 dark:text-purple-400 font-medium">{labelSuggestions}</span>
      </p>
    {/if}
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
              $companionForm.relationship.ageRelation === age.id
                ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20'
                : 'border-gray-200 dark:border-slate-700 hover:border-purple-300'
            }"
          >
            <div class="text-left">
              <div class="text-sm font-semibold text-slate-900 dark:text-slate-100">{age.label}</div>
              <div class="text-xs text-slate-500 dark:text-slate-400">{age.desc}</div>
            </div>
            {#if $companionForm.relationship.ageRelation === age.id}
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
              $companionForm.relationship.authorityLevel === auth.id
                ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20'
                : 'border-gray-200 dark:border-slate-700 hover:border-purple-300'
            }"
          >
            <div class="text-left">
              <div class="text-sm font-semibold text-slate-900 dark:text-slate-100">{auth.label}</div>
              <div class="text-xs text-slate-500 dark:text-slate-400">{auth.desc}</div>
            </div>
            {#if $companionForm.relationship.authorityLevel === auth.id}
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
          selected={$companionForm.relationship.emotionalTone === tone.id}
          onclick={() => updateRelationship({ emotionalTone: tone.id })}
        />
      {/each}
    </div>
  </div>
</div>
