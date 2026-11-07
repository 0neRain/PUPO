"""Un Pupo per studente e per materia: ognuno ha la sua cartella con due database separati.

    data/<studente>/<materia>/reference.db   -> database di riferimento
    data/<studente>/<materia>/learning.db    -> mente del Pupo
"""

from __future__ import annotations

import re
from pathlib import Path

from .agent import PupoAgent
from .comparison import ComparisonModule
from .learning_db import LearningDB
from .llm import LLM
from .reference_db import ReferenceDB


def slug(value: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip().lower()).strip("-")
    if not s:
        raise ValueError(f"Nome non valido: {value!r}")
    return s


class Workspace:
    def __init__(self, data_dir: Path, student: str, subject: str, llm: LLM) -> None:
        self.subject = subject
        self.dir = Path(data_dir) / slug(student) / slug(subject)
        self.llm = llm
        self.reference = ReferenceDB(self.dir / "reference.db")
        self.learning = LearningDB(self.dir / "learning.db")

    def pupo(self) -> PupoAgent:
        # Il Pupo riceve SOLO il database di apprendimento.
        return PupoAgent(self.learning, self.llm, self.subject)

    def comparison(self) -> ComparisonModule:
        return ComparisonModule(self.reference, self.learning, self.llm, self.subject)
