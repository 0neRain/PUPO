import json

import pytest

from pupo.comparison import ComparisonModule
from pupo.learning_db import LearningDB
from pupo.llm import FakeLLM
from pupo.reference_db import ReferenceDB, Topic, build_syllabus, _chunks
from pupo.workspace import Workspace, slug


def test_learning_db_starts_empty_and_keeps_wrong_beliefs(tmp_path):
    db = LearningDB(tmp_path / "learning.db")
    assert db.beliefs() == []
    assert "vuoto" in db.notebook()
    db.add_lesson("La derivata di x^2 è x", ["La derivata di x^2 è x"])  # sbagliato: resta così
    assert [b.statement for b in db.beliefs()] == ["La derivata di x^2 è x"]
    db.reset()
    assert db.beliefs() == []


def test_databases_are_separate_files(tmp_path):
    ws = Workspace(tmp_path, "Mario Rossi", "Analisi 1", llm=None)
    assert (ws.dir / "reference.db").exists()
    assert (ws.dir / "learning.db").exists()
    assert ws.dir == tmp_path / "mario-rossi" / "analisi-1"


def test_slug_rejects_empty():
    with pytest.raises(ValueError):
        slug("  ///  ")


def test_teach_stores_statements_and_returns_question(tmp_path):
    def handler(messages, json_mode):
        if json_mode:
            return json.dumps({"statements": ["Un limite può non esistere"]})
        assert "Un limite può non esistere" in messages[0]["content"]  # quaderno nel prompt
        return "Ho capito che un limite può non esistere. Ma quando succede?"

    ws = Workspace(tmp_path, "s", "analisi", FakeLLM(handler))
    reply = ws.pupo().teach("Ciao Pupo, oggi: un limite può non esistere.")
    assert reply.endswith("?")
    assert len(ws.learning.beliefs()) == 1
    assert len(ws.learning.history("teach")) == 2


def test_teach_with_no_content_does_not_store_beliefs(tmp_path):
    def handler(messages, json_mode):
        return '{"statements": []}' if json_mode else "Ciao prof!"

    ws = Workspace(tmp_path, "s", "analisi", FakeLLM(handler))
    ws.pupo().teach("Ciao!")
    assert ws.learning.beliefs() == []


def _judge_handler(verdicts):
    """Il giudice finto assegna gli stati nell'ordine dato, argomento per argomento."""
    queue = list(verdicts)

    def handler(messages, json_mode):
        statuses = queue.pop(0)
        return json.dumps({"results": [{"i": i, "status": s} for i, s in enumerate(statuses)]})

    return handler


def test_progress_percentages(tmp_path):
    ref = ReferenceDB(tmp_path / "r.db")
    ref.set_topics([
        Topic("Limiti", ["c1", "c2", "c3", "c4"]),
        Topic("Derivate", ["d1", "d2"]),
    ])
    learn = LearningDB(tmp_path / "l.db")
    learn.add_lesson("spiegazione", ["qualcosa"])
    llm = FakeLLM(_judge_handler([
        ["correct", "correct", "correct", "wrong"],
        ["missing", "correct"],
    ]))

    report = ComparisonModule(ref, learn, llm, "analisi").progress()

    limiti, derivate = report.topics
    assert (limiti.percent, limiti.correct, limiti.wrong, limiti.missing) == (75, 3, 1, 0)
    assert (derivate.percent, derivate.correct, derivate.missing) == (50, 1, 1)
    assert report.overall_percent == round(100 * 4 / 6)


def test_progress_report_does_not_leak_concepts(tmp_path):
    ref = ReferenceDB(tmp_path / "r.db")
    ref.set_topics([Topic("Limiti", ["CONCETTO SEGRETO"])])
    learn = LearningDB(tmp_path / "l.db")
    learn.add_lesson("x", ["y"])
    report = ComparisonModule(ref, learn, FakeLLM(_judge_handler([["correct"]])), "a").progress()
    assert "CONCETTO SEGRETO" not in json.dumps(report.to_dict())


def test_progress_empty_mind_is_zero_without_calling_llm(tmp_path):
    ref = ReferenceDB(tmp_path / "r.db")
    ref.set_topics([Topic("Limiti", ["c1", "c2"])])
    llm = FakeLLM(lambda m, j: pytest.fail("non doveva chiamare il modello"))
    report = ComparisonModule(ref, LearningDB(tmp_path / "l.db"), llm, "a").progress()
    assert report.overall_percent == 0


def test_judge_bad_output_gives_no_credit(tmp_path):
    ref = ReferenceDB(tmp_path / "r.db")
    ref.set_topics([Topic("Limiti", ["c1", "c2"])])
    learn = LearningDB(tmp_path / "l.db")
    learn.add_lesson("x", ["y"])
    llm = FakeLLM(lambda m, j: '{"results": [{"i": 7, "status": "correct"}, {"i": 0, "status": "boh"}]}')
    report = ComparisonModule(ref, learn, llm, "a").progress()
    assert report.overall_percent == 0


def test_progress_requires_syllabus(tmp_path):
    module = ComparisonModule(ReferenceDB(tmp_path / "r.db"), LearningDB(tmp_path / "l.db"), None, "a")
    with pytest.raises(ValueError):
        module.progress()


def test_build_syllabus_single_and_merge(tmp_path):
    ref = ReferenceDB(tmp_path / "r.db")
    ref.add_document("a.txt", "lezione 1")
    ref.add_document("b.txt", "lezione 2")
    responses = [
        {"topics": [{"name": "Limiti", "concepts": ["c1"]}]},
        {"topics": [{"name": "Limiti", "concepts": ["c2"]}]},
        {"topics": [{"name": "Limiti", "concepts": ["c1", "c2"]}]},  # risultato dell'unione
    ]
    llm = FakeLLM(lambda m, j: json.dumps(responses.pop(0)))
    topics = build_syllabus(ref, llm, "analisi")
    assert [(t.name, t.concepts) for t in topics] == [("Limiti", ["c1", "c2"])]
    assert ref.topics()[0].concepts == ["c1", "c2"]


def test_build_syllabus_without_material_fails(tmp_path):
    with pytest.raises(ValueError):
        build_syllabus(ReferenceDB(tmp_path / "r.db"), None, "a")


def test_chunks_cover_all_text():
    text = "\n\n".join(f"paragrafo {i} " + "x" * 50 for i in range(100))
    chunks = _chunks(text, size=500)
    assert all(len(c) <= 500 for c in chunks)
    assert "".join(chunks).replace("\n", "") == text.replace("\n", "")


def test_invalid_json_is_retried(tmp_path):
    answers = ["non è json", '{"statements": ["ok"]}', "Domanda?"]
    ws = Workspace(tmp_path, "s", "a", FakeLLM(lambda m, j: answers.pop(0)))
    ws.pupo().teach("spiegazione")
    assert [b.statement for b in ws.learning.beliefs()] == ["ok"]
