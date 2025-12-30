<script lang="ts">
  import LandingPage from "./lib/components/LandingPage.svelte";
  import AgentPage from "./lib/components/AgentPage.svelte";
  import {
    currentPageStore,
    selectedDomain,
    navigateToAgent,
    navigateToLanding,
  } from "./lib/state";
</script>

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
