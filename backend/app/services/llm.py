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
    from mcp_servers.search_server import web_search
    from mcp_servers.travel_server import (
        search_flights, search_places, search_hotels, search_flights_backup,
        search_ground_transport, search_ground_transport_backup, get_directions,
        geocode_address, reverse_geocode, text_search_places, search_places_nearby
    )
    from mcp_servers.trends_server import (
        get_google_trends, get_youtube_trends, search_tweets, search_youtube,
        get_tiktok_trends, search_tiktok, search_instagram, get_instagram_posts, search_facebook
    )
    
    MCP_TOOLS = [
        # Travel tools
        search_flights, search_places, search_hotels, search_flights_backup,
        search_ground_transport, search_ground_transport_backup, get_directions,
        geocode_address, reverse_geocode, text_search_places, search_places_nearby,
        # Jobs tools
        search_jobs, get_active_jobs, optimize_resume, analyze_job_match,
        # Search tools
        web_search,
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

    async def respond(self, prompt: str, context: Iterable[Insight] | None = None, history: Iterable[Any] | None = None) -> LLMResult:
        combined_prompt = prompt
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
        
        # System prompt to guide tool usage and reasoning
        system_prompt = """You are a travel and research assistant with access to powerful tools. Follow these principles:

## TOOL USAGE RULES:
1. **Chain tools together** when needed. For complex queries:
   - First use location-specific tools (geocode_address, get_directions)
   - Then use detail tools (search_places_nearby, text_search_places)
   - Always gather complete information before responding

2. **Be specific and confident** when presenting tool results:
   - Present ALL information the tools returned as factual and helpful
   - Include exact bus/tram numbers, walking times, and station names
   - Include addresses, ratings, and opening hours from place searches
   - Never hedge or say "I cannot give exact numbers" - present what you found

3. **Fallback strategy** - if specialized tools don't answer fully:
   - Use web_search as a backup for current information
   - Combine multiple tool results for complete answers

4. **Transportation queries** should include:
   - Specific route numbers (e.g., "Bus 4" or "Tram Line 2")
   - Departure/arrival points with walking directions
   - Total journey time including transfers

## RESPONSE STYLE:
- Be direct, confident, and actionable
- Format information clearly with bullet points or numbered steps
- Include all relevant details the tools provided
- Present tool results as useful information, not uncertain guesses

## FOLLOW-UP ENGAGEMENT:
**ALWAYS end your response with a relevant follow-up question** to help the user dig deeper. Examples:
- "Would you like me to find restaurants or hotels near [location]?"
- "Should I search for the best time to visit or ticket prices?"
- "Want me to look up alternative routes or nearby attractions?"
- "Can I help you find more details about [specific item mentioned]?"

Now respond to the user's query:
"""
        
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
