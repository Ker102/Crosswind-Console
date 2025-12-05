from __future__ import annotations

from fastapi import APIRouter, Depends

from ..dependencies import get_llm_client
from ..schemas import LLMRequest, LLMResponse
from ..services.llm import GeminiClient

router = APIRouter(prefix="/llm", tags=["llm"])


@router.post("/prompt", response_model=LLMResponse)
async def run_llm_prompt(
    payload: LLMRequest, llm_client: GeminiClient = Depends(get_llm_client)
) -> LLMResponse:
    result = await llm_client.respond(payload.prompt, payload.context, payload.history, payload.mode)
    return LLMResponse(output=result.output if hasattr(result, 'output') else result.text, model=result.model, latency_ms=result.latency_ms)
