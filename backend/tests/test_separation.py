"""Verifica la decisione di progetto: il Pupo NON può accedere al database di riferimento."""

import ast
import inspect
from pathlib import Path

from pupo import agent
from pupo.agent import PupoAgent

PKG = Path(agent.__file__).parent


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            names.add(node.module or "")
            names.update(a.name for a in node.names)
        elif isinstance(node, ast.Import):
            names.update(a.name for a in node.names)
    return names


def test_agent_does_not_import_reference_or_comparison():
    imported = _imported_modules(PKG / "agent.py")
    for forbidden in ("reference_db", "comparison", "ReferenceDB", "ComparisonModule"):
        assert not any(forbidden in m for m in imported), f"agent.py importa {forbidden}"


def test_agent_only_receives_learning_db():
    params = list(inspect.signature(PupoAgent.__init__).parameters)
    assert params == ["self", "learning", "llm", "subject"]


def test_pupo_prompts_contain_only_notebook(tmp_path):
    """Quello che arriva al modello del Pupo non contiene il materiale di riferimento."""
    from pupo.llm import FakeLLM
    from pupo.workspace import Workspace

    def handler(messages, json_mode):
        return '{"statements": ["Il limite descrive dove va una funzione"]}' if json_mode else "Ok!"

    llm = FakeLLM(handler)
    ws = Workspace(tmp_path, "s", "analisi", llm)
    ws.reference.add_document("sbobina.txt", "SEGRETO: la derivata è il limite del rapporto incrementale")
    ws.pupo().teach("Il limite descrive dove va una funzione")
    ws.pupo().answer("Cos'è la derivata?")

    for call in llm.calls:
        for message in call:
            assert "SEGRETO" not in message["content"]
