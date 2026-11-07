"""Estrazione di testo dai documenti caricati.

Condiviso tra la CLI (file su disco) e l'API (file caricati via HTTP), per non
duplicare la logica di lettura di .txt/.md/.pdf.
"""

from __future__ import annotations

import io
from pathlib import Path

TEXT_EXTENSIONS = {".txt", ".md"}
AUDIO_EXTENSIONS = {".mp3", ".m4a", ".wav", ".webm", ".mp4", ".mpeg", ".mpga", ".ogg"}


def extract_text(filename: str, data: bytes) -> str:
    """Ricava il testo di un documento (materiale) dal suo contenuto grezzo."""
    ext = Path(filename).suffix.lower()
    if ext in TEXT_EXTENSIONS:
        return data.decode("utf-8")
    if ext == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError:
            raise ValueError('Per i PDF installa il supporto: pip install -e ".[pdf]"')
        return "\n\n".join(page.extract_text() or "" for page in PdfReader(io.BytesIO(data)).pages)
    raise ValueError(f"Formato non supportato: {ext}. Usa .txt, .md o .pdf (per l'audio: transcribe).")
