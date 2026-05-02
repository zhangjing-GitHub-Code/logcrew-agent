"""Shared data models for LogCrew agents."""

from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field


class LogEntry(BaseModel):
    timestamp: datetime
    service: str
    level: str
    trace_id: str
    message: str
    meta: dict[str, Any] = Field(default_factory=dict)


class Incident(BaseModel):
    id: str
    trace_id: str
    logs: list[LogEntry]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "open"


class RootCause(BaseModel):
    hypothesis: str
    confidence: float = Field(ge=0.0, le=1.0)
    evidences: list[str] = Field(default_factory=list)
