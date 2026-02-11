<script lang="ts">
  import { theme, toggleTheme } from '@stores/theme';
  import { getModelConfig, listModels } from '@services/api';
  import { Sun, Moon, Bell, Shield, Palette, Globe, HelpCircle, Cpu, Check, X } from '@lucide/svelte';

  let currentTheme = $state<'light' | 'dark'>('dark');
  let notifications = $state(true);
  let soundEffects = $state(true);
  
  // Backend config state
  let selectedModel = $state<string>('');
  let temperature = $state<number>(0.7);
  let max_tokens = $state<number>(512);
  let availableModels = $state<string[]>([]);
  let loadingConfig = $state(true);
  let configError = $state<string | null>(null);
  let saveSuccess = $state(false);
  let saveError = $state<string | null>(null);
  let isSaving = $state(false);

  // Original values to detect changes
  let originalModel = $state<string>('');
  let originalTemp = $state<number>(0.7);
  let originalMaxTokens = $state<number>(512);

  // Check if settings changed
  const hasChanges = $derived(
    selectedModel !== originalModel ||
    temperature !== originalTemp ||
    max_tokens !== originalMaxTokens
  );

  theme.subscribe(value => {
    currentTheme = value;
  });

  // Load backend config
  async function loadBackendConfig() {
    try {
      loadingConfig = true;
      configError = null;
      
      const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      
      const [configRes, modelsRes] = await Promise.all([
        fetch(`${apiBase}/api/config`),
        fetch(`${apiBase}/api/models`)
      ]);
      
      if (!configRes.ok || !modelsRes.ok) {
        throw new Error('Backend tidak tersedia');
      }
      
      const config = await configRes.json();
      const models = await modelsRes.json();
      
      selectedModel = config.model || 'llama3.2:3b';
      temperature = config.temperature || 0.7;
      max_tokens = config.max_tokens || 512;
      availableModels = models || [];
      
      // Store original values
      originalModel = selectedModel;
      originalTemp = temperature;
      originalMaxTokens = max_tokens;
    } catch (err) {
      configError = err instanceof Error ? err.message : 'Gagal memuat konfigurasi';
      console.error('Failed to load backend config:', err);
    } finally {
      loadingConfig = false;
    }
  }

  // Save config to backend
  async function saveConfig() {
    try {
      isSaving = true;
      saveError = null;
      saveSuccess = false;
      
      const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      
      const response = await fetch(`${apiBase}/api/config`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: selectedModel,
          temperature: temperature,
          max_tokens: max_tokens
        })
      });
      
      if (!response.ok) {
        throw new Error('Gagal menyimpan konfigurasi');
      }
      
      const updated = await response.json();
      
      // Update original values
      originalModel = updated.model;
      originalTemp = updated.temperature;
      originalMaxTokens = updated.max_tokens;
      
      saveSuccess = true;
      
      // Hide success message after 3 seconds
      setTimeout(() => {
        saveSuccess = false;
      }, 3000);
      
    } catch (err) {
      saveError = err instanceof Error ? err.message : 'Gagal menyimpan';
      setTimeout(() => {
        saveError = null;
      }, 5000);
    } finally {
      isSaving = false;
    }
  }

  // Reset to original values
  function resetChanges() {
    selectedModel = originalModel;
    temperature = originalTemp;
    max_tokens = originalMaxTokens;
  }

  // Load on mount
  $effect(() => {
    loadBackendConfig();
  });

  const settingsSections = $derived([
    {
      title: 'Appearance',
      icon: Palette,
      items: [
        {
          id: 'theme',
          label: 'Theme',
          description: 'Choose your preferred color theme',
          component: 'theme-toggle'
        }
      ]
    },
    {
      title: 'AI Model Configuration',
      icon: Cpu,
      items: [
        {
          id: 'model',
          label: 'LLM Model',
          description: 'Select the AI model to use',
          component: 'model-select'
        },
        {
          id: 'temperature',
          label: 'Temperature',
          description: 'Controls creativity and randomness (0.0 = predictable, 2.0 = creative)',
          component: 'temperature-slider'
        },
        {
          id: 'max_tokens',
          label: 'Max Tokens',
          description: 'Maximum response length',
          component: 'tokens-slider'
        }
      ]
    },
    {
      title: 'Notifications',
      icon: Bell,
      items: [
        {
          id: 'notifications',
          label: 'Push Notifications',
          description: 'Receive notifications for new messages',
          component: 'toggle',
          value: notifications,
          onChange: () => notifications = !notifications
        },
        {
          id: 'sounds',
          label: 'Sound Effects',
          description: 'Play sounds for messages and actions',
          component: 'toggle',
          value: soundEffects,
          onChange: () => soundEffects = !soundEffects
        }
      ]
    },
    {
      title: 'About',
      icon: HelpCircle,
      items: [
        {
          id: 'version',
          label: 'Version',
          description: 'Backend v2.0.0 • Frontend v1.0.0',
          component: 'text'
        },
        {
          id: 'backend',
          label: 'Backend Status',
          description: configError ? '❌ Offline' : '✅ Online',
          component: 'text'
        }
      ]
    }
  ]);
