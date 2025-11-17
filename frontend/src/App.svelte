<script lang="ts">
  import SceneCanvas from './lib/components/SceneCanvas.svelte'
  import InsightCard from './lib/components/InsightCard.svelte'
  import {
    askLLM,
    categoryMeta,
    errorStore,
    infoChips,
    insightsStore,
    llmLatencyStore,
    llmOutputStore,
    loadingStore,
    promptStore,
    selectedDomain,
    setDomain,
    summaryStore,
    triggerDiscovery,
  } from './lib/state'
  import type { Domain } from './lib/types'

  const domainEntries = Object.entries(categoryMeta) as [Domain, (typeof categoryMeta)[Domain]][]

  function pickDomain(domain: Domain) {
    setDomain(domain)
  }

  async function submitDiscovery(event: SubmitEvent) {
    event.preventDefault()
    await triggerDiscovery($promptStore)
  }

  async function askGemini() {
    if (!$promptStore) return
    await askLLM($promptStore)
  }
</script>

<div class="page">
  <header class="hero">
    <div class="hero__scene">
      <SceneCanvas />
    </div>
    <div class="hero__copy">
      <p class="eyebrow">Cross-domain intelligence</p>
      <h1>{categoryMeta[$selectedDomain].title}</h1>
      <p class="lede">{categoryMeta[$selectedDomain].description}</p>
      <div class="chips">
        {#each $infoChips as chip}
          <span>{chip}</span>
        {/each}
      </div>
    </div>
  </header>

  <main class="deck">
    <section class="panel">
      <div class="panel__tabs">
        {#each domainEntries as [domain, meta]}
          <button
            type="button"
            class:selected={domain === $selectedDomain}
            style={`--accent: ${meta.accent}`}
            on:click={() => pickDomain(domain)}
          >
            <span>{meta.title}</span>
          </button>
        {/each}
      </div>

      <form class="prompt" on:submit={submitDiscovery}>
        <label for="prompt">Guide the search</label>
        <textarea
          id="prompt"
          name="prompt"
          bind:value={$promptStore}
          placeholder="Ex: remote ai research roles enabling climate modeling"
        ></textarea>
        <div class="actions">
          <button type="submit" class="primary" disabled={$loadingStore}>
            {#if $loadingStore}
              Running...
            {:else}
              Discover {categoryMeta[$selectedDomain].title}
            {/if}
          </button>
          <button type="button" on:click={askGemini} disabled={$loadingStore || !$promptStore}>
            Ask Gemini
          </button>
        </div>
      </form>

      {#if $errorStore}
        <div class="alert">{$errorStore}</div>
      {/if}

      <section class="summary">
        <h2>LLM synthesis</h2>
        <p>{$llmOutputStore || $summaryStore}</p>
        {#if $llmLatencyStore}
          <small>Latency: {$llmLatencyStore.toFixed(0)}ms</small>
        {/if}
      </section>
    </section>

    <section class="insights">
      <header>
        <h2>Signals</h2>
        <p>Cards update with every discovery run.</p>
      </header>
      <div class="insights__grid">
        {#if $insightsStore.length === 0}
          <p class="placeholder">No signals yet. Prompt the agent to fetch fresh data.</p>
        {:else}
          {#each $insightsStore as insight}
            <InsightCard insight={insight} accent={categoryMeta[$selectedDomain].accent} />
          {/each}
        {/if}
      </div>
    </section>
  </main>
</div>

<style>
  :global(body) {
    margin: 0;
    font-family: 'Space Grotesk', 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    background: radial-gradient(circle at top, #10051c, #030309 50%, #010102 100%);
    color: #fff;
    min-height: 100vh;
  }

  .page {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1.5rem 4rem;
    display: flex;
    flex-direction: column;
    gap: 2rem;
  }

  .hero {
    display: grid;
    grid-template-columns: minmax(280px, 1fr) 1fr;
    gap: 1.5rem;
    align-items: stretch;
  }

  .hero__scene {
    min-height: 320px;
  }

  .hero__copy {
    background: rgba(10, 10, 20, 0.85);
    border-radius: 1.5rem;
    padding: 1.5rem;
    border: 1px solid rgba(255, 255, 255, 0.05);
  }

  .eyebrow {
    text-transform: uppercase;
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    color: rgba(255, 255, 255, 0.65);
  }

  .lede {
    font-size: 1.1rem;
    color: rgba(255, 255, 255, 0.85);
  }

  .chips {
    display: inline-flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 1rem;
  }

  .chips span {
    border-radius: 999px;
    padding: 0.35rem 0.9rem;
    background: rgba(255, 255, 255, 0.08);
    font-size: 0.8rem;
  }

  .deck {
    display: grid;
    grid-template-columns: minmax(280px, 380px) 1fr;
    gap: 1.5rem;
  }

  .panel {
    background: rgba(10, 10, 20, 0.9);
    border-radius: 1.5rem;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    border: 1px solid rgba(255, 255, 255, 0.05);
  }

  .panel__tabs {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 0.5rem;
  }

  .panel__tabs button {
    border-radius: 1rem;
    border: 1px solid transparent;
    background: rgba(255, 255, 255, 0.04);
    color: #fff;
    padding: 0.75rem;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .panel__tabs button.selected {
    border-color: var(--accent);
    box-shadow: 0 0 20px color-mix(in srgb, var(--accent), transparent 60%);
  }

  form.prompt {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  form label {
    font-size: 0.9rem;
    font-weight: 600;
  }

  textarea {
    min-height: 120px;
    background: rgba(0, 0, 0, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 1rem;
    color: #fff;
    padding: 1rem;
    resize: vertical;
  }

  .actions {
    display: flex;
    gap: 0.75rem;
  }

  .actions button {
    flex: 1;
    border-radius: 999px;
    border: none;
    padding: 0.75rem 1rem;
    font-weight: 600;
    cursor: pointer;
  }

  .actions .primary {
    background: #7b2cbf;
    color: #fff;
  }

  .alert {
    background: rgba(230, 57, 70, 0.15);
    border: 1px solid rgba(230, 57, 70, 0.4);
    padding: 0.75rem 1rem;
    border-radius: 0.75rem;
  }

  .summary {
    background: rgba(0, 0, 0, 0.35);
    border-radius: 1rem;
    padding: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.06);
  }

  .insights {
    background: rgba(10, 10, 20, 0.8);
    border-radius: 1.5rem;
    padding: 1.5rem;
    border: 1px solid rgba(255, 255, 255, 0.05);
  }

  .insights__grid {
    margin-top: 1rem;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1rem;
  }

  .placeholder {
    color: rgba(255, 255, 255, 0.6);
  }

  @media (max-width: 900px) {
    .hero {
      grid-template-columns: 1fr;
    }
    .deck {
      grid-template-columns: 1fr;
    }
  }
</style>
