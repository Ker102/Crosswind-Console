"""
Persistent MCP Client - Uses HTTP connection pooling for fast MCP tool calls.
Replaces slow npx-based mcp-remote with direct httpx client.
"""
import asyncio
import os
from typing import Dict, List, Any, Optional
import httpx
from dataclasses import dataclass


@dataclass
class MCPToolResult:
    """Result from an MCP tool call"""
    success: bool
    content: str
    error: Optional[str] = None


class PersistentMCPClient:
    """
    HTTP-based MCP client with connection pooling.
    Much faster than npx mcp-remote (2-5s vs 30-90s).
    """
    
    # RapidAPI MCP endpoint
    MCP_BASE_URL = "https://mcp.rapidapi.com"
    
    # API host configurations for different services
    API_HOSTS = {
        "flights-sky": "flights-sky.p.rapidapi.com",
        "booking": "booking-com.p.rapidapi.com",
        "google-flights2": "google-flights2.p.rapidapi.com",
    }
    
    def __init__(self, rapidapi_key: str = None):
        self._rapidapi_key = rapidapi_key or os.getenv("RAPIDAPI_KEY", "")
        self._client: Optional[httpx.AsyncClient] = None
        self._tool_cache: Dict[str, List[Dict]] = {}
    
    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create persistent HTTP client"""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                timeout=60.0,
                limits=httpx.Limits(max_connections=20, max_keepalive_connections=10)
            )
        return self._client
    
    async def close(self):
        """Close the HTTP client"""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None
    
    def _get_headers(self, api_host: str) -> Dict[str, str]:
        """Get headers for RapidAPI MCP request"""
        return {
            "Content-Type": "application/json",
            "x-api-key": self._rapidapi_key,
            "x-api-host": api_host,
        }
    
    async def list_tools(self, service: str) -> List[Dict]:
        """
        List available tools for a service.
        
        Args:
            service: One of 'flights-sky', 'booking', 'google-flights2'
        
        Returns:
            List of tool definitions with name, description, inputSchema
        """
        if service in self._tool_cache:
            return self._tool_cache[service]
        
        api_host = self.API_HOSTS.get(service)
        if not api_host:
            return []
        
        client = await self._get_client()
        
        try:
            response = await client.post(
                f"{self.MCP_BASE_URL}/tools/list",
                headers=self._get_headers(api_host),
                json={}
            )
            response.raise_for_status()
            data = response.json()
            
            tools = data.get("tools", [])
            self._tool_cache[service] = tools
            return tools
            
        except Exception as e:
            print(f"Error listing tools for {service}: {e}")
            return []
    
    async def call_tool(
        self, 
        service: str, 
        tool_name: str, 
        arguments: Dict[str, Any]
    ) -> MCPToolResult:
        """
        Call an MCP tool on a remote service.
        
        Args:
            service: One of 'flights-sky', 'booking', 'google-flights2'
            tool_name: Name of the tool to call
            arguments: Tool arguments as a dictionary
        
        Returns:
            MCPToolResult with success status and content
        """
        api_host = self.API_HOSTS.get(service)
        if not api_host:
            return MCPToolResult(
                success=False,
                content="",
                error=f"Unknown service: {service}"
            )
        
        client = await self._get_client()
        
        try:
            response = await client.post(
                f"{self.MCP_BASE_URL}/tools/call",
                headers=self._get_headers(api_host),
                json={
                    "name": tool_name,
                    "arguments": arguments
                }
            )
            response.raise_for_status()
            data = response.json()
            
            # Extract content from MCP response
            content_parts = []
            for item in data.get("content", []):
                if isinstance(item, dict) and "text" in item:
                    content_parts.append(item["text"])
                elif isinstance(item, str):
                    content_parts.append(item)
            
            return MCPToolResult(
                success=True,
                content="\n".join(content_parts) if content_parts else str(data)
            )
            
        except httpx.HTTPStatusError as e:
            return MCPToolResult(
                success=False,
                content="",
                error=f"HTTP {e.response.status_code}: {e.response.text[:200]}"
            )
        except Exception as e:
            return MCPToolResult(
                success=False,
                content="",
                error=str(e)
            )


# Singleton instance for connection reuse
_mcp_client: Optional[PersistentMCPClient] = None


def get_mcp_client() -> PersistentMCPClient:
    """Get singleton MCP client instance"""
    global _mcp_client
    if _mcp_client is None:
        _mcp_client = PersistentMCPClient()
    return _mcp_client


async def shutdown_mcp_client():
    """Shutdown the MCP client (call on app shutdown)"""
    global _mcp_client
    if _mcp_client:
        await _mcp_client.close()
        _mcp_client = None
