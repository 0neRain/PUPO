# App PUPO (Expo + TypeScript)

App cross-platform per PUPO: Android, iOS (provabili con Expo Go) e web, un solo codice.
L'app non contiene logica AI: chiama l'API in `backend/api/` (vedi `backend/api/README.md`).

Illustrazioni del Pupo riusate da `../Design/pupo-export/` (vedi `../Design/PUPO.md` per la
scheda del personaggio): stadi di crescita (0-25/26-60/61-90/91-100%) nella Home e in
Preparazione, icona app, varianti per materia.

## Avvio

```bash
cd app
cp .env.example .env     # EXPO_PUBLIC_API_URL, default http://localhost:8000
npm install
npx expo start            # poi "w" per il web
```

Il backend deve girare in parallelo (`cd backend && python -m uvicorn api.main:app --reload --port 8000`).

## Schermate

1. **Home** (tab) — elenco materie (salvate localmente, nessun login), ciascuna con l'illustrazione
   del Pupo allo stadio corrispondente alla percentuale e un badge "Ripassa" se è passato tanto tempo.
2. **Materiale** (dentro la materia) — incolla testo, elenco di quanto già caricato, crea il programma.
3. **Insegna al Pupo** (dentro la materia) — chat, il Pupo annota e fa domande.
4. **Interroga il Pupo** (dentro la materia) — chat, il Pupo risponde solo da ciò che sa.
5. **Preparazione** (dentro la materia) — barre per argomento + totale, stesso badge di ripasso.
6. **Sfide** (tab) — mock statico, solo per il pitch: nessuna logica reale ancora.

## Note

- Nessuna autenticazione: lo studente è un nome locale (salvato con AsyncStorage), inviato come
  header `X-Student` a ogni chiamata.
- L'elenco delle materie di uno studente è locale all'app (il backend non lo espone): vedi
  `lib/student.ts`.
