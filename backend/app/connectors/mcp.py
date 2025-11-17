"""Thin abstractions that would call MCP servers for live data.

Right now the connectors return curated mock payloads to unblock the
end-to-end flow. Each method mimics asynchronous IO so the rest of the
application can be written exactly as if it were talking to Firecrawl or
other remote services.
"""

from __future__ import annotations

import asyncio
import random
from typing import Any

from ..schemas import Domain, Insight


class MCPConnector:
    def __init__(self) -> None:
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
        """Pretend to fetch live data via Firecrawl/bespoke MCP servers."""

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


mcp_connector = MCPConnector()
