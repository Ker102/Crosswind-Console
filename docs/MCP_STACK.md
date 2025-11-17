# MCP Server Stack Blueprint

We layer the discovery backend with MCP servers so each category (jobs, travel, trends) can tap into live browsers, crawlers, and APIs. The first milestone is to register the two foundational servers—Playwright and Firecrawl—exposed through the Docker MCP gateway. Subsequent phases will bolt on specialized servers per category.

## Base Servers (Activated Now)

| Server | Tools | Purpose | Notes |
| --- | --- | --- | --- |
| `MCP_DOCKER::browser_*` (Playwright) | `browser_navigate`, `browser_click`, `browser_evaluate`, etc. | Headless browsing to walk job boards, airline portals, OTA dashboards, and social media surfaces when APIs are unavailable. | Already exposed by the Docker gateway. Use when structured APIs are missing or when verifying scraped context visually. |
| `MCP_DOCKER::firecrawl_*` (Firecrawl) | `firecrawl_search`, `firecrawl_scrape`, `firecrawl_extract`, `firecrawl_map` | High-volume scraping/searching layer for structured extraction of flights, accommodations, job posts, and trend write-ups. | Default to `firecrawl_search` → `firecrawl_scrape` per domain due to better throttling + caching. |

### How to Call Them
- **Python/Backend**: use the `MCP_DOCKER` tools via the CLI harness (e.g., `firecrawl_search` for job keywords, or `browser_navigate` + `browser_scrape` flows). Wrap these calls behind async connector functions so FastAPI endpoints stay responsive.
- **Ops**: ensure the Docker MCP gateway is up; no extra config is needed beyond referencing the correct tool names.

## Category Roadmap

| Category | Goal | Planned MCP Servers |
| --- | --- | --- |
| Jobs | Aggregate openings, salary intel, and skill spikes. | Base (Playwright + Firecrawl) + later connectors for Lever/Greenhouse/GitHub Jobs + LinkedIn automation. |
| Travel | Surface fare drops + stay deals. | Base + flight-specific crawlers (e.g., Hopper-style Firecrawl queries), OTA scrapers, and aggregator APIs for currency conversions. |
| Trends | Track social media formats + hashtags. | Base + social analytics MCP servers (TikTok data API, Instagram Graph proxy) + browser-backed automations for story scrapes. |

Future commits will add each category’s specialized servers inside this document (and reference implementation modules) so we maintain a transparent inventory.
