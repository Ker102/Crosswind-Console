from __future__ import annotations

from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field, HttpUrl


class Domain(str, Enum):
    jobs = "jobs"
    travel = "travel"
    trends = "trends"


class Insight(BaseModel):
    id: str
    title: str
    description: str
    source: HttpUrl | None = None
    score: float | None = Field(default=None, ge=0, le=1)
    metadata: dict[str, Any] = Field(default_factory=dict)


class QueryPayload(BaseModel):
    domain: Domain
    prompt: str | None = None
    filters: dict[str, Any] | None = None


class DiscoveryResponse(BaseModel):
    domain: Domain
    summary: str
    items: list[Insight]
    llm_trace: str | None = None


class ChatMessage(BaseModel):
    role: Literal["user", "model"]
    content: str


class LLMRequest(BaseModel):
    mode: Literal["jobs", "travel", "trends", "general"] = "general"
    prompt: str
    context: list[Insight] | None = None
    history: list[ChatMessage] | None = None
    travel_intent: dict[str, Any] | None = None


class LLMResponse(BaseModel):
    output: str
    model: str
    latency_ms: float | None = None


class HealthResponse(BaseModel):
    status: Literal["ok", "degraded"] = "ok"
    environment: str


class SandboxRequest(BaseModel):
    prompt: str
    namespace: Literal["travel", "jobs", "trends"] = "travel"
    history: list[ChatMessage] | None = None


class SandboxResponse(BaseModel):
    output: str
    model: str
    latency_ms: float
    tools_used: list[str]
    rag_context: list[dict[str, Any]]

