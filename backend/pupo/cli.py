"""Interfaccia a riga di comando del prototipo.

Esempi:
    pupo --subject analisi1 upload sbobina.txt
    pupo --subject analisi1 transcribe lezione.mp3
    pupo --subject analisi1 syllabus
    pupo --subject analisi1 teach
    pupo --subject analisi1 quiz
    pupo --subject analisi1 progress
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .config import Settings
from .documents import AUDIO_EXTENSIONS, extract_text
from .reference_db import build_syllabus
from .workspace import Workspace


def read_document(path: Path) -> str:
    try:
        return extract_text(path.name, path.read_bytes())
    except ValueError as e:
        raise SystemExit(str(e))


def bar(percent: int, width: int = 20) -> str:
    filled = round(width * percent / 100)
    return "█" * filled + "░" * (width - filled)


def make_llm(settings: Settings):
    import os

    from .llm import OpenAILLM

    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Manca OPENAI_API_KEY: copia .env.example in backend/.env e inserisci la chiave.")
    return OpenAILLM(settings.model, settings.transcribe_model)


def cmd_upload(ws: Workspace, args) -> None:
    for name in args.files:
        path = Path(name)
        ws.reference.add_document(path.name, read_document(path), kind="upload")
        print(f"✓ Caricato nel materiale: {path.name}")
    print("Suggerimento: dopo aver caricato tutto, esegui 'syllabus' per aggiornare il programma.")


def cmd_transcribe(ws: Workspace, args) -> None:
    path = Path(args.audio)
    if path.suffix.lower() not in AUDIO_EXTENSIONS:
        raise SystemExit(f"Formato audio non supportato: {path.suffix}")
    print(f"Trascrivo {path.name}…")
    text = ws.llm.transcribe(path)
    ws.reference.add_document(path.name, text, kind="transcript")
    print(f"✓ Trascrizione salvata nel materiale ({len(text.split())} parole).")


def cmd_material(ws: Workspace, args) -> None:
    docs = ws.reference.documents()
    if not docs:
        print("Nessun materiale caricato.")
    for d in docs:
        print(f"[{d.id}] {d.source} ({d.kind}, {len(d.text.split())} parole)")


def cmd_syllabus(ws: Workspace, args) -> None:
    print("Ricavo argomenti e concetti chiave dal materiale…")
    topics = build_syllabus(ws.reference, ws.llm, ws.subject)
    print(f"✓ Programma creato: {len(topics)} argomenti.")
    for t in topics:
        print(f"  • {t.name} ({len(t.concepts)} concetti)")


def _chat_loop(prompt_label: str, handle) -> None:
    print("Scrivi e premi Invio. Comandi: /esci per uscire.\n")
    while True:
        try:
            text = input(f"{prompt_label} > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not text:
            continue
        if text.lower() in {"/esci", "/exit", "/quit"}:
            break
        print(f"\nPupo > {handle(text)}\n")


def cmd_teach(ws: Workspace, args) -> None:
    print(f"=== Insegna al Pupo – {ws.subject} ===")
    print("Sei il professore: spiega un argomento al Pupo con parole tue.")
    _chat_loop("Tu (prof)", ws.pupo().teach)


def cmd_quiz(ws: Workspace, args) -> None:
    print(f"=== Interroga il Pupo – {ws.subject} ===")
    _chat_loop("Tu (domanda)", ws.pupo().answer)


def cmd_progress(ws: Workspace, args) -> None:
    report = ws.comparison().progress()
    print(f"=== Preparazione – {ws.subject} ===\n")
    width = max(len(t.topic) for t in report.topics)
    for t in report.topics:
        detail = f"{t.correct}/{t.total} ok"
        if t.wrong:
            detail += f", {t.wrong} da correggere"
        print(f"  {t.topic:<{width}}  {bar(t.percent)} {t.percent:>3}%  ({detail})")
    print(f"\n  {'TOTALE':<{width}}  {bar(report.overall_percent)} {report.overall_percent:>3}%")


def cmd_reset(ws: Workspace, args) -> None:
    if input("Svuotare la mente del Pupo? Il materiale resta. (s/N) ").strip().lower() == "s":
        ws.learning.reset()
        print("✓ Il Pupo è tornato a non sapere niente.")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="pupo", description="PUPO – l'AI che impara da te.")
    p.add_argument("--student", default="demo", help="nome dello studente (default: demo)")
    p.add_argument("--subject", required=True, help="materia, es. analisi1")
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("upload", help="Materiale: carica file di testo/PDF")
    s.add_argument("files", nargs="+")
    s.set_defaults(func=cmd_upload)

    s = sub.add_parser("transcribe", help="Materiale: trascrivi una lezione registrata")
    s.add_argument("audio")
    s.set_defaults(func=cmd_transcribe)

    sub.add_parser("material", help="Materiale: elenca i documenti caricati").set_defaults(func=cmd_material)
    sub.add_parser("syllabus", help="Crea il programma dal materiale").set_defaults(func=cmd_syllabus)
    sub.add_parser("teach", help="Insegna al Pupo").set_defaults(func=cmd_teach)
    sub.add_parser("quiz", help="Interroga il Pupo").set_defaults(func=cmd_quiz)
    sub.add_parser("progress", help="Percentuale di preparazione").set_defaults(func=cmd_progress)
    sub.add_parser("reset", help="Svuota la mente del Pupo").set_defaults(func=cmd_reset)
    return p


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    settings = Settings.from_env()
    needs_llm = args.command not in {"upload", "material", "reset"}
    llm = make_llm(settings) if needs_llm else None
    ws = Workspace(settings.data_dir, args.student, args.subject, llm)
    try:
        args.func(ws, args)
    except ValueError as e:
        print(f"Errore: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
