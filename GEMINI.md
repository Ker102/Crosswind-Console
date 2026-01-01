# Crosswind-Console Project Context

## Project Overview
Crosswind-Console is a unified research dashboard that surfaces job opportunities, travel deals, and social trend insights. It blends a Svelte-based immersive UI with a FastAPI orchestration layer that coordinates MCP-driven data gathering and Gemini-powered reasoning.

## Tech Stack
- **Frontend**: Svelte, Vite, Three.js (Spline), TailwindCSS
- **Backend**: FastAPI, Python, Uvicorn
- **Auth**: Next.js, NextAuth, Prisma
- **AI/Data**: Google Gemini API, MCP (Model Context Protocol)
- **Database**: Prisma (PostgreSQL/SQLite)

## Architecture
- **Frontend (`/frontend`)**: Handles UI, state management (Svelte stores), and 3D visualizations.
- **Backend (`/backend`)**: Orchestrates data fetching via MCP and reasoning via Gemini. Exposes REST endpoints.
- **Auth (`/auth`)**: Manages user authentication and session persistence using NextAuth.
- **MCP (`/mcp`)**: Contains scripts and configurations for MCP servers (Firecrawl, Playwright).

## Development Guidelines

### Frontend
- Use Svelte stores for global state management (`src/lib/state.ts`).
- Keep components modular and reusable (`src/lib/components/`).
- Use `src/lib/api.ts` for typed API calls to the backend.
- Ensure responsive design and immersive aesthetics.

### Backend
- Define routers in `app/routers/` for different domains (discovery, llm).
- Use Pydantic models in `app/schemas.py` for data validation.
- Implement business logic in `app/services/`.
- Use `GEMINI_API_KEY` for LLM integration.

### Auth
- Configure NextAuth in `src/lib/authOptions.ts`.
- Use Prisma for database interactions (`src/lib/prisma.ts`).
- Ensure secure session handling.

### MCP
- Use `mcp/servers.config.json` for server configurations.
- Ensure MCP servers are running for data fetching.
- **Flight Search**:
    - **Kiwi API (`search_flights`)**: Supports date ranges (`date_from`, `date_to`), round trips (`return_from`, `return_to`), cabin class (`ECONOMY`, `BUSINESS`, etc.), and direct flight filtering.
    - **Skyscanner API (`search_flights_sky`)**: Supports specific dates, whole month search (`whole_month="YYYY-MM"`), and round trips.
    - **Usage**: The LLM agent is instructed to use both for comprehensive price comparisons.
- **Airbnb Search**:
    - **Apify Actor (`search_airbnb`)**: Uses `tri_angle/new-fast-airbnb-scraper` via `travel_server.py`.
    - **Features**: Supports location, dates (`check_in`, `check_out`), guests (`adults`, `children`), price range, and currency.
    - **Auth**: Requires `APIFY_API_TOKEN` in `.env`.

## Development Workflow

### Commit Policy
- **Commit frequently** - even minor changes should be committed immediately
- The more commits the better - small, atomic commits are preferred
- Always write clear commit messages describing the change

### Progress Tracking
- **Before committing**, always update:
  - `GEMINI.md` - Update "Current Progress" section with completed work
  - `CLAUDE.md` - Update "Current Work" section with status
- Include **next steps** or **suggested steps** in the progress update
- This ensures continuity between sessions with different AI agents

## Common Commands

### Backend
```bash
cd backend
# Activate venv
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm run dev
```

### Auth
```bash
cd auth
npm run dev -- --port 3001
```

### MCP
```bash
./mcp/run_firecrawl.sh
./mcp/run_playwright.sh
```

## Current Progress

### Completed (2026-01-01)
- ✅ Autocomplete feature fully implemented
- ✅ SQLite fallback for local dev (no Docker required)
- ✅ Database seeded with 6,726 airports and 52 currencies
- ✅ Removed debug UI from App.svelte
- ✅ "City (any)" option for airport search - groups airports by city
- ✅ Fixed config.py to find .env in project root
- ✅ Fixed database.py to ignore Prisma-format URLs
- ✅ Fixed Autocomplete selection (onmousedown prevents blur race condition)
- ✅ Fixed Gemini API loading - now works in Travel agent

### In Progress
- 🔄 RAG database population planning

### Next Steps
- Implement RAG ingestion for WikiVoyage (travel) and O*NET (jobs)
- Set up GitHub Actions workflow for automated data updates
- Test with Kiwi/Skyscanner APIs (they accept city codes)

## Future Implementation: Chat Session Persistence
**Status:** Planned (Deferred)
**Goal:** Enable users to restore full chat history (user/model messages) per session.
**Implementation Plan:**
1. **Schema Update (`auth/prisma/schema.prisma`)**:
    - Add `Conversation` model (id, userId, title, createdAt).
    - Add `Message` model (id, conversationId, role, content, createdAt).
2. **Backend Logic**:
    - Update `llm.py` to save new messages to DB.
    - Create endpoint to fetch history by `conversationId`.
3. **Frontend State**:
    - Update `auth.ts` to fetch conversation history on load.
    - Update `state.ts` to rehydrate `messages` array from DB.

