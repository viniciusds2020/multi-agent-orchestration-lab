from __future__ import annotations

import time

from orchestration_lab.domain import AgentTrace, EngineName, ExecutionResult

ROLES = [
    ("planner", "Planejador", "Decompôs o objetivo em pesquisa, arquitetura e validação."),
    (
        "researcher",
        "Pesquisador",
        "Levantou hipóteses, restrições, riscos e evidências necessárias.",
    ),
    ("architect", "Arquiteto de IA", "Propôs componentes, contratos, segurança e observabilidade."),
    ("reviewer", "Crítico", "Revisou lacunas, critérios de aceite e próximos experimentos."),
]


def simulate(engine: EngineName, objective: str) -> ExecutionResult:
    started = time.perf_counter()
    traces = [
        AgentTrace(name, role, f"{text} Objetivo analisado: {objective}", index)
        for index, (name, role, text) in enumerate(ROLES, start=1)
    ]
    final = (
        "Plano recomendado: validar o problema e a métrica, construir um experimento pequeno, "
        "instrumentar qualidade/custo/latência, aplicar revisão humana e promover somente após "
        "os critérios de aceite. O modo simulado permite avaliar a orquestração "
        "sem consumir tokens."
    )
    return ExecutionResult(
        engine=engine,
        mode="simulation",
        objective=objective,
        final_answer=final,
        traces=traces,
        duration_ms=round((time.perf_counter() - started) * 1000),
        metadata={"agents": len(traces), "human_review_recommended": True},
    )
