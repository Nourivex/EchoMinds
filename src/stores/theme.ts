import { writable } from 'svelte/store';

// Check if we're in browser
const isBrowser = typeof window !== 'undefined';

// Get initial theme from localStorage or default to dark
const initialTheme = isBrowser 
  ? (localStorage.getItem('theme') as 'light' | 'dark') || 'dark'
  : 'dark';

// Set initial class immediately on page load
if (isBrowser) {
  document.documentElement.classList.remove('light', 'dark');
  document.documentElement.classList.add(initialTheme);
}

export const theme = writable<'light' | 'dark'>(initialTheme);

// Subscribe to changes and update localStorage + HTML class
if (isBrowser) {
  theme.subscribe(value => {
    localStorage.setItem('theme', value);
    // Remove both classes first, then add the active one
    document.documentElement.classList.remove('light', 'dark');
    document.documentElement.classList.add(value);
  });
}

export function toggleTheme() {
  theme.update(current => current === 'dark' ? 'light' : 'dark');
}
