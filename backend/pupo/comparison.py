"""Modulo di confronto: calcola la percentuale di preparazione.

È l'UNICO componente che vede entrambi i database. Restituisce solo numeri (per argomento),
mai il testo dei concetti del riferimento: così né il Pupo né la barra di preparazione
possono rivelare il contenuto del materiale.

Formula (per argomento):
    percentuale = concetti spiegati correttamente / concetti totali dell'argomento
Un concetto spiegato in modo sbagliato vale 0, come uno mancante, ma viene contato a parte
così lo studente sa se deve "aggiungere" o "correggere".
Totale = somma dei concetti corretti / somma dei concetti di tutti gli argomenti.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

from . import prompts
from .learning_db import LearningDB
from .llm import LLM, chat_json
from .reference_db import ReferenceDB

VALID_STATUSES = {"correct", "wrong", "missing"}


@dataclass(frozen=True)
class TopicProgress:
    topic: str
    percent: int
    correct: int
    wrong: int
    missing: int
    total: int


@dataclass(frozen=True)
class ProgressReport:
    overall_percent: int
    topics: list[TopicProgress]

    def to_dict(self) -> dict:
        return {"overall_percent": self.overall_percent, "topics": [asdict(t) for t in self.topics]}


def _percent(part: int, whole: int) -> int:
    return round(100 * part / whole) if whole else 0


class ComparisonModule:
    def __init__(self, reference: ReferenceDB, learning: LearningDB, llm: LLM, subject: str) -> None:
        self._reference = reference
        self._learning = learning
        self._llm = llm
        self._subject = subject

    def _judge(self, concepts: list[str], notebook: str) -> list[str]:
        numbered = "\n".join(f"{i}. {c}" for i, c in enumerate(concepts))
        data = chat_json(self._llm, [
            {"role": "system", "content": prompts.JUDGE_SYSTEM.format(subject=self._subject)},
            {"role": "user", "content": f"CONCETTI CHIAVE:\n{numbered}\n\nQUADERNO:\n{notebook}"},
        ])
        statuses = ["missing"] * len(concepts)  # in caso di dubbio: non dare credito
        for item in data.get("results", []):
            try:
                i = int(item.get("i"))
            except (TypeError, ValueError):
                continue
            status = str(item.get("status", "")).lower()
            if 0 <= i < len(concepts) and status in VALID_STATUSES:
                statuses[i] = status
        return statuses

    def progress(self) -> ProgressReport:
        topics = self._reference.topics()
        if not topics:
            raise ValueError("Programma non ancora creato: carica il materiale e crea il programma.")

        has_beliefs = bool(self._learning.beliefs())
        notebook = self._learning.notebook()
        results = []
        for topic in topics:
            n = len(topic.concepts)
            if has_beliefs:
                statuses = self._judge(topic.concepts, notebook)
            else:  # mente vuota: inutile chiamare il modello
                statuses = ["missing"] * n
            correct = statuses.count("correct")
            results.append(TopicProgress(
                topic=topic.name,
                percent=_percent(correct, n),
                correct=correct,
                wrong=statuses.count("wrong"),
                missing=statuses.count("missing"),
                total=n,
            ))

        total = sum(t.total for t in results)
        correct = sum(t.correct for t in results)
        return ProgressReport(overall_percent=_percent(correct, total), topics=results)
