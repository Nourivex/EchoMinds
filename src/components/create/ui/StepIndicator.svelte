<script lang="ts">
  interface Props {
    totalSteps: number;
    currentStep: number;
    stepLabels: string[];
  }

  let { totalSteps, currentStep, stepLabels }: Props = $props();
</script>

<div class="flex items-center justify-between mb-8">
  {#each stepLabels as label, index}
    <div class="flex items-center flex-1">
      <!-- Step Circle -->
      <div class="flex flex-col items-center">
        <div
          class="w-10 h-10 rounded-full flex items-center justify-center font-semibold transition-all {
            index < currentStep
              ? 'bg-green-500 text-white'
              : index === currentStep
              ? 'bg-purple-600 text-white ring-4 ring-purple-200 dark:ring-purple-900'
              : 'bg-gray-200 dark:bg-slate-700 text-gray-500 dark:text-slate-400'
          }"
        >
          {#if index < currentStep}
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
            </svg>
          {:else}
            {index + 1}
          {/if}
        </div>
        <span class="text-xs mt-2 font-medium {
          index === currentStep 
            ? 'text-purple-600 dark:text-purple-400' 
            : 'text-gray-500 dark:text-slate-400'
        }">{label}</span>
      </div>
      
      <!-- Connector Line -->
      {#if index < totalSteps - 1}
        <div class="flex-1 h-0.5 mx-2 {
          index < currentStep 
            ? 'bg-green-500' 
            : 'bg-gray-200 dark:bg-slate-700'
        }"></div>
      {/if}
    </div>
  {/each}
</div>
