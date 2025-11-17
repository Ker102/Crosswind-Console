from __future__ import annotations

import asyncio
import textwrap
import time
from dataclasses import dataclass
from typing import Iterable

try:
    import google.generativeai as genai
except Exception:  # pragma: no cover - optional dependency during early dev
    genai = None

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
        if self._enabled:
            genai.configure(api_key=self._api_key)
            self._model = genai.GenerativeModel(self.model_id)

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
        response = await loop.run_in_executor(None, lambda: self._model.generate_content(base_prompt))
        latency_ms = (time.perf_counter() - start) * 1000
        text = response.text if hasattr(response, "text") else str(response)
        return LLMResult(text=text, latency_ms=latency_ms, model=self.model_id)

    async def respond(self, prompt: str, context: Iterable[Insight] | None = None) -> LLMResult:
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
        response = await loop.run_in_executor(None, lambda: self._model.generate_content(combined_prompt))
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
