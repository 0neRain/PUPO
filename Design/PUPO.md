# Pupo — scheda del personaggio

Mascotte di un'app universitaria in cui lo studente impara insegnando a uno studente AI.
Pupo ("bambino") nasce senza sapere nulla e impara solo da ciò che lo studente gli spiega.
Personalità: curioso, un po' ingenuo, entusiasta, mai saccente.

## Stile
- Illustrazione vettoriale flat, forme morbide, angoli arrotondati, nessun contorno.
- Ombra piatta in un solo tono: blu notte #1E1B3A al 20% di opacità sul lato destro/basso.
- Proporzioni chibi: testa ≈ 60% dell'altezza, corpo piccolo e tondo, braccine e gambette corte.
- Nessun becco, piuma o forma da uccello. Nessuna scritta o logo sul personaggio.

## Anatomia (coordinate nel viewBox del personaggio "0 -56 200 272")
- Testa: ellisse cx 100, cy 86, rx 74, ry 60.
- Corpo: ellisse cx 100, cy 166, rx 46, ry 38 (fusa con la testa = silhouette a fagiolo).
- Pancia: ellisse chiara cx 100, cy 174, rx 28, ry 22, bianco al 16%.
- Barra di carica sulla pancia: capsula blu notte x 80, y 164, 40×14; riempimento verde acqua (max 34 px).
- Braccine: ellissi 10×17 ai lati del corpo, dietro al corpo. Gambette: capsule 18×26 a x 76 e 106.
- Occhi: ellissi blu notte rx 13, ry 16 a (74, 90) e (126, 90), riflesso bianco r 5 + puntino r 2.2.
- Guance: ellissi rosa #FF8FB3 rx 10, ry 6 a (54, 110) e (146, 110) (sulle varianti non viola: giallo #FFB800).
- Bocca: piccolo arco blu notte, tratto 4.
- Ciuffo (elemento distintivo), giallo #FFB800, tratto 9, estremi arrotondati:
  - Neutro / base / stadi di crescita / varianti / icona: **spirale** `M100 28 C98 10 94 -6 104 -16 C114 -26 128 -16 122 -6 C117 2 106 -2 110 -10`
  - Curioso: punto interrogativo «?» · Confuso: «?» corallo · Illuminato, Felice, Competitivo: punto esclamativo «!» · Triste, Addormentato: ciuffo afflosciato.

## Palette
| Ruolo | Colore |
|---|---|
| Corpo | Viola caldo #7B5CFF |
| Ciuffo, accenti, sfondo icona | Giallo-arancio #FFB800 |
| Barra di carica, successo | Verde acqua #2ED3A0 |
| Confusione, errore | Corallo #FF6B6B |
| Guance (corpo viola) | Rosa #FF8FB3 |
| Occhi, dettagli, ombra | Blu notte #1E1B3A |
| Riflessi | Bianco #FFFFFF |
| Nappa del cappello nell'icona | Vermiglio #F0443A |

## Espressioni
Neutro · Curioso (manina alzata, «?») · Confuso (occhio strizzato, guance e ciuffo corallo) ·
Illuminato (occhi a stella, «!» con raggi) · Felice (braccia in alto, coriandoli) ·
Triste (palpebre cadenti, lacrima) · Competitivo (fascia corallo, sopracciglia decise) ·
Addormentato (occhi chiusi, bolla, luna).

## Stadi di crescita (ciuffo sempre a spirale)
1. 0–25% — piccolo (scala 0.72), sguardo perso, nessun accessorio, barra vuota.
2. 26–60% — scala 0.84, blocchetto per appunti e matita, barra a metà.
3. 61–90% — scala 0.93, postura sicura, sorriso pieno, barra quasi piena.
4. 91–100% — scala 1, braccia in alto, tocco da laurea, stelline, barra piena con alone.

## Varianti per materia (stesso Pupo, corpo e accessorio diversi)
| Materia | Corpo | Accessorio |
|---|---|---|
| Matematica / Analisi | #4A7BF7 | mini righello |
| Storia / Lettere | #D2694A | mini pergamena |
| Biologia / Medicina | #7FAA8B | provetta e foglia |
| Informatica | #7D96B8 | tessera con { } |
| Diritto / Economia | #9A3352 | bilancia |

## Icona app
Solo la testa su quadrato giallo #FFB800 (raggio angoli 22%), senza ombre esterne, centrata.
Tocco da laurea piatto blu notte con bottone e nappa vermiglio #F0443A. Guance rosa, occhi grandi.

## File
- `svg/` — un SVG autonomo per ogni figura (nessun riferimento esterno, colori già risolti).
- `png/` — gli stessi in PNG con sfondo trasparente (icona a 1024×1024).
- `tavole-png/` — le 5 tavole complete del character sheet (2×).
- `sorgenti/` — i file originali delle tavole (HTML con SVG inline).
