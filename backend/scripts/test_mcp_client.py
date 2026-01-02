"""Test MCP client connection to travel server"""
import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load env from project root
load_dotenv(Path(__file__).parent.parent.parent / ".env")

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.mcp_client import MCPClient

async def test_mcp():
    # Travel server config
    config = {
        "command": "py",
        "args": [str(Path(__file__).parent.parent.parent / "mcp_servers" / "travel_server.py")]
    }
    
    print(f"🚀 Testing MCP connection to travel server...")
    print(f"   Command: {config['command']} {' '.join(config['args'])}")
    
    client = MCPClient(config)
    
    try:
        await client.connect()
        print("✅ Connected!")
        
        # List available tools
        print("\n📋 Listing available tools...")
        tools = await client.list_tools()
        
        if tools:
            print(f"\n✅ Found {len(tools)} tools:")
            for tool in tools[:10]:  # Show first 10
                print(f"   - {tool.get('name', 'unknown')}")
            if len(tools) > 10:
                print(f"   ... and {len(tools) - 10} more")
        else:
            print("❌ No tools found")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(test_mcp())
