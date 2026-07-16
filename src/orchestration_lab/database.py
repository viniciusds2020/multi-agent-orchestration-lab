from __future__ import annotations

import json
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def connection():
    path = Path(os.getenv("DATABASE_PATH", "data/orchestration_lab.db"))
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    try:
        yield db
        db.commit()
    finally:
        db.close()


def initialize() -> None:
    with connection() as db:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS runs(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                engine TEXT NOT NULL,
                mode TEXT NOT NULL,
                objective TEXT NOT NULL,
                status TEXT NOT NULL,
                duration_ms INTEGER NOT NULL,
                input_tokens INTEGER NOT NULL,
                output_tokens INTEGER NOT NULL,
                result_json TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def save_result(result: dict) -> int:
    with connection() as db:
        return db.execute(
            """
            INSERT INTO runs(engine,mode,objective,status,duration_ms,input_tokens,
                             output_tokens,result_json)
            VALUES(?,?,?,'completed',?,?,?,?)
            """,
            (
                result["engine"], result["mode"], result["objective"], result["duration_ms"],
                result["input_tokens"], result["output_tokens"],
                json.dumps(result, ensure_ascii=False),
            ),
        ).lastrowid


def recent_runs(limit: int = 30) -> list[dict]:
    with connection() as db:
        return [
            dict(row) for row in db.execute(
                """SELECT id,engine,mode,objective,status,duration_ms,input_tokens,
                output_tokens,created_at FROM runs ORDER BY id DESC LIMIT ?""",
                (min(max(limit, 1), 100),),
            ).fetchall()
        ]

