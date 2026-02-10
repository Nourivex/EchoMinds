<script lang="ts">
  import { theme, toggleTheme } from '@stores/theme';
  import { Sun, Moon, Bell, Shield, Palette, Globe, HelpCircle } from '@lucide/svelte';

  let currentTheme = $state<'light' | 'dark'>('dark');
  let notifications = $state(true);
  let soundEffects = $state(true);

  theme.subscribe(value => {
    currentTheme = value;
  });

  const settingsSections = [
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
          description: '1.0.0',
          component: 'text'
        }
      ]
    }
  ];
</script>

<div class="h-full overflow-y-auto bg-gradient-to-b from-gray-50 to-white dark:from-slate-950 dark:to-slate-900 px-4 sm:px-6 py-8">
  <div class="max-w-3xl mx-auto">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl sm:text-4xl font-bold text-slate-900 dark:text-slate-100 mb-2">Settings</h1>
      <p class="text-slate-600 dark:text-slate-400">Customize your experience</p>
    </div>

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

    <!-- Footer -->
    <div class="mt-8 mb-8 text-center text-sm text-slate-500 dark:text-slate-400">
      <p>© 2026 EchoMinds. Made with 💜 for meaningful connections.</p>
    </div>
  </div>
</div>
