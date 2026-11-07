"""Dipendenze FastAPI: studente/materia dalla richiesta, Workspace, LLM.

Niente autenticazione per ora: lo studente arriva da un header semplice,
la materia dal path dell'endpoint.
"""

from __future__ import annotations

import os

from fastapi import Depends, Header, HTTPException

from pupo.config import Settings
from pupo.llm import LLM, OpenAILLM
from pupo.workspace import Workspace


def get_settings() -> Settings:
    return Settings.from_env()


def get_student(x_student: str = Header(default="demo", alias="X-Student")) -> str:
    return x_student


def _make_llm(settings: Settings) -> LLM:
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(
            status_code=503,
            detail="Manca OPENAI_API_KEY: configura backend/.env per usare questa funzione.",
        )
    return OpenAILLM(settings.model, settings.transcribe_model)


def workspace_without_llm(subject: str, student: str = Depends(get_student)) -> Workspace:
    """Per le operazioni che non servono il modello (es. caricare materiale)."""
    settings = get_settings()
    return Workspace(settings.data_dir, student, subject, None)


def workspace_with_llm(subject: str, student: str = Depends(get_student)) -> Workspace:
    """Per le operazioni che servono il modello (trascrizione, programma, Pupo, progresso)."""
    settings = get_settings()
    return Workspace(settings.data_dir, student, subject, _make_llm(settings))
