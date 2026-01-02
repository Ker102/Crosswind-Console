"""Test MCP client using official mcp library"""
import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load env
load_dotenv(Path(__file__).parent.parent.parent / ".env")

# Set env vars for the server process
os.environ.setdefault("RAPIDAPI_KEY", os.getenv("RAPIDAPI_KEY", ""))
os.environ.setdefault("GOOGLE_MAPS_API_KEY", os.getenv("GOOGLE_MAPS_API_KEY", ""))
os.environ.setdefault("TRIPADVISOR_API_KEY", os.getenv("TRIPADVISOR_API_KEY", ""))
os.environ.setdefault("APIFY_API_TOKEN", os.getenv("APIFY_API_TOKEN", ""))

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test():
    travel_server = Path(__file__).parent.parent.parent / "mcp_servers" / "travel_server.py"
    
    print(f"🚀 Connecting to MCP server...")
    print(f"   Server: {travel_server}")
    
    server_params = StdioServerParameters(
        command="py",
        args=[str(travel_server)],
        env=dict(os.environ)
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()
                print("✅ Connected and initialized!")
                
                # List available tools
                print("\n📋 Requesting tool list...")
                tools_result = await session.list_tools()
                
                if tools_result.tools:
                    print(f"\n✅ Found {len(tools_result.tools)} tools:")
                    for tool in tools_result.tools[:15]:
                        desc = tool.description[:60] if tool.description else "No description"
                        print(f"   - {tool.name}: {desc}...")
                    if len(tools_result.tools) > 15:
                        print(f"   ... and {len(tools_result.tools) - 15} more")
                else:
                    print("❌ No tools found")
                    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
