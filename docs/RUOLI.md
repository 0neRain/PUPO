# Ruoli e divisione del lavoro

Assegnazione: Ruolo 1 = [NOME] · Ruolo 2 = [NOME] · Ruolo 3 = [NOME] · Ruolo 4 = [NOME]

| Ruolo | Area | Cartelle / file di cui è responsabile |
|---|---|---|
| 1 – Ricerca e problema | Studi, competitor, dati, metriche | `docs/ricerca/` |
| 2 – Prodotto e UX | Personalità del Pupo, user journey, schermate, sfide amichevoli | `backend/pupo/prompts.py` (personalità, con Ruolo 3), `app/`, `docs/ux/` |
| 3 – Architettura e prototipo | Database, agente, modulo di confronto, API | `backend/` |
| 4 – Pitch ed etica | Acronimo, script, FAQ giudici, privacy/GDPR, presentazione | `docs/pitch/` |

## Regole di lavoro sul repository

- Non lavorare direttamente su `main`: crea un branch (`ruolo2/personalita-pupo`, `ruolo3/api`, …)
  e apri una pull request.
- Non fare mai commit di `.env` (chiavi API) o della cartella `data/` (materiale e registrazioni).
- Le **decisioni già prese** sono in `docs/PROMPT_TEAM.md`, sezione 4. Il codice le rispetta:
  in particolare `backend/pupo/agent.py` **non deve mai** importare `reference_db`
  (c'è un test che lo controlla).

## Prossimi passi tecnici

1. **API HTTP** in `backend/api/` (FastAPI), che espone le stesse funzioni della CLI. [Ruolo 3]
2. **App Expo** in `app/`: schermate Materiale, Insegna al Pupo, barra di preparazione, sfide. [Ruolo 2 + 3]
3. Migliorare la **personalità** del Pupo in `prompts.py` con i dialoghi di esempio. [Ruolo 2]
4. Validare la **percentuale**: confrontarla con quiz reali su una materia di prova. [Ruolo 1 + 3]
