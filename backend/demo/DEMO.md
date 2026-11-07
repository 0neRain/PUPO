# Script demo – PUPO (CLI)

Demo end-to-end per la presentazione: Giulia carica una lezione di Analisi 1, insegna al Pupo
in modo volutamente diseguale (bene sui Limiti, vago sulle Derivate) e scopre la propria lacuna
nella barra di preparazione. Stesso esempio usato nello user journey di `docs/PROMPT_TEAM.md`
(sezione 5).

## Prima della presentazione

```bash
cd backend
pip install -e ".[dev]"
cp ../.env.example .env   # poi inserisci una vera OPENAI_API_KEY in backend/.env
```

Fai almeno una **prova a secco completa** (dry run) prima di presentare: i tempi di risposta
del modello non sono istantanei e un problema di rete è meglio scoprirlo prima.

Per ripartire da zero tra una prova e l'altra:

```bash
rm -rf data/giulia/analisi1
```

## 1. Materiale: carica la lezione

```bash
pupo --student giulia --subject analisi1 upload demo/analisi1_lezione.txt
```

## 2. Crea il programma

```bash
pupo --student giulia --subject analisi1 syllabus
```

Dovrebbe ricavare (circa) due argomenti: **Limiti** e **Derivate**, con i rispettivi concetti
chiave. Mostra questo passaggio come "il Pupo ancora non sa niente, solo il riferimento esiste".

## 3. Insegna al Pupo

```bash
pupo --student giulia --subject analisi1 teach
```

Spiegazione 1 — **Limiti**, completa (da scrivere al prompt `Tu (prof) >`):

> Un limite è il valore a cui si avvicina una funzione quando x si avvicina a un certo punto,
> anche se la funzione in quel punto non è definita. Se il limite da sinistra e quello da destra
> sono diversi, il limite non esiste. Una funzione è continua in un punto se il limite coincide
> con il valore della funzione in quel punto.

Il Pupo dovrebbe riformulare e fare una domanda (es. "e se servisse un asintoto?"): rispondi a
braccio, è il punto in cui si vede la personalità del Pupo.

Spiegazione 2 — **Derivate**, volutamente vaga (per mostrare la lacuna dopo):

> La derivata è tipo la velocità con cui cambia una funzione, si usa per trovare i massimi e i
> minimi.

Qui il Pupo dovrebbe notare che manca qualcosa (definizione con il limite, retta tangente,
regole di derivazione) o fare una domanda che Giulia non sa rispondere al volo — è il momento
"ha trovato la lacuna" del pitch.

Esci dalla chat con `/esci`.

## 4. Interroga il Pupo

```bash
pupo --student giulia --subject analisi1 quiz
```

Domande suggerite:

- "Cos'è un limite?"
- "Quando un limite non esiste?"
- "Cos'è la derivata?" — qui il Pupo dovrebbe rispondere in modo incompleto o dire che non gli è
  chiaro, **perché la spiegazione ricevuta era incompleta**: è la riprova che risponde solo dal
  proprio quaderno, non da conoscenza generale.

Esci con `/esci`.

## 5. Percentuale di preparazione

```bash
pupo --student giulia --subject analisi1 progress
```

Risultato atteso (indicativo, dipende dal giudizio del modello): **Limiti** alto (es. 75-100%),
**Derivate** basso (es. 25-50%). È la battuta finale della demo:

> "Il Pupo ha capito bene i limiti, ma sulle derivate Giulia ha ancora da lavorare — e lo sa
> prima dell'esame, non durante."

## Rete di sicurezza

Se durante la presentazione la demo live non dovesse funzionare (rete, API lenta), tieni pronti
screenshot o l'output testuale di una prova a secco riuscita, da mostrare al posto del terminale
live.
