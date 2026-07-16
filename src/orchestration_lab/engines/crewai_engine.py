from __future__ import annotations

import os
import time

from orchestration_lab.domain import AgentTrace, ExecutionResult
from orchestration_lab.simulation import simulate


class CrewAIEngine:
    def __init__(self, live: bool = False) -> None:
        self.live = live and bool(os.getenv("GROQ_API_KEY"))

    def run(self, objective: str) -> ExecutionResult:
        if not self.live:
            return simulate("crewai", objective)
        started = time.perf_counter()
        from crewai import LLM, Agent, Crew, Process, Task

        llm = LLM(
            model=f"groq/{os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')}",
            temperature=0.2,
        )
        definitions = [
            ("Planejador", "Decompor objetivos em um plano verificável."),
            ("Pesquisador", "Identificar evidências, riscos e restrições."),
            ("Arquiteto de IA", "Projetar solução segura, observável e testável."),
            ("Crítico", "Revisar a proposta e definir critérios de aceite."),
        ]
        agents = [
            Agent(role=role, goal=goal, backstory="Especialista sênior em sistemas de IA.",
                  llm=llm, verbose=False, allow_delegation=False)
            for role, goal in definitions
        ]
        tasks = []
        for index, agent in enumerate(agents):
            context = tasks[-1:] if tasks else []
            tasks.append(Task(
                description=f"Analise o objetivo: {objective}",
                expected_output="Texto conciso em português com decisões e riscos.",
                agent=agent,
                context=context,
            ))
        output = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=False,
        ).kickoff()
        traces = [
            AgentTrace(f"agent_{i}", definitions[i - 1][0], str(task.output), i)
            for i, task in enumerate(tasks, start=1)
        ]
        return ExecutionResult(
            engine="crewai", mode="live", objective=objective, final_answer=str(output),
            traces=traces, duration_ms=round((time.perf_counter() - started) * 1000),
            metadata={"process": "sequential"},
        )
