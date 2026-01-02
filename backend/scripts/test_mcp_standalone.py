"""Standalone MCP client test - no app imports"""
import asyncio
import subprocess
import json
import os
from pathlib import Path
from dotenv import load_dotenv

# Load env
load_dotenv(Path(__file__).parent.parent.parent / ".env")

class MCPClientStandalone:
    """Minimal MCP client for testing"""
    def __init__(self, command: str, args: list):
        self.command = command
        self.args = args
        self.process = None
        self._request_id = 0
        
    async def connect(self):
        self.process = subprocess.Popen(
            [self.command] + self.args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            bufsize=1
        )
        # Wait a moment for server to initialize
        await asyncio.sleep(1)
        
    async def list_tools(self):
        self._request_id += 1
        request = {"jsonrpc": "2.0", "method": "tools/list", "id": self._request_id}
        return await self._send(request)
        
    async def _send(self, request):
        if not self.process:
            raise RuntimeError("Not connected")
        
        self.process.stdin.write(json.dumps(request) + "\n")
        self.process.stdin.flush()
        
        # Read response with timeout
        try:
            response_str = self.process.stdout.readline()
            if response_str:
                return json.loads(response_str)
            else:
                stderr = self.process.stderr.read()
                raise RuntimeError(f"No response. Stderr: {stderr}")
        except Exception as e:
            stderr = self.process.stderr.read() if self.process.stderr else ""
            raise RuntimeError(f"Error: {e}. Stderr: {stderr}")
    
    def close(self):
        if self.process:
            self.process.terminate()
            self.process.wait()

async def test():
    # Test with the travel server
    travel_server = Path(__file__).parent.parent.parent / "mcp_servers" / "travel_server.py"
    
    print(f"🚀 Testing MCP connection...")
    print(f"   Server: {travel_server}")
    
    client = MCPClientStandalone("py", [str(travel_server)])
    
    try:
        await client.connect()
        print("✅ Process started")
        
        print("\n📋 Requesting tool list...")
        result = await client.list_tools()
        
        tools = result.get("result", {}).get("tools", [])
        if tools:
            print(f"\n✅ Found {len(tools)} tools:")
            for t in tools[:10]:
                print(f"   - {t.get('name')}: {t.get('description', '')[:50]}...")
        else:
            print(f"Response: {result}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(test())
