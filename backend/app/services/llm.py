from __future__ import annotations

import asyncio
import logging
import os
import sys
import textwrap
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

# Configure logging to file
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(Path(__file__).parent.parent.parent / "llm_debug.log", mode='a'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Add project root to path to allow importing mcp modules
sys.path.append(str(Path(__file__).parents[3]))

try:
    import google.generativeai as genai
    from google.generativeai.types import FunctionDeclaration
except Exception:
    genai = None

# Import MCP Tools
try:
    from mcp_servers.jobs_server import get_active_jobs, search_jobs, optimize_resume, analyze_job_match
    from mcp_servers.search_server import web_search, scrape_webpage, crawl_website
    from mcp_servers.travel_server import (
        search_flights, search_places, search_hotels, search_flights_sky,
        search_ground_transport, search_ground_transport_backup, get_directions,
        geocode_address, reverse_geocode, text_search_places, search_places_nearby,
        search_airbnb, search_amadeus_flights, search_amadeus_hotels
    )
    from mcp_servers.trends_server import (
        get_google_trends, get_youtube_trends, search_tweets, search_youtube,
        get_tiktok_trends, search_tiktok, search_instagram, get_instagram_posts, search_facebook
    )
    
    MCP_TOOLS = [
        # Travel tools (search_flights=Kiwi, search_flights_sky=Skyscanner, search_amadeus_*=Amadeus - use for comparison)
        search_flights, search_flights_sky, search_amadeus_flights, search_amadeus_hotels,
        search_places, search_hotels, search_airbnb,
        search_ground_transport, search_ground_transport_backup, get_directions,
        geocode_address, reverse_geocode, text_search_places, search_places_nearby,
        # Jobs tools
        search_jobs, get_active_jobs, optimize_resume, analyze_job_match,
        # Search & scraping tools (backup for all agents)
        web_search, scrape_webpage, crawl_website,
        # Trends tools
        get_youtube_trends, search_youtube, get_google_trends, search_tweets,
        get_tiktok_trends, search_tiktok, search_instagram, get_instagram_posts, search_facebook
    ]
except ImportError:
    MCP_TOOLS = []
    print("Warning: Could not import MCP tools. Ensure mcp module is in path.")

from ..config import Settings
from ..schemas import Domain, Insight

# Import RAG service for context retrieval
try:
    from .rag_service import RAGService
    RAG_AVAILABLE = True
except ImportError as e:
    RAGService = None
    RAG_AVAILABLE = False
    logger.warning(f"RAGService not available: {e}")


@dataclass
class LLMResult:
    text: str
    latency_ms: float | None
    model: str
    trace: str | None = None


class GeminiClient:
    def __init__(self, settings: Settings) -> None:
        self.model_id = settings.gemini_model
        self._api_key = settings.gemini_api_key
        self._enabled = bool(self._api_key and genai)
        self._model = None
        
        # Debug logging
        logger.info(f"GEMINI_API_KEY loaded: {bool(self._api_key)}")
        logger.info(f"google-generativeai imported: {bool(genai)}")
        logger.info(f"Gemini enabled: {self._enabled}")
        
        # Propagate settings to os.environ for MCP tools
        if settings.rapidapi_key: os.environ["RAPIDAPI_KEY"] = settings.rapidapi_key
        if settings.google_maps_api_key: os.environ["GOOGLE_MAPS_API_KEY"] = settings.google_maps_api_key
        if settings.google_search_cx: os.environ["GOOGLE_SEARCH_CX"] = settings.google_search_cx
        if settings.x_bearer_token: os.environ["X_BEARER_TOKEN"] = settings.x_bearer_token
        if settings.tripadvisor_api_key: os.environ["TRIPADVISOR_API_KEY"] = settings.tripadvisor_api_key
        if settings.apify_api_token: os.environ["APIFY_API_TOKEN"] = settings.apify_api_token
        
        # Propagate Supabase and Together AI for RAG service
        if settings.supabase_url: os.environ["SUPABASE_URL"] = settings.supabase_url
        if settings.supabase_key: os.environ["SUPABASE_KEY"] = settings.supabase_key
        if settings.together_api_key: os.environ["TOGETHER_API_KEY"] = settings.together_api_key

        if self._enabled:
            genai.configure(api_key=self._api_key)
            # Initialize model with tools and max output tokens
            self._model = genai.GenerativeModel(
                self.model_id,
                tools=MCP_TOOLS,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=65536  # Maximum for gemini-2.5-pro
                )
            )
        
        # Initialize RAG service for context retrieval
        self.rag_service = None
        self._rag_enabled = False
        if RAG_AVAILABLE:
            try:
                self.rag_service = RAGService()
                self._rag_enabled = True
                logger.info("RAG service initialized successfully")
            except Exception as e:
                logger.warning(f"RAG service initialization failed: {e}")

    async def summarize(self, domain: Domain, insights: Iterable[Insight], prompt: str | None) -> LLMResult:
        context = "\n".join(
            f"- {item.title}: {item.description}" for item in insights
        )
        base_prompt = textwrap.dedent(
            f"""You are a research copilot creating concise intel recaps.
            Summarize the most important signals for the `{domain.value}` domain.
            Highlight opportunities and suggested next steps in <= 120 words.
            """
        ).strip()
        if prompt:
            base_prompt += f"\nUser prompt: {prompt}"
        base_prompt += f"\nContext:\n{context}"

        if not self._enabled:
            fallback = self._build_fallback_summary(domain, insights, prompt)
            return LLMResult(text=fallback, latency_ms=None, model="mock-gemini", trace="mock")

        loop = asyncio.get_running_loop()
        start = time.perf_counter()
        # Summarization typically doesn't need tools, but we can enable them if needed.
        # For now, keeping it text-only for speed unless prompt implies research.
        response = await loop.run_in_executor(None, lambda: self._model.generate_content(base_prompt))
        latency_ms = (time.perf_counter() - start) * 1000
        text = response.text if hasattr(response, "text") else str(response)
        return LLMResult(text=text, latency_ms=latency_ms, model=self.model_id)

    async def respond(self, prompt: str, context: Iterable[Insight] | None = None, history: Iterable[Any] | None = None, mode: str = "general", travel_intent: dict | None = None) -> LLMResult:
        combined_prompt = prompt
        if travel_intent and mode == "travel":
            combined_prompt = (
                "STRUCTURED_TRAVEL_INTENT (use this to build exact tool params):\n"
                + str(travel_intent)
                + "\n\nUser prompt:\n"
                + combined_prompt
            )
        if context:
            combined_prompt += "\n\nContext:\n" + "\n".join(
                f"- {item.title}: {item.description}" for item in context
            )
        if not self._enabled:
            return LLMResult(
                text="Gemini disabled. Install a key and restart the API.",
                latency_ms=None,
                model="mock-gemini",
                trace="mock",
            )
        
        # Retrieve RAG context for API parameter guidance
        rag_context = ""
        if self._rag_enabled and mode in ["travel", "jobs", "trends"]:
            try:
                # Search RAG for relevant parameter docs
                rag_docs = await self.rag_service.search(prompt, mode, top_k=3)
                if rag_docs:
                    rag_context = "\n\n## API PARAMETER GUIDANCE (from RAG database)\n"
                    rag_context += "Use this information to format tool parameters correctly:\n\n"
                    rag_context += "\n\n---\n\n".join([
                        f"### {doc.get('title', 'Untitled')}\n{doc.get('content', '')[:1000]}"
                        for doc in rag_docs
                    ])
                    logger.info(f"RAG: Retrieved {len(rag_docs)} docs for mode={mode}")
            except Exception as e:
                logger.warning(f"RAG search failed: {e}")
                rag_context = ""
        
        # Prepend RAG context to the prompt if available
        if rag_context:
            combined_prompt = rag_context + "\n\n---\n\n" + combined_prompt
        
        start = time.perf_counter()
        
        # Convert history to Gemini format if provided
        chat_history = []
        if history:
            for msg in history:
                chat_history.append({
                    "role": msg.role,
                    "parts": [msg.content]
                })

        # Manual function calling loop (async-compatible)
        # Disable automatic function calling since our tools are async
        chat = self._model.start_chat(history=chat_history)
        
        # Build tool name -> function mapping
        tool_map = {func.__name__: func for func in MCP_TOOLS}
        logger.info(f"Available tools: {list(tool_map.keys())}")
        
        # Agent-specific system prompts
        SYSTEM_PROMPTS = {
            "travel": """You are a TRAVEL PLANNING ORCHESTRATOR. You execute task-specific chains to complete travel requests.

## CHAIN-OF-THOUGHT PROCESS
Before ANY tool call, briefly think about which chain(s) to run:
<thinking>
1. What is the user asking for? (flights/hotels/transport/places/full trip)
2. Which chain(s) should I execute?
3. What are the key parameters? (dates, locations, passengers)
</thinking>

---

## AVAILABLE CHAINS

### 🛫 FLIGHT_SEARCH_CHAIN
**Use for**: "Find flights", "Book flight", flight prices, "fly to X"
**Tools**: search_flights, search_flights_sky, search_google_flights, search_booking_flights
**Steps**:
1. Parse origin/destination → IATA codes (TLL, HEL, JFK, CDG, etc.)
2. Parse dates → YYYY-MM-DD format. Default year: 2025
3. Call search_flights(from_location=IATA, to_location=IATA, date_from="YYYY-MM-DD")
4. Call search_flights_sky(from_location=IATA, to_location=IATA, date="YYYY-MM-DD")
5. If either fails → Try search_google_flights, then search_booking_flights
6. Compare results, rank by price
7. OUTPUT: Top 5 flight options with prices, airlines, times

**Round trips**: Add return_from (Kiwi) or return_date (Skyscanner)
**Date ranges**: Use date_from + date_to (Kiwi only)
**Whole month**: Use whole_month="YYYY-MM" (Skyscanner only)
**Stops filter**: Use max_stops=0 (direct), 1 (up to 1 stop), 2 (up to 2 stops), or None (any)

### 📊 FLIGHT RESULT ANALYSIS GUIDELINES (CRITICAL)
When presenting flight search results to the user:

1. **ANALYZE ALL FLIGHTS** - Don't just show the cheapest. Read the metadata summary at the top.
2. **ALWAYS MENTION DIRECT FLIGHTS** - Even if not the cheapest, state "Direct flights available from $X"
3. **SHOW PRICE TRADE-OFFS** - Format like: "Direct flights from $91 (1h 05m) or save $14 with a 1-stop via Stockholm ($77, 3h 30m)"
4. **HIGHLIGHT THE SUMMARY** - The tool output starts with a summary (📊 Found X flights...). Use this data!
5. **INCLUDE BOOKING LINKS** - Always provide the booking links for recommended options
6. **MENTION STOPS FILTER** - If user filtered stops, acknowledge it: "Showing direct flights only as requested"

---

### 🏨 ACCOMMODATION_CHAIN
**Use for**: "Find hotel", "Where to stay", "apartments in X", accommodation
**Tools**: search_hotels, search_airbnb
**Steps**:
1. Parse location and check-in/check-out dates
2. Call search_hotels(location="City", check_in="YYYY-MM-DD", check_out="YYYY-MM-DD")
3. Call search_airbnb(location="City", check_in="YYYY-MM-DD", check_out="YYYY-MM-DD")
4. Compare prices and ratings
5. OUTPUT: Top 5 hotels + Top 5 apartments with prices and links

---

### 🚌 TRANSPORT_CHAIN
**Use for**: "How to get from airport", "directions to", ground transport
**Tools**: get_directions, search_ground_transport
**Steps**:
1. Identify origin (airport/station) and destination (hotel/city center)
2. Call get_directions(origin="Airport Name", destination="City Center", mode="transit")
3. Call search_ground_transport(origin="...", destination="...") for alternatives
4. OUTPUT: Route options with times, costs, and specific instructions

**For ferries**: Use get_directions with mode="transit" (includes ferry routes)

---

### 📍 PLACES_CHAIN
**Use for**: "Things to do", "restaurants near", "attractions in X"
**Tools**: search_places, text_search_places, search_places_nearby
**Steps**:
1. Identify location/city
2. Call search_places(query="top attractions in [City]")
3. If hotel location known, call search_places_nearby(lat, lng, type="restaurant")
4. OUTPUT: Categorized list (restaurants, sights, activities) with ratings

---

### ✈️🏨 FULL_TRIP_CHAIN (Orchestrator)
**Use for**: "Plan a trip", "Travel to X", "Weekend in Y", comprehensive planning
**Executes**: FLIGHT_SEARCH → TRANSPORT → ACCOMMODATION → PLACES
**Steps**:
1. Parse user query for all components (dates, destination, travelers)
2. Execute FLIGHT_SEARCH_CHAIN → Get best flight options
3. Execute TRANSPORT_CHAIN → Airport to city center directions
4. Execute ACCOMMODATION_CHAIN → Hotels and apartments
5. Execute PLACES_CHAIN → Top attractions (optional)
6. SYNTHESIZE: Combine into complete travel plan with all options

---

## EXECUTION RULES (CRITICAL)

1. **ANNOUNCE which chain you're running**:
   [EXECUTING: FLIGHT_SEARCH_CHAIN]
   
2. **NEVER stop mid-chain** - Complete all steps before moving on

3. **For FULL_TRIP_CHAIN**: Run ALL sub-chains sequentially. Do not stop after flights.

4. **Compare multiple sources**: Always call both Kiwi AND Skyscanner for flights, Hotels AND Airbnb for accommodation

5. **If a tool fails**: Try the backup tools before giving up

6. **ALWAYS end with a synthesized summary** combining all results

---

## PARAMETER QUICK REFERENCE

| Parameter | Format | Example |
|-----------|--------|---------|
| Dates | YYYY-MM-DD | 2025-01-15 |
| Airports | IATA code | TLL, HEL, JFK, CDG |
| Cabin class | ECONOMY, BUSINESS, FIRST_CLASS | cabin_class="BUSINESS" |
| Round trip | return_from (Kiwi), return_date (Sky) | return_from="2025-01-20" |

---

## INTENT DETECTION

| User says... | Chain to run |
|--------------|--------------|
| "Flights to Paris" | FLIGHT_SEARCH_CHAIN only |
| "Hotels in Barcelona" | ACCOMMODATION_CHAIN only |
| "How to get from airport" | TRANSPORT_CHAIN only |
| "Things to do in Rome" | PLACES_CHAIN only |
| "Plan a trip to Tokyo" | FULL_TRIP_CHAIN (all 4) |
| "Flights and hotel in X" | FLIGHT_SEARCH + ACCOMMODATION |

---

## RESPONSE FORMAT

End every response with:
1. **Clear summary** of all options found
2. **Prices compared** across sources
3. **Follow-up question**: "Want me to book any of these?" or "Should I search for activities too?"
""",
            
            "jobs": """You are a JOBS/CAREER AGENT assistant with access to powerful tools.

## YOUR PRIMARY TOOLS (use these first):
- search_jobs, get_active_jobs - find job listings
- optimize_resume - improve resume for specific jobs
- analyze_job_match - score resume against job descriptions

## BACKUP TOOLS (use for company research or additional info):
- web_search, scrape_webpage, crawl_website

## RULES:
1. **Always search jobs** when user asks about opportunities in a field/location
2. **Use optimize_resume** when user shares resume text and job description
3. **Use analyze_job_match** to score compatibility
4. **Scrape company pages** when user wants info about specific employers
5. **Be encouraging** but honest about job matches
6. **Deliberate steps**: plan briefly (role/location/filters), then run search_jobs; if provided resume+JD, run analyze_job_match and optimize_resume; summarize with links.

## RESPONSE STYLE:
- List jobs with title, company, location, salary (if available)
- For resume help: provide specific, actionable suggestions
- For job matches: highlight strengths and areas to improve

## ALWAYS END WITH a relevant follow-up question:
- "Want me to optimize your resume for any of these roles?"
- "Should I search for more jobs in a different location or field?"
- "Can I analyze how well your skills match a specific job?"
""",
            
            "trends": """You are a TRENDS/SOCIAL MEDIA AGENT assistant with access to powerful tools.

## YOUR PRIMARY TOOLS (use these first):
- search_tweets - real Twitter/X search
- get_tiktok_trends, search_tiktok - TikTok content
- search_instagram, get_instagram_posts - Instagram content
- search_facebook - Facebook content
- get_youtube_trends, search_youtube - YouTube content
- get_google_trends - trending topics

## BACKUP TOOLS (use for deeper research):
- web_search, scrape_webpage, crawl_website

## RULES:
1. **Use multiple social platforms** to get a complete picture of trends
2. **Search specific hashtags** when asked about topics
3. **Use get_*_trends** for what's currently viral
4. **Combine platforms** for cross-platform trend analysis
5. **Be data-driven** - include engagement metrics when available
6. **Deliberate steps**: normalize topic/hashtags/geo/time; pick 2+ platforms; call trend + search APIs; synthesize top signals with dates/metrics.

## RESPONSE STYLE:
- Include usernames, post dates, engagement (likes/views)
- Highlight viral content and emerging patterns
- Present insights with specific examples

## ALWAYS END WITH a relevant follow-up question:
- "Want me to search for this trend on another platform?"
- "Should I find related hashtags or influencers?"
- "Can I dig deeper into a specific piece of content?"
""",

            "general": """You are a helpful research assistant with access to many tools across travel, jobs, and trends.

## AVAILABLE TOOLS:
- Travel: get_directions, search_flights, search_hotels, search_places, geocode_address
- Jobs: search_jobs, optimize_resume, analyze_job_match
- Trends: search_tweets, get_tiktok_trends, search_instagram, search_facebook, get_youtube_trends
- Research: web_search, scrape_webpage, crawl_website

## RULES:
1. **Choose the right tools** based on the query type
2. **Chain tools** for complex queries
3. **Use web_search/scrape_webpage as backup** when specialized tools don't suffice
4. **Be confident** with tool results

## ALWAYS END WITH a relevant follow-up question.
"""
        }
        
        # Select system prompt based on mode
        system_prompt = SYSTEM_PROMPTS.get(mode, SYSTEM_PROMPTS["general"])
        logger.info(f"Using agent mode: {mode}")
        
        trace_log = []
        response = await asyncio.get_running_loop().run_in_executor(
            None, lambda: chat.send_message(system_prompt + combined_prompt)
        )
        
        # Loop to handle function calls
        max_iterations = 5  # Prevent infinite loops
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            # Check if response contains function calls
            if not response.candidates or not response.candidates[0].content.parts:
                break
                
            function_calls = [
                part.function_call for part in response.candidates[0].content.parts
                if hasattr(part, 'function_call') and part.function_call
            ]
            
            if not function_calls:
                # No more function calls, we have the final response
                break
            
            # Process each function call
            function_responses = []
            for fc in function_calls:
                func_name = fc.name
                func_args = dict(fc.args) if fc.args else {}
                
                logger.info(f"TOOL CALL: {func_name}({func_args})")
                trace_log.append(f"Called: {func_name}({func_args})")
                
                if func_name in tool_map:
                    try:
                        # Call the async function
                        result = await tool_map[func_name](**func_args)
                        result_str = str(result)
                        
                        # Parse result for structured logging
                        is_error = result_str.startswith("Error") or result_str.startswith("No ")
                        line_count = result_str.count("\n---") if "---" in result_str else 0
                        
                        # Extract any price mentions
                        import re
                        prices = re.findall(r'\$[\d,]+(?:\.\d{2})?|\d+\s*(?:USD|EUR|GBP)', result_str)
                        price_summary = f", prices: {prices[:3]}" if prices else ""
                        
                        logger.info(f"TOOL RESULT: {func_name} - count={line_count}, error={is_error}{price_summary}")
                        logger.debug(f"TOOL RESULT FULL: {func_name}: {result_str[:1000]}...")
                        trace_log.append(f"Result: {line_count} items{price_summary}")
                    except Exception as e:
                        result = f"Error calling {func_name}: {str(e)}"
                        logger.error(f"TOOL ERROR: {func_name}: {e}")
                        trace_log.append(f"Error: {str(e)}")
                else:
                    result = f"Unknown function: {func_name}"
                    trace_log.append(f"Unknown: {func_name}")
                
                # Build function response
                function_responses.append(
                    genai.protos.Part(
                        function_response=genai.protos.FunctionResponse(
                            name=func_name,
                            response={"result": str(result)}
                        )
                    )
                )
            
            # Send function responses back to the model
            response = await asyncio.get_running_loop().run_in_executor(
                None, lambda: chat.send_message(function_responses)
            )
        
        latency_ms = (time.perf_counter() - start) * 1000
        text = response.text if hasattr(response, "text") else str(response)
        trace = " | ".join(trace_log) if trace_log else None
        logger.info(f"Final response (latency: {latency_ms:.0f}ms): {text[:200]}...")
        return LLMResult(text=text, latency_ms=latency_ms, model=self.model_id, trace=trace)

    def _build_fallback_summary(
        self, domain: Domain, insights: Iterable[Insight], prompt: str | None
    ) -> str:
        titles = ", ".join(item.title for item in insights)
        return (
            f"{domain.value.title()} intel synthesized locally. "
            f"Signals: {titles}." + (f" Prompt: {prompt}" if prompt else "")
        )
