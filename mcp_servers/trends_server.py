import os
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("trends")

# API keys are read at call time in each function to ensure proper loading
# RapidAPI Hosts (constants)
INSTAGRAM_HOST = "instagram-scraper-2022.p.rapidapi.com"
TIKTOK_HOST = "tiktok-scraper7.p.rapidapi.com"
TRENDLY_HOST = "trendly.p.rapidapi.com"
FACEBOOK_HOST = "facebook-scraper3.p.rapidapi.com"

@mcp.tool()
async def get_youtube_trends(region_code: str = "US", max_results: int = 5) -> str:
    """
    Get trending videos on YouTube for a specific region.
    
    Args:
        region_code: ISO 3166-1 alpha-2 country code (e.g., "US", "GB", "IN").
        max_results: Number of videos to return (default 5).
    """
    YOUTUBE_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")
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
    YOUTUBE_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")
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
    RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
    if not RAPIDAPI_KEY:
        return "Error: RAPIDAPI_KEY is not set."

    url = f"https://{TRENDLY_HOST}/interest_over_time" 
    
    querystring = {"keyword": keyword, "geo": geo}

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": TRENDLY_HOST
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=querystring)
            response.raise_for_status()
            data = response.json()
            return str(data)[:1000] # Return raw data for now as structure is unknown
        except Exception as e:
            return f"Error fetching Google Trends: {str(e)}"

