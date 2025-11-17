import { derived, get, writable } from 'svelte/store'
import { fetchDiscovery, sendLLMPrompt } from './api'
import type { Domain, Insight } from './types'

export const categoryMeta: Record<Domain, { title: string; accent: string; description: string; scene: string }> = {
  jobs: {
    title: 'Career Intelligence',
    accent: '#9d4edd',
    description: 'Curated job leads, hiring patterns, and skills spikes.',
    scene: 'orbital',
  },
  travel: {
    title: 'Travel Radar',
    accent: '#48bfe3',
    description: 'Live flight drops, coliving retreats, and nomad perks.',
    scene: 'wave',
  },
  trends: {
    title: 'Culture Pulse',
    accent: '#f4a261',
    description: 'Social formats and viral signals across major platforms.',
    scene: 'pulse',
  },
}

export const selectedDomain = writable<Domain>('jobs')
export const promptStore = writable('')
export const insightsStore = writable<Insight[]>([])
export const summaryStore = writable('Choose a category to spin up curated intelligence.')
export const loadingStore = writable(false)
export const errorStore = writable<string | null>(null)
export const llmOutputStore = writable<string>('')
export const llmLatencyStore = writable<number | null>(null)

export const infoChips = derived(selectedDomain, ($domain) => [
  categoryMeta[$domain].description,
  'Powered by Gemini + MCP connectors',
])

export async function triggerDiscovery(customPrompt?: string) {
  loadingStore.set(true)
  errorStore.set(null)
  const domain = get(selectedDomain)
  const prompt = customPrompt ?? get(promptStore)

  try {
    const response = await fetchDiscovery({ domain, prompt, filters: {} })
    insightsStore.set(response.items)
    summaryStore.set(response.summary)
    llmOutputStore.set(response.summary)
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Unknown error'
    errorStore.set(message)
  } finally {
    loadingStore.set(false)
  }
}

export async function askLLM(prompt: string) {
  loadingStore.set(true)
  errorStore.set(null)
  try {
    const response = await sendLLMPrompt({ prompt, mode: get(selectedDomain), context: get(insightsStore) })
    llmOutputStore.set(response.output)
    llmLatencyStore.set(response.latency_ms ?? null)
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Unknown error'
    errorStore.set(message)
  } finally {
    loadingStore.set(false)
  }
}

export function setDomain(domain: Domain) {
  selectedDomain.set(domain)
  summaryStore.set(categoryMeta[domain].description)
  insightsStore.set([])
}
