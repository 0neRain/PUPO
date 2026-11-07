"""Database di apprendimento: la "mente" del Pupo.

All'inizio è vuoto. Si riempie SOLO con ciò che lo studente spiega al Pupo.
Le spiegazioni sbagliate diventano conoscenza sbagliata: qui non si corregge niente.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .storage import connect, now

SCHEMA = """
CREATE TABLE IF NOT EXISTS lessons (
    id INTEGER PRIMARY KEY,
    student_text TEXT NOT NULL,   -- spiegazione originale dello studente
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS beliefs (
    id INTEGER PRIMARY KEY,
    lesson_id INTEGER NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    statement TEXT NOT NULL,      -- cosa il Pupo ha annotato nel quaderno
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY,
    mode TEXT NOT NULL,           -- 'teach' | 'quiz'
    role TEXT NOT NULL,           -- 'user' (studente) | 'assistant' (Pupo)
    content TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


@dataclass
class Belief:
    id: int
    statement: str


class LearningDB:
    def __init__(self, path: Path | str) -> None:
        self.conn = connect(path, SCHEMA)

    def add_lesson(self, student_text: str, statements: list[str]) -> int:
        with self.conn:
            cur = self.conn.execute(
                "INSERT INTO lessons (student_text, created_at) VALUES (?, ?)", (student_text, now())
            )
            lesson_id = cur.lastrowid
            self.conn.executemany(
                "INSERT INTO beliefs (lesson_id, statement, created_at) VALUES (?, ?, ?)",
                [(lesson_id, s, now()) for s in statements],
            )
        return lesson_id

    def beliefs(self) -> list[Belief]:
        rows = self.conn.execute("SELECT id, statement FROM beliefs ORDER BY id").fetchall()
        return [Belief(id=r["id"], statement=r["statement"]) for r in rows]

    def notebook(self) -> str:
        """Il quaderno del Pupo come testo, da dare al modello."""
        beliefs = self.beliefs()
        if not beliefs:
            return "(vuoto: non ti hanno ancora spiegato niente)"
        return "\n".join(f"{i + 1}. {b.statement}" for i, b in enumerate(beliefs))

    def add_message(self, mode: str, role: str, content: str) -> None:
        self.conn.execute(
            "INSERT INTO messages (mode, role, content, created_at) VALUES (?, ?, ?, ?)",
            (mode, role, content, now()),
        )
        self.conn.commit()

    def history(self, mode: str, limit: int = 12) -> list[dict]:
        rows = self.conn.execute(
            "SELECT role, content FROM messages WHERE mode = ? ORDER BY id DESC LIMIT ?", (mode, limit)
        ).fetchall()
        return [{"role": r["role"], "content": r["content"]} for r in reversed(rows)]

    def reset(self) -> None:
        """Svuota la mente del Pupo (ricomincia da zero)."""
        with self.conn:
            self.conn.execute("DELETE FROM beliefs")
            self.conn.execute("DELETE FROM lessons")
            self.conn.execute("DELETE FROM messages")
