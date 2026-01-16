# Crosswind-Console Agent Rules

## 🎯 Core Principles

### 1. Continuous Documentation
- **Update `GEMINI.md`** after every significant feature or change
- Keep the "Current Progress" section up to date with completion status
- Document new APIs, tools, and architectural decisions

### 2. Frequent Commits
- Commit after completing each logical unit of work
- Use conventional commit format: `feat:`, `fix:`, `docs:`, `refactor:`
- Push regularly to avoid large merge conflicts

### 3. MCP Tool Utilization
- **Always prefer MCP tools** over manual API calls when available
- Check `/mcp_servers/` for existing tool implementations before creating new ones
- Use the persistent MCP client (`mcp_client.py`) for performance

---

## 📁 Project Structure Awareness

```
Crosswind-Console/
├── backend/
│   ├── app/services/     # LLM, RAG, Trip Planner services
│   ├── app/routers/      # FastAPI endpoints
│   └── scripts/          # Test and utility scripts
├── frontend/
│   └── src/lib/          # Svelte components
├── mcp_servers/          # MCP tool implementations
└── GEMINI.md             # Project context (ALWAYS CHECK FIRST)
```

---

## 🔧 Technical Guidelines

### Backend (Python/FastAPI)
- Use `async/await` for all I/O operations
- Import MCP tools from `mcp_servers.*` (not direct API calls)
- Add type hints using `Optional`, `List`, `Dict` from `typing`

### Frontend (Svelte)
- Use Svelte 5 Runes syntax (`$state`, `$derived`, `$effect`)
- Keep components focused and reusable

### Testing
- Create test scripts in `backend/scripts/test_*.py`
- Test locally before committing

---

## 📊 Progress Tracking

1. **Before starting work**: Check `GEMINI.md` for current state
2. **During work**: Update `task.md` (if using Antigravity)
3. **After completing**: Update `GEMINI.md` and commit

---

## 🚫 Avoid

- Making changes without understanding existing architecture
- Skipping commits for large batches of changes
- Duplicating existing MCP tool functionality
- Leaving TODO comments without tracking them
