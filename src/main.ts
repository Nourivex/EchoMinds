import { mount } from 'svelte'
import './app.css'
import App from './App.svelte'

// Initialize theme before mounting app
const savedTheme = localStorage.getItem('theme') as 'light' | 'dark' || 'dark';
document.documentElement.classList.add(savedTheme);

const app = mount(App, {
  target: document.getElementById('app')!,
})

export default app
