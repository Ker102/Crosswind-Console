from __future__ import annotations

import asyncio
import os
import sys
import textwrap
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

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
        search_airbnb
    )
    from mcp_servers.trends_server import (
        get_google_trends, get_youtube_trends, search_tweets, search_youtube,
        get_tiktok_trends, search_tiktok, search_instagram, get_instagram_posts, search_facebook
    )
    
    MCP_TOOLS = [
        # Travel tools (search_flights=Kiwi, search_flights_sky=Skyscanner - use BOTH for comparison)
        search_flights, search_flights_sky, search_places, search_hotels, search_airbnb,
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
        print(f"[DEBUG] GEMINI_API_KEY loaded: {bool(self._api_key)}")
        print(f"[DEBUG] google-generativeai imported: {bool(genai)}")
        print(f"[DEBUG] Gemini enabled: {self._enabled}")
        
        # Propagate settings to os.environ for MCP tools
        if settings.rapidapi_key: os.environ["RAPIDAPI_KEY"] = settings.rapidapi_key
        if settings.google_maps_api_key: os.environ["GOOGLE_MAPS_API_KEY"] = settings.google_maps_api_key
        if settings.google_search_cx: os.environ["GOOGLE_SEARCH_CX"] = settings.google_search_cx
        if settings.x_bearer_token: os.environ["X_BEARER_TOKEN"] = settings.x_bearer_token
        if settings.tripadvisor_api_key: os.environ["TRIPADVISOR_API_KEY"] = settings.tripadvisor_api_key
        if settings.apify_api_token: os.environ["APIFY_API_TOKEN"] = settings.apify_api_token

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
        print(f"[DEBUG] Available tools: {list(tool_map.keys())}")
        
        # Agent-specific system prompts
        SYSTEM_PROMPTS = {
            "travel": """You are a TRAVEL AGENT assistant with access to powerful tools. 

## YOUR PRIMARY TOOLS (use these first):
- **FLIGHTS**: Use BOTH search_flights (Kiwi) AND search_flights_sky (Skyscanner) to compare prices!
- **STAYS**: search_airbnb (Apify), search_hotels (Booking.com)
- get_directions, search_places
- geocode_address, text_search_places, search_places_nearby
- search_ground_transport

## BACKUP TOOLS (use when primary tools don't give complete info):
- **FLIGHTS BACKUP**: search_google_flights, search_booking_flights
- web_search, scrape_webpage, crawl_website

## FERRY & SEA TRAVEL:
When user asks about **ferries** or travel by sea (especially Baltic routes like Tallinn-Helsinki):
1. **FIRST**: Use `get_directions(origin="Tallinn", destination="Helsinki", mode="transit")` - Google includes ferry routes!
2. **BACKUP**: Use `scrape_webpage` on directferries.com for schedules/prices
3. **BACKUP**: Use `web_search` for "Tallinn Helsinki ferry schedule [month] [year]"
4. Major operators: Tallink Silja, Viking Line, Eckerö Line, Finnlines

## RULES:
1. **For flight searches**: Call BOTH search_flights (Kiwi) AND search_flights_sky (Skyscanner) to compare prices.
   - **Date format**: ALWAYS use ISO `YYYY-MM-DD`. If user omits year, assume **2025**.
   - **Kiwi params**: `from_location`/`to_location` = IATA (e.g., "TLL", "HEL"); `date_from`, `return_from` (ISO).
   - **Interpret ranges**:
     - If user gives a start–end range with NO explicit return (e.g., "Dec 10-20"), treat it as an **outbound window**. Use Kiwi with `date_from=<start>`, `date_to=<end>` and surface outbound options in that window. For Skyscanner, ask for a specific date or propose a few representative dates in that window.
     - If user explicitly mentions return, treat as round trip: set Kiwi `return_from`, Skyscanner `return_date`.
   - **Skyscanner params**: use IATA inputs; internally it maps to `placeIdFrom`/`placeIdTo`. Set `date` and optionally `return_date` (ISO).
   - **Skyscanner whole month**: if user says “whole month” or only gives month, use `whole_month="YYYY-MM"` (only on `/web/flights/search-one-way`).
   - **Raw RapidAPI (from docs)**:
     - Kiwi (RapidAPI): `/one-way` or `/round-trip` with `source`, `destination`, `date`, optional `returnDate`, `adults`, `children`, `infants`, `cabinClass`, `limit`, `currency`, `sort`.
     - Flights Sky: auto-complete first; then `/web/flights/search-one-way` or `/search-roundtrip` with `fromEntityId/placeIdFrom`, `toEntityId/placeIdTo`, `departDate`, optional `returnDate`, `adults`, `cabinClass`, `market`, `locale`, `currency`; if `context.status == incomplete`, poll `/flights/search-incomplete?sessionId=...` until complete.
   - **If Skyscanner says “could not find airport/city”**: immediately retry with the remote raw API:
     1) `flights_auto_complete(query="TLL")` → grab `PlaceId` (e.g., "TLL")
     2) `flights_auto_complete(query="HEL")` → grab `PlaceId`
     3) `flights_search_roundtrip(placeIdFrom="<TLL>", placeIdTo="<HEL>", departDate="YYYY-MM-DD", returnDate="YYYY-MM-DD", adults=1, cabinClass="economy")`
     4) If `context.status=="incomplete"`, poll `flights_search_incomplete(sessionId=...)` until `status=="complete"`.
   - **If Skyscanner still fails**: fall back to `search_google_flights` then `search_booking_flights`.
   - **Filters**: Use `direct_only=True`, `cabin_class="BUSINESS"` as requested.
   - **Passengers**: Always include `adults`, `children`, `infants` when specified.
2. **Accommodation add-on**: if travel_intent.accommodations.enabled:
   - City = provided or destination.
   - Price filters: honor priceMin/priceMax; minRating when present; maxResults <= 10.
   - Use search_hotels (Booking) and search_airbnb (Apify); include links if present.
3. **Deliberate multi-step plan before tools (think briefly, then act)**:
   - Step 1: Normalize inputs (IATA, dates, tripType/window/month, transportMode).
   - Step 2: Pick tools (Kiwi window/roundtrip, Skyscanner single/whole-month + incomplete polling; accommodations if enabled).
   - Step 3: Execute tools; if incomplete, poll; if empty, fallbacks (Google/Booking flights or ground/sea).
   - Step 4: Summarize with prices, carriers, dates, and links (max 10).

## FEW-SHOT EXAMPLES (User Prompt → Tool Call):

**User**: "Find flights from Tallinn to Helsinki on December 10th"
**Kiwi**: search_flights(from_location="TLL", to_location="HEL", date_from="2025-12-10")
**Skyscanner**: search_flights_sky(from_location="TLL", to_location="HEL", date="2025-12-10")
If result says “could not find airport/city” → raw fallback:
  flights_auto_complete("TLL") -> PlaceIdFrom
  flights_auto_complete("HEL") -> PlaceIdTo
  flights_search_roundtrip(placeIdFrom=..., placeIdTo=..., departDate="2025-12-10", returnDate="2025-12-20", adults=1, cabinClass="economy")
  If status incomplete → flights_search_incomplete(sessionId=...) until complete.

**User**: "Cheapest flights from London to Paris between December 10-20" (no return mentioned)
**Kiwi (outbound window)**: search_flights(from_location="LHR", to_location="CDG", date_from="2025-12-10", date_to="2025-12-20")
**Skyscanner**: ask for a specific date in that window, or propose a couple (e.g., 2025-12-12, 2025-12-18) and run search_flights_sky for each.
If Skyscanner incomplete → flights_search_incomplete(sessionId=...); if still empty → search_google_flights then search_booking_flights.

**User**: "Whole month flights from Tallinn to Helsinki in December"
**Skyscanner whole-month**: search_flights_sky(from_location="TLL", to_location="HEL", whole_month="2025-12")
If incomplete → flights_search_incomplete(sessionId=...); if still empty → search_google_flights then search_booking_flights.

**User**: "Round trip from NYC to Tokyo, leaving Dec 15, returning Dec 25"
**Kiwi**: search_flights(from_location="JFK", to_location="NRT", date_from="2025-12-15", return_from="2025-12-25")
**Skyscanner**: search_flights_sky(from_location="JFK", to_location="NRT", date="2025-12-15", return_date="2025-12-25")

**User**: "Business class flights from Dubai to Singapore for 2 adults and 1 child"
**Kiwi**: search_flights(from_location="DXB", to_location="SIN", date_from="2025-12-10", cabin_class="BUSINESS", adults=2, children=1)
**Skyscanner**: search_flights_sky(from_location="DXB", to_location="SIN", date="2025-12-10", cabin_class="business", adults=2)

**User**: "Skyscanner didn't find good flights, try Google or Booking"
**Action**: search_google_flights(from_location="London", to_location="Paris", date="2024-12-15")
**Action**: search_booking_flights(from_location="London", to_location="Paris", date="2024-12-15")

**Action**: search_booking_flights(from_location="London", to_location="Paris", date="2024-12-15")

**User**: "Advanced: Use raw API to find hotels in Tokyo"
**Action**: flights_auto_complete(query="Tokyo")
**Action**: (matches "Tokyo, Japan" -> ID "27539733") -> flights_search_roundtrip(fromEntityId=..., toEntityId="27539733", ...)

## EXPERT: RAW RAPIDAPI TOOLS (last resort):
The `rapidapi-sky` server provides raw tools (e.g., `flights_auto_complete`, `flights_search_...`).
These match the API directly. They are "dumb":
1. You MUST call `flights_auto_complete` first to get `entityId` (JSON extract).
2. Then call `flights_search_one_way` using that `entityId`.
3. If status is incomplete, call `flights_search_incomplete`.
Use these ONLY if `search_flights_sky` (which does this automatically) fails!

**User**: "Ferry from Tallinn to Helsinki"
**Action**: get_directions(origin="Tallinn, Estonia", destination="Helsinki, Finland", mode="transit")
**Backup**: scrape_webpage(url="https://www.directferries.com/tallinn_helsinki_ferry.htm")

2. **For accommodation**: Use `search_airbnb` for apartments/longer stays and `search_hotels` for hotels.
3. **Always use get_directions** for "how to get from A to B" questions with specific transport info
4. **Chain tools**: geocode first, then search nearby places
5. **Be confident**: Include exact bus/tram numbers, walking times, station names
6. **Never hedge** - present all tool results as helpful information
7. **Transportation answers MUST include**: specific route numbers, departure points, total journey time

## RESPONSE STYLE:
- Bullet points or numbered steps for directions
- Include addresses and distances for places
- For flights: show prices from BOTH sources so user can compare
- Be direct and actionable
- If intent is a date **window** (no return), ask a quick clarifier or propose 2-3 dates inside the window and run Kiwi (window) plus Skyscanner (specific dates).

## ALWAYS END WITH a relevant follow-up question:
- "Want me to find hotels or restaurants nearby?"
- "Should I look up ticket prices or alternative routes?"
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
        print(f"[DEBUG] Using agent mode: {mode}")
        
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
                
                print(f"[TOOL CALL] {func_name}({func_args})")
                trace_log.append(f"Called: {func_name}({func_args})")
                
                if func_name in tool_map:
                    try:
                        # Call the async function
                        result = await tool_map[func_name](**func_args)
                        print(f"[TOOL RESULT] {func_name}: {str(result)[:200]}...")
                        trace_log.append(f"Result: {str(result)[:100]}...")
                    except Exception as e:
                        result = f"Error calling {func_name}: {str(e)}"
                        print(f"[TOOL ERROR] {func_name}: {e}")
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
        print(f"[DEBUG] Final response (latency: {latency_ms:.0f}ms): {text[:200]}...")
        return LLMResult(text=text, latency_ms=latency_ms, model=self.model_id, trace=trace)

    def _build_fallback_summary(
        self, domain: Domain, insights: Iterable[Insight], prompt: str | None
    ) -> str:
        titles = ", ".join(item.title for item in insights)
        return (
            f"{domain.value.title()} intel synthesized locally. "
            f"Signals: {titles}." + (f" Prompt: {prompt}" if prompt else "")
        )
