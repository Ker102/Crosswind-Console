import os
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("trends")

# API Keys and Endpoints
YOUTUBE_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY") # User said same key as Maps
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
X_BEARER_TOKEN = os.environ.get("X_BEARER_TOKEN")

# RapidAPI Hosts
INSTAGRAM_HOST = "instagram-scraper-2022.p.rapidapi.com"
TIKTOK_HOST = "tiktok-scraper7.p.rapidapi.com"
TRENDLY_HOST = "trendly.p.rapidapi.com"

@mcp.tool()
async def get_youtube_trends(region_code: str = "US", max_results: int = 5) -> str:
    """
    Get trending videos on YouTube for a specific region.
    
    Args:
        region_code: ISO 3166-1 alpha-2 country code (e.g., "US", "GB", "IN").
        max_results: Number of videos to return (default 5).
    """
    if not YOUTUBE_API_KEY:
        return "Error: GOOGLE_MAPS_API_KEY (used for YouTube) is not set."

    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet,statistics",
        "chart": "mostPopular",
        "regionCode": region_code,
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get("items", []):
                title = item["snippet"]["title"]
                channel = item["snippet"]["channelTitle"]
                views = item["statistics"].get("viewCount", "N/A")
                video_id = item["id"]
                link = f"https://www.youtube.com/watch?v={video_id}"
                results.append(f"Title: {title}\nChannel: {channel}\nViews: {views}\nLink: {link}\n---")
            
            return "\n".join(results)
        except Exception as e:
            return f"Error fetching YouTube trends: {str(e)}"

@mcp.tool()
async def search_youtube(query: str, max_results: int = 5) -> str:
    """
    Search for videos on YouTube.
    
    Args:
        query: Search term.
        max_results: Number of videos to return.
    """
    if not YOUTUBE_API_KEY:
        return "Error: GOOGLE_MAPS_API_KEY is not set."

    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get("items", []):
                title = item["snippet"]["title"]
                channel = item["snippet"]["channelTitle"]
                video_id = item["id"]["videoId"]
                link = f"https://www.youtube.com/watch?v={video_id}"
                results.append(f"Title: {title}\nChannel: {channel}\nLink: {link}\n---")
            
            return "\n".join(results)
        except Exception as e:
            return f"Error searching YouTube: {str(e)}"

@mcp.tool()
async def get_google_trends(keyword: str, geo: str = "US") -> str:
    """
    Get Google Trends data for a keyword using Trendly (RapidAPI).
    
    Args:
        keyword: The term to check trends for.
        geo: Region code (e.g., "US").
    """
    if not RAPIDAPI_KEY:
        return "Error: RAPIDAPI_KEY is not set."

    url = f"https://{TRENDLY_HOST}/trends" # Hypothetical endpoint based on typical RapidAPI structure, adjusting to user provided link context if needed or generic wrapper
    # Note: The user provided https://rapidapi.com/odlica-odlica-default/api/trendly
    # We will assume a standard 'search' or 'interest' endpoint. 
    # Since I cannot browse the exact docs live, I will use a generic structure common to these APIs.
    # If this fails, the user will see the error and we can adjust.
    
    # Actually, let's use a safer generic approach or just return a placeholder if we are unsure of the exact endpoint path without docs.
    # But I will try to implement a reasonable guess for "interest over time".
    
            return "\n".join(results)
        except Exception as e:
            return f"Error searching X: {str(e)}"

if __name__ == "__main__":
    mcp.run()
