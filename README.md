# PUPO

**PUPO è un agente AI che fa lo studente: non sa niente e impara solo da quello che gli spieghi tu.**
Spiegandogli la materia, lo studente impara davvero e scopre, argomento per argomento, quanto è preparato.

Progetto per la Reply Student Tech Clash 2026 – *AI on Campus* (direzione **Learning**).

---

## Struttura del repository

```
PUPO/
├── backend/
│   ├── pupo/
│   │   ├── reference_db.py   # Database di riferimento (materiale caricato dallo studente)
│   │   ├── learning_db.py    # Database di apprendimento (la "mente" del Pupo)
│   │   ├── agent.py          # L'agente Pupo: vede SOLO il database di apprendimento
│   │   ├── comparison.py     # Modulo di confronto: restituisce SOLO percentuali
│   │   ├── documents.py      # Estrazione testo da .txt/.md/.pdf (CLI e API)
│   │   ├── prompts.py        # System prompt del Pupo e degli altri componenti
│   │   ├── llm.py            # Collegamento a OpenAI (+ LLM finto per i test)
│   │   ├── workspace.py      # Un Pupo per studente e per materia
│   │   ├── config.py         # Configurazione da variabili d'ambiente
│   │   └── cli.py            # Interfaccia a riga di comando
│   ├── api/             # API HTTP (FastAPI) per l'app
│   ├── demo/            # Materiale + script per una demo end-to-end
│   └── tests/           # Test offline, senza chiave API
├── app/                 # App Expo (React Native + TypeScript): Android, iOS, web
├── Design/              # Illustrazioni del Pupo (character sheet, icona, stadi di crescita)
└── docs/
    ├── ARCHITETTURA.md  # Come funziona: input, mente, confronto, decisioni, output
    ├── RUOLI.md         # Chi lavora su cosa
    └── PROMPT_TEAM.md   # Prompt di progetto condiviso per i Claude del team
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

## API HTTP (per l'app)

```bash
cd backend
python -m uvicorn api.main:app --reload --port 8000
```

Espone le stesse operazioni della CLI su HTTP (vedi `backend/api/README.md` per gli endpoint).
Studente e materia non richiedono autenticazione: la materia va nel path (`/subjects/<materia>/...`),
lo studente in un header opzionale `X-Student` (default `demo`).

## Test

```bash
cd backend
pip install -e ".[dev]"
pytest
```

I test non usano OpenAI: girano con un LLM finto e verificano, tra le altre cose,
che l'agente Pupo non possa accedere al database di riferimento.

## Modelli, librerie e logica custom

**Modelli** (OpenAI, configurabili via `PUPO_MODEL`/`PUPO_TRANSCRIBE_MODEL` in `.env`):
- `gpt-4o-mini` — chat del Pupo (`teach`/`quiz`), estrazione delle affermazioni dalle spiegazioni,
  creazione del programma dal materiale, giudizio di correttezza nel modulo di confronto.
- `whisper-1` — trascrizione delle lezioni registrate.

**Librerie principali**: `openai` (SDK ufficiale), `fastapi` + `uvicorn` + `python-multipart`
(API HTTP), `pypdf` (estrazione testo da PDF, opzionale), `python-dotenv` (variabili d'ambiente),
`pytest` (test). Nessun framework di orchestrazione agentica: l'agente è system prompt + chiamate
dirette all'SDK OpenAI (`backend/pupo/llm.py`), per restare semplice e verificabile.

**Logica custom** (il cuore del progetto, non delegata al modello):
- **Separazione dei due database** (`reference_db.py` vs `learning_db.py`): l'agente Pupo
  (`agent.py`) non importa mai `reference_db`, verificato da un test statico
  (`tests/test_separation.py` ispeziona gli import con `ast`, non si fida solo del prompt).
- **Modulo di confronto** (`comparison.py`): l'unico componente che vede entrambi i database,
  e restituisce solo numeri (mai testo del riferimento), con un giudice LLM per concetto che
  classifica `correct` / `wrong` / `missing`; in caso di dubbio non dà credito.
- **Promemoria di ripasso** (`agent.py` + `learning_db.py`): se sono passati più di 3 giorni
  dall'ultima interazione, il Pupo lo nota nel prompt, senza mai cancellare nulla dalla sua mente.

## Esempi di interazione

Dalla stessa materia di esempio in `backend/demo/` (Analisi 1: limiti e derivate), eseguiti
davvero contro l'API OpenAI, non inventati.

**Insegnare al Pupo** (spiegazione completa):
> **Prof:** Un limite è il valore a cui si avvicina una funzione quando x si avvicina a un certo
> punto, anche se la funzione in quel punto non è definita. Se il limite da sinistra e quello da
> destra sono diversi, il limite non esiste. Una funzione è continua in un punto se il limite
> coincide con il valore della funzione in quel punto.
>
> **Pupo:** Ok, ho capito. [...] Quindi, se non ci sono valori definiti in un punto, posso
> comunque calcolare il limite? E come faccio a sapere se i limiti da sinistra e da destra sono
> diversi?

**Insegnare al Pupo** (spiegazione volutamente vaga, sulle derivate):
> **Prof:** La derivata è tipo la velocità con cui cambia una funzione, si usa per trovare i
> massimi e i minimi.
>
> **Pupo:** Ho capito che la derivata rappresenta la velocità con cui cambia una funzione [...]
> Ma come faccio a calcolare la derivata di una funzione? E cosa succede se la derivata in un
> punto è zero? Significa sempre che c'è un massimo o minimo?

**Interrogare il Pupo** su qualcosa di insegnato:
> **Tu:** Cos'è un limite?
> **Pupo:** Un limite è il valore a cui si avvicina una funzione quando x si avvicina a un certo
> punto, anche se la funzione in quel punto non è definita.

**Il Pupo tiene il confine** — interrogato su un argomento mai spiegato (gli integrali non sono
mai stati menzionati), non usa la conoscenza generale del modello sottostante:
> **Tu:** Cos'è un integrale?
> **Pupo:** Non me l'hanno ancora spiegato.

Risultato finale di `progress` sulla stessa sessione: **Limiti 67%** (spiegazione completa),
**Derivate 0%** (spiegazione vaga) — la percentuale riflette onestamente cosa il Pupo ha
davvero imparato, non cosa "sa" il modello.

## Documentazione

- [Architettura](docs/ARCHITETTURA.md)
- [Ruoli e divisione del lavoro](docs/RUOLI.md)
