"""Utilità SQLite condivise. Ogni database è un file separato."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path


def connect(path: Path | str, schema: str) -> sqlite3.Connection:
    if str(path) != ":memory:":
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    # check_same_thread=False: l'API HTTP può risolvere la dipendenza che crea la connessione
    # e l'endpoint che la usa in due thread diversi del threadpool di FastAPI/Starlette.
    conn = sqlite3.connect(str(path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(schema)
    conn.commit()
    return conn


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
