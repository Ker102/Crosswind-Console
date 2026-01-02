import asyncio
import subprocess
import json
import os
from typing import Dict, List, Optional, Any

class MCPClient:
    def __init__(self, server_config: Dict[str, Any]):
        self.config = server_config
        self.process: Optional[subprocess.Popen] = None
        self._request_id = 0
        
    async def connect(self):
        """Start MCP server process via stdio"""
        try:
            # Prepare command
            cmd = [self.config["command"]] + self.config["args"]
            
            # Start process
            # Note: shell=True might be needed on Windows for npx if not in path, 
            # but usually better to avoid.
            self.process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,  # Use text mode for easier JSON handling
                encoding='utf-8',
                bufsize=1   # Line buffered
            )
            print(f"✅ Connected to MCP server: RapidAPI Hub - Flights Scraper Sky")
            
        except Exception as e:
            print(f"❌ Failed to connect to MCP server: {e}")
            raise e
    
    async def list_tools(self) -> List[Dict]:
        """Get available tools and their schemas"""
        if not self.process:
            await self.connect()
            
        request = {
            "jsonrpc": "2.0", 
            "method": "tools/list", 
            "id": self._get_next_id()
        }
        
        response = await self._send(request)
        return response.get("result", {}).get("tools", [])
    
    async def call_tool(self, name: str, arguments: Dict) -> Dict:
        """Call a tool with arguments"""
        if not self.process:
            await self.connect()
            
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments},
            "id": self._get_next_id()
        }
        
        return await self._send(request)
    
    def _get_next_id(self) -> int:
        self._request_id += 1
        return self._request_id
    
    async def _send(self, request: Dict) -> Dict:
        """Send JSON-RPC request to MCP server"""
        if not self.process or self.process.poll() is not None:
            raise RuntimeError("MCP server process is not running")

        json_req = json.dumps(request)
        self.process.stdin.write(json_req + "\n")
        self.process.stdin.flush()
        
        # Read response line by line
        # This is simple; a robust client needs async reading loop
        response_str = self.process.stdout.readline()
        
        if not response_str:
            stderr = self.process.stderr.read()
            raise RuntimeError(f"MCP server closed connection. Stderr: {stderr}")
            
        return json.loads(response_str)

    def close(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
