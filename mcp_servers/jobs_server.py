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

# ResumeOptimizer API Host
RESUME_OPTIMIZER_HOST = "resumeoptimizerpro.p.rapidapi.com"

@mcp.tool()
async def optimize_resume(resume_text: str, job_description: str) -> str:
    """
    Optimize a resume for a specific job posting. Makes the resume more likely to pass ATS systems.
    
    Args:
        resume_text: The full text of the resume to optimize.
        job_description: The job posting text to optimize the resume for.
    """
    RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
    if not RAPIDAPI_KEY:
        return "Error: RAPIDAPI_KEY is not set."

    url = f"https://{RESUME_OPTIMIZER_HOST}/optimize"
    
    payload = {
        "resume": resume_text,
        "job_description": job_description
    }
    
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RESUME_OPTIMIZER_HOST,
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            optimized = data.get("optimized_resume", "")
            score = data.get("score", "N/A")
            suggestions = data.get("suggestions", [])
            
            result = f"📊 Match Score: {score}\n\n"
            
            if suggestions:
                result += "💡 Suggestions:\n"
                for s in suggestions[:5]:
                    result += f"  • {s}\n"
                result += "\n"
            
            if optimized:
                result += f"📝 Optimized Resume Preview:\n{optimized[:1000]}..."
            
            return result
        except Exception as e:
            return f"Error optimizing resume: {str(e)}"

@mcp.tool()
async def analyze_job_match(resume_text: str, job_description: str) -> str:
    """
    Analyze how well a resume matches a job description. Shows strengths, partial matches, and gaps.
    
    Args:
        resume_text: The full text of the resume.
        job_description: The job posting text to compare against.
    """
    RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
    if not RAPIDAPI_KEY:
        return "Error: RAPIDAPI_KEY is not set."

    url = f"https://{RESUME_OPTIMIZER_HOST}/analyze"
    
    payload = {
        "resume": resume_text,
        "job_description": job_description
    }
    
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RESUME_OPTIMIZER_HOST,
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            score = data.get("match_score", "N/A")
            strengths = data.get("strengths", [])
            partial = data.get("partial_matches", [])
            gaps = data.get("gaps", [])
            
            result = f"📊 Job Match Score: {score}\n\n"
            
            if strengths:
                result += "✅ Strengths:\n"
                for s in strengths[:5]:
                    result += f"  • {s}\n"
                result += "\n"
            
            if partial:
                result += "🔶 Partial Matches:\n"
                for p in partial[:5]:
                    result += f"  • {p}\n"
                result += "\n"
            
            if gaps:
                result += "❌ Gaps to Address:\n"
                for g in gaps[:5]:
                    result += f"  • {g}\n"
            
            return result
        except Exception as e:
            return f"Error analyzing job match: {str(e)}"

if __name__ == "__main__":
    mcp.run()
