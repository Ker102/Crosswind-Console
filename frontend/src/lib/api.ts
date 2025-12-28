import type { DiscoveryRequest, DiscoveryResponse, LLMRequest, LLMResponse } from './types'

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL as string | undefined) ?? 'http://localhost:8000/api'

async function request<T>(path: string, payload: unknown): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    const message = await response.text()
    throw new Error(message || 'API request failed')
  }
  return response.json() as Promise<T>
}

async function get<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`)
  if (!response.ok) {
    throw new Error('API request failed')
  }
  return response.json() as Promise<T>
}

export function fetchDiscovery(payload: DiscoveryRequest) {
  return request<DiscoveryResponse>('/discovery/', payload)
}

export function sendLLMPrompt(payload: LLMRequest) {
  return request<LLMResponse>('/llm/prompt', payload)
}

// Autocomplete API
export type AutocompleteItem = { value: string; label: string }

export function searchAirports(query: string): Promise<AutocompleteItem[]> {
  return get<AutocompleteItem[]>(`/autocomplete/airports?q=${encodeURIComponent(query)}`)
}

export function searchCurrencies(query: string): Promise<AutocompleteItem[]> {
  return get<AutocompleteItem[]>(`/autocomplete/currencies?q=${encodeURIComponent(query)}`)
}

