from __future__ import annotations

import os
from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel, Field

from orchestration_lab.database import recent_runs
from orchestration_lab.service import execute

router = APIRouter(prefix="/api")


class ExecutionRequest(BaseModel):
    engine: Literal["crewai", "langgraph"]
    objective: str = Field(min_length=10, max_length=5000)
    live: bool = False


class CompareRequest(BaseModel):
    objective: str = Field(min_length=10, max_length=5000)
    live: bool = False


@router.get("/capabilities")
def capabilities() -> dict:
    return {
        "engines": ["crewai", "langgraph"],
        "live_available": bool(os.getenv("GROQ_API_KEY")),
        "default_model": os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        "agents": ["Planejador", "Pesquisador", "Arquiteto de IA", "Crítico"],
    }


@router.post("/execute")
def run(request: ExecutionRequest) -> dict:
    return execute(request.engine, request.objective, request.live)


@router.post("/compare")
def compare(request: CompareRequest) -> dict:
    return {
        "crewai": execute("crewai", request.objective, request.live),
        "langgraph": execute("langgraph", request.objective, request.live),
    }


@router.get("/runs")
def runs(limit: int = 30) -> list[dict]:
    return recent_runs(limit)
