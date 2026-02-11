<script lang="ts">
  import { updatePersonality, companionForm } from '@stores/companionForm';
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
