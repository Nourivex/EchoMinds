import { writable } from 'svelte/store';

// Check if we're in browser
const isBrowser = typeof window !== 'undefined';

// Get initial theme from localStorage or default to dark
const initialTheme = isBrowser 
  ? (localStorage.getItem('theme') as 'light' | 'dark') || 'dark'
  : 'dark';

export const theme = writable<'light' | 'dark'>(initialTheme);

// Subscribe to changes and update localStorage + HTML class
if (isBrowser) {
  theme.subscribe(value => {
    localStorage.setItem('theme', value);
    document.documentElement.classList.toggle('dark', value === 'dark');
    document.documentElement.classList.toggle('light', value === 'light');
  });
}

export function toggleTheme() {
  theme.update(current => current === 'dark' ? 'light' : 'dark');
}
