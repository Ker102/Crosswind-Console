from __future__ import annotations

from typing import Any

from ..connectors.mcp import mcp_connector
from ..schemas import Domain, Insight


async def fetch_travel(prompt: str | None, filters: dict[str, Any] | None) -> list[Insight]:
    insights = await mcp_connector.fetch_domain(Domain.travel, prompt=prompt, filters=filters)
    for item in insights:
        item.metadata.setdefault("category", "travel")
        item.metadata.setdefault("visual", "globe")
    return insights
