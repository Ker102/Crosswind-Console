"""High-level client that calls Firecrawl/Playwright MCP servers."""

from __future__ import annotations

import asyncio
import hashlib
import logging
import random
import textwrap
from typing import Any

from ..schemas import Domain, Insight
from ..mcp.hub import FirecrawlToolset, MCPHub

logger = logging.getLogger(__name__)


class MCPConnector:
    def __init__(self) -> None:
        self.hub = MCPHub()
        self.firecrawl = FirecrawlToolset(self.hub)
        self._sample_payloads: dict[Domain, list[Insight]] = {
            Domain.jobs: [
                Insight(
                    id="job-remote-ai-",
                    title="Remote AI Research Engineer",
                    description="Series B startup scaling evaluation agents",
                    source="https://jobs.example.com/ai-research",
                    score=0.92,
                    metadata={"location": "Remote", "salary": "$180k-$210k"},
                ),
                Insight(
                    id="job-data-",
                    title="Data + Product Scientist, Climate",
                    description="Use satellite imagery to build risk forecasts",
                    source="https://jobs.example.com/climate-data",
                    score=0.81,
                    metadata={"location": "Berlin", "type": "Hybrid"},
                ),
            ],
            Domain.travel: [
                Insight(
                    id="travel-flight-nomad",
                    title="Lisbon ↔ Tokyo creative nomad fares",
                    description="5-stop multi-city itinerary w/ 35% below avg",
                    source="https://travel.example.com/nomad-fare",
                    score=0.88,
                    metadata={"airline": "Multiple", "price": "$1,150"},
                ),
                Insight(
                    id="travel-stay-azores",
                    title="Azores cowork villa",
                    description="Oceanfront suites + coliving perks for 1 month",
                    source="https://stays.example.com/azores-co",
                    score=0.73,
                    metadata={"price_per_night": "$95", "perks": ["Workspace", "Spa"]},
                ),
            ],
            Domain.trends: [
                Insight(
                    id="trend-artefact",
                    title="Artefact-style multi-modal carousels",
                    description="Designers remixing AI motion reels on TikTok",
                    source="https://trends.example.com/artefact",
                    score=0.79,
                    metadata={"platform": "TikTok", "hashtag_views": "42M"},
                ),
                Insight(
                    id="trend-travelstack",
                    title="TravelStack micro-itinerary threads",
                    description="Creators publish tappable micro itineraries",
                    source="https://trends.example.com/travelstack",
                    score=0.69,
                    metadata={"platform": "Instagram", "saves_growth": "180%"},
                ),
            ],
        }

    async def fetch_domain(self, domain: Domain, *, prompt: str | None, filters: dict[str, Any] | None) -> list[Insight]:
        query = self._build_query(domain, prompt, filters)
        if not query:
            return await self._fallback(domain, prompt)

        try:
            results = await self.firecrawl.search(query)
            insights = self._convert_firecrawl_results(results, domain)
            if insights:
                return insights
        except Exception as exc:  # pragma: no cover - network/runtime issues fall back to mocks
            logger.warning("Firecrawl query failed (%s): %s", domain.value, exc)

        return await self._fallback(domain, prompt)

    def _build_query(self, domain: Domain, prompt: str | None, filters: dict[str, Any] | None) -> str | None:
        base = {
            Domain.jobs: "latest hiring intel",
            Domain.travel: "travel deals",
            Domain.trends: "social media trends",
        }[domain]

        parts = [base]
        if prompt:
            parts.append(prompt.strip())
        if filters:
            filter_terms = " ".join(
                f"{key}:{value}" for key, value in filters.items() if isinstance(value, (str, int))
            )
            if filter_terms:
                parts.append(filter_terms)
        joined = " ".join(part for part in parts if part)
        return joined or None

    async def _fallback(self, domain: Domain, prompt: str | None) -> list[Insight]:
        await asyncio.sleep(0.05)
        base_payload = self._sample_payloads.get(domain, [])
        dynamic_payload: list[Insight] = []
        for insight in base_payload:
            clone = insight.model_copy(deep=True)
            if clone.score is not None:
                jitter = random.uniform(-0.05, 0.05)
                clone.score = max(0.0, min(1.0, clone.score + jitter))
            if prompt:
                tokens = prompt.split()
                if tokens:
                    clone.metadata.setdefault("prompt_tags", []).append(tokens[0])
            dynamic_payload.append(clone)
        return dynamic_payload

    def _convert_firecrawl_results(self, payload: list[dict[str, Any]], domain: Domain) -> list[Insight]:
        insights: list[Insight] = []
        for idx, entry in enumerate(payload):
            title = (entry.get("title") or entry.get("metadata", {}).get("title") or "Untitled source").strip()
            url = entry.get("url") or entry.get("metadata", {}).get("sourceURL")
            summary_source = (
                entry.get("description")
                or entry.get("markdown")
                or entry.get("snippet")
                or entry.get("metadata", {}).get("description")
                or ""
            )
            description = textwrap.shorten(summary_source.replace("\n", " "), width=220, placeholder="…")
            metadata = {
                "source": entry.get("metadata", {}),
                "position": idx + 1,
            }
            if entry.get("markdown"):
                metadata["markdown_preview"] = entry["markdown"][:1200]

            insights.append(
                Insight(
                    id=self._build_id(domain, url or title, idx),
                    title=title,
                    description=description or "See linked source for more details.",
                    source=url,
                    score=max(0.35, 0.85 - idx * 0.1),
                    metadata=metadata,
                )
            )
        return insights

    @staticmethod
    def _build_id(domain: Domain, seed: str, idx: int) -> str:
        digest = hashlib.sha1(f"{seed}-{idx}".encode(), usedforsecurity=False).hexdigest()[:10]
        return f"{domain.value}-{digest}"


mcp_connector = MCPConnector()
