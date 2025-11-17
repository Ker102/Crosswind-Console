#!/usr/bin/env bash
set -euo pipefail

# Optional: allow overriding browsers path for hermetic installs
if [[ -n "${PLAYWRIGHT_BROWSERS_PATH:-}" ]]; then
  export PLAYWRIGHT_BROWSERS_PATH
fi

echo "[mcp] Launching Playwright MCP server..."
exec npx @playwright/mcp@latest
