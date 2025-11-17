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
  src/lib/api.ts        # Typed front-end gateway to FastAPI
  src/lib/state.ts      # Store + derived selectors
  src/routes/+page.svelte
  src/routes/+layout.svelte
  static/3d/scene.json  # Placeholder for Spline/Three.js scene data
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