@mcp.tool()
async def search_tweets(query: str, max_results: int = 10) -> str:
    """
    Search for recent tweets on X (Twitter) using the official API.
    
    Args:
        query: Search query (e.g., "AI trends", "#travel", "from:elonmusk").
        max_results: Number of tweets to return (10-100, default 10).
    """
    X_BEARER_TOKEN = os.environ.get("X_BEARER_TOKEN")
    if not X_BEARER_TOKEN:
        return "Error: X_BEARER_TOKEN is not set."

    url = "https://api.x.com/2/tweets/search/recent"
    params = {
        "query": query,
        "max_results": min(max(max_results, 10), 100),
        "tweet.fields": "created_at,public_metrics,author_id",
        "expansions": "author_id",
        "user.fields": "username,name"
    }
    
    headers = {
        "Authorization": f"Bearer {X_BEARER_TOKEN}"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            if "data" not in data:
                return f"No tweets found for '{query}'."
            
            # Build user lookup
            users = {u["id"]: u for u in data.get("includes", {}).get("users", [])}
            
            results = []
            for tweet in data["data"][:10]:
                text = tweet.get("text", "")[:200]
                author_id = tweet.get("author_id", "")
                author = users.get(author_id, {})
                username = author.get("username", "unknown")
                name = author.get("name", "Unknown")
                metrics = tweet.get("public_metrics", {})
                likes = metrics.get("like_count", 0)
                retweets = metrics.get("retweet_count", 0)
                
                results.append(
                    f"@{username} ({name})\n"
                    f"{text}\n"
                    f"❤️ {likes} | 🔁 {retweets}\n---"
                )
            
            return "\n".join(results)
        except httpx.HTTPStatusError as e:
            return f"X API Error: {e.response.status_code} - {e.response.text[:200]}"
        except Exception as e:
            return f"Error searching tweets: {str(e)}"

@mcp.tool()
async def get_tiktok_trends(region: str = "US") -> str:
    """
    Get trending videos on TikTok for a specific region.
    
    Args:
        region: Country code (e.g., "US", "GB", "IN").
    """
    RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
    if not RAPIDAPI_KEY:
        return "Error: RAPIDAPI_KEY is not set."

    url = f"https://{TIKTOK_HOST}/feed/list"
    params = {"region": region, "count": "10"}
    
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": TIKTOK_HOST
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            videos = data.get("data", {}).get("videos", [])
            if not videos:
                return "No trending TikTok videos found."
            
            results = []
            for video in videos[:7]:
                title = video.get("title", "No title")[:100]
                author = video.get("author", {}).get("nickname", "Unknown")
                plays = video.get("play_count", 0)
                likes = video.get("digg_count", 0)
                url_link = video.get("play", "")
                
                results.append(
                    f"🎵 {title}\n"
                    f"   By: {author}\n"
                    f"   ▶️ {plays:,} plays | ❤️ {likes:,} likes\n---"
                )
            
            return "\n".join(results)
        except Exception as e:
            return f"Error fetching TikTok trends: {str(e)}"

@mcp.tool()
async def search_tiktok(query: str) -> str:
    """
    Search for TikTok videos by keyword.
    
    Args:
        query: Search term (e.g., "cooking recipes", "dance challenge").
    """
    RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
    if not RAPIDAPI_KEY:
        return "Error: RAPIDAPI_KEY is not set."

    url = f"https://{TIKTOK_HOST}/feed/search"
    params = {"keywords": query, "count": "10", "cursor": "0"}
    
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": TIKTOK_HOST
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            videos = data.get("data", {}).get("videos", [])
            if not videos:
                return f"No TikTok videos found for '{query}'."
            
            results = []
            for video in videos[:7]:
                title = video.get("title", "No title")[:100]
                author = video.get("author", {}).get("nickname", "Unknown")
                plays = video.get("play_count", 0)
                
                results.append(
                    f"🎵 {title}\n"
                    f"   By: {author} | ▶️ {plays:,} plays\n---"
                )
            
            return "\n".join(results)
        except Exception as e:
            return f"Error searching TikTok: {str(e)}"

@mcp.tool()
async def search_instagram(query: str, search_type: str = "hashtag") -> str:
    """
    Search Instagram for hashtags or user profiles.
    
    Args:
        query: What to search for (hashtag name without # or username).
        search_type: Either "hashtag" or "user".
    """
    RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
    if not RAPIDAPI_KEY:
        return "Error: RAPIDAPI_KEY is not set."

    if search_type == "hashtag":
        url = f"https://{INSTAGRAM_HOST}/ig/hashtag/"
        params = {"hashtag": query}
    else:
        url = f"https://{INSTAGRAM_HOST}/ig/user_id/"
        params = {"user": query}
    
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": INSTAGRAM_HOST
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            if search_type == "hashtag":
                count = data.get("media_count", 0)
                name = data.get("name", query)
                return f"Hashtag #{name}\nPosts: {count:,}"
            else:
                user_id = data.get("id", "")
                return f"User @{query}\nUser ID: {user_id}"
        except Exception as e:
            return f"Error searching Instagram: {str(e)}"

@mcp.tool()
async def get_instagram_posts(hashtag: str, count: int = 10) -> str:
    """
    Get recent posts from an Instagram hashtag.
    
    Args:
        hashtag: The hashtag to fetch posts from (without #).
        count: Number of posts to return (default 10).
    """
    RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
    if not RAPIDAPI_KEY:
        return "Error: RAPIDAPI_KEY is not set."

    url = f"https://{INSTAGRAM_HOST}/ig/hashtag_posts/"
    params = {"hashtag": hashtag, "count": str(count)}
    
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": INSTAGRAM_HOST
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            posts = data.get("data", [])
            if not posts:
                return f"No posts found for #{hashtag}."
            
            results = []
            for post in posts[:7]:
                caption = post.get("caption", {}).get("text", "No caption")[:150]
                likes = post.get("like_count", 0)
                comments = post.get("comment_count", 0)
                owner = post.get("owner", {}).get("username", "unknown")
                
                results.append(
                    f"📸 @{owner}\n"
                    f"   {caption}\n"
                    f"   ❤️ {likes:,} | 💬 {comments:,}\n---"
                )
            
            return "\n".join(results)
        except Exception as e:
            return f"Error fetching Instagram posts: {str(e)}"

@mcp.tool()
async def search_facebook(query: str) -> str:
    """
    Search for public Facebook content (posts, pages) by keyword.
    
    Args:
        query: Search term (e.g., "AI news", "travel tips", "cooking recipes").
    """
    RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
    if not RAPIDAPI_KEY:
        return "Error: RAPIDAPI_KEY is not set."

    url = f"https://{FACEBOOK_HOST}/search"
    params = {"query": query, "count": "10"}
    
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": FACEBOOK_HOST
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            results_data = data.get("results", [])
            if not results_data:
                return f"No Facebook results found for '{query}'."
            
            results = []
            for item in results_data[:7]:
                title = item.get("title", "No title")[:100]
                description = item.get("description", "No description")[:150]
                url_link = item.get("url", "")
                item_type = item.get("type", "unknown")
                
                results.append(
                    f"📘 {title}\n"
                    f"   {description}\n"
                    f"   Type: {item_type}\n"
                    f"   Link: {url_link}\n---"
                )
            
            return "\n".join(results)
        except Exception as e:
            return f"Error searching Facebook: {str(e)}"

if __name__ == "__main__":
    mcp.run()
