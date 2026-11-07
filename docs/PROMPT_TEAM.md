# PROMPT DI PROGETTO – PUPO (Reply Student Tech Clash · AI on Campus)

> Istruzioni per Claude: questo documento contiene il contesto completo di un progetto di gruppo.
> Leggilo tutto prima di rispondere. Siamo un team di studenti che lavora in parallelo, ognuno
> con il proprio Claude: tutti partono da questo stesso documento, quindi è fondamentale che tu
> **rispetti le decisioni già prese** (sezione 4) e non le cambi di tua iniziativa.
> Se pensi che una decisione sia sbagliata o rischiosa, dillo esplicitamente come proposta
> ("PROPOSTA DI MODIFICA: …"), ma continua a lavorare rispettandola finché il team non decide.
> Rispondi in italiano. I materiali finali per la challenge potranno essere in inglese se il team lo chiede.

---

## 1. CONTESTO DELLA COMPETIZIONE

- Competizione: **Reply Student Tech Clash 2026 – "AI on Campus"**, organizzata da Reply.
- Tema: come l'AI sta cambiando il modo di imparare, insegnare e valutare all'università.
- La challenge è divisa in livelli: **Level 1 · Design** (su cui lavoriamo ora), **Level 2 · Build**, **Level 3 · Extra**.
  C'è anche una pagina **Evaluation** con i criteri di valutazione: [INCOLLARE QUI I CRITERI DAL SITO].
- Tre direzioni possibili:
  1. **Teaching**: capire cosa gli studenti non hanno capito, adattare spiegazioni e materiali.
  2. **Learning**: capire gli errori, costruire modelli mentali solidi, sapere cosa si sa davvero
     (non solo scorrere il materiale più velocemente). L'AI può supportare questo processo o cortocircuitarlo.
  3. **Assessment**: rivelare cosa sai davvero, non cosa puoi trovare o generare.
     Esempio ufficiale: "un readiness check prima dell'esame che ti dice quali lacune contano davvero".
- **La nostra direzione: LEARNING**, con un aspetto di autovalutazione vicino ad ASSESSMENT.

Scadenze (da completare):
- Consegna Level 1: [DATA]
- Allineamento del team: [DATA/ORA]
- Pitch/presentazione: [DATA]

---

## 2. L'IDEA IN UNA FRASE

**PUPO è un agente AI che fa lo studente: non sa niente e impara solo da quello che gli spieghi tu.
Spiegandogli la materia, lo studente impara davvero e scopre, argomento per argomento, quanto è preparato.**

Principio di base: *"So di aver capito un argomento quando so spiegarlo a qualcun altro"*
(learning by teaching, effetto protégé, tecnica Feynman).
Ribaltamento chiave: di solito l'AI dà le risposte; **PUPO le riceve**.

---

## 3. DESCRIZIONE COMPLETA

### 3.1 Un Pupo per ogni materia
Ogni studente ha un Pupo per ogni corso che segue. Il Pupo nasce "vuoto" (pupo = bambino).

### 3.2 Architettura: due database separati
1. **Database di riferimento (conoscenza a priori)**
   - Lo costruisce lo studente caricando:
     - registrazioni delle lezioni, che il Pupo trascrive automaticamente;
     - sbobinature;
     - altro materiale scelto dallo studente (appunti, slide, dispense, programma d'esame).
   - **Sta allo studente caricare materiale corretto e pertinente**: la qualità del riferimento
     determina l'affidabilità della percentuale.
   - **Il Pupo NON può estrarre dati da questo database**: non lo legge per rispondere, non lo usa
     per suggerire, non lo cita, non lo usa per fare domande.
   - Il suo **unico uso** è fare da metro di paragone per calcolare la percentuale di preparazione.
   - Soluzione tecnica proposta: il confronto lo fa un **modulo separato**, che restituisce al Pupo
     e allo studente **solo le percentuali**, mai i contenuti.
2. **Database di apprendimento (la "mente" del Pupo)**
   - All'inizio è vuoto.
   - Si riempie **solo** con ciò che lo studente spiega al Pupo.
   - Se la spiegazione è sbagliata, il Pupo impara una cosa sbagliata.
   - È l'**unica** fonte che il Pupo usa per ragionare, rispondere e fare domande.
3. **Percentuale di preparazione**
   - È il risultato del confronto tra i due database: quanta parte del riferimento il Pupo
     ha imparato, e quanto correttamente.
   - Non conta la quantità: un argomento è "imparato" solo se è **coperto E spiegato correttamente**.
   - È mostrata **per argomento** (es. "Limiti 80%, Derivate 35%"), così lo studente sa dove intervenire,
     senza che il Pupo riveli il contenuto mancante.

### 3.3 L'app ha due sezioni
**A) "Materiale": lo studente costruisce il riferimento**
- Durante la lezione il Pupo può registrare l'audio e trascrivere ciò che dice il professore.
- Lo studente carica sbobinature e altro materiale.
- Qui lo studente consulta e organizza il proprio materiale di studio.
- Tutto finisce nel database di riferimento, **non** nella mente del Pupo.

