from __future__ import annotations

from typing import Awaitable, Callable, Dict

from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies import get_llm_client
from ..schemas import DiscoveryResponse, Domain, Insight, QueryPayload
from ..services import jobs, travel, trends
from ..services.llm import GeminiClient

router = APIRouter(prefix="/discovery", tags=["discovery"])

DomainService = Callable[[str | None, dict | None], Awaitable[list[Insight]]]

SERVICE_MAP: Dict[Domain, DomainService] = {
    Domain.jobs: jobs.fetch_jobs,
    Domain.travel: travel.fetch_travel,
    Domain.trends: trends.fetch_trends,
}


@router.post("/", response_model=DiscoveryResponse)
async def run_discovery(
    payload: QueryPayload,
    llm_client: GeminiClient = Depends(get_llm_client),
) -> DiscoveryResponse:
    service = SERVICE_MAP.get(payload.domain)
    if service is None:  # pragma: no cover - Enum prevents this but guards future additions
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Domain unsupported")

    insights = await service(payload.prompt, payload.filters or {})
    llm_result = await llm_client.summarize(payload.domain, insights, payload.prompt)

    return DiscoveryResponse(
        domain=payload.domain,
        items=insights,
        summary=llm_result.text,
        llm_trace=llm_result.trace,
    )
