from fastapi.testclient import TestClient

from orchestration_lab.database import initialize
from orchestration_lab.main import app


def test_both_engines_run_without_api_key(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "test.db"))
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    initialize()
    with TestClient(app) as client:
        for engine in ("crewai", "langgraph"):
            response = client.post(
                "/api/execute",
                json={
                    "engine": engine,
                    "objective": "Planejar um classificador de chamados corporativos.",
                    "live": False,
                },
            )
            assert response.status_code == 200
            assert response.json()["mode"] == "simulation"
            assert len(response.json()["traces"]) == 4
        assert len(client.get("/api/runs").json()) == 2


def test_capabilities_and_health(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "health.db"))
    with TestClient(app) as client:
        assert client.get("/health").json()["status"] == "ok"
        assert client.get("/api/capabilities").json()["engines"] == ["crewai", "langgraph"]