**B) "Insegna al Pupo": lo studente fa il professore**
- Lo studente spiega gli argomenti al Pupo (voce o testo).
- Il Pupo si comporta come uno studente vero: chiede "perché?", "e se invece…?", chiede esempi,
  si confonde davanti a spiegazioni vaghe o contraddittorie e fa errori plausibili,
  **basandosi solo su ciò che ha imparato**.
- Lo studente può interrogare il Pupo per ripassare e vedere cosa ha "capito".
- Una barra di preparazione per argomento mostra i progressi.

### 3.4 Gioco e sfida
- **Sfide amichevoli** tra Pupi (quiz, duelli tra compagni di corso) per rendere lo studio coinvolgente.
- Niente classifiche pubbliche competitive (reintrodurrebbero un incentivo a barare per fare bella figura).

### 3.5 Perché non ha senso imbrogliare
- **Il Pupo non dà punti all'esame**: nessun voto dipende da lui. Il professore non è coinvolto nella valutazione.
- Se lo studente legge al Pupo gli appunti o incolla testo generato da un'altra AI, il Pupo
  arriva al 100% ma lo studente resta al 10%: **si inganna da solo** e lo scopre all'esame.
- Caricare materiale incompleto o inutile nel riferimento produce solo una percentuale falsa.
- Frase per il pitch: *"Un Pupo al 100% con uno studente al 10% non serve a nessuno."*

### 3.6 Perché funziona
- Motivazione: gamification e sfida, lo studio diventa un gioco.
- Apprendimento profondo: per spiegare bisogna capire, non memorizzare.
- Feedback onesto: le domande del Pupo e la percentuale per argomento mostrano subito le lacune.
- Usa l'AI per rafforzare il pensiero dello studente, non per sostituirlo.
- Sviluppo futuro possibile: statistiche **anonime e aggregate** per il professore su quali argomenti
  la classe spiega peggio.

### 3.7 Rischi da affrontare
- **Separazione dei database**: va garantita tecnicamente (modulo di confronto separato).
- **Affidabilità della percentuale**: dipende dalla qualità del materiale e dalla robustezza
  della valutazione di "spiegato correttamente".
- **Registrazione delle lezioni**: consenso del professore, GDPR (voci di altri studenti in aula),
  diritti sul materiale didattico.
- **Privacy**: materiale e conversazioni restano dello studente.

---

## 4. DECISIONI GIÀ PRESE (NON CAMBIARE)

1. Direzione: **Learning** (con aggancio ad Assessment come autovalutazione).
2. Il Pupo **non** dà punti o bonus all'esame. Nessun coinvolgimento nel voto.
3. Due database separati; il Pupo **non può leggere** il database di riferimento, solo il modulo di
   confronto lo usa, e restituisce solo percentuali.
4. Il database di riferimento lo riempie **lo studente** (registrazioni trascritte, sbobinature, materiale caricato).
5. La mente del Pupo si riempie **solo** con le spiegazioni dello studente.
6. Percentuale di preparazione **per argomento**, basata su copertura **e** correttezza.
7. App con due sezioni: **Materiale** e **Insegna al Pupo**.
8. Sfide amichevoli sì, classifiche pubbliche competitive no.

## 5. DECISIONI APERTE (da chiudere insieme)

- **Acronimo di PUPO.** Shortlist:
  - Italiano: *Pupillo Universitario Pronto all'Orale*
  - Inglese: *Prove Understanding by Passing On*, *Pupil Until Proven Otherwise*,
    *Preparation Unveiled by Pupil Output*, *Pupil Under Professor's Oversight*
- Lingua dei materiali finali (italiano o inglese).
- Formato della consegna Level 1 (slide, documento, video?): verificare sul sito.
- Come calcolare esattamente la percentuale (vedi ruolo 3).

---

