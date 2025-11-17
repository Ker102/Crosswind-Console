import type { Domain, Insight, StoredProgress, UserSession } from './types'

const AUTH_BASE_URL = (import.meta.env.VITE_AUTH_BASE_URL as string | undefined) ?? 'http://localhost:3001'

function withCredentials(init?: RequestInit): RequestInit {
  return {
    credentials: 'include',
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers ?? {}),
    },
  }
}

export function getSignInUrl() {
  return `${AUTH_BASE_URL}/api/auth/signin`
}

export function getSignOutUrl() {
  return `${AUTH_BASE_URL}/api/auth/signout`
}

export async function fetchSession(): Promise<UserSession | null> {
  try {
    const response = await fetch(`${AUTH_BASE_URL}/api/session`, withCredentials())
    if (!response.ok) {
      return null
    }
    const data = (await response.json()) as { authenticated: boolean; session?: UserSession | null }
    return data.authenticated && data.session ? data.session : null
  } catch (error) {
    console.error('Failed to fetch session', error)
    return null
  }
}

export async function loadProgress(domain: Domain): Promise<StoredProgress | null> {
  try {
    const response = await fetch(`${AUTH_BASE_URL}/api/progress?domain=${domain}`, withCredentials())
    if (!response.ok) {
      return null
    }
    return (await response.json()) as StoredProgress
  } catch (error) {
    console.error('Failed to load progress', error)
    return null
  }
}

export async function saveProgress(
  domain: Domain,
  prompt: string | null,
  summary: string,
  items: Insight[]
) {
  try {
    await fetch(
      `${AUTH_BASE_URL}/api/progress`,
      withCredentials({
        method: 'POST',
        body: JSON.stringify({ domain, prompt, payload: { summary, items } }),
      })
    )
  } catch (error) {
    console.error('Failed to persist progress', error)
  }
}
