<script lang="ts">
  import MainLayout from '@components/layouts/MainLayout.svelte';
  import HomePage from '@components/pages/HomePage.svelte';
  import ChatInterface from '@components/chat/ChatInterface.svelte';
  import { router } from '@stores/router';
  import { mockCharacters } from '@lib/data/mockData';

  let routerState = $state({ currentRoute: 'home', selectedCharacterId: null });

  router.subscribe(state => {
    routerState = state;
  });

  const selectedCharacter = $derived(
    routerState.selectedCharacterId
      ? mockCharacters.find(c => c.id === routerState.selectedCharacterId)
      : null
  );

  function handleCharacterSelect(characterId: string) {
    router.navigateToChat(characterId);
  }

  function handleBackToHome() {
    router.navigateToHome();
  }
</script>

{#if routerState.currentRoute === 'home'}
  <MainLayout>
    <HomePage onCharacterSelect={handleCharacterSelect} />
  </MainLayout>
{:else if routerState.currentRoute === 'chat'}
  <MainLayout 
    showBackButton={true} 
    onBackClick={handleBackToHome}
    title={selectedCharacter?.name || 'Chat'}
  >
    <ChatInterface character={selectedCharacter} />
  </MainLayout>
{/if}