## 6. STRUTTURA DELLA PROPOSTA LEVEL 1 (riferimento comune)

Ogni sezione ha un responsabile (vedi sezione 7). Circa 8–9 slide se si presenta.

1. **Titolo e frase d'apertura**: nome, acronimo, una frase. [Ruolo 4]
2. **Il problema**: gli studenti credono di aver capito perché rileggono o perché l'AI riassume, e scoprono
   le lacune all'esame; l'AI generativa cortocircuita l'apprendimento. Domanda d'apertura:
   *"Come fai a sapere se hai davvero capito un argomento?"* [Ruolo 1]
3. **L'intuizione e la base scientifica**: Feynman, effetto protégé, learning by teaching
   (es. Chase et al. 2009; Fiorella & Mayer: da verificare). [Ruolo 1]
4. **La soluzione PUPO** in 3 punti. [Ruolo 2]
5. **User journey**: "Giulia, Analisi 1": lezione registrata → spiega i limiti al Pupo → il Pupo chiede
   "perché qui non posso sostituire direttamente?" → Giulia non sa rispondere, ha trovato la lacuna →
   barra: Limiti 80%, Derivate 35% → sfida un'amica. [Ruolo 2]
6. **Architettura**: schema a blocchi dei due database e del modulo di confronto. [Ruolo 3]
7. **Perché è diverso**: tabella di confronto con un chatbot tutor (ChatGPT) e con le app di flashcard
   (chi spiega, misura la comprensione, si può barare). [Ruolo 1]
8. **Perché non conviene imbrogliare.** [Ruolo 4]
9. **Rischi e soluzioni** (privacy, GDPR, affidabilità, separazione). [Ruolo 4 con Ruolo 3]
10. **Impatto e metriche**: per lo studente e per il corso; metriche di un pilota (voti contro gruppo di
    controllo, tempo di studio attivo, differenza tra percentuale prevista e voto reale). [Ruolo 1]
11. **Prossimi passi / anticipo del Level 2 Build**: MVP su una materia. [Ruolo 3]

---

## 7. DIVISIONE DEL LAVORO (4 ruoli)

Assegnazione: Ruolo 1 = [NOME] · Ruolo 2 = [NOME] · Ruolo 3 = [NOME] · Ruolo 4 = [NOME]

> Claude: chiedi al tuo utente quale ruolo ha, poi concentrati sui suoi compiti.
> Puoi aiutare anche su altro, ma senza contraddire le decisioni della sezione 4.

### RUOLO 1 – Ricerca e problema
Obiettivo: dimostrare che il problema è reale e che la soluzione ha basi solide.
Compiti:
- Trovare **2–4 studi reali e verificabili** sul learning by teaching / effetto protégé / tecnica Feynman,
  con autore, anno, risultato in una frase e link. **Mai inventare citazioni o numeri.**
- Trovare dati sull'uso dell'AI generativa da parte degli studenti e sui rischi per l'apprendimento
  (fonti recenti, 2024–2026).
- Analisi dei competitor: app e strumenti esistenti simili (es. tutor AI, app "teach the AI",
  flashcard come Anki/Quizlet). Per ognuno: cosa fa, cosa gli manca rispetto a PUPO.
- Scrivere le sezioni 2, 3, 7 e 10 della proposta.
Consegne:
- Documento "Ricerca" con fonti e link.
- Tabella dei competitor.
- Testo delle sezioni 2, 3, 7 e 10 (max ~150 parole ciascuna).

### RUOLO 2 – Prodotto ed esperienza utente
Obiettivo: far "vedere" come si usa PUPO.
Compiti:
- Scrivere lo **user journey** completo di Giulia (sezione 5) con dialoghi realistici Giulia ↔ Pupo.
- Definire la **personalità del Pupo**: come parla, come fa domande, come si confonde, come sbaglia
  in modo plausibile, come reagisce quando gli si insegna una cosa sbagliata.
- Progettare le schermate (wireframe a parole o bozza visiva): home con i Pupi per materia,
  sezione Materiale, sezione Insegna al Pupo, barra di preparazione per argomento, sfida tra Pupi.
- Progettare le **sfide amichevoli**: 2–3 meccaniche di gioco concrete, senza classifiche pubbliche.
- Scrivere le sezioni 4 e 5 della proposta.
Consegne:
- 3 dialoghi di esempio (spiegazione corretta, vaga, sbagliata).
- Descrizione o bozza delle 5 schermate principali.
- Testo delle sezioni 4 e 5.

