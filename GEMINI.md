# Crosswind-Console Project Context

## Project Overview
Crosswind-Console is a unified research dashboard that surfaces job opportunities, travel deals, and social trend insights. It blends a Svelte-based immersive UI with a FastAPI orchestration layer that coordinates MCP-driven data gathering and Gemini-powered reasoning.

## Tech Stack
- **Frontend**: Svelte 5 (Runes), Vite, Lucide Icons
- **Backend**: FastAPI, Python, Uvicorn
- **Auth**: Next.js, NextAuth, Prisma
- **AI/Data**: Google Gemini 3 Pro Preview, LangChain 1.2, MCP (Model Context Protocol), Supabase pgvector
- **Database**: PostgreSQL + pgvector (Supabase), SQLite (local fallback)

## Architecture

### Core Systems
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Frontend  │────▶│   Backend   │────▶│  Supabase   │
│   (Svelte)  │     │  (FastAPI)  │     │  (pgvector) │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
       ┌─────────────┐          ┌─────────────┐
       │   Gemini    │          │   Remote    │
       │     LLM     │          │   MCP       │
       └─────────────┘          └─────────────┘
```

### Key Directories
- **Frontend (`/frontend`)**: Svelte UI, components, API client
- **Backend (`/backend`)**: FastAPI, LLM services, RAG integration
- **MCP Servers (`/mcp_servers`)**: Local MCP tool servers
- **Auth (`/auth`)**: NextAuth authentication

---

## Hybrid MCP-RAG System (NEW)

### Overview
The system uses **RAG (Retrieval-Augmented Generation)** to provide the LLM with API parameter guidance, combined with **remote MCP servers** for real-time data fetching.

### RAG Database (Supabase pgvector)
**11 documents ingested** across 3 namespaces:

| Namespace | Documents |
|-----------|-----------|
| `travel` | flight_params, hotel_params, airbnb_params, google_maps_guidance, tool_guidance, flights_sky_config, Flights Sky API Ref, Kiwi API Ref |
| `jobs` | tool_guidance |
| `trends` | tool_guidance |

### Key RAG Files
| Location | Content |
|----------|---------|
| `/backend/data/rag/travel/` | Human-curated parameter guidance (flight_params.md, hotel_params.md, etc.) |
| `/mcp_servers/api_docs/` | Clean API references (sky_params.md, kiwi_params.md) |
| `/backend/scripts/ingest_api_docs.py` | Script to ingest docs into Supabase |

### Remote MCP Servers (configured in `/mcp_servers/servers.config.json`)
| Server | Tools | Purpose |
|--------|-------|---------|
| `rapidapi-sky` | 54 | Flights, hotels, car hire (Flights Sky API) |
| `rapidapi-booking` | 58 | Hotels, attractions (Booking.com API) |
| `google-maps` | 7 | Directions, geocoding, places |

---

## Backend Services

### LLM Services (`/backend/app/services/`)
| Service | Purpose |
|---------|---------|
| `llm.py` | Main LLM service with local MCP tool calling |
| `sandbox_llm.py` | **NEW** - Sandbox mode: RAG + remote MCP tool calling |
| `rag_service.py` | RAG search via Supabase pgvector |

### API Endpoints (`/backend/app/routers/`)
| Endpoint | Purpose |
|----------|---------|
| `POST /api/llm/prompt` | Standard chat with local MCP tools |
| `POST /api/llm/sandbox` | **NEW** - RAG-enhanced chat with remote MCP |
| `GET /api/mcp/servers` | List configured MCP servers |
| `GET /api/mcp/tools/{server}` | List tools from a server |
| `POST /api/mcp/tools/{server}/{tool}/execute` | Execute MCP tool |

---

## Frontend Components

### Key Components (`/frontend/src/lib/components/`)
| Component | Purpose |
|-----------|---------|
| `AgentPage.svelte` | Main agent interface with mode toggle |
| `SandboxMode.svelte` | **NEW** - Chat UI for sandbox (RAG + MCP) |
| `DetailedFormMode.svelte` | **NEW** - Dynamic forms from MCP schemas |
| `DynamicForm.svelte` | **NEW** - Renders MCP tool parameters as forms |
| `ToolSelector.svelte` | **NEW** - Browse and select MCP tools |

### API Client (`/frontend/src/lib/api.ts`)
```typescript
// Sandbox API
sendSandboxPrompt({ prompt, namespace, history })

// MCP API
getMCPServers()
getMCPTools(serverName)
getMCPToolForm(serverName, toolName)
executeMCPTool(serverName, toolName, args)
```

---

## Environment Variables (.env)
```bash
# Gemini
GEMINI_API_KEY=your_key
GEMINI_MODEL=gemini-3-pro-preview

# Supabase (RAG)
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=your_anon_key

# Embeddings
TOGETHER_API_KEY=your_key

# MCP APIs
RAPIDAPI_KEY=your_key
GOOGLE_MAPS_API_KEY=your_key
APIFY_API_TOKEN=your_key
```

---

## Development Commands

```bash
# Backend
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload

# Frontend
cd frontend
npm run dev

# Auth
cd auth
npm run dev -- --port 3001

# Ingest RAG docs
cd backend/scripts
python ingest_api_docs.py

# Check RAG database
python check_rag_db.py
```

---

## Current Progress (2026-01-18)

### Completed
- [x] **LangChain Migration** (v1.2.3): Replaced raw Gemini SDK with LangChain agent (`bind_tools` pattern).
- [x] **Amadeus Integration**: Added official Amadeus `Flight Offers` and `Hotel List/Search` tools.
- [x] **Performance Optimization**: Created persistent HTTP MCP client (latency reduced from ~60s to ~3s).
- [x] **Hybrid RAG**: Integrated Supabase pgvector with 11 API documentation sources.
- [x] **Frontend Sandbox**: Functional chat UI with tool execution feedback.
- [x] **Trip Planner Phase 1**: LangGraph service with 4 nodes (`parse_intent` -> `search_flights` -> `search_hotels` -> `rank_options`).
- [x] **Supabase Session Persistence**: Session storage for Trip Planner with CRUD endpoints.

### Current State
- **Architecture**: LangChain 1.x + Gemini 2.0 Flash + LangGraph + Supabase RAG
- **Tools**: ~122 remote MCP tools (Amadeus, Flights Sky, Booking.com, Google Maps)
- **Trip Planner**: Graph architecture complete with session persistence via Supabase

### Next Steps
- Add "Human-in-the-loop" approval UI
- Deepen preference analysis functionality
- Frontend integration for Trip Planner

---

## 🚀 Future Features (Planned)

### Trip Planner Agent (LangGraph)
A multi-step, stateful AI agent for complete trip planning.

| Feature | Description |
|---------|-------------|
| **LangGraph Workflow** | StateGraph with flight → hotel → activity search pipeline |
| **Human-in-the-loop** | User approval before finalizing itinerary |
| **Deep Preferences** | Complex constraints ("cheap but comfortable", "beachfront + free cancellation") |
| **Multimodal Input** | Image upload to find similar destinations/hotels |
| **Vibe Matching** | Search by abstract concepts ("Cyberpunk aesthetic", "Writer's retreat") |

📄 **Full Design Doc**: [trip_planner_agent_design.md](file:///C:/Users/krist/.gemini/antigravity/brain/823f1366-a4c4-4c01-9a1f-0581b479520f/trip_planner_agent_design.md)

**Dependencies**: `langgraph`, `langgraph-checkpoint-sqlite`

**Estimated Effort**: ~2 weeks

---

## Last Updated
2026-01-16


