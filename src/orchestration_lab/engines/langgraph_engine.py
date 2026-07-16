from __future__ import annotations

import os
import time
from typing import TypedDict

from orchestration_lab.domain import AgentTrace, ExecutionResult
from orchestration_lab.provider import GroqProvider
from orchestration_lab.simulation import simulate


class GraphState(TypedDict):
    objective: str
    context: str
    traces: list[dict]
    input_tokens: int
    output_tokens: int


class LangGraphEngine:
    def __init__(self, live: bool = False) -> None:
        self.live = live and bool(os.getenv("GROQ_API_KEY"))

    def run(self, objective: str) -> ExecutionResult:
        if not self.live:
            return simulate("langgraph", objective)
        started = time.perf_counter()
        from langgraph.graph import END, START, StateGraph

        provider = GroqProvider()
        roles = ["Planejador", "Pesquisador", "Arquiteto de IA", "Crítico"]

        def node(role: str):
            def execute(state: GraphState) -> dict:
                response = provider.complete(
                    role=role, objective=state["objective"], context=state["context"]
                )
                trace = {"agent": role.lower().replace(" ", "_"), "role": role,
                         "output": response.content, "sequence": len(state["traces"]) + 1}
                return {
                    "context": state["context"] + "\n" + response.content,
                    "traces": state["traces"] + [trace],
                    "input_tokens": state["input_tokens"] + response.input_tokens,
                    "output_tokens": state["output_tokens"] + response.output_tokens,
                }
            return execute

        builder = StateGraph(GraphState)
        names = ["planner", "researcher", "architect", "reviewer"]
        for name, role in zip(names, roles, strict=True):
            builder.add_node(name, node(role))
        builder.add_edge(START, names[0])
        for source, target in zip(names, names[1:], strict=True):
            builder.add_edge(source, target)
        builder.add_edge(names[-1], END)
        graph = builder.compile()
        state = graph.invoke({
            "objective": objective, "context": "", "traces": [],
            "input_tokens": 0, "output_tokens": 0,
        })
        return ExecutionResult(
            engine="langgraph", mode="live", objective=objective,
            final_answer=state["traces"][-1]["output"],
            traces=[AgentTrace(**item) for item in state["traces"]],
            duration_ms=round((time.perf_counter() - started) * 1000),
            input_tokens=state["input_tokens"], output_tokens=state["output_tokens"],
            metadata={"graph": names},
        )

