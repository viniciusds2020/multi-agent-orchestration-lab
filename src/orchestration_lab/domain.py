from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Literal

EngineName = Literal["crewai", "langgraph"]


@dataclass
class AgentTrace:
    agent: str
    role: str
    output: str
    sequence: int


@dataclass
class ExecutionResult:
    engine: EngineName
    mode: str
    objective: str
    final_answer: str
    traces: list[AgentTrace]
    duration_ms: int
    input_tokens: int = 0
    output_tokens: int = 0
    metadata: dict = field(default_factory=dict)

    def as_dict(self) -> dict:
        return {
            **asdict(self),
            "traces": [asdict(trace) for trace in self.traces],
        }

