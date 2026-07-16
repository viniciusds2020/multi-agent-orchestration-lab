from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from orchestration_lab.api import router
from orchestration_lab.database import initialize

STATIC_DIR = Path(__file__).parent / "static"


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize()
    yield


app = FastAPI(
    title="Multi-Agent Orchestration Lab",
    version="0.1.0",
    description="CrewAI and LangGraph comparative laboratory.",
    lifespan=lifespan,
)
app.include_router(router)
app.mount("/assets", StaticFiles(directory=STATIC_DIR), name="assets")


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


def run() -> None:
    import uvicorn
    uvicorn.run("orchestration_lab.main:app", host="0.0.0.0", port=8000)

