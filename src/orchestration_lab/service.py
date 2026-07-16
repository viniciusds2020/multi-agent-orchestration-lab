from __future__ import annotations

from orchestration_lab.database import save_result
from orchestration_lab.domain import EngineName
from orchestration_lab.engines.crewai_engine import CrewAIEngine
from orchestration_lab.engines.langgraph_engine import LangGraphEngine


def execute(engine: EngineName, objective: str, live: bool = False) -> dict:
    implementation = CrewAIEngine(live) if engine == "crewai" else LangGraphEngine(live)
    result = implementation.run(objective).as_dict()
    result["run_id"] = save_result(result)
    return result

