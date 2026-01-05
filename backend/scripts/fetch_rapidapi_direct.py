import asyncio
import os
import json
import httpx
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
if not RAPIDAPI_KEY:
    # Fallback to key from screenshot if env var missing (not recommended for prod but helpful here)
    # But better to warn.
    print("WARNING: RAPIDAPI_KEY not found in env")

async def query_rapidapi_mcp():
    base_url = "https://mcp.rapidapi.com"
    sse_url = f"{base_url}/sse"
    
    headers = {
        "x-api-host": "flights-sky.p.rapidapi.com",
        "x-api-key": RAPIDAPI_KEY,
        "Accept": "text/event-stream"
    }
    
    print(f"Connecting to {sse_url}...")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. Start SSE Session
        async with client.stream("GET", sse_url, headers=headers) as formatted_sse:
            print(f"Update: Connected to SSE (Status {formatted_sse.status_code})")
            
            if formatted_sse.status_code != 200:
                print(f"Failed to connect: {formatted_sse.status_code}")
                content = await formatted_sse.aread()
                print(content.decode())
                return

            # Extract the POST endpoint (usually /message?sessionId=...)
            post_endpoint = None
            session_id = None
            
            async for line in formatted_sse.aiter_lines():
                if line.startswith("event: endpoint"):
                    # Next line is data: <url>
                    pass
                elif line.startswith("data:"):
                    # This might be the endpoint URL
                    data = line[5:].strip()
                    print(f"Received data: {data}")
                    
                    # Try to parse if it's a URL or contains session ID
                    if data.startswith("/"):
                        post_endpoint = f"{base_url}{data}"
                        print(f"Found POST endpoint: {post_endpoint}")
                        break
                    elif "http" in data:
                        post_endpoint = data
                        print(f"Found POST endpoint: {post_endpoint}")
                        break
            
            if not post_endpoint:
                print("Could not find POST endpoint from SSE stream.")
                return

            # 2. Send Initialize
            print("Sending 'initialize'...")
            init_payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "test-client", "version": "1.0"}
                }
            }
            
            response = await client.post(post_endpoint, json=init_payload, headers=headers)
            print(f"Initialize Response: {response.status_code}")
            print(response.json())
            
            # 2.5 Send Notif (initialized)
            await client.post(post_endpoint, json={
                "jsonrpc": "2.0",
                "method": "notifications/initialized"
            }, headers=headers)

            # 3. Send tools/list
            print("Sending 'tools/list'...")
            tools_payload = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list",
                "params": {}
            }
            
            response = await client.post(post_endpoint, json=tools_payload, headers=headers)
            if response.status_code == 200:
                tools_data = response.json()
                print("\n✅ Tools Received:")
                print(json.dumps(tools_data, indent=2))
                
                # Save to file
                with open("rapidapi_custom_tools.json", "w") as f:
                    json.dump(tools_data, f, indent=2)
            else:
                print(f"Error fetching tools: {response.status_code}")
                print(response.text)

if __name__ == "__main__":
    asyncio.run(query_rapidapi_mcp())
