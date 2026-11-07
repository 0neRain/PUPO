"""Test dell'API HTTP con FastAPI TestClient, senza chiamare OpenAI (FakeLLM)."""

import io
import json

import pytest
from fastapi import Header
from fastapi.testclient import TestClient

from api.deps import workspace_with_llm, workspace_without_llm
from api.main import app
from pupo.llm import FakeLLM
from pupo.workspace import Workspace


@pytest.fixture
def client(tmp_path):
    """Un client con Workspace isolati in tmp_path e un FakeLLM al posto di OpenAI."""
    llm = FakeLLM(lambda messages, json_mode: "")  # sovrascritto nei singoli test, se serve

    def _ws_with_llm(subject: str, student: str = Header(default="demo", alias="X-Student")) -> Workspace:
        return Workspace(tmp_path, student, subject, llm)

    def _ws_without_llm(subject: str, student: str = Header(default="demo", alias="X-Student")) -> Workspace:
        return Workspace(tmp_path, student, subject, None)

    app.dependency_overrides[workspace_with_llm] = _ws_with_llm
    app.dependency_overrides[workspace_without_llm] = _ws_without_llm
    try:
        yield TestClient(app), llm
    finally:
        app.dependency_overrides.clear()


def test_health(client):
    c, _ = client
    assert c.get("/health").json() == {"status": "ok"}


def test_add_material_as_text(client):
    c, _ = client
    r = c.post(
        "/subjects/analisi1/material",
        data={"text": "I limiti descrivono il comportamento di una funzione.", "source": "appunti.txt"},
    )
    assert r.status_code == 200
    assert r.json()["source"] == "appunti.txt"


def test_add_material_as_file(client):
    c, _ = client
    r = c.post(
        "/subjects/analisi1/material",
        files={"file": ("sbobina.txt", io.BytesIO(b"Lezione sui limiti."), "text/plain")},
    )
    assert r.status_code == 200
    assert r.json()["source"] == "sbobina.txt"


def test_add_material_without_file_or_text_fails(client):
    c, _ = client
    r = c.post("/subjects/analisi1/material")
    assert r.status_code == 400


def test_add_material_rejects_unsupported_extension(client):
    c, _ = client
    r = c.post(
        "/subjects/analisi1/material",
        files={"file": ("appunti.docx", io.BytesIO(b"qualcosa"), "application/octet-stream")},
    )
    assert r.status_code == 400


def test_recordings_transcribes_and_stores_in_reference(client, tmp_path):
    c, _ = client
    r = c.post(
        "/subjects/analisi1/recordings",
        files={"file": ("lezione1.mp3", io.BytesIO(b"audio finto"), "audio/mpeg")},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["source"] == "lezione1.mp3"
    assert "trascrizione finta" in body["text"]

    ws = Workspace(tmp_path, "demo", "analisi1", None)
    docs = ws.reference.documents()
    assert len(docs) == 1
    assert docs[0].kind == "transcript"


def test_recordings_rejects_unsupported_extension(client):
    c, _ = client
    r = c.post(
        "/subjects/analisi1/recordings",
        files={"file": ("lezione1.txt", io.BytesIO(b"non audio"), "text/plain")},
    )
    assert r.status_code == 400


def test_syllabus_builds_topics_from_material(client):
    c, llm = client
    c.post(
        "/subjects/analisi1/material",
        data={"text": "lezione sui limiti", "source": "a.txt"},
    )
    llm.handler = lambda m, j: json.dumps({"topics": [{"name": "Limiti", "concepts": ["c1", "c2"]}]})

    r = c.post("/subjects/analisi1/syllabus")
    assert r.status_code == 200
    assert r.json() == {"topics": [{"name": "Limiti", "concepts": ["c1", "c2"]}]}


def test_syllabus_without_material_fails(client):
    c, _ = client
    r = c.post("/subjects/analisi1/syllabus")
    assert r.status_code == 400


def test_teach_returns_pupo_reply_and_stores_belief(client, tmp_path):
    c, llm = client

    def handler(messages, json_mode):
        if json_mode:
            return json.dumps({"statements": ["Un limite può non esistere"]})
        return "Ho capito. Ma quando succede?"

    llm.handler = handler

    r = c.post("/subjects/analisi1/teach", json={"explanation": "Un limite può non esistere."})
    assert r.status_code == 200
    assert r.json() == {"reply": "Ho capito. Ma quando succede?"}

    ws = Workspace(tmp_path, "demo", "analisi1", None)
    assert len(ws.learning.beliefs()) == 1


def test_teach_with_empty_explanation_fails(client):
    c, _ = client
    r = c.post("/subjects/analisi1/teach", json={"explanation": "   "})
    assert r.status_code == 400


def test_quiz_returns_pupo_reply(client):
    c, llm = client
    llm.handler = lambda m, j: "Non me l'hanno ancora spiegato."

    r = c.post("/subjects/analisi1/quiz", json={"question": "Cos'è una derivata?"})
    assert r.status_code == 200
    assert r.json() == {"reply": "Non me l'hanno ancora spiegato."}


def test_progress_returns_progress_report_dict(client):
    c, llm = client
    c.post("/subjects/analisi1/material", data={"text": "lezione", "source": "a.txt"})

    llm.handler = lambda m, j: json.dumps({"topics": [{"name": "Limiti", "concepts": ["c1", "c2"]}]})
    assert c.post("/subjects/analisi1/syllabus").status_code == 200

    llm.handler = lambda m, j: json.dumps({"statements": ["qualcosa"]}) if j else "Ok, domanda?"
    assert c.post("/subjects/analisi1/teach", json={"explanation": "qualcosa"}).status_code == 200

    llm.handler = lambda m, j: json.dumps(
        {"results": [{"i": 0, "status": "correct"}, {"i": 1, "status": "missing"}]}
    )

    r = c.get("/subjects/analisi1/progress")
    assert r.status_code == 200
    assert r.json() == {
        "overall_percent": 50,
        "topics": [
            {"topic": "Limiti", "percent": 50, "correct": 1, "wrong": 0, "missing": 1, "total": 2}
        ],
    }


def test_progress_requires_syllabus(client):
    c, _ = client
    r = c.get("/subjects/analisi1/progress")
    assert r.status_code == 400


def test_progress_does_not_leak_reference_concepts(client):
    c, llm = client
    c.post("/subjects/analisi1/material", data={"text": "lezione", "source": "a.txt"})
    llm.handler = lambda m, j: json.dumps(
        {"topics": [{"name": "Limiti", "concepts": ["CONCETTO SEGRETO"]}]}
    )
    assert c.post("/subjects/analisi1/syllabus").status_code == 200

    r = c.get("/subjects/analisi1/progress")
    assert "CONCETTO SEGRETO" not in r.text


def test_students_are_isolated_by_header(client, tmp_path):
    c, _ = client
    c.post(
        "/subjects/analisi1/material",
        data={"text": "lezione di Mario", "source": "a.txt"},
        headers={"X-Student": "mario"},
    )
    c.post(
        "/subjects/analisi1/material",
        data={"text": "lezione di Giulia", "source": "b.txt"},
        headers={"X-Student": "giulia"},
    )
    mario = Workspace(tmp_path, "mario", "analisi1", None)
    giulia = Workspace(tmp_path, "giulia", "analisi1", None)
    assert len(mario.reference.documents()) == 1
    assert len(giulia.reference.documents()) == 1
