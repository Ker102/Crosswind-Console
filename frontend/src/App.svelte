<script lang="ts">
  import LandingPage from "./lib/components/LandingPage.svelte";
  import AgentPage from "./lib/components/AgentPage.svelte";
  import {
    currentPageStore,
    selectedDomain,
    navigateToAgent,
    navigateToLanding,
  } from "./lib/state";

  // Debug logging - this will fire whenever stores change
  $: console.log(
    "[APP] Store values - page:",
    $currentPageStore,
    "domain:",
    $selectedDomain,
  );
</script>

<!-- Debug: Show current state using direct store access -->
<div
  style="position: fixed; top: 0; left: 0; background: black; color: lime; padding: 4px; z-index: 9999; font-size: 12px;"
>
  Page: {$currentPageStore} | Domain: {$selectedDomain}
</div>

{#if $currentPageStore === "landing"}
  <LandingPage onSelectCategory={(cat) => navigateToAgent(cat)} />
{:else}
  <AgentPage
    category={$selectedDomain}
    onBack={navigateToLanding}
    onCategoryChange={(cat) => navigateToAgent(cat)}
  />
{/if}

<style>
  :global(body) {
    margin: 0;
    padding: 0;
    font-family: "Inter", sans-serif;
    overflow: hidden;
  }
</style>
