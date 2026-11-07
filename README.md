# PUPO

**PUPO è un agente AI che fa lo studente: non sa niente e impara solo da quello che gli spieghi tu.**
Spiegandogli la materia, lo studente impara davvero e scopre, argomento per argomento, quanto è preparato.

Progetto per la Reply Student Tech Clash 2026 – *AI on Campus* (direzione **Learning**).

---

## Struttura del repository

```
PUPO/
├── backend/            # Python: il cuore del Pupo (Ruolo 3)
│   ├── pupo/
│   │   ├── reference_db.py   # Database di riferimento (materiale caricato dallo studente)
│   │   ├── learning_db.py    # Database di apprendimento (la "mente" del Pupo)
│   │   ├── agent.py          # L'agente Pupo: vede SOLO il database di apprendimento
│   │   ├── comparison.py     # Modulo di confronto: restituisce SOLO percentuali
│   │   ├── prompts.py        # System prompt del Pupo e degli altri componenti (Ruoli 2-3)
│   │   ├── llm.py            # Collegamento a OpenAI (+ LLM finto per i test)
│   │   ├── workspace.py      # Un Pupo per studente e per materia
│   │   ├── config.py         # Configurazione da variabili d'ambiente
│   │   └── cli.py            # Interfaccia a riga di comando
│   ├── api/            # (prossimo passo) API HTTP per l'app
│   └── tests/          # Test offline, senza chiave API
├── app/                # (prossimo passo) App cross-platform Expo: Android, iOS, web/PC
└── docs/
    ├── ARCHITETTURA.md # Come funziona e perché i database sono separati
    ├── RUOLI.md        # Chi lavora su cosa
    └── PROMPT_TEAM.md  # Prompt di progetto condiviso per i Claude del team
```

## Avvio rapido (riga di comando)

Requisiti: Python 3.10+ e una chiave API OpenAI.

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
cp ../.env.example .env        # poi inserisci la tua OPENAI_API_KEY nel file .env
```

Flusso tipico, per una materia (es. `analisi1`):

```bash
# 1. Sezione "Materiale": carica appunti/sbobinature o trascrivi una lezione registrata
pupo --subject analisi1 upload sbobina_lezione1.txt
pupo --subject analisi1 transcribe lezione2.mp3

# 2. Crea il programma (argomenti e concetti chiave) dal materiale caricato
pupo --subject analisi1 syllabus

# 3. Sezione "Insegna al Pupo": spiegagli la materia
pupo --subject analisi1 teach

# 4. Interroga il Pupo per vedere cosa ha capito
pupo --subject analisi1 quiz

# 5. Percentuale di preparazione per argomento
pupo --subject analisi1 progress
```

I dati vengono salvati in `backend/data/<studente>/<materia>/` in **due file separati**:
`reference.db` e `learning.db`.

## Test

```bash
cd backend
pip install -e ".[dev]"
pytest
```

I test non usano OpenAI: girano con un LLM finto e verificano, tra le altre cose,
che l'agente Pupo non possa accedere al database di riferimento.

## Documentazione

- [Architettura](docs/ARCHITETTURA.md)
- [Ruoli e divisione del lavoro](docs/RUOLI.md)
