"""Database di riferimento: la "conoscenza a priori".

Contiene il materiale caricato dallo studente (registrazioni trascritte, sbobinature, appunti)
e il programma che se ne ricava (argomenti + concetti chiave).

DECISIONE DI PROGETTO: l'agente Pupo non usa mai questo database.
Lo usano solo:
- la sezione "Materiale" (lo studente consulta i propri file);
- il modulo di confronto (`comparison.py`), che restituisce solo percentuali.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from . import prompts
from .llm import LLM, chat_json
from .storage import connect, now

SCHEMA = """
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY,
    source TEXT NOT NULL,        -- nome del file o descrizione
    kind TEXT NOT NULL,          -- 'upload' | 'transcript'
    text TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS topics (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    position INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS concepts (
    id INTEGER PRIMARY KEY,
    topic_id INTEGER NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    text TEXT NOT NULL
);
"""

# Limite di caratteri per singola chiamata al modello quando si estrae il programma.
CHUNK_CHARS = 12_000


@dataclass
class Document:
    id: int
    source: str
    kind: str
    text: str
    created_at: str


@dataclass
class Topic:
    name: str
    concepts: list[str] = field(default_factory=list)


class ReferenceDB:
    def __init__(self, path: Path | str) -> None:
        self.conn = connect(path, SCHEMA)

    # --- Materiale ----------------------------------------------------------------------------

    def add_document(self, source: str, text: str, kind: str = "upload") -> int:
        text = text.strip()
        if not text:
            raise ValueError("Il documento è vuoto.")
        cur = self.conn.execute(
            "INSERT INTO documents (source, kind, text, created_at) VALUES (?, ?, ?, ?)",
            (source, kind, text, now()),
        )
        self.conn.commit()
        return cur.lastrowid

    def documents(self) -> list[Document]:
        rows = self.conn.execute("SELECT * FROM documents ORDER BY id").fetchall()
        return [Document(**dict(r)) for r in rows]

    # --- Programma (argomenti e concetti) -------------------------------------------------------

    def set_topics(self, topics: list[Topic]) -> None:
        with self.conn:
            self.conn.execute("DELETE FROM concepts")
            self.conn.execute("DELETE FROM topics")
            for pos, topic in enumerate(topics):
                cur = self.conn.execute(
                    "INSERT INTO topics (name, position) VALUES (?, ?)", (topic.name, pos)
                )
                self.conn.executemany(
                    "INSERT INTO concepts (topic_id, text) VALUES (?, ?)",
                    [(cur.lastrowid, c) for c in topic.concepts],
                )

    def topics(self) -> list[Topic]:
        result = []
        for t in self.conn.execute("SELECT id, name FROM topics ORDER BY position").fetchall():
            concepts = [
                r["text"]
                for r in self.conn.execute(
                    "SELECT text FROM concepts WHERE topic_id = ? ORDER BY id", (t["id"],)
                )
            ]
            result.append(Topic(name=t["name"], concepts=concepts))
        return result


def _chunks(text: str, size: int = CHUNK_CHARS) -> list[str]:
    paragraphs = text.split("\n\n")
    chunks, current = [], ""
    for p in paragraphs:
        while len(p) > size:  # paragrafo enorme: taglio netto
            if current:
                chunks.append(current)
                current = ""
            chunks.append(p[:size])
            p = p[size:]
        if len(current) + len(p) + 2 > size and current:
            chunks.append(current)
            current = ""
        current = f"{current}\n\n{p}" if current else p
    if current.strip():
        chunks.append(current)
    return chunks


def _parse_topics(data: dict) -> list[Topic]:
    topics = []
    for t in data.get("topics", []):
        name = str(t.get("name", "")).strip()
        concepts = [str(c).strip() for c in t.get("concepts", []) if str(c).strip()]
        if name and concepts:
            topics.append(Topic(name=name, concepts=concepts))
    return topics


def build_syllabus(reference: ReferenceDB, llm: LLM, subject: str) -> list[Topic]:
    """Ricava argomenti e concetti chiave dal materiale caricato e li salva nel riferimento."""
    docs = reference.documents()
    if not docs:
        raise ValueError("Nessun materiale caricato: carica prima appunti, sbobinature o registrazioni.")

    partials: list[list[Topic]] = []
    system = prompts.SYLLABUS_SYSTEM.format(subject=subject)
    for doc in docs:
        for chunk in _chunks(doc.text):
            data = chat_json(llm, [
                {"role": "system", "content": system},
                {"role": "user", "content": f"Materiale ({doc.source}):\n\n{chunk}"},
            ])
            partials.append(_parse_topics(data))

    if len(partials) == 1:
        topics = partials[0]
    else:
        listing = "\n\n".join(
            "\n".join(f"- {t.name}: " + "; ".join(t.concepts) for t in part) for part in partials
        )
        data = chat_json(llm, [
            {"role": "system", "content": prompts.SYLLABUS_MERGE_SYSTEM.format(subject=subject)},
            {"role": "user", "content": listing},
        ])
        topics = _parse_topics(data)

    if not topics:
        raise ValueError("Non sono riuscito a ricavare argomenti dal materiale.")
    reference.set_topics(topics)
    return topics
