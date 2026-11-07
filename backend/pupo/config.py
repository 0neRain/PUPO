"""Configurazione letta dalle variabili d'ambiente (e dal file .env, se presente)."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # python-dotenv è opzionale
    pass


@dataclass(frozen=True)
class Settings:
    model: str
    transcribe_model: str
    data_dir: Path

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            model=os.getenv("PUPO_MODEL", "gpt-4o-mini"),
            transcribe_model=os.getenv("PUPO_TRANSCRIBE_MODEL", "whisper-1"),
            data_dir=Path(os.getenv("PUPO_DATA_DIR", "data")),
        )
