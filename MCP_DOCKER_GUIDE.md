# Codex Docker MCP Gateway Guide

This document summarizes the MCP servers and tools available to Codex through the Docker MCP gateway. Keep it with each project so any AI assistant can quickly discover which remote capabilities exist and how to invoke them.

## Active MCP Servers
- `MCP_DOCKER` – Containerized gateway exposing Playwright browser automation, Firecrawl web intelligence, GitHub/HTTP fetchers, and basic MCP management helpers.
- `fetch` (hosted via Docker gateway) – Remote fetcher that converts arbitrary URLs to Markdown or raw text chunks; ideal for public pages outside Firecrawl's reach.
- `sequentialthinking` (hosted via Docker gateway) – Reflection-focused reasoning assistant that guides multi-step analyses via the `sequentialthinking` tool.

## Tool Catalog

### Playwright Browser Tools
- `browser_navigate` – Open a URL.
- `browser_navigate_back` – Navigate backward in history.
- `browser_close` – Close the current page tab.
- `browser_tabs` – List/select/close tabs.
- `browser_resize` – Resize viewport.
- `browser_press_key` – Simulate keyboard input.
- `browser_type` – Type into focused element.
- `browser_fill_form` – Fill form fields in bulk.
- `browser_click` – Click an element.
- `browser_doubleClick` – Not exposed; use `browser_click` twice if needed.
- `browser_drag` – Drag from one element to another.
- `browser_hover` – Hover over an element.
- `browser_select_option` – Choose dropdown values.
- `browser_file_upload` – Provide files to an `<input type="file">`.
- `browser_handle_dialog` – Accept/decline dialogs or prompts.
- `browser_console_messages` – Read collected console logs (call after navigation/actions).
- `browser_network_requests` – Inspect recorded network calls.
- `browser_snapshot` – Capture accessibility tree snapshot (best for structured inspection).
- `browser_take_screenshot` – Screenshot viewport or element.
- `browser_wait_for` – Wait for text to appear/disappear.
- `browser_evaluate` – Run custom JS in page context.
- `browser_install` – Install the underlying browser if required.

### Firecrawl Web Intelligence
- `firecrawl_search` – Web search with optional scraping.
- `firecrawl_scrape` – Extract single page content (Markdown/HTML/etc.).
- `firecrawl_map` – Discover URLs on a site.
- `firecrawl_crawl` – Crawl multiple related pages.
- `firecrawl_extract` – Extract structured data via schema + prompt.
- `firecrawl_check_crawl_status` – Poll the status/results of long-running crawls.

### GitHub/HTTP Content Helpers
- `fetch_generic_documentation` – Pull repository docs (owner + repo).
- `fetch_generic_url_content` – Download any allowed URL (raw files, APIs, etc.).
- `search_generic_code` – GitHub code search for a repo.
- `search_generic_documentation` – Search repo documentation corpus.
- `match_common_libs_owner_repo_mapping` – Map a library name to owner/repo before querying.

### Fetch Server Tools (`fetch`)
- `fetch` – Stream any URL as Markdown or raw text.
  - Required: `url`
  - Optional: `max_length` (default 5000 chars), `start_index` for pagination, `raw` for unconverted output.
  - Usage: iterate by increasing `start_index` when content truncates; respect site policies unless server configured otherwise.

### Sequential Thinking Server Tools (`sequentialthinking`)
- `sequentialthinking` – Plan/analyze via guided thought sequences with branching, revisions, and hypothesis verification.
  - Key args: `thought`, `thought_number`, `total_thoughts`, `next_thought_needed`, `is_revision`, `revises_thought`, `branch_from_thought`, `branch_id`, `needs_more_thoughts`.
  - Usage pattern: propose initial total thoughts, iterate while documenting reasoning, flag revisions/branches explicitly, and switch `next_thought_needed` to false only when final answer is ready.

### MCP Management & Utilities
- `code-mode` – Spin up a mini JavaScript environment that can combine tools.
- `mcp-find` – Discover other MCP servers (rarely needed; Docker gateway usually preconfigured).
- `mcp-add` / `mcp-remove` – Register or unregister additional servers.
- `mcp-config-set` – Update config for active servers.
- `mcp-exec` – Directly call a tool by name when higher flexibility is required.

## Usage Notes
1. Prefer this Docker gateway for any remote browsing, Firecrawl search/scrape, or GitHub fetch. No extra MCP servers are needed once `MCP_DOCKER` is configured.
2. Browser flow example: `browser_navigate` → actions (`browser_click`, `browser_type`, …) → diagnostics (`browser_console_messages`, `browser_network_requests`).
3. Firecrawl flow example: `firecrawl_search` to discover URLs, `firecrawl_scrape` for details, `firecrawl_extract` for structured output, `firecrawl_check_crawl_status` if a crawl was started.
4. Repository/HTTP fetch flow: use `fetch_generic_documentation` or `search_generic_code` for GitHub, and `fetch_generic_url_content` for raw files or APIs.
5. Keep this file synchronized across projects so any agent immediately knows it can rely solely on the Docker MCP server and which tool to pick for each scenario.
