#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${FIRECRAWL_API_KEY:-}" ]]; then
  echo "[mcp] FIRECRAWL_API_KEY is not set. Export it or populate the repo .env file." >&2
  exit 1
fi

echo "[mcp] Launching Firecrawl MCP server..."
exec npx -y firecrawl-mcp
