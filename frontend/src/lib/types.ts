export type Domain = 'jobs' | 'travel' | 'trends'

export interface Insight {
  id: string
  title: string
  description: string
  score?: number | null
  source?: string | null
  metadata?: Record<string, unknown>
}

export interface DiscoveryRequest {
  domain: Domain
  prompt?: string
  filters?: Record<string, unknown>
}

export interface DiscoveryResponse {
  domain: Domain
  summary: string
  items: Insight[]
  llm_trace?: string | null
}

export interface TravelIntent {
  mode: 'detailed' | 'sandbox'
  transportMode: 'all' | 'flights' | 'ground' | 'sea'
  tripType: 'one-way' | 'round-trip' | 'outbound-window' | 'whole-month'
  from: string
  to: string
  departDate?: string
  returnDate?: string
  windowStart?: string
  windowEnd?: string
  wholeMonth?: string
  cabinClass?: 'ECONOMY' | 'ECONOMY_PREMIUM' | 'BUSINESS' | 'FIRST_CLASS'
  directOnly?: boolean
  adults?: number
  children?: number
  infants?: number
  currency?: string
  accommodations?: {
    enabled: boolean
    city?: string
    priceMin?: number
    priceMax?: number
    minRating?: number
    maxResults?: number
    providers?: string[]
  }
}

export interface LLMRequest {
  mode?: Domain | 'general'
  prompt: string
  context?: Insight[]
  history?: { role: 'user' | 'model'; content: string }[]
  travel_intent?: TravelIntent
}

export interface LLMResponse {
  output: string
  model: string
  latency_ms?: number | null
}

export interface UserSession {
  user?: {
    id: string
    name?: string | null
    email?: string | null
    image?: string | null
  }
  expires?: string
}

export interface StoredProgressPayload {
  summary: string
  items: Insight[]
}

export interface StoredProgress {
  domain: Domain
  prompt?: string | null
  payload?: StoredProgressPayload | null
  updatedAt?: string | null
}