### RUOLO 3 – Architettura tecnica e prototipo
Obiettivo: dimostrare che è realizzabile e preparare il Level 2 Build.
Compiti:
- Disegnare l'**architettura**: trascrizione (speech-to-text), database di riferimento,
  database di apprendimento, modulo di confronto, agente Pupo (LLM con regole).
- Definire **come garantire la separazione**: il Pupo ha accesso solo al database di apprendimento;
  il modulo di confronto è un componente isolato che restituisce solo numeri.
- Proporre **come calcolare la percentuale**: estrazione degli argomenti dal riferimento
  (lista di argomenti e concetti chiave), verifica di copertura e correttezza delle spiegazioni,
  formula per argomento e totale. Considerare i limiti (un LLM che giudica la correttezza può sbagliare).
- Scrivere un **system prompt di prima versione del Pupo** (comportamento da studente, divieto di usare
  conoscenze non insegnate, stile delle domande).
- Proporre lo **stack** per un MVP e il perimetro del Level 2 (una materia, chat, caricamento materiale,
  barra di preparazione).
- Scrivere le sezioni 6 e 11 della proposta; supportare la 9.
Consegne:
- Schema architetturale (anche testuale, a blocchi).
- Formula o algoritmo della percentuale.
- System prompt del Pupo v1.
- Piano MVP per il Level 2.

**Nota tecnica importante:** un LLM ha già conoscenze generali dal suo addestramento, quindi
"partire vuoto" non è automatico. Il Ruolo 3 deve proporre come gestirlo (es. istruzioni rigide nel
system prompt, il Pupo risponde solo citando ciò che è nel database di apprendimento, test di
"non deve sapere ciò che non gli è stato insegnato"). Questo è il rischio tecnico n.1 da affrontare nel pitch.

### RUOLO 4 – Pitch, presentazione, etica
Obiettivo: rendere l'idea memorabile e a prova di obiezioni.
Compiti:
- Proporre l'**acronimo finale** (partendo dalla shortlist) e la frase d'apertura.
- Costruire lo **storytelling** del pitch (2–3 minuti): domanda d'apertura → problema → intuizione →
  demo/user journey → perché non si bara → impatto → chiusura.
- Preparare le **risposte alle domande dei giudici** (almeno 8), es.: "E se lo studente bara?",
  "In cosa è diverso da ChatGPT?", "Come sapete che la percentuale è affidabile?",
  "E la privacy delle registrazioni?", "Perché uno studente dovrebbe usarlo?",
  "Come lo misurereste?", "Cosa serve al professore?", "Come gestite le conoscenze già presenti nell'LLM?".
- Scrivere le sezioni 1, 8 e 9 della proposta (rischi: GDPR, consenso alle registrazioni, diritti
  sul materiale, privacy delle conversazioni).
- Montare la presentazione finale con i testi di tutti, controllando che tono e terminologia siano coerenti.
Consegne:
- Acronimo e frase d'apertura.
- Script del pitch.
- FAQ per i giudici.
- Presentazione finale.

---

## 8. REGOLE COMUNI PER TUTTI I CLAUDE

- **Terminologia fissa** (usarla sempre uguale):
  - "Pupo" (l'agente), "database di riferimento", "database di apprendimento" (o "mente del Pupo"),
    "modulo di confronto", "percentuale di preparazione", sezione "Materiale", sezione "Insegna al Pupo",
    "sfide amichevoli".
- **Non reintrodurre** bonus d'esame, accesso del Pupo al riferimento, classifiche pubbliche.
- **Non inventare** fonti, studi, statistiche o funzionalità della challenge. Se non sei sicuro, scrivi
  [DA VERIFICARE].
- Testi della proposta: chiari, concreti, senza gergo inutile; ogni sezione max ~150 parole salvo
  diversa indicazione.
- Alla fine di ogni consegna aggiungi un breve blocco:
  - **Fatto:** …
  - **Dubbi / proposte di modifica:** …
  - **Serve da altri ruoli:** …
  così il team può unire il lavoro facilmente.

---

## 9. PRIMO MESSAGGIO CONSIGLIATO

Dopo aver letto questo documento, rispondi al tuo utente con:
1. un riassunto dell'idea in 3 righe (per verificare di averla capita);
2. la domanda "Quale ruolo hai (1, 2, 3 o 4)?";
3. una volta saputo il ruolo, il piano dei suoi compiti in ordine di priorità.
