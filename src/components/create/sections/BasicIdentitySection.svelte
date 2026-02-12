<script lang="ts">
  import { updateBasic, companionForm } from "@stores/companionForm";
  import {
    User,
    Users,
    Sparkles,
    Globe,
    Shield,
    Skull,
    Crown,
    Heart,
    Leaf,
    Mountain,
    Waves,
    Zap,
    Moon,
    Sun,
    HeartHandshake,
    Palette,
    Briefcase,
    Sprout,
    Compass,
    Sword,
    Coffee,
  } from "@lucide/svelte";

  // Default avatar silhouettes (vector-based, clean)
  const avatarOptions = [
    { id: "default-1", icon: User, label: "Basic" },
    { id: "default-2", icon: Users, label: "Friendly" },
    { id: "default-3", icon: Sparkles, label: "Magical" },
    { id: "default-4", icon: Crown, label: "Royal" },
    { id: "default-5", icon: Heart, label: "Lovely" },
    { id: "default-6", icon: Shield, label: "Guardian" },
    { id: "default-7", icon: Zap, label: "Dynamic" },
    { id: "default-8", icon: Moon, label: "Mysterious" },
  ];

  const raceOptions = [
    // Real-world races (with Lucide icons)
    { id: "asian", label: "Asian", icon: Globe },
    { id: "caucasian", label: "Caucasian", icon: User },
    { id: "african", label: "African", icon: Sun },
    { id: "hispanic", label: "Hispanic", icon: Heart },
    { id: "middle-eastern", label: "Middle Eastern", icon: Moon },
    { id: "indigenous", label: "Indigenous", icon: Leaf },
    { id: "pacific-islander", label: "Pacific Islander", icon: Waves },
    { id: "mixed", label: "Mixed/Multiracial", icon: Users },

    // Fantasy races (with Lucide icons)
    { id: "elf", label: "Elf", icon: Sparkles },
    { id: "dwarf", label: "Dwarf", icon: Mountain },
    { id: "vampire", label: "Vampire", icon: Moon },
    { id: "werewolf", label: "Werewolf", icon: Zap },
    { id: "fairy", label: "Fairy", icon: Sparkles },
    { id: "demon", label: "Demon", icon: Skull },
    { id: "angel", label: "Angel", icon: Sun },
    { id: "dragon", label: "Dragon", icon: Zap },
    { id: "mermaid", label: "Mermaid", icon: Waves },
    { id: "wizard", label: "Wizard", icon: Sparkles },
    { id: "android", label: "Android", icon: Shield },
    { id: "alien", label: "Alien", icon: Globe },
  ];

  const categoryOptions = [
    {
      id: "supportive",
      label: "Supportive",
      icon: HeartHandshake,
      color: "text-blue-400",
    },
    {
      id: "creative",
      label: "Creative",
      icon: Palette,
      color: "text-purple-400",
    },
    {
      id: "professional",
      label: "Professional",
      icon: Briefcase,
      color: "text-gray-400",
    },
    {
      id: "mindfulness",
      label: "Mindfulness",
      icon: Sprout,
      color: "text-green-400",
    },
    {
      id: "adventure",
      label: "Adventure",
      icon: Compass,
      color: "text-orange-400",
    },
    {
      id: "action",
      label: "Combat/Action",
      icon: Sword,
      color: "text-red-400",
    },
    {
      id: "casual",
      label: "Casual/Daily",
      icon: Coffee,
      color: "text-amber-400",
    },
  ];

  let isEnhancingDesc = $state(false);
  let enhanceError = $state("");

  async function enhanceDescription() {
    const { name, gender, race } = $companionForm.basic;
    if (!name) {
      enhanceError = "⚠️ Please enter a name first!";
      setTimeout(() => (enhanceError = ""), 3000);
      return;
    }

    isEnhancingDesc = true;
    enhanceError = "";

    try {
      const prompt = `Create a short, compelling character description (one sentence, max 15 words) for:
- Name: ${name}
- Gender: ${gender}
- Race: ${race}

Format: Just the description, no quotes or explanations.
Example: "A mysterious elf with wisdom beyond years"`;

      const response = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: prompt,
          userId: "system-enhancer",
          characterId: "system",
          conversationId: `enhance-${Date.now()}`,
        }),
      });

      if (!response.ok) throw new Error("Enhancement failed");

      const data = await response.json();
      const enhanced = data.response.trim().replace(/^"|"$/g, "");

      updateBasic({ description: enhanced });
    } catch (error) {
      console.error("Enhancement error:", error);
      enhanceError = "❌ Enhancement failed. Try again or write manually.";
    } finally {
      isEnhancingDesc = false;
    }
  }
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
    <label
      class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3"
    >
      Gender *
    </label>
    <div class="grid grid-cols-2 gap-3">
      <button
        type="button"
        onclick={() => updateBasic({ gender: "Male" })}
        class="flex items-center justify-center gap-3 p-4 rounded-xl border-2 transition-all {$companionForm
          .basic.gender === 'Male'
          ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20 shadow-md ring-2 ring-blue-200'
          : 'border-gray-200 dark:border-slate-700 hover:border-blue-300 dark:hover:border-blue-600'}"
      >
        <User size={24} class="text-blue-600 dark:text-blue-400" />
        <span class="text-base font-medium text-slate-700 dark:text-slate-300"
          >Male</span
        >
      </button>
      <button
        type="button"
        onclick={() => updateBasic({ gender: "Female" })}
        class="flex items-center justify-center gap-3 p-4 rounded-xl border-2 transition-all {$companionForm
          .basic.gender === 'Female'
          ? 'border-pink-500 bg-pink-50 dark:bg-pink-900/20 shadow-md ring-2 ring-pink-200'
          : 'border-gray-200 dark:border-slate-700 hover:border-pink-300 dark:hover:border-pink-600'}"
      >
        <User size={24} class="text-pink-600 dark:text-pink-400" />
        <span class="text-base font-medium text-slate-700 dark:text-slate-300"
          >Female</span
        >
      </button>
    </div>
  </div>

  <!-- STEP 2: RACE (Second Priority) -->
  <div>
    <label
      class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3"
    >
      Race/Ethnicity *
    </label>
    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2">
      {#each raceOptions as race}
        <button
          type="button"
          onclick={() => updateBasic({ race: race.id })}
          class="flex items-center gap-2 p-2.5 rounded-lg border-2 transition-all {$companionForm
            .basic.race === race.id
            ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20 shadow-md ring-2 ring-purple-200'
            : 'border-gray-200 dark:border-slate-700 hover:border-purple-300 dark:hover:border-purple-600'}"
        >
          {#if race.icon}
            {@const IconComponent = race.icon}
            <IconComponent
              size={18}
              class="text-purple-600 dark:text-purple-400"
            />
          {/if}
          <span class="text-xs font-medium text-slate-700 dark:text-slate-300"
            >{race.label}</span
          >
        </button>
      {/each}
    </div>
  </div>

  <!-- STEP 3: Avatar Selection (Vector Silhouettes) -->
  <div>
    <label
      class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3"
    >
      Choose Avatar Style *
    </label>
    <div class="grid grid-cols-4 gap-3">
      {#each avatarOptions as avatar}
        <button
          type="button"
          onclick={() => updateBasic({ avatar: avatar.id })}
          class="flex flex-col items-center justify-center gap-2 p-4 rounded-xl border-2 transition-all {$companionForm
            .basic.avatar === avatar.id
            ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20 shadow-md ring-2 ring-purple-200'
            : 'border-gray-200 dark:border-slate-700 hover:border-purple-300 dark:hover:border-purple-600 hover:scale-105'}"
        >
          {#if avatar.icon}
            {@const IconComponent = avatar.icon}
            <IconComponent
              size={32}
              class="text-slate-600 dark:text-slate-400"
            />
          {/if}
          <span
            class="text-[10px] font-medium text-slate-600 dark:text-slate-400"
            >{avatar.label}</span
          >
        </button>
      {/each}
    </div>
    <p class="text-xs text-slate-500 dark:text-slate-500 mt-2">
      💡 Clean vector avatars. AI-generated portraits coming soon!
    </p>
  </div>

  <!-- STEP 4: Name -->
  <div>
    <label
      for="name"
      class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2"
    >
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

  <!-- STEP 5: Description with AI Enhancement -->
  <div>
    <div class="flex items-center justify-between mb-2">
      <label
        for="description"
        class="block text-sm font-semibold text-slate-700 dark:text-slate-300"
      >
        Short Description *
      </label>
      <button
        type="button"
        onclick={enhanceDescription}
        disabled={isEnhancingDesc || !$companionForm.basic.name}
        class="text-xs px-3 py-1 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-medium rounded-full transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-1"
      >
        {#if isEnhancingDesc}
          <span class="animate-spin">⏳</span>
          <span>Enhancing...</span>
        {:else}
          <Sparkles size={12} />
          <span>Enhance</span>
        {/if}
      </button>
    </div>
    <input
      id="description"
      type="text"
      value={$companionForm.basic.description}
      oninput={(e) => updateBasic({ description: e.currentTarget.value })}
      placeholder="One-line tagline (e.g., 'Your creative companion')"
      class="w-full px-4 py-3 bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 outline-none transition-all"
    />
    {#if enhanceError}
      <p class="text-xs text-red-600 dark:text-red-400 mt-1">{enhanceError}</p>
    {:else}
      <p class="text-xs text-slate-500 dark:text-slate-500 mt-1">
        💡 Click "Enhance" to let AI write a compelling description for you
      </p>
    {/if}
  </div>

  <!-- STEP 6: Category -->
  <div>
    <label
      class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3"
    >
      Category *
    </label>
    <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
      {#each categoryOptions as cat}
        <button
          type="button"
          onclick={() => updateBasic({ category: cat.id })}
          class="flex items-center gap-3 p-3 rounded-xl border-2 transition-all {$companionForm
            .basic.category === cat.id
            ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20 shadow-md ring-2 ring-purple-200'
            : 'border-gray-200 dark:border-slate-700 hover:border-purple-300 dark:hover:border-purple-600'}"
        >
          <div class={cat.color}>
            <svelte:component this={cat.icon} size={20} strokeWidth={2.5} />
          </div>
          <span class="text-sm font-medium text-slate-700 dark:text-slate-300"
            >{cat.label}</span
          >
        </button>
      {/each}
    </div>
  </div>
</div>
