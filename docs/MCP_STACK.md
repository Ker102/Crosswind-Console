# MCP Server Stack Blueprint

We layer the discovery backend with MCP servers so each category (jobs, travel, trends) can tap into live browsers, crawlers, and APIs. The first milestone is to register the two foundational servers—Playwright and Firecrawl—**running locally via the scripts inside `mcp/`**. Subsequent phases will bolt on specialized servers per category.

## Base Servers (Activated Now)

| Server | Tools | Purpose | Notes |
| --- | --- | --- | --- |
| `mcp/run_playwright.sh` (Playwright MCP) | `browser_navigate`, `browser_click`, `browser_evaluate`, etc. | Headless browsing to walk job boards, airline portals, OTA dashboards, and social media surfaces when APIs are unavailable. | Launches `npx @playwright/mcp@latest`; optional env `PLAYWRIGHT_BROWSERS_PATH` supported. |
| `mcp/run_firecrawl.sh` (Firecrawl MCP) | `firecrawl_search`, `firecrawl_scrape`, `firecrawl_extract`, `firecrawl_map` | High-volume scraping/searching layer for structured extraction of flights, accommodations, job posts, and trend write-ups. | Requires `FIRECRAWL_API_KEY`; command wraps `npx -y firecrawl-mcp`. |

### How to Call Them
- **Python/Backend**: once the stdio servers are running, connect via MCP clients (e.g., the upcoming Gemini integration or a standalone `mcp` Python SDK) using the declarative config in `mcp/servers.config.json`.
- **Ops**: run `./mcp/run_firecrawl.sh` and `./mcp/run_playwright.sh` locally (or containerize them) and keep the processes alive alongside FastAPI.

## Category Roadmap

| Category | Goal | Planned MCP Servers |
| --- | --- | --- |
| Jobs | Aggregate openings, salary intel, and skill spikes. | Base (Playwright + Firecrawl) + later connectors for Lever/Greenhouse/GitHub Jobs + LinkedIn automation. |
| Travel | Surface fare drops + stay deals. | Base + flight-specific crawlers (e.g., Hopper-style Firecrawl queries), OTA scrapers, and aggregator APIs for currency conversions. |
| Trends | Track social media formats + hashtags. | Base + social analytics MCP servers (TikTok data API, Instagram Graph proxy) + browser-backed automations for story scrapes. |

Future commits will add each category’s specialized servers inside this document (and reference implementation modules) so we maintain a transparent inventory.
