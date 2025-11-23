import os
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("jobs")
                    title = job.get("title", "Unknown")
                    company = job.get("organization", "Unknown")
                    url = job.get("url", "")
                    results.append(f"{title} at {company}: {url}")
                return "\n".join(results)
            
            return str(data)[:1000] # Fallback
            
        except Exception as e:
            return f"Error fetching active jobs: {str(e)}"

if __name__ == "__main__":
    mcp.run()
