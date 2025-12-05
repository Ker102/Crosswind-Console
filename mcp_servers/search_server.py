import os
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("search")

@mcp.tool()
async def web_search(query: str, num_results: int = 5) -> str:
    """
    Search the web using Google Custom Search API.
    
    Args:
        query: The search query.
        num_results: Number of results to return (max 10).
    """
    # Read env vars at call time, not import time
    GOOGLE_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")
    GOOGLE_CX = os.environ.get("GOOGLE_SEARCH_CX")
    
    if not GOOGLE_API_KEY:
        return "Error: GOOGLE_MAPS_API_KEY is not set."
    if not GOOGLE_CX:
        return "Error: GOOGLE_SEARCH_CX is not set. Please create a Programmable Search Engine."

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CX,
        "q": query,
        "num": num_results
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get("items", []):
                title = item.get("title", "No Title")
                link = item.get("link", "")
                snippet = item.get("snippet", "")
                results.append(f"Title: {title}\nLink: {link}\nSnippet: {snippet}\n---")
            
            return "\n".join(results)
        except Exception as e:
            return f"Error searching web: {str(e)}"

if __name__ == "__main__":
    mcp.run()
