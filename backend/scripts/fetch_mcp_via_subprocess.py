"""
Spawn mcp-remote and query tools via newline-delimited JSON-RPC over stdin/stdout.
Based on MCP protocol spec: messages are newline-delimited JSON.
"""
import subprocess
import json
import os
import sys
import time
import threading
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
if not RAPIDAPI_KEY:
    print("ERROR: RAPIDAPI_KEY not found in .env")
    sys.exit(1)

def read_stderr(proc):
    """Read stderr in background thread to capture mcp-remote logs."""
    for line in proc.stderr:
        print(f"[stderr] {line.strip()}")

def main():
    # Build the command
    cmd = [
        "npx", "-y", "mcp-remote",
        "https://mcp.rapidapi.com",
        "--header", f"x-api-host: flights-sky.p.rapidapi.com",
        "--header", f"x-api-key: {RAPIDAPI_KEY}"
    ]
    
    print(f"Starting mcp-remote...")
    
    # Start the subprocess
    import platform
    use_shell = platform.system() == "Windows"
    
    proc = subprocess.Popen(
        cmd if not use_shell else " ".join(cmd),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=use_shell
    )
    
    # Start stderr reader thread
    stderr_thread = threading.Thread(target=read_stderr, args=(proc,), daemon=True)
    stderr_thread.start()
    
    try:
        # Give it time to connect
        print("Waiting for mcp-remote to connect...")
        time.sleep(5)
        
        # Check if process is still running
        if proc.poll() is not None:
            print(f"Process exited with code {proc.returncode}")
            return
        
        # 1. Send initialize (newline-delimited JSON)
        print("\n--- Sending initialize ---")
        init_msg = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "schema-fetcher", "version": "1.0"}
            }
        }
        proc.stdin.write(json.dumps(init_msg) + "\n")
        proc.stdin.flush()
        print(f"-> Sent: initialize")
        
        # Read response (with timeout)
        import select
        time.sleep(2)  # Give time for response
        
        # Try to read a line
        response_line = proc.stdout.readline()
        if response_line:
            print(f"<- Response: {response_line[:200]}...")
            try:
                response = json.loads(response_line)
                print(f"<- Parsed: {json.dumps(response, indent=2)[:500]}")
            except json.JSONDecodeError:
                print(f"<- Raw: {response_line}")
        else:
            print("No response received")
        
        # 2. Send initialized notification
        init_notif = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        proc.stdin.write(json.dumps(init_notif) + "\n")
        proc.stdin.flush()
        print("-> Sent: notifications/initialized")
        
        # 3. Request tools/list
        print("\n--- Sending tools/list ---")
        tools_msg = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        proc.stdin.write(json.dumps(tools_msg) + "\n")
        proc.stdin.flush()
        print("-> Sent: tools/list")
        
        # Read response
        time.sleep(3)
        response_line = proc.stdout.readline()
        if response_line:
            print(f"<- Response received ({len(response_line)} bytes)")
            try:
                response = json.loads(response_line)
                tools = response.get("result", {}).get("tools", [])
                print(f"\n✅ Found {len(tools)} tools!")
                
                # Print summary
                for i, tool in enumerate(tools[:25]):
                    name = tool.get("name", "unknown")
                    desc = tool.get("description", "")[:40]
                    print(f"  {i+1}. {name}: {desc}...")
                
                if len(tools) > 25:
                    print(f"  ... and {len(tools) - 25} more")
                
                # Save full output
                output_file = "rapidapi_sky_tools_full.json"
                with open(output_file, "w") as f:
                    json.dump(response, f, indent=2)
                print(f"\n✨ Saved full schemas to {output_file}")
                
            except json.JSONDecodeError as e:
                print(f"<- Failed to parse: {e}")
                print(f"<- Raw: {response_line[:500]}")
        else:
            print("No response received for tools/list")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except:
            proc.kill()
        print("\nProcess terminated.")

if __name__ == "__main__":
    main()
