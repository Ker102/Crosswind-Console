# Cross-Domain Intelligent Discovery Platform

A unified research dashboard that surfaces job opportunities, travel deals, and social trend insights. The experience blends a Svelte-based immersive UI (with room for Spline/Three.js scenes) and a FastAPI orchestration layer that coordinates MCP-driven data gathering and Gemini-powered reasoning.

## Vision
- **Single workspace** where seekers toggle across jobs, travel, and social categories.
- **Integrated LLM reasoning** (Google Gemini API) to enrich prompts and summarize MCP-sourced data.
- **3D-enhanced UI** showcasing dynamic cards, stats, and visual metaphors for each domain.
- **Modular data connectors** using MCP servers (Firecrawl, Fetch, browser automation) to reach best-of-breed APIs and live content.

## High-Level Architecture
```
frontend/ (Svelte + Vite)
  src/App.svelte            # Immersive dashboard shell + layout + auth hooks
  src/lib/api.ts            # Typed front-end gateway to FastAPI
  src/lib/state.ts          # Stores, persistence triggers, auth bootstrap
  src/lib/components/       # Three.js scene + insight cards
  src/lib/types.ts          # Shared contracts w/ backend + auth
backend/
  app/main.py           # FastAPI application
  app/routers/
    discovery.py        # Jobs/Travel/Trends endpoints
    llm.py              # Gemini proxy endpoints
  app/services/
    jobs.py             # Aggregation logic (MCP stubs)
    travel.py
    trends.py
    llm.py
  app/schemas.py        # Pydantic models
  tests/
auth/ (Next.js + NextAuth)
  prisma/schema.prisma       # User/Account/Session/Progress tables
  src/lib/authOptions.ts     # NextAuth config (Google OAuth + Prisma adapter)
  src/lib/prisma.ts          # Prisma client singleton
  src/app/api/auth/[...nextauth]
  src/app/api/progress       # Session-aware persistence API
  src/app/api/session        # Session snapshot + CORS for Svelte UI
```

## Workflow Overview
1. User selects a discovery mode (jobs, travel, trends).
2. Frontend sends the selection and an optional natural-language prompt to FastAPI.
3. FastAPI orchestrates:
   - Domain-specific MCP connectors (Firecrawl for scraping, Fetch for structured pulls, etc.).
   - Google Gemini API for reasoning + summarization.
4. Aggregated insights are streamed back to the dashboard for visualization.

## Planned Milestones
1. Bootstrap FastAPI backend skeleton with domain routers and mocked responses.
2. Initialize Svelte frontend with routing, state, and API helpers.
3. Design immersive 3D-inspired dashboard (placeholder scene + cards/charts).
4. Implement MCP and Gemini integration layers (API keys + server orchestration).
5. Add tests, deployment scripts, and documentation.

Stay tuned as we iterate aggressively with many small commits.

## Local Development

### Backend (FastAPI + Gemini proxy)
1. `cd backend`
2. Create a virtual env (`python -m venv .venv` or `uv venv`) and activate it.
3. `pip install -e .[dev]`
4. Copy `.env.example` to `.env` and add `GEMINI_API_KEY` when ready.
5. `uvicorn app.main:app --reload`

### Frontend (Svelte + Three.js scene)
1. `cd frontend`
2. `cp .env.example .env` and adjust `VITE_API_BASE_URL` if needed.
3. `npm install`
4. `npm run dev` (or `npm run check` for static analysis)
5. Open the printed URL to explore the dashboard UI.

### Auth Service (NextAuth + Prisma)
1. `cd auth`
2. Ensure the repo-level `.env` (copied from `.env.example`) includes Google OAuth creds, `NEXTAUTH_SECRET`, `NEXTAUTH_URL`, `FRONTEND_ORIGIN`, and `DATABASE_URL`.
3. `set -a && source ../.env && set +a && npx prisma migrate dev --name init` (first run only).
4. `npm run dev -- --port 3001` (scripts automatically load the shared `.env`).
5. Visit `http://localhost:3001` to test sign-in and the `/api/progress` endpoint.

### MCP Servers (Playwright + Firecrawl)
1. `cp .env.example .env` and add `FIRECRAWL_API_KEY` (Firecrawl dashboard) plus optional `PLAYWRIGHT_BROWSERS_PATH`.
2. Ensure Node.js ≥ 18 is installed.
3. Launch servers in separate terminals:
   - `./mcp/run_firecrawl.sh`
   - `./mcp/run_playwright.sh`
4. Point your MCP-aware client (Gemini CLI, future backend tooling) to `mcp/servers.config.json` for ready-made command definitions.
