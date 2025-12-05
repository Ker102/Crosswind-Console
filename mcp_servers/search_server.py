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


@mcp.tool()
async def scrape_webpage(url: str, only_main_content: bool = True) -> str:
    """
    Extract content from a webpage as clean markdown using Firecrawl.
    Use this as a BACKUP when other tools don't provide enough detail,
    or to get the full content of a specific page.
    
    Args:
        url: The URL of the webpage to scrape.
        only_main_content: If True, extract only the main content (skip headers/footers/ads).
    """
    FIRECRAWL_API_KEY = os.environ.get("FIRECRAWL_API_KEY")
    if not FIRECRAWL_API_KEY:
        return "Error: FIRECRAWL_API_KEY is not set. Cannot scrape webpage."

    api_url = "https://api.firecrawl.dev/v1/scrape"
    headers = {
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "url": url,
        "formats": ["markdown"],
        "onlyMainContent": only_main_content
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(api_url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            if data.get("success"):
                markdown = data.get("data", {}).get("markdown", "")
                title = data.get("data", {}).get("metadata", {}).get("title", "Unknown")
                
                # Truncate if too long (keep first ~3000 chars)
                if len(markdown) > 3000:
                    markdown = markdown[:3000] + "\n\n... [Content truncated]"
                
                return f"**Page: {title}**\n\n{markdown}"
            else:
                return f"Firecrawl error: {data.get('error', 'Unknown error')}"
        except Exception as e:
            return f"Error scraping webpage: {str(e)}"


@mcp.tool()
async def crawl_website(url: str, max_pages: int = 5) -> str:
    """
    Crawl a website and extract content from multiple pages.
    Use this as a BACKUP for comprehensive research when you need info from many pages of a site.
    
    Args:
        url: The starting URL for the crawl.
        max_pages: Maximum number of pages to crawl (default 5, max 10).
    """
    FIRECRAWL_API_KEY = os.environ.get("FIRECRAWL_API_KEY")
    if not FIRECRAWL_API_KEY:
        return "Error: FIRECRAWL_API_KEY is not set. Cannot crawl website."

    max_pages = min(max_pages, 10)  # Cap at 10 pages
    
    api_url = "https://api.firecrawl.dev/v1/crawl"
    headers = {
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "url": url,
        "limit": max_pages,
        "scrapeOptions": {
            "formats": ["markdown"],
            "onlyMainContent": True
        }
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            # Start the crawl job
            response = await client.post(api_url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            if not data.get("success"):
                return f"Firecrawl error: {data.get('error', 'Unknown error')}"
            
            crawl_id = data.get("id")
            if not crawl_id:
                return "Error: No crawl job ID returned"
            
            # Poll for results (with timeout)
            import asyncio
            status_url = f"https://api.firecrawl.dev/v1/crawl/{crawl_id}"
            
            for _ in range(12):  # Max 60 seconds (12 * 5s)
                await asyncio.sleep(5)
                status_response = await client.get(status_url, headers=headers)
                status_data = status_response.json()
                
                if status_data.get("status") == "completed":
                    pages = status_data.get("data", [])
                    results = []
                    for page in pages[:max_pages]:
                        title = page.get("metadata", {}).get("title", "Unknown")
                        page_url = page.get("metadata", {}).get("sourceURL", "")
                        markdown = page.get("markdown", "")[:1000]  # First 1000 chars per page
                        results.append(f"### {title}\nURL: {page_url}\n{markdown}\n---")
                    
                    return f"Crawled {len(pages)} pages:\n\n" + "\n".join(results)
                
                if status_data.get("status") == "failed":
                    return f"Crawl failed: {status_data.get('error', 'Unknown error')}"
            
            return "Crawl timed out. Try with fewer pages."
        except Exception as e:
            return f"Error crawling website: {str(e)}"


if __name__ == "__main__":
    mcp.run()
