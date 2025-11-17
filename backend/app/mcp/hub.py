from __future__ import annotations

import asyncio
import json
import logging
from dataclasses import dataclass
from typing import Any

from mcp import types as mcp_types
from mcp.client.session_group import ClientSessionGroup
from mcp.client.stdio import StdioServerParameters

from ..config import Settings, get_settings

logger = logging.getLogger(__name__)


@dataclass
class MCPServerSpec:
    name: str
    params: StdioServerParameters


class MCPHub:
    """Maintains shared MCP client sessions for Firecrawl + Playwright."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self._group: ClientSessionGroup | None = None
        self._group_lock = asyncio.Lock()
        self._connection_lock = asyncio.Lock()
        self._server_tools: dict[str, set[str]] = {}
        self._disabled_servers: set[str] = set()

    async def _ensure_group(self) -> ClientSessionGroup:
        async with self._group_lock:
            if self._group is None:
                self._group = ClientSessionGroup()
                await self._group.__aenter__()
        return self._group

    def _server_spec(self, server: str) -> MCPServerSpec | None:
        if server == "firecrawl":
            api_key = self.settings.firecrawl_api_key
            if not api_key:
                return None
            return MCPServerSpec(
                name="firecrawl",
                params=StdioServerParameters(
                    command="npx",
                    args=["-y", "firecrawl-mcp"],
                    env={"FIRECRAWL_API_KEY": api_key},
                ),
            )
        if server == "playwright":
            env: dict[str, str] = {}
            if self.settings.playwright_browsers_path:
                env["PLAYWRIGHT_BROWSERS_PATH"] = self.settings.playwright_browsers_path
            return MCPServerSpec(
                name="playwright",
                params=StdioServerParameters(
                    command="npx",
                    args=["@playwright/mcp@latest"],
                    env=env or None,
                ),
            )
        return None

    async def ensure_server(self, server: str) -> None:
        if server in self._server_tools or server in self._disabled_servers:
            return
        spec = self._server_spec(server)
        if spec is None:
            self._disabled_servers.add(server)
            raise RuntimeError(f"MCP server '{server}' is not configured")

        async with self._connection_lock:
            if server in self._server_tools:
                return
            group = await self._ensure_group()
            before = set(group.tools.keys())
            try:
                await group.connect_to_server(spec.params)
            except Exception as exc:  # pragma: no cover - initialization errors are logged
                self._disabled_servers.add(server)
                logger.exception("Failed to connect to MCP server %s", server)
                raise RuntimeError(f"Unable to connect to MCP server '{server}'") from exc

            after = set(group.tools.keys())
            new_tools = after - before
            self._server_tools[server] = new_tools
            logger.info("Connected to %s MCP server with tools: %s", server, sorted(new_tools))

    async def call_tool(self, server: str, tool: str, arguments: dict[str, Any]) -> mcp_types.CallToolResult:
        await self.ensure_server(server)
        if server not in self._server_tools:
            raise RuntimeError(f"MCP server '{server}' not available")
        if tool not in self._server_tools[server]:
            raise RuntimeError(f"Tool '{tool}' not registered for server '{server}'")
        group = await self._ensure_group()
        return await group.call_tool(tool, arguments)

    @property
    def firecrawl_ready(self) -> bool:
        return "firecrawl" in self._server_tools and "firecrawl_search" in self._server_tools["firecrawl"]

    @property
    def playwright_ready(self) -> bool:
        return "playwright" in self._server_tools and "browser_navigate" in self._server_tools["playwright"]


class MCPToolParser:
    """Utility helpers to normalize MCP tool results."""

    @staticmethod
    def extract_json(result: mcp_types.CallToolResult) -> Any:
        if result.isError:
            message = MCPToolParser.collect_text(result)
            raise RuntimeError(message or "MCP tool execution failed")

        if result.structuredContent:
            return result.structuredContent

        payloads: list[Any] = []
        for block in result.content or []:
            if isinstance(block, mcp_types.TextContent):
                text = block.text.strip()
                if not text:
                    continue
                try:
                    payloads.append(json.loads(text))
                except json.JSONDecodeError:
                    payloads.append(text)
            else:  # Images or other content types
                try:
                    payloads.append(block.model_dump())
                except AttributeError:  # pragma: no cover
                    payloads.append(str(block))

        if not payloads:
            raise RuntimeError("Tool returned no usable payload")
        return payloads[0] if len(payloads) == 1 else payloads

    @staticmethod
    def collect_text(result: mcp_types.CallToolResult) -> str:
        chunks: list[str] = []
        for block in result.content or []:
            if isinstance(block, mcp_types.TextContent) and block.text:
                chunks.append(block.text)
        return "\n".join(chunks)


class FirecrawlToolset:
    """High-level helpers around Firecrawl MCP tools."""

    DEFAULT_LIMIT = 4

    def __init__(self, hub: MCPHub) -> None:
        self.hub = hub

    async def search(self, query: str, *, limit: int | None = None) -> list[dict[str, Any]]:
        payload = {
            "query": query,
            "limit": limit or self.DEFAULT_LIMIT,
            "scrapeOptions": {
                "formats": ["markdown"],
                "onlyMainContent": True,
                "storeInCache": True,
            },
        }
        result = await self.hub.call_tool("firecrawl", "firecrawl_search", payload)
        parsed = MCPToolParser.extract_json(result)
        if isinstance(parsed, dict):
            data_obj = parsed.get("data") or parsed
            if isinstance(data_obj, dict) and "web" in data_obj:
                return data_obj.get("web", [])
            if isinstance(parsed, list):  # pragma: no cover
                return parsed
        if isinstance(parsed, list):  # pragma: no cover
            return parsed
        logger.debug("Unexpected Firecrawl payload: %s", parsed)
        return []

