# Crosswind-Console Project Context

## Project Overview
Crosswind-Console is a unified research dashboard that surfaces job opportunities, travel deals, and social trend insights. It blends a Svelte-based immersive UI with a FastAPI orchestration layer that coordinates MCP-driven data gathering and Gemini-powered reasoning.

## Tech Stack
- **Frontend**: Svelte 5 (Runes), Vite, Lucide Icons
- **Backend**: FastAPI, Python 3.10+, Uvicorn
- **Auth**: Next.js, NextAuth, Prisma
- **AI/Data**: Google Gemini API (`google-generativeai`), MCP (Model Context Protocol)
- **Database**: Prisma (PostgreSQL/SQLite)

## Directory Structure
```
Crosswind-Console/
├── frontend/          # Svelte 5 app (Vite)
│   └── src/lib/
│       ├── components/  # UI components (LandingPage, AgentPage)
│       ├── api.ts       # Backend API client
│       └── state.ts     # Svelte stores
├── backend/           # FastAPI server
│   └── app/
│       ├── routers/     # API endpoints (discovery, llm)
│       ├── services/    # Business logic (llm.py)
│       ├── schemas.py   # Pydantic models
│       └── config.py    # Settings (loads .env)
├── mcp_servers/       # MCP tool implementations
│   ├── jobs_server.py
│   ├── travel_server.py
│   ├── trends_server.py
│   └── search_server.py
├── auth/              # NextAuth authentication
└── .env               # Environment variables (API keys)
```

## Development Commands

### Start Backend (Terminal 1)
```bash
cd Crosswind-Console
uvicorn backend.app.main:app --reload
# Runs on http://localhost:8000
```

### Start Frontend (Terminal 2)
```bash
cd Crosswind-Console/frontend
npm run dev
# Runs on http://localhost:5173
```

### Start Auth (Optional, Terminal 3)
```bash
cd Crosswind-Console/auth
npm run dev -- --port 3001
```

## Environment Variables (.env in project root)
```
GEMINI_API_KEY=your_gemini_key
RAPIDAPI_KEY=your_rapidapi_key
GOOGLE_MAPS_API_KEY=your_maps_key
GOOGLE_SEARCH_CX=your_search_cx
X_BEARER_TOKEN=your_twitter_token
TRIPADVISOR_API_KEY=your_tripadvisor_key
```

## Key Files

### Frontend
- `frontend/src/App.svelte` - Main app, handles page routing
- `frontend/src/lib/components/LandingPage.svelte` - Hero/category selection
- `frontend/src/lib/components/AgentPage.svelte` - Chat interface for agents
- `frontend/src/lib/api.ts` - `sendLLMPrompt()` function

### Backend
- `backend/app/main.py` - FastAPI app, CORS setup
- `backend/app/services/llm.py` - `GeminiClient` with MCP tool integration
- `backend/app/config.py` - `Settings` class (pydantic-settings)
- `backend/app/routers/llm.py` - `/api/llm/prompt` endpoint

### MCP Servers
- `mcp_servers/jobs_server.py` - `search_jobs`, `get_active_jobs`
- `mcp_servers/travel_server.py` - `search_flights`, `search_hotels`, `search_places`
- `mcp_servers/trends_server.py` - `get_google_trends`, `search_tweets`
- `mcp_servers/search_server.py` - `web_search`

## Coding Guidelines

### Svelte 5 (Runes)
- Use `$state()` for reactive state
- Use `$derived()` for computed values
- Use `$props()` for component props
- `{@const}` must be direct child of `{#each}` or `{#if}` blocks

### FastAPI
- Use `pydantic-settings` for configuration
- Routers in `app/routers/`, services in `app/services/`
- Async functions for I/O operations

### MCP Tools
- Decorated with `@mcp.tool()`
- Must be async functions
- Import in `llm.py` and add to `MCP_TOOLS` list
- **Flight APIs**:
    - `search_flights` (Kiwi): Date ranges, cabin class, direct only.
    - `search_flights_sky` (Skyscanner): Whole month search, round trips.


## Common Issues

### "Gemini disabled" Error
1. Check `.env` has `GEMINI_API_KEY`
2. Restart backend: `uvicorn backend.app.main:app --reload`
3. Verify `google-generativeai` is installed: `pip install google-generativeai`

### Frontend Compilation Errors
1. Ensure `{@const}` is direct child of block elements
2. Verify all referenced variables are defined (e.g., `$derived()`)
3. Restart dev server: `npm run dev`

### Navigation Freezes
- Usually caused by undefined components or variables in `AgentPage.svelte`
- Check browser console for errors

## Last Updated
2025-12-05
