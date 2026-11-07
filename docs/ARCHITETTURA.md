# Architettura di PUPO

```
                    ┌────────────────────────── STUDENTE ──────────────────────────┐
                    │                                                              │
         Sezione "Materiale"                                     Sezione "Insegna al Pupo"
   (registrazioni, sbobine, appunti)                               (spiega / interroga)
                    │                                                              │
                    ▼                                                              ▼
     ┌──────────────────────────────┐                          ┌──────────────────────────────┐
     │  DATABASE DI RIFERIMENTO     │                          │        AGENTE PUPO           │
     │  reference.db                │                          │  agent.py                    │
     │  - documenti caricati        │      ✗ nessun accesso    │  - annota nel quaderno       │
     │  - programma: argomenti +    │ ◄─────────────────────── │  - fa domande da studente    │
     │    concetti chiave           │                          │  - risponde SOLO dal quaderno│
     └──────────────┬───────────────┘                          └──────────────┬───────────────┘
                    │                                                         │
                    │                                                         ▼
                    │                                          ┌──────────────────────────────┐
                    │                                          │  DATABASE DI APPRENDIMENTO   │
                    │                                          │  learning.db ("mente")       │
                    │                                          │  - lezioni dello studente    │
                    │                                          │  - affermazioni (quaderno)   │
                    │                                          └──────────────┬───────────────┘
                    │                                                         │
                    └──────────────►  MODULO DI CONFRONTO  ◄──────────────────┘
                                      comparison.py
                                      restituisce SOLO numeri
                                            │
                                            ▼
                         Percentuale di preparazione per argomento
                         es. Limiti 75% · Derivate 50% · Totale 67%
```

## Componenti

| Componente | File | Vede il riferimento? | Vede la mente del Pupo? |
|---|---|---|---|
| Database di riferimento | `reference_db.py` | – | no |
| Database di apprendimento | `learning_db.py` | no | – |
| Agente Pupo | `agent.py` | **no** (verificato da test) | sì |
| Modulo di confronto | `comparison.py` | sì | sì |

I due database sono **due file SQLite separati** per ogni studente e materia:
`data/<studente>/<materia>/reference.db` e `learning.db`.

## Flusso

1. **Materiale.** Lo studente carica file (`upload`) o registrazioni (`transcribe`, con Whisper).
   Tutto va nel database di riferimento.
2. **Programma.** `build_syllabus` ricava dal materiale gli argomenti e i concetti chiave
   (3–10 per argomento). Il materiale lungo viene diviso in blocchi e poi i risultati vengono uniti.
3. **Insegna al Pupo.** A ogni spiegazione:
   - un primo passaggio estrae le affermazioni e le annota nel quaderno **così come sono**,
     anche se sbagliate;
   - il Pupo risponde usando solo il quaderno: riformula ciò che ha capito e fa una domanda.
4. **Interroga il Pupo.** Il Pupo risponde solo dal quaderno; se una cosa non gli è stata
   spiegata, lo dice.
5. **Preparazione.** Il modulo di confronto chiede a un "giudice" di classificare ogni concetto
   chiave come `correct`, `wrong` o `missing` rispetto al quaderno.

## Formula della percentuale

- Per argomento: `concetti corretti / concetti totali dell'argomento`.
- Totale: `somma dei concetti corretti / somma dei concetti di tutti gli argomenti`.
- I concetti sbagliati valgono 0 come quelli mancanti, ma vengono mostrati a parte
  ("da correggere"), perché lo studente deve sapere se aggiungere o correggere.
- Se il giudice risponde in modo non valido, il concetto conta come mancante: **in caso di dubbio
  non si dà credito**, per non dare una falsa sicurezza.

## Rischio tecnico n.1: il modello "sa già" le cose

Un modello come GPT conosce già moltissimo dal suo addestramento, quindi il Pupo non parte davvero
vuoto. Contromisure nel prototipo:
- il system prompt vieta di usare conoscenze non presenti nel quaderno;
- il quaderno è esplicito e numerato: il Pupo ragiona su quello;
- la percentuale **non** dipende da cosa dice il Pupo, ma dal confronto tra quaderno e programma:
  anche se il Pupo "barasse" nelle risposte, la percentuale resterebbe onesta.

Da fare (Ruolo 3): una serie di test con domande su cose **non** spiegate, per misurare quanto spesso
il Pupo risponde comunque, e migliorare il prompt di conseguenza.

## Limiti noti del prototipo

- Il giudice è un modello linguistico e può sbagliare: la percentuale va validata su casi reali.
- La storia della chat è limitata agli ultimi messaggi; il quaderno invece è sempre completo.
  Con quaderni molto lunghi servirà una ricerca per argomento (RAG) sulla mente del Pupo.
- Nessuna autenticazione: va aggiunta con l'API.
