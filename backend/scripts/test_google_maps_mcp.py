"""Test Google Maps MCP server to see available tools"""
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env")

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_google_maps_mcp():
    print("🗺️ Testing Google Maps MCP Server")
    print("=" * 50)
    
    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-google-maps"],
        env={**os.environ, "GOOGLE_MAPS_API_KEY": os.getenv("GOOGLE_MAPS_API_KEY", "")}
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("✅ Connected to Google Maps MCP Server!\n")
                
                tools_result = await session.list_tools()
                
                if tools_result.tools:
                    print(f"📋 Found {len(tools_result.tools)} tools:\n")
                    
                    for tool in tools_result.tools:
                        print(f"🔧 {tool.name}")
                        if tool.description:
                            print(f"   {tool.description[:100]}...")
                        if tool.inputSchema:
                            props = tool.inputSchema.get("properties", {})
                            required = tool.inputSchema.get("required", [])
                            print(f"   Params: {list(props.keys())}")
                            print(f"   Required: {required}")
                        print()
                else:
                    print("❌ No tools found")
                    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_google_maps_mcp())
