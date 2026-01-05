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
│       ├── components/  # UI components
│       │   ├── AgentPage.svelte      # Main agent with mode toggle
│       │   ├── SandboxMode.svelte    # RAG + MCP chat interface
│       │   ├── DetailedFormMode.svelte # Dynamic form generator
│       │   ├── DynamicForm.svelte    # Renders MCP tool schemas
│       │   └── ToolSelector.svelte   # Browse MCP tools
│       ├── api.ts       # Backend API client (includes sandbox, MCP APIs)
│       └── state.ts     # Svelte stores
├── backend/           # FastAPI server
│   └── app/
│       ├── routers/
│       │   ├── llm.py           # /api/llm/prompt, /api/llm/sandbox
│       │   └── mcp_tools.py     # /api/mcp/* endpoints
│       ├── services/
│       │   ├── llm.py           # Standard LLM with local MCP
│       │   ├── sandbox_llm.py   # NEW: RAG + remote MCP
│       │   └── rag_service.py   # RAG embed + search
│       └── data/rag/            # RAG source documents
│           ├── travel/          # flight_params, hotel_params, etc.
│           ├── jobs/            # tool_guidance
│           └── trends/          # tool_guidance
├── mcp_servers/       # MCP configurations
│   ├── servers.config.json  # Remote MCP server configs
│   ├── api_docs/            # Clean API references
│   │   ├── sky_params.md    # Flights Sky API
│   │   └── kiwi_params.md   # Kiwi API
│   └── travel_server.py     # Local travel MCP server
├── auth/              # NextAuth authentication
└── .env               # Environment variables (API keys)
```

## Development Commands

### Start All Services
```bash
# Terminal 1: Backend
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Auth
cd auth
npm run dev -- --port 3001
```

### RAG Management
```bash
cd backend/scripts

# Check current RAG contents
python check_rag_db.py

# Ingest new docs
python ingest_api_docs.py
```

## Environment Variables (.env)
```
GEMINI_API_KEY=your_gemini_key
GEMINI_MODEL=gemini-2.0-flash
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=your_anon_key
TOGETHER_API_KEY=your_key
RAPIDAPI_KEY=your_rapidapi_key
GOOGLE_MAPS_API_KEY=your_key
APIFY_API_TOKEN=your_key
```

---

## Hybrid MCP-RAG System

### How It Works
1. **User Query** → Frontend sends to `/api/llm/sandbox`
2. **RAG Search** → Retrieves relevant parameter docs from Supabase
3. **Gemini** → Receives query + RAG context + tool definitions
4. **Tool Calls** → Gemini selects tools, backend executes via remote MCP
5. **Response** → Synthesized result with tool traces

### RAG Database (11 Documents)
| Namespace | Documents |
|-----------|-----------|
| `travel` | flight_params.md, hotel_params.md, airbnb_params.md, google_maps_guidance.md, tool_guidance.md, flights_sky_config.md, Flights Sky API Ref, Kiwi API Ref |
| `jobs` | tool_guidance.md |
| `trends` | tool_guidance.md |

### Remote MCP Servers
| Server | Tools | API Host |
|--------|-------|----------|
| `rapidapi-sky` | 54 | flights-sky.p.rapidapi.com |
| `rapidapi-booking` | 58 | booking-com.p.rapidapi.com |
| `google-maps` | 7 | @modelcontextprotocol/server-google-maps |

---

## Key Files Reference

### Backend
| File | Purpose |
|------|---------|
| `services/sandbox_llm.py` | SandboxLLMService: RAG + remote MCP |
| `services/rag_service.py` | RAGService: embed + search |
| `routers/mcp_tools.py` | MCP tool endpoints |
| `data/rag/travel/*.md` | Parameter guidance docs |

### Frontend
| File | Purpose |
|------|---------|
| `components/SandboxMode.svelte` | Sandbox chat UI |
| `components/AgentPage.svelte` | Main interface, mode toggle |
| `api.ts` | sendSandboxPrompt, getMCPTools, etc. |

### MCP
| File | Purpose |
|------|---------|
| `servers.config.json` | Remote MCP server definitions |
| `api_docs/sky_params.md` | Flights Sky API reference |
| `api_docs/kiwi_params.md` | Kiwi API reference |

---

## Current Status (2026-01-05)

### ✅ Completed
- [x] Supabase pgvector RAG setup
- [x] RAG document ingestion (11 docs)
- [x] Remote MCP client integration (~120 tools)
- [x] Dynamic form generator (MCP schema → forms)
- [x] Sandbox LLM service (RAG + remote MCP)
- [x] Frontend SandboxMode integration
- [x] API endpoint `/api/llm/sandbox`

### 🔜 Next Steps
- Test end-to-end sandbox flow with live APIs
- Add Jobs/Trends API documentation
- Implement chat session persistence
- Polish tool execution feedback UI

---

## Coding Guidelines

### Svelte 5 (Runes)
```svelte
let state = $state(initialValue)
let computed = $derived(state * 2)
let { prop = $bindable() } = $props()
```

### FastAPI
```python
# Use async and dependency injection
async def endpoint(db: AsyncSession = Depends(get_db)):
    pass
```

### MCP Tools
- Local tools: Import from `mcp_servers/*.py`
- Remote tools: Call via `sandbox_llm.py` → `_call_remote_tool()`

---

## Last Updated
2026-01-05
