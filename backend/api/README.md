# API (prossimo passo – Ruolo 3)

Qui andrà l'API HTTP (FastAPI) che l'app usa per parlare con il backend.
Deve esporre le stesse operazioni della CLI, usando le classi in `pupo/`:

| Endpoint (proposta) | Usa | Sezione dell'app |
|---|---|---|
| `POST /subjects/{s}/material` (testo o file) | `ReferenceDB.add_document` | Materiale |
| `POST /subjects/{s}/recordings` (audio) | `llm.transcribe` + `ReferenceDB.add_document` | Materiale |
| `POST /subjects/{s}/syllabus` | `build_syllabus` | Materiale |
| `POST /subjects/{s}/teach` | `PupoAgent.teach` | Insegna al Pupo |
| `POST /subjects/{s}/quiz` | `PupoAgent.answer` | Insegna al Pupo |
| `GET  /subjects/{s}/progress` | `ComparisonModule.progress` | Barra di preparazione |

Regola: nessun endpoint deve restituire all'app il contenuto del database di riferimento
**attraverso il Pupo**. Lo studente può rivedere il proprio materiale nella sezione Materiale,
ma il Pupo e la barra di preparazione non lo usano mai per dare risposte.
