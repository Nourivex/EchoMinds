<script lang="ts">
  import Sidebar from '@components/layouts/Sidebar.svelte';
  import Topbar from '@components/layouts/Topbar.svelte';
  import HomePage from '@components/pages/HomePage.svelte';
  import MyChatsPage from '@components/pages/MyChatsPage.svelte';
  import ExplorePage from '@components/pages/ExplorePage.svelte';
  import CreatePage from '@components/pages/CreatePage.svelte';
  import SettingsPage from '@components/pages/SettingsPage.svelte';
  import { router } from '@stores/router';

  let routerState = $state({ currentRoute: 'home', selectedCharacterId: null });

  router.subscribe(state => {
    routerState = state;
  });
</script>

<div class="flex h-screen w-full bg-gray-50 dark:bg-slate-900">
  <!-- All routes dengan Sidebar -->
  <Sidebar>
    <div class="h-full flex flex-col">
      <Topbar />
      
      <!-- Content Area dengan proper spacing -->
      <div class="flex-1 overflow-hidden pb-safe">
        {#if routerState.currentRoute === 'home'}
          <HomePage />
        {:else if routerState.currentRoute === 'my-chats' || routerState.currentRoute === 'chat'}
          <MyChatsPage />
        {:else if routerState.currentRoute === 'explore'}
          <ExplorePage />
        {:else if routerState.currentRoute === 'create'}
          <CreatePage />
        {:else if routerState.currentRoute === 'settings'}
          <SettingsPage />
        {/if}
      </div>
    </div>
  </Sidebar>
</div>
