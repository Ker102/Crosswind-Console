from __future__ import annotations

import os
from fastapi import APIRouter, Depends

from ..dependencies import get_llm_client
from ..schemas import LLMRequest, LLMResponse, SandboxRequest, SandboxResponse
from ..services.llm import GeminiClient
from ..services.sandbox_llm import LangChainSandboxService

router = APIRouter(prefix="/llm", tags=["llm"])

# Singleton sandbox service
_sandbox_service = None

def get_sandbox_service() -> LangChainSandboxService:
    global _sandbox_service
    if _sandbox_service is None:
        _sandbox_service = LangChainSandboxService(
            gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
            model_id=os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        )
    return _sandbox_service


@router.post("/prompt", response_model=LLMResponse)
async def run_llm_prompt(
    payload: LLMRequest, llm_client: GeminiClient = Depends(get_llm_client)
) -> LLMResponse:
    result = await llm_client.respond(payload.prompt, payload.context, payload.history, payload.mode, payload.travel_intent)
    return LLMResponse(output=result.output if hasattr(result, 'output') else result.text, model=result.model, latency_ms=result.latency_ms)


@router.post("/sandbox", response_model=SandboxResponse)
async def sandbox_mode(payload: SandboxRequest) -> SandboxResponse:
    """
    Sandbox mode endpoint - uses LangChain agent with RAG + persistent MCP tools.
    
    This is the main endpoint for natural language queries that need:
    1. Domain knowledge from RAG (parameter formats, valid values, etc.)
    2. Real-time data from remote MCP tools (flights, hotels, places, etc.)
    """
    service = get_sandbox_service()
    
    # Convert history to dict format
    history = None
    if payload.history:
        history = [{"role": msg.role, "content": msg.content} for msg in payload.history]
    
    result = await service.process(
        prompt=payload.prompt,
        namespace=payload.namespace,
        history=history
    )
    
    return SandboxResponse(
        output=result.text,
        model=result.model,
        latency_ms=result.latency_ms,
        tools_used=result.tools_used,
        rag_context=result.rag_context
    )

