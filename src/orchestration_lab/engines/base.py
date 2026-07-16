from __future__ import annotations

from typing import Protocol

from orchestration_lab.domain import ExecutionResult


class OrchestrationEngine(Protocol):
    def run(self, objective: str) -> ExecutionResult: ...

