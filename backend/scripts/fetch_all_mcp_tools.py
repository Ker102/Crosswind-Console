"""Fetch ALL tool schemas from remote MCP servers with longer timeout."""
import httpx
import json
import asyncio

BASE_URL = "http://localhost:8000/api/mcp"

async def fetch_server_tools(server: str):
    """Fetch tools from a single server with extended timeout."""
    print(f"\nFetching tools for {server}...")
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(120.0)) as client:
            response = await client.get(f"{BASE_URL}/tools/{server}")
            if response.status_code == 200:
                data = response.json()
                tools = data.get("tools", [])
                print(f"  ✅ Found {len(tools)} tools")
                return server, data
            else:
                print(f"  ❌ Error: {response.status_code}")
                return server, None
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return server, None

async def main():
    servers = ['rapidapi-sky']  # Focus on just sky for now
    
    results = {}
    for server in servers:
        name, data = await fetch_server_tools(server)
        if data:
            results[name] = data
            
            # Print tool summaries
            tools = data.get("tools", [])
            for tool in tools:
                tool_name = tool.get("name", "unknown")
                # Get input schema
                input_schema = tool.get("inputSchema", {})
                properties = input_schema.get("properties", {})
                required = input_schema.get("required", [])
                
                print(f"\n  📦 {tool_name}")
                print(f"     Required: {required}")
                if properties:
                    for prop_name, prop_info in list(properties.items())[:5]:
                        prop_type = prop_info.get("type", "?")
                        prop_desc = prop_info.get("description", "")[:50]
                        print(f"     - {prop_name} ({prop_type}): {prop_desc}")
                    if len(properties) > 5:
                        print(f"     ... and {len(properties) - 5} more parameters")
    
    # Save full output
    with open("mcp_sky_tools_full.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n✨ Saved full schemas to mcp_sky_tools_full.json")

if __name__ == "__main__":
    asyncio.run(main())
