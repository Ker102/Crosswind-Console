<script lang="ts">
  import type { Insight } from '../types'

  export let insight: Insight
  export let accent = '#9d4edd'

  const metadataEntries = Object.entries(insight.metadata ?? {})
</script>

<article class="card" style={`--accent: ${accent}`}>
  <header>
    <p class="eyebrow">{insight.id}</p>
    <h3>{insight.title}</h3>
  </header>
  <p class="description">{insight.description}</p>

  {#if metadataEntries.length}
    <dl>
      {#each metadataEntries as [key, value]}
        <div>
          <dt>{key}</dt>
          <dd>{value as string}</dd>
        </div>
      {/each}
    </dl>
  {/if}

  {#if insight.source}
    <a class="source" href={insight.source} target="_blank" rel="noreferrer">View source ↗</a>
  {/if}
</article>

<style>
  .card {
    border-radius: 1rem;
    background: rgba(15, 15, 30, 0.85);
    padding: 1.25rem;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.35);
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  header h3 {
    margin: 0.25rem 0 0;
    font-size: 1.1rem;
  }

  .eyebrow {
    text-transform: uppercase;
    letter-spacing: 0.2em;
    font-size: 0.7rem;
    color: rgba(255, 255, 255, 0.45);
  }

  .description {
    margin: 0;
    color: rgba(255, 255, 255, 0.85);
  }

  dl {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 0.5rem 1rem;
    margin: 0;
  }

  dt {
    text-transform: uppercase;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    color: rgba(255, 255, 255, 0.45);
  }

  dd {
    margin: 0;
    font-weight: 600;
    color: var(--accent);
  }

  .source {
    margin-top: auto;
    color: var(--accent);
    text-decoration: none;
    font-weight: 600;
  }
</style>
