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
    from mcp.jobs_server import get_active_jobs, search_jobs
    from mcp.search_server import web_search
    from mcp.travel_server import search_flights, search_places, search_hotels, search_flights_backup
    from mcp.trends_server import get_google_trends, get_youtube_trends, search_tweets, search_youtube
    
    MCP_TOOLS = [
        search_flights, search_places, search_hotels, search_flights_backup,
        search_jobs, get_active_jobs,
        web_search,
        get_youtube_trends, search_youtube, get_google_trends, search_tweets
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
        
        # Propagate settings to os.environ for MCP tools
        if settings.rapidapi_key: os.environ["RAPIDAPI_KEY"] = settings.rapidapi_key
        if settings.google_maps_api_key: os.environ["GOOGLE_MAPS_API_KEY"] = settings.google_maps_api_key
        if settings.google_search_cx: os.environ["GOOGLE_SEARCH_CX"] = settings.google_search_cx
        if settings.x_bearer_token: os.environ["X_BEARER_TOKEN"] = settings.x_bearer_token
        if settings.tripadvisor_api_key: os.environ["TRIPADVISOR_API_KEY"] = settings.tripadvisor_api_key

        if self._enabled:
            genai.configure(api_key=self._api_key)
            # Initialize model with tools
            self._model = genai.GenerativeModel(
                self.model_id,
                tools=MCP_TOOLS
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
        
        loop = asyncio.get_running_loop()
        start = time.perf_counter()
        
        # Convert history to Gemini format if provided
        chat_history = []
        if history:
            for msg in history:
                chat_history.append({
                    "role": msg.role,
                    "parts": [msg.content]
                })

        # Enable automatic function calling
        # Using chat session for automatic tool use loop
        chat = self._model.start_chat(
            history=chat_history,
            enable_automatic_function_calling=True
        )
        
        response = await loop.run_in_executor(None, lambda: chat.send_message(combined_prompt))
        
        latency_ms = (time.perf_counter() - start) * 1000
        text = response.text if hasattr(response, "text") else str(response)
        return LLMResult(text=text, latency_ms=latency_ms, model=self.model_id)

    def _build_fallback_summary(
        self, domain: Domain, insights: Iterable[Insight], prompt: str | None
    ) -> str:
        titles = ", ".join(item.title for item in insights)
        return (
            f"{domain.value.title()} intel synthesized locally. "
            f"Signals: {titles}." + (f" Prompt: {prompt}" if prompt else "")
        )
