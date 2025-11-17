# MCP Server Setup

To let Gemini (and any other MCP-capable client) call live browsers and scrapers **from inside this project**, run the Playwright and Firecrawl MCP servers locally. These are standalone Node processes that expose Model Context Protocol endpoints over stdio or HTTP, ready to be wired into the backend orchestration layer.

> Official references:
> - Playwright MCP server: https://github.com/microsoft/playwright-mcp
> - Firecrawl MCP server: https://docs.firecrawl.dev/mcp-server

## Prerequisites
- Node.js 18+
- `npx` available on your PATH
- Export the secrets listed in `.env.example` (copy to `.env` and populate values)

## Directory Structure
```
mcp/
  README.md              # you are here
  servers.config.json    # declarative config both servers share
  run_firecrawl.sh       # helper to launch Firecrawl MCP
  run_playwright.sh      # helper to launch Playwright MCP
```

## Configure Environment
1. Copy `.env.example` at the repository root to `.env`.
2. Fill in:
   - `FIRECRAWL_API_KEY` – from https://firecrawl.dev/app/api-keys (required)
   - `PLAYWRIGHT_BROWSERS_PATH` – optional; set to `0` if you want Playwright to install browsers into `node_modules` (useful for hermetic environments).
3. Source the env file before running any `run_*.sh` script or export the variables manually.

## Firecrawl MCP (Scraping/Crawling)
Run via helper script (loads env + performs safety checks):
```bash
./mcp/run_firecrawl.sh
```
This wraps the official command:
```bash
env FIRECRAWL_API_KEY=$FIRECRAWL_API_KEY npx -y firecrawl-mcp
```
The server exposes tools such as `firecrawl_search`, `firecrawl_scrape`, `firecrawl_extract`, etc.

## Playwright MCP (Browser Automation)
Run via helper script:
```bash
./mcp/run_playwright.sh
```
Underlying command (from Microsoft’s repo):
```bash
npx @playwright/mcp@latest
```
Set `PLAYWRIGHT_BROWSERS_PATH=0` if you need to avoid installing browsers globally. The script will respect whatever value you export.

## Using servers.config.json
`servers.config.json` mirrors the JSON format expected by many MCP clients (Gemini CLI, Cursor, VS Code, Goose, etc.). Point your client to this file or copy/paste the blocks into your tool of choice—the values already match the helper scripts.

```json
{
  "mcpServers": {
    "firecrawl": {
      "command": "npx",
      "args": ["-y", "firecrawl-mcp"],
      "env": {
        "FIRECRAWL_API_KEY": "${FIRECRAWL_API_KEY}"
      }
    },
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"],
      "env": {
        "PLAYWRIGHT_BROWSERS_PATH": "${PLAYWRIGHT_BROWSERS_PATH:-}" }
    }
  }
}
```

Gemini (via `google-gemini` CLI) can read this config directly once we add MCP-tool calling logic to the backend.

## Next Steps
- Add FastAPI services that speak MCP via stdio or HTTP transport for each domain connector.
- Expand `docs/MCP_STACK.md` with additional category-specific MCP servers as they come online.
