<script lang="ts">
  import LandingPage from "./lib/components/LandingPage.svelte";
  import AgentPage from "./lib/components/AgentPage.svelte";

  let currentPage = "landing"; // landing, agent
  let selectedCategory = "travel";

  const handleCategorySelect = (category: string) => {
    selectedCategory = category;
    currentPage = "agent";
  };

  const handleBack = () => {
    currentPage = "landing";
  };
</script>

{#if currentPage === "landing"}
  <LandingPage onSelectCategory={handleCategorySelect} />
{:else}
  <AgentPage
    category={selectedCategory}
    onBack={handleBack}
    onCategoryChange={handleCategorySelect}
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
