# Crosswind-Console Project Context

## Project Overview
Crosswind-Console is a unified research dashboard that surfaces job opportunities, travel deals, and social trend insights. It blends a Svelte-based immersive UI with a FastAPI orchestration layer that coordinates MCP-driven data gathering and Gemini-powered reasoning.

## Tech Stack
- **Frontend**: Svelte 5 (Runes), Vite, Lucide Icons
- **Backend**: FastAPI, Python 3.10+, Uvicorn, SQLAlchemy
- **Auth**: Next.js, NextAuth, Prisma
- **AI/Data**: Google Gemini API (`google-generativeai`), MCP (Model Context Protocol)
- **Database**: PostgreSQL + pgvector (Supabase for production), SQLite (local fallback)

## Directory Structure
```
Crosswind-Console/
├── frontend/          # Svelte 5 app (Vite)
│   └── src/lib/
│       ├── components/  # UI (LandingPage, AgentPage, Autocomplete)
│       ├── api.ts       # Backend API client
│       └── state.ts     # Svelte stores
├── backend/           # FastAPI server
│   └── app/
│       ├── routers/     # API endpoints (discovery, llm, autocomplete)
│       ├── services/    # Business logic (llm.py)
│       ├── models.py    # SQLAlchemy models (Airport, Currency)
│       ├── database.py  # DB connection + session
│       ├── seed_data.py # Populate airports/currencies
│       └── config.py    # Settings (loads .env)
├── mcp_servers/       # MCP tool implementations
├── auth/              # NextAuth authentication
├── docker-compose.yml # PostgreSQL + pgvector for local dev
└── .env               # Environment variables (API keys)
```

## Development Commands

### Start Database (Docker)
```bash
docker-compose up -d
# PostgreSQL on localhost:5432
```

### Seed Database
```bash
cd backend
python -m app.seed_data
```

### Start Backend (Terminal 1)
```bash
uvicorn backend.app.main:app --reload
# Runs on http://localhost:8000
```

### Start Frontend (Terminal 2)
```bash
cd frontend
npm run dev
# Runs on http://localhost:5173
```

## Environment Variables (.env)
```
GEMINI_API_KEY=your_gemini_key
DATABASE_URL=postgresql+asyncpg://crosswind:crosswind_dev@localhost:5432/crosswind
RAPIDAPI_KEY=your_rapidapi_key
# ... other keys
```

## Key Files

### Frontend
- `frontend/src/lib/components/Autocomplete.svelte` - Reusable autocomplete dropdown
- `frontend/src/lib/api.ts` - `searchAirports()`, `searchCurrencies()`
- `frontend/src/lib/components/AgentPage.svelte` - Travel form with autocomplete

### Backend
- `backend/app/database.py` - SQLAlchemy async engine
- `backend/app/models.py` - Airport, Currency models
- `backend/app/routers/autocomplete.py` - `/api/autocomplete/airports`, `/currencies`
- `backend/app/seed_data.py` - Populates DB from open data sources

## Current Work: Autocomplete & Config Fixes
**Status:** Completed (2026-01-01)

### Completed
- [x] Backend: SQLite fallback for local dev (no Docker required)
- [x] Backend: PostgreSQL + SQLAlchemy models
- [x] Backend: Airport/Currency seed script (6,726 airports, 52 currencies)
- [x] Backend: Search API endpoints
- [x] Backend: City grouping - returns "London (any - 6 airports)" for multi-airport cities
- [x] Backend: Fixed config.py to find .env in project root
- [x] Backend: Fixed database.py to ignore Prisma-format DATABASE_URL
- [x] Frontend: Autocomplete.svelte component
- [x] Frontend: Integrated into AgentPage.svelte
- [x] Frontend: City options styled with 🌐 icon and green highlight
- [x] Frontend: Fixed selection (onmousedown prevents blur race condition)
- [x] Gemini API now loads correctly in Travel agent
- [x] Fixed Kiwi API parsing for new GraphQL-style response structure

### Next Steps
- Implement RAG ingestion for WikiVoyage (travel) and O*NET (jobs)
- Set up automated data update pipeline (GitHub Actions)
- Test with Kiwi/Skyscanner APIs (they accept city codes)

## Coding Guidelines

### Svelte 5 (Runes)
- Use `$state()` for reactive state
- Use `$derived()` for computed values
- Use `$props()` with `$bindable()` for two-way binding

### FastAPI
- Async SQLAlchemy for database operations
- Dependency injection with `Depends(get_db)`

### MCP Tools
- `search_flights` (Kiwi): Date ranges, cabin class
- `search_flights_sky` (Skyscanner): Whole month search
- `search_airbnb` (Apify): Airbnb with date/guest/price filters

## Last Updated
2025-12-28

