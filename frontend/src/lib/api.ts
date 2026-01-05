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
  const url = `${API_BASE_URL}${path}`
  console.log('[API] GET request:', url)
  try {
    const response = await fetch(url)
    console.log('[API] Response status:', response.status)
    if (!response.ok) {
      const text = await response.text()
      console.error('[API] Error response:', text)
      throw new Error('API request failed')
    }
    const data = await response.json()
    console.log('[API] Response data:', data)
    return data as T
  } catch (e) {
    console.error('[API] Fetch error:', e)
    throw e
  }
}

export function fetchDiscovery(payload: DiscoveryRequest) {
  return request<DiscoveryResponse>('/discovery/', payload)
}

export function sendLLMPrompt(payload: LLMRequest) {
  return request<LLMResponse>('/llm/prompt', payload)
}

// Autocomplete API
export type AutocompleteItem = {
  value: string;
  label: string;
  type?: "city" | "airport";
  airportCount?: number;
}

export function searchAirports(query: string): Promise<AutocompleteItem[]> {
  return get<AutocompleteItem[]>(`/autocomplete/airports?q=${encodeURIComponent(query)}`)
}

export function searchCurrencies(query: string): Promise<AutocompleteItem[]> {
  return get<AutocompleteItem[]>(`/autocomplete/currencies?q=${encodeURIComponent(query)}`)
}

// Sandbox API (RAG + MCP)
export interface SandboxRequest {
  prompt: string;
  namespace: 'travel' | 'jobs' | 'trends';
  history?: { role: 'user' | 'model'; content: string }[];
}

export interface SandboxResponse {
  output: string;
  model: string;
  latency_ms: number;
  tools_used: string[];
  rag_context: { title: string; content: string }[];
}

export function sendSandboxPrompt(payload: SandboxRequest) {
  return request<SandboxResponse>('/llm/sandbox', payload)
}

// MCP Tools API
export interface MCPTool {
  name: string;
  description?: string;
  server: string;
  category: string;
}

export interface MCPToolForm {
  toolName: string;
  serverName: string;
  description?: string;
  fields: {
    name: string;
    type: string;
    label: string;
    required: boolean;
    description?: string;
    options?: string[];
  }[];
}

export function getMCPServers() {
  return get<{ servers: { name: string; category: string }[] }>('/mcp/servers')
}

export function getMCPTools(serverName: string) {
  return get<{ server: string; tools: MCPTool[]; count: number }>(`/mcp/tools/${serverName}`)
}

export function getMCPToolForm(serverName: string, toolName: string) {
  return get<MCPToolForm>(`/mcp/tools/${serverName}/${toolName}/form`)
}

export function executeMCPTool(serverName: string, toolName: string, args: Record<string, any>) {
  return request<{ success: boolean; result: any[] }>(`/mcp/tools/${serverName}/${toolName}/execute`, args)
}
