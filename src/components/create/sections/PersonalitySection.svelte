<script lang="ts">
  import { updatePersonality, companionForm } from '@stores/companionForm';
  import { generateCharacterDetails } from '@services/smartGenerator';
  
  let isGenerating = $state(false);
  let generationError = $state('');

  async function handleAutoGenerate() {
    // Validation: Need at least name, gender, race, category, description
    const { name, gender, race, category, description } = $companionForm.basic;
    
    if (!name || !description || description.length < 10) {
      generationError = '⚠️ Please complete Step 1 (Name & Description) first!';
      setTimeout(() => generationError = '', 3000);
      return;
    }

    isGenerating = true;
    generationError = '';

    try {
      const result = await generateCharacterDetails({
        name,
        gender,
        race,
        category,
        description
      });

      updatePersonality({
        traits: result.personality,
        background: result.background
      });
    } catch (error) {
      console.error('Generation failed:', error);
      generationError = '❌ Generation failed. Please try again or write manually.';
    } finally {
      isGenerating = false;
    }
  }
</script>

<div class="space-y-6">
  <div class="text-center mb-6">
    <h2 class="text-2xl font-bold text-slate-900 dark:text-slate-100 mb-2">
      <span class="text-3xl mr-2">🧠</span> Personality & Background
    </h2>
    <p class="text-sm text-slate-600 dark:text-slate-400">
      Definisikan traits dan latar belakang karakter
    </p>
  </div>

  <!-- Smart Auto-Generate Button -->
  <div class="bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 p-4 rounded-xl border border-purple-200 dark:border-purple-800">
    <div class="flex items-start gap-3">
      <div class="flex-1">
        <div class="flex items-center gap-2 mb-1">
          <span class="text-lg">✨</span>
          <h3 class="font-semibold text-slate-800 dark:text-slate-200">Smart Auto-Generate</h3>
        </div>
        <p class="text-xs text-slate-600 dark:text-slate-400">
          Biarkan AI membuat personality & background otomatis berdasarkan identitas karakter
        </p>
      </div>
      <button
        type="button"
        onclick={handleAutoGenerate}
        disabled={isGenerating}
        class="px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-medium rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 shadow-md"
      >
        {#if isGenerating}
          <span class="animate-spin">⏳</span>
          <span>Generating...</span>
        {:else}
          <span>✨</span>
          <span>Generate</span>
        {/if}
      </button>
    </div>
    {#if generationError}
      <div class="mt-2 text-sm text-red-600 dark:text-red-400">
        {generationError}
      </div>
    {/if}
  </div>

  <!-- Personality Traits -->
  <div>
    <label for="traits" class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">
      Personality Traits *
    </label>
    <textarea
      id="traits"
      value={$companionForm.personality.traits}
      oninput={(e) => updatePersonality({ traits: e.currentTarget.value })}
      placeholder="e.g., Calm, empathetic, curious, loves deep conversations..."
      rows="4"
      class="w-full px-4 py-3 bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 outline-none transition-all resize-none"
    ></textarea>
    <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">
      💡 Jelaskan karakter personality seperti tenang, empati, ceria, misterius, dll.
    </p>
  </div>

  <!-- Background & Lore -->
  <div>
    <label for="background" class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">
      Background & Lore <span class="text-xs text-slate-500">(Opsional)</span>
    </label>
    <textarea
      id="background"
      value={$companionForm.personality.background}
      oninput={(e) => updatePersonality({ background: e.currentTarget.value })}
      placeholder="Their story, profession, where they come from... (optional but makes them richer)"
      rows="4"
      class="w-full px-4 py-3 bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 outline-none transition-all resize-none"
    ></textarea>
    <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">
      💡 Cerita mereka, profesi, asal-usul — ini membuat karakter lebih kaya & immersive
    </p>
  </div>
</div>
