"""Test RapidAPI Remote MCP servers"""
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env")

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_remote_mcp(name: str, command: str, args: list[str], env: dict = None):
    """Test a remote MCP server connection"""
    print(f"\n🔌 Testing: {name}")
    print(f"   Command: {command} {' '.join(args[:3])}...")
    
    full_env = dict(os.environ)
    if env:
        full_env.update(env)
    
    # Substitute env vars in args
    processed_args = []
    for arg in args:
        if "${" in arg:
            for key, val in full_env.items():
                arg = arg.replace(f"${{{key}}}", val or "")
        processed_args.append(arg)
    
    server_params = StdioServerParameters(
        command=command,
        args=processed_args,
        env=full_env
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("   ✅ Connected!")
                
                tools_result = await session.list_tools()
                if tools_result.tools:
                    print(f"   📋 Found {len(tools_result.tools)} tools:")
                    for tool in tools_result.tools[:5]:
                        print(f"      - {tool.name}")
                    if len(tools_result.tools) > 5:
                        print(f"      ... and {len(tools_result.tools) - 5} more")
                else:
                    print("   ⚠️ No tools returned")
                return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

async def main():
    print("=" * 50)
    print("Testing Remote MCP Servers")
    print("=" * 50)
    
    # Test RapidAPI Flights Sky
    await test_remote_mcp(
        "RapidAPI - Flights Sky",
        "npx",
        ["-y", "mcp-remote", "https://mcp.rapidapi.com",
         "--header", f"x-api-host: flights-sky.p.rapidapi.com",
         "--header", f"x-api-key: {os.getenv('RAPIDAPI_KEY')}"]
    )
    
    # Test RapidAPI Booking.com
    await test_remote_mcp(
        "RapidAPI - Booking.com",
        "npx",
        ["-y", "mcp-remote", "https://mcp.rapidapi.com",
         "--header", f"x-api-host: booking-com.p.rapidapi.com",
         "--header", f"x-api-key: {os.getenv('RAPIDAPI_KEY')}"]
    )
    
    print("\n" + "=" * 50)
    print("Remote MCP Server Test Complete")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
