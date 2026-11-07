"""API HTTP di PUPO (FastAPI).

Espone le stesse operazioni della CLI (`pupo.cli`), usando le classi di `pupo/`:
vedi la tabella degli endpoint in `api/README.md`.

Regola di progetto: nessun endpoint fa leggere al Pupo il database di riferimento.
`/material` e `/recordings` scrivono solo nel database di riferimento (`ws.reference`);
`/teach`, `/quiz` e `/progress` passano dal `Workspace`, che costruisce il Pupo con
`ws.pupo()` (solo `learning`) e il confronto con `ws.comparison()` (l'unico componente
che vede entrambi i database, e che restituisce solo numeri).
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from pupo.documents import AUDIO_EXTENSIONS, extract_text
from pupo.reference_db import build_syllabus
from pupo.workspace import Workspace

from .deps import workspace_with_llm, workspace_without_llm

app = FastAPI(title="PUPO API")

# CORS aperto per l'app Expo in sviluppo (web, Android, iOS girano su origin diverse).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class TeachRequest(BaseModel):
    explanation: str


class QuizRequest(BaseModel):
    question: str


class ReplyResponse(BaseModel):
    reply: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/subjects/{subject}/material")
async def add_material(
    subject: str,
    file: UploadFile | None = File(default=None),
    text: str | None = Form(default=None),
    source: str | None = Form(default=None),
    ws: Workspace = Depends(workspace_without_llm),
) -> dict:
    """Sezione "Materiale": carica un documento di testo, come file (.txt/.md/.pdf) o testo diretto."""
    if file is not None:
        name = file.filename or "materiale"
        try:
            content = extract_text(name, await file.read())
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    elif text is not None:
        name = source or "appunti.txt"
        content = text
    else:
        raise HTTPException(status_code=400, detail="Fornisci un file o del testo.")

    try:
        doc_id = ws.reference.add_document(name, content, kind="upload")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"id": doc_id, "source": name}


@app.get("/subjects/{subject}/material")
def list_material(subject: str, ws: Workspace = Depends(workspace_without_llm)) -> dict:
    """Sezione "Materiale": elenca i documenti già caricati nel database di riferimento."""
    return {
        "documents": [
            {
                "id": d.id,
                "source": d.source,
                "kind": d.kind,
                "created_at": d.created_at,
                "words": len(d.text.split()),
            }
            for d in ws.reference.documents()
        ]
    }


@app.post("/subjects/{subject}/recordings")
async def add_recording(
    subject: str,
    file: UploadFile = File(...),
    ws: Workspace = Depends(workspace_with_llm),
) -> dict:
    """Sezione "Materiale": trascrive una registrazione audio nel database di riferimento."""
    ext = Path(file.filename or "").suffix.lower()
    if ext not in AUDIO_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Formato audio non supportato: {ext}")

    data = await file.read()
    with tempfile.NamedTemporaryFile(suffix=ext) as tmp:
        tmp.write(data)
        tmp.flush()
        text = ws.llm.transcribe(Path(tmp.name))

    doc_id = ws.reference.add_document(file.filename or "registrazione", text, kind="transcript")
    return {"id": doc_id, "source": file.filename, "text": text}


@app.post("/subjects/{subject}/syllabus")
def create_syllabus(subject: str, ws: Workspace = Depends(workspace_with_llm)) -> dict:
    """Ricava argomenti e concetti chiave dal materiale caricato (database di riferimento)."""
    try:
        topics = build_syllabus(ws.reference, ws.llm, subject)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"topics": [{"name": t.name, "concepts": t.concepts} for t in topics]}


@app.post("/subjects/{subject}/teach", response_model=ReplyResponse)
def teach(subject: str, body: TeachRequest, ws: Workspace = Depends(workspace_with_llm)) -> ReplyResponse:
    """Sezione "Insegna al Pupo": lo studente spiega, il Pupo annota e fa una domanda."""
    try:
        reply = ws.pupo().teach(body.explanation)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ReplyResponse(reply=reply)


@app.post("/subjects/{subject}/quiz", response_model=ReplyResponse)
def quiz(subject: str, body: QuizRequest, ws: Workspace = Depends(workspace_with_llm)) -> ReplyResponse:
    """Interroga il Pupo: risponde solo dal proprio quaderno (database di apprendimento)."""
    try:
        reply = ws.pupo().answer(body.question)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ReplyResponse(reply=reply)


@app.get("/subjects/{subject}/progress")
def progress(subject: str, ws: Workspace = Depends(workspace_with_llm)) -> dict:
    """Barra di preparazione: percentuale per argomento, dal modulo di confronto."""
    try:
        report = ws.comparison().progress()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return report.to_dict()
