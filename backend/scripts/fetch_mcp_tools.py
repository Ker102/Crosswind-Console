"""Fetch tool schemas from remote MCP servers."""
import httpx
import json

BASE_URL = "http://localhost:8000/api/mcp"

servers = ['rapidapi-sky', 'rapidapi-kiwi', 'rapidapi-booking']

all_tools = {}
for server in servers:
    try:
        print(f"Fetching tools for {server}...")
        response = httpx.get(f"{BASE_URL}/tools/{server}", timeout=60)
        if response.status_code == 200:
            data = response.json()
            tools = data.get("tools", [])
            all_tools[server] = data
            print(f"  Found {len(tools)} tools")
            
            # Print tool names
            for tool in tools[:10]:  # First 10
                print(f"    - {tool.get('name')}")
            if len(tools) > 10:
                print(f"    ... and {len(tools) - 10} more")
        else:
            print(f"  Error: {response.status_code}")
    except Exception as e:
        print(f"  Error: {e}")

# Save to file
output_file = "mcp_remote_tools.json"
with open(output_file, "w") as f:
    json.dump(all_tools, f, indent=2)
print(f"\nSaved full tool schemas to {output_file}")
