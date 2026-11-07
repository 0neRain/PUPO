# App cross-platform (prossimo passo – Ruoli 2 e 3)

Proposta: **Expo (React Native + TypeScript)**. Con un solo codice si ottiene:
- app **Android** e **iOS** (provabili subito sul telefono con l'app Expo Go);
- versione **web**, usabile da PC nel browser.

Avvio, quando si inizia:

```bash
npx create-expo-app@latest . --template tabs
npx expo start          # poi: "w" per il web, QR code per il telefono
```

## Schermate previste

1. **Home**: i miei Pupi, uno per materia, ciascuno con la sua percentuale totale.
2. **Materiale**: carica file, registra la lezione (trascrizione automatica), consulta il materiale.
3. **Insegna al Pupo**: chat (testo o voce) in cui lo studente spiega e il Pupo fa domande.
4. **Interroga il Pupo**: lo studente fa domande per vedere cosa ha capito.
5. **Preparazione**: barra per argomento (es. "Limiti 80%, Derivate 35%").
6. **Sfide**: duelli amichevoli tra Pupi, senza classifiche pubbliche.

L'app non contiene logica AI: chiama l'API in `backend/api/`.
