<script lang="ts">
  import { onMount } from 'svelte';
  import { Sparkles, ArrowLeft, ArrowRight, Check, AlertCircle } from '@lucide/svelte';
  import { 
    companionForm, 
    currentStep, 
    stepValidation, 
    isFormValid,
    nextStep,
    prevStep,
    resetForm,
    toAPIPayload
  } from '@stores/companionForm';
  
  import StepIndicator from '@components/create/ui/StepIndicator.svelte';
  import BasicIdentitySection from '@components/create/sections/BasicIdentitySection.svelte';
  import PersonalitySection from '@components/create/sections/PersonalitySection.svelte';
  import CommunicationSection from '@components/create/sections/CommunicationSection.svelte';
  import RelationshipSection from '@components/create/sections/RelationshipSection.svelte';

  const stepLabels = [
    'Basic Identity',
    'Personality',
    'Communication',
    'Relationship'
  ];

  let isBackendAvailable = $state(false);
  let isCheckingBackend = $state(true);
  let isSubmitting = $state(false);
  let submitSuccess = $state(false);
  let submitError = $state<string | null>(null);
  let createdCharacterId = $state<string | null>(null);

  onMount(async () => {
    await checkBackend();
  });

  async function checkBackend() {
    try {
      const response = await fetch('http://localhost:8000/api/health');
      const data = await response.json();
      isBackendAvailable = data.status === 'healthy' || data.status === 'degraded';
    } catch (error) {
      isBackendAvailable = false;
    } finally {
      isCheckingBackend = false;
    }
  }

  function handlePrevious() {
    prevStep();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function handleNext() {
    const validation = $stepValidation;
    if (validation[$currentStep]) {
      nextStep();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }

  async function handleSubmit() {
    if (!$isFormValid) return;
    
    isSubmitting = true;
    submitError = null;
    
    try {
      const payload = toAPIPayload($companionForm);
      
      const response = await fetch('http://localhost:8000/api/characters', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      createdCharacterId = result.id;
      submitSuccess = true;
      
      // Reset form after 2 seconds and redirect to chat
      setTimeout(() => {
        resetForm();
        window.location.href = `/chat/${result.id}`;
      }, 2000);
      
    } catch (error) {
      submitError = error instanceof Error ? error.message : 'Failed to create character';
      console.error('Character creation error:', error);
    } finally {
      isSubmitting = false;
    }
  }

  $effect(() => {
    if (submitSuccess) {
      const timer = setTimeout(() => {
        submitSuccess = false;
      }, 5000);
      return () => clearTimeout(timer);
    }
  });

  $effect(() => {
    if (submitError) {
      const timer = setTimeout(() => {
        submitError = null;
      }, 5000);
      return () => clearTimeout(timer);
    }
  });
</script>

<svelte:head>
  <title>Create New Companion | EchoMinds</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-slate-50 via-purple-50 to-blue-50 dark:from-slate-950 dark:via-purple-950 dark:to-slate-950 py-8 px-4 pb-16">
  <div class="max-w-4xl mx-auto">
    
    <!-- Header -->
    <div class="text-center mb-8">
      <div class="inline-flex items-center gap-3 mb-4">
        <Sparkles size={40} class="text-purple-600 dark:text-purple-400" />
        <h1 class="text-4xl font-bold text-slate-900 dark:text-slate-100">
          Create Your Companion
        </h1>
      </div>
      <p class="text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
        Bangun AI companion yang personal dengan sistem 7-layer relationship. Setiap detail yang kamu atur akan membentuk kepribadian dan cara mereka berinteraksi denganmu.
      </p>
    </div>

    <!-- Backend Status Warning -->
    {#if isCheckingBackend}
      <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-xl p-4 mb-6 flex items-center gap-3">
        <div class="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
        <span class="text-sm text-blue-900 dark:text-blue-100">Checking backend availability...</span>
      </div>
    {:else if !isBackendAvailable}
      <div class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl p-4 mb-6">
        <div class="flex items-start gap-3">
          <AlertCircle size={20} class="text-red-600 flex-shrink-0 mt-0.5" />
          <div>
            <p class="font-semibold text-red-900 dark:text-red-100 mb-1">Backend Not Available</p>
            <p class="text-sm text-red-700 dark:text-red-300">
              Backend server tidak dapat diakses di <code class="px-1.5 py-0.5 bg-red-100 dark:bg-red-900/40 rounded text-xs">localhost:8000</code>. 
              Pastikan backend sudah berjalan dengan <code class="px-1.5 py-0.5 bg-red-100 dark:bg-red-900/40 rounded text-xs">python backend/main.py</code>
            </p>
          </div>
        </div>
      </div>
    {/if}

    <!-- Success Alert -->
    {#if submitSuccess}
      <div class="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-xl p-4 mb-6 animate-in fade-in slide-in-from-top-2">
        <div class="flex items-start gap-3">
          <Check size={20} class="text-green-600 flex-shrink-0 mt-0.5" />
          <div>
            <p class="font-semibold text-green-900 dark:text-green-100 mb-1">Character Created Successfully! 🎉</p>
            <p class="text-sm text-green-700 dark:text-green-300">
              Redirecting to chat in a moment...
            </p>
          </div>
        </div>
      </div>
    {/if}

    <!-- Error Alert -->
    {#if submitError}
      <div class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl p-4 mb-6 animate-in fade-in slide-in-from-top-2">
        <div class="flex items-start gap-3">
          <AlertCircle size={20} class="text-red-600 flex-shrink-0 mt-0.5" />
          <div>
            <p class="font-semibold text-red-900 dark:text-red-100 mb-1">Creation Failed</p>
            <p class="text-sm text-red-700 dark:text-red-300">{submitError}</p>
          </div>
        </div>
      </div>
    {/if}

    <!-- Wizard Container -->
    <div class="bg-white dark:bg-slate-900 rounded-2xl shadow-2xl border border-slate-200 dark:border-slate-800 overflow-hidden">
      
      <!-- Step Indicator -->
      <div class="bg-slate-50 dark:bg-slate-800/50 px-6 py-6 border-b border-slate-200 dark:border-slate-700">
        <StepIndicator 
          totalSteps={4} 
          currentStep={$currentStep} 
          stepLabels={stepLabels} 
        />
      </div>

      <!-- Form Content -->
      <div class="p-8">
        {#if $currentStep === 0}
          <BasicIdentitySection />
        {:else if $currentStep === 1}
          <PersonalitySection />
        {:else if $currentStep === 2}
          <CommunicationSection />
        {:else if $currentStep === 3}
          <RelationshipSection />
        {/if}
      </div>

      <!-- Navigation Footer -->
      <div class="bg-slate-50 dark:bg-slate-800/50 px-8 py-6 border-t border-slate-200 dark:border-slate-700 flex items-center justify-between">
        
        <!-- Previous Button -->
        <button
          type="button"
          onclick={handlePrevious}
          disabled={$currentStep === 0}
          class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl font-semibold text-sm transition-all disabled:opacity-40 disabled:cursor-not-allowed
                 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700 disabled:hover:bg-transparent"
        >
          <ArrowLeft size={18} />
          Previous
        </button>

        <!-- Step Counter -->
        <div class="text-sm font-medium text-slate-600 dark:text-slate-400">
          Step {$currentStep + 1} of {stepLabels.length}
        </div>

        <!-- Next/Submit Button -->
        {#if $currentStep < stepLabels.length - 1}
          <button
            type="button"
            onclick={handleNext}
            disabled={!$stepValidation[$currentStep]}
            class="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl font-semibold text-sm transition-all
                   bg-purple-600 hover:bg-purple-700 text-white shadow-lg shadow-purple-500/30
                   disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-purple-600"
          >
            Next
            <ArrowRight size={18} />
          </button>
        {:else}
          <button
            type="button"
            onclick={handleSubmit}
            disabled={!$isFormValid || isSubmitting || !isBackendAvailable}
            class="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl font-semibold text-sm transition-all
                   bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 
                   text-white shadow-lg shadow-purple-500/30
                   disabled:opacity-50 disabled:cursor-not-allowed disabled:from-purple-600 disabled:to-blue-600"
          >
            {#if isSubmitting}
              <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              Creating...
            {:else}
              <Check size={18} />
              Create Companion
            {/if}
          </button>
        {/if}
      </div>

    </div>

    <!-- Helper Text -->
    <div class="mt-8 mb-8 text-center">
      <p class="text-xs text-slate-500 dark:text-slate-400">
        Tip: Setiap layer relationship akan membentuk cara character merespons dan berinteraksi denganmu secara konsisten.
      </p>
    </div>

  </div>
</div>

<style>
  @keyframes fade-in {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  @keyframes slide-in-from-top-2 {
    from { transform: translateY(-0.5rem); }
    to { transform: translateY(0); }
  }

  .animate-in {
    animation: fade-in 0.3s ease-out, slide-in-from-top-2 0.3s ease-out;
  }
</style>
