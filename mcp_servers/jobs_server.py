import os
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("jobs")
# API keys are read at call time in each function to ensure proper loading

@mcp.tool()
async def search_jobs(query: str, location: str = "Remote", remote_jobs_only: bool = True) -> str:
    """
    Search for jobs using JSearch API via RapidAPI.
    
    Args:
        query: Job title or keywords (e.g., "Python Developer").
        location: Location (e.g., "New York", "Remote").
        remote_jobs_only: Whether to filter for remote jobs.
    """
    RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
    RAPIDAPI_HOST = "jsearch.p.rapidapi.com"
    if not RAPIDAPI_KEY:
        return "Error: RAPIDAPI_KEY is not set."

    url = f"https://{RAPIDAPI_HOST}/search"
    
    querystring = {
        "query": f"{query} in {location}",
        "page": "1",
        "num_pages": "1"
    }

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=querystring)
            response.raise_for_status()
            data = response.json()
            
            if "data" not in data or not data["data"]:
                return "No jobs found."

            results = []
            for job in data["data"][:5]:
                title = job.get("job_title", "Unknown")
                employer = job.get("employer_name", "Unknown")
                city = job.get("job_city", "")
                country = job.get("job_country", "")
                apply_link = job.get("job_apply_link", "")
                
                location_str = f"{city}, {country}" if city else "Remote"
                
                results.append(f"Role: {title}\nCompany: {employer}\nLocation: {location_str}\nLink: {apply_link}\n---")
            
            return "\n".join(results)

        except Exception as e:
            return f"Error searching jobs: {str(e)}"

@mcp.tool()
async def get_active_jobs() -> str:
    """
    Get a list of currently active/trending jobs (Mock/Placeholder or broad search).
    """
    return await search_jobs(query="Software Engineer", location="Remote")

if __name__ == "__main__":
    mcp.run()
