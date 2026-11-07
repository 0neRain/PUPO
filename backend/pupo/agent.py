"""L'agente Pupo.

DECISIONE DI PROGETTO: il Pupo ha accesso SOLO al database di apprendimento.
Questo modulo non importa `reference_db` e `PupoAgent` non riceve mai il database di riferimento:
c'è un test (`tests/test_separation.py`) che lo verifica.
"""

from __future__ import annotations

from . import prompts
from .learning_db import LearningDB
from .llm import LLM, chat_json

# Sotto questa soglia di giorni di inattività, il Pupo non fa notare il tempo passato.
FORGETTING_THRESHOLD_DAYS = 3


class PupoAgent:
    def __init__(self, learning: LearningDB, llm: LLM, subject: str) -> None:
        self.learning = learning
        self.llm = llm
        self.subject = subject

    def _memory_note(self) -> str:
        """Nota per il prompt se è passato tanto tempo dall'ultima volta: vedi FORGETTING_THRESHOLD_DAYS."""
        days = self.learning.days_since_last_activity()
        if days is None or days < FORGETTING_THRESHOLD_DAYS:
            return ""
        return prompts.MEMORY_NOTE.format(days=days, subject=self.subject)

    def _extract_statements(self, explanation: str) -> list[str]:
        data = chat_json(self.llm, [
            {"role": "system", "content": prompts.BELIEF_EXTRACTION_SYSTEM.format(subject=self.subject)},
            {"role": "user", "content": explanation},
        ])
        return [str(s).strip() for s in data.get("statements", []) if str(s).strip()]

    def teach(self, explanation: str) -> str:
        """Sezione "Insegna al Pupo": lo studente spiega, il Pupo annota e fa una domanda."""
        explanation = explanation.strip()
        if not explanation:
            raise ValueError("La spiegazione è vuota.")

        memory_note = self._memory_note()  # prima di registrare questa interazione come "ora"

        statements = self._extract_statements(explanation)
        if statements:
            self.learning.add_lesson(explanation, statements)

        system = prompts.PUPO_TEACH_SYSTEM.format(
            subject=self.subject, notebook=self.learning.notebook(), memory_note=memory_note
        )
        messages = [{"role": "system", "content": system}]
        messages += self.learning.history("teach")
        messages.append({"role": "user", "content": explanation})
        reply = self.llm.chat(messages, temperature=0.7)

        self.learning.add_message("teach", "user", explanation)
        self.learning.add_message("teach", "assistant", reply)
        return reply

    def answer(self, question: str) -> str:
        """Interrogazione: il Pupo risponde usando solo il proprio quaderno."""
        question = question.strip()
        if not question:
            raise ValueError("La domanda è vuota.")

        memory_note = self._memory_note()  # prima di registrare questa interazione come "ora"

        system = prompts.PUPO_QUIZ_SYSTEM.format(
            subject=self.subject, notebook=self.learning.notebook(), memory_note=memory_note
        )
        messages = [{"role": "system", "content": system}]
        messages += self.learning.history("quiz", limit=6)
        messages.append({"role": "user", "content": question})
        reply = self.llm.chat(messages, temperature=0.2)

        self.learning.add_message("quiz", "user", question)
        self.learning.add_message("quiz", "assistant", reply)
        return reply
