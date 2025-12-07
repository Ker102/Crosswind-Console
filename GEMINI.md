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
