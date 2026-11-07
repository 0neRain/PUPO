"""Collegamento al modello linguistico.

Tutto il resto del codice parla con un oggetto `LLM`, così si può:
- usare OpenAI in produzione (`OpenAILLM`);
- usare un LLM finto nei test, senza chiave API e senza costi (`FakeLLM`).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Callable, Protocol

Message = dict  # {"role": "system" | "user" | "assistant", "content": str}


class LLM(Protocol):
    def chat(self, messages: list[Message], *, json_mode: bool = False, temperature: float = 0.7) -> str: ...

    def transcribe(self, audio_path: Path) -> str: ...


def chat_json(llm: LLM, messages: list[Message]) -> dict:
    """Chiede una risposta JSON e la decodifica, con un secondo tentativo se non è valida."""
    raw = llm.chat(messages, json_mode=True, temperature=0)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        retry = messages + [
            {"role": "assistant", "content": raw},
            {"role": "user", "content": "La risposta non era JSON valido. Rispondi solo con JSON valido."},
        ]
        return json.loads(llm.chat(retry, json_mode=True, temperature=0))


class OpenAILLM:
    def __init__(self, model: str, transcribe_model: str = "whisper-1") -> None:
        from openai import OpenAI  # import qui: i test non richiedono il pacchetto configurato

        self._client = OpenAI()  # legge OPENAI_API_KEY dall'ambiente
        self.model = model
        self.transcribe_model = transcribe_model

    def chat(self, messages: list[Message], *, json_mode: bool = False, temperature: float = 0.7) -> str:
        kwargs = {}
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        response = self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            **kwargs,
        )
        return response.choices[0].message.content or ""

    def transcribe(self, audio_path: Path) -> str:
        with open(audio_path, "rb") as f:
            result = self._client.audio.transcriptions.create(model=self.transcribe_model, file=f)
        return result.text


class FakeLLM:
    """LLM finto per i test: `handler(messages, json_mode)` decide cosa rispondere."""

    def __init__(self, handler: Callable[[list[Message], bool], str]) -> None:
        self.handler = handler
        self.calls: list[list[Message]] = []

    def chat(self, messages: list[Message], *, json_mode: bool = False, temperature: float = 0.7) -> str:
        self.calls.append(messages)
        return self.handler(messages, json_mode)

    def transcribe(self, audio_path: Path) -> str:
        return f"[trascrizione finta di {Path(audio_path).name}]"