</script>

<div class="h-full overflow-y-auto bg-gradient-to-b from-gray-50 to-white dark:from-slate-950 dark:to-slate-900 px-4 sm:px-6 py-8 pb-20">
  <div class="max-w-3xl mx-auto">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl sm:text-4xl font-bold text-slate-900 dark:text-slate-100 mb-2">Settings</h1>
      <p class="text-slate-600 dark:text-slate-400">Customize your experience</p>
    </div>

    {#if loadingConfig}
      <!-- Loading -->
      <div class="text-center py-8">
        <div class="w-12 h-12 border-4 border-purple-500/30 border-t-purple-500 rounded-full animate-spin mb-3 mx-auto"></div>
        <p class="text-sm text-slate-600 dark:text-slate-400">Loading configuration...</p>
      </div>
    {:else}
      <!-- Settings Sections -->
      <div class="space-y-6">
        {#each settingsSections as section}
          <div class="bg-white dark:bg-slate-800/50 rounded-2xl border border-gray-200 dark:border-slate-700 overflow-hidden">
            <!-- Section Header -->
            <div class="px-6 py-4 border-b border-gray-200 dark:border-slate-700 flex items-center gap-3">
              <section.icon size={20} class="text-purple-500" />
              <h2 class="text-lg font-semibold text-slate-900 dark:text-slate-100">{section.title}</h2>
            </div>

            <!-- Section Items -->
            <div class="divide-y divide-gray-200 dark:divide-slate-700">
              {#each section.items as item}
                <div class="px-6 py-4 flex items-center justify-between gap-4">
                  <div class="flex-1 min-w-0">
                    <h3 class="text-sm font-medium text-slate-900 dark:text-slate-100 mb-0.5">{item.label}</h3>
                    <p class="text-xs text-slate-500 dark:text-slate-400">{item.description}</p>
                  </div>

                  <!-- Component based on type -->
                  {#if item.component === 'theme-toggle'}
                    <button
                      onclick={toggleTheme}
                      class="flex items-center gap-2 px-4 py-2 bg-gray-100 dark:bg-slate-700 hover:bg-gray-200 dark:hover:bg-slate-600 rounded-lg transition-colors"
                    >
                      {#if currentTheme === 'dark'}
                        <Moon size={16} />
                        <span class="text-sm font-medium text-slate-700 dark:text-slate-300">Dark</span>
                      {:else}
                        <Sun size={16} />
                        <span class="text-sm font-medium text-slate-700 dark:text-slate-300">Light</span>
                      {/if}
                    </button>
                  {:else if item.component === 'model-select'}
                    <select
                      bind:value={selectedModel}
                      class="px-4 py-2 bg-gray-100 dark:bg-slate-700 border border-gray-300 dark:border-slate-600 rounded-lg text-sm text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all min-w-[200px]"
                    >
                      {#if availableModels.length === 0}
                        <option value={selectedModel}>{selectedModel}</option>
                      {:else}
                        {#each availableModels as model}
                          <option value={model}>{model}</option>
                        {/each}
                      {/if}
                    </select>
                  {:else if item.component === 'temperature-slider'}
                    <div class="flex items-center gap-4 min-w-[280px]">
                      <input
                        type="range"
                        bind:value={temperature}
                        min="0"
                        max="2"
                        step="0.1"
                        class="flex-1 h-2 bg-gray-200 dark:bg-slate-700 rounded-lg appearance-none cursor-pointer accent-purple-500"
                      />
                      <span class="text-sm font-medium text-slate-900 dark:text-slate-100 min-w-[3ch] text-center">{temperature.toFixed(1)}</span>
                    </div>
                  {:else if item.component === 'tokens-slider'}
                    <div class="flex items-center gap-4 min-w-[280px]">
                      <input
                        type="range"
                        bind:value={max_tokens}
                        min="50"
                        max="4096"
                        step="50"
                        class="flex-1 h-2 bg-gray-200 dark:bg-slate-700 rounded-lg appearance-none cursor-pointer accent-purple-500"
                      />
                      <span class="text-sm font-medium text-slate-900 dark:text-slate-100 min-w-[4ch] text-right">{max_tokens}</span>
                    </div>
                  {:else if item.component === 'toggle'}
                    <button
                      onclick={item.onChange}
                      class="relative w-12 h-6 rounded-full transition-colors {item.value ? 'bg-purple-600' : 'bg-gray-300 dark:bg-slate-600'}"
                    >
                      <div class="absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full shadow-md transition-transform {item.value ? 'translate-x-6' : 'translate-x-0'}"></div>
                    </button>
                  {:else if item.component === 'text'}
                    <span class="text-sm text-slate-500 dark:text-slate-400">{item.description}</span>
                  {/if}
                </div>
              {/each}
            </div>
          </div>
        {/each}
      </div>

      <!-- Save/Reset Buttons (only show when changes exist) -->
      {#if hasChanges}
        <div class="mt-6 p-4 bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-800 rounded-2xl">
          <div class="flex items-center justify-between gap-4">
            <div class="flex-1">
              <p class="text-sm font-medium text-purple-900 dark:text-purple-100">
                Unsaved changes
              </p>
              <p class="text-xs text-purple-700 dark:text-purple-300">
                Your AI model configuration has been modified
              </p>
            </div>
            <div class="flex gap-2">
              <button
                onclick={resetChanges}
                disabled={isSaving}
                class="px-4 py-2 bg-white dark:bg-slate-800 border border-gray-300 dark:border-slate-600 text-slate-700 dark:text-slate-300 rounded-lg text-sm font-medium hover:bg-gray-50 dark:hover:bg-slate-700 transition-colors disabled:opacity-50"
              >
                Reset
              </button>
              <button
                onclick={saveConfig}
                disabled={isSaving}
                class="px-6 py-2 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 text-white rounded-lg text-sm font-medium shadow-lg shadow-purple-500/30 transition-all disabled:opacity-50 flex items-center gap-2"
              >
                {#if isSaving}
                  <div class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                  Saving...
                {:else}
                  <Check size={16} />
                  Save Changes
                {/if}
              </button>
            </div>
          </div>
        </div>
      {/if}

      <!-- Success Alert -->
      {#if saveSuccess}
        <div class="mt-4 p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-2xl flex items-center gap-3">
          <div class="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
            <Check size={16} class="text-white" />
          </div>
          <div class="flex-1">
            <p class="text-sm font-medium text-green-900 dark:text-green-100">
              Configuration saved successfully!
            </p>
            <p class="text-xs text-green-700 dark:text-green-300">
              Your changes have been applied to the backend
            </p>
          </div>
        </div>
      {/if}

      <!-- Error Alert -->
      {#if saveError}
        <div class="mt-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-2xl flex items-center gap-3">
          <div class="w-8 h-8 bg-red-500 rounded-full flex items-center justify-center">
            <X size={16} class="text-white" />
          </div>
          <div class="flex-1">
            <p class="text-sm font-medium text-red-900 dark:text-red-100">
              Failed to save configuration
            </p>
            <p class="text-xs text-red-700 dark:text-red-300">
              {saveError}
            </p>
          </div>
        </div>
      {/if}

      <!-- Footer -->
      <div class="mt-8 mb-8 text-center text-sm text-slate-500 dark:text-slate-400">
        <p>© 2026 EchoMinds. Made with 💜 for meaningful connections.</p>
      </div>
    {/if}
  </div>
</div>
