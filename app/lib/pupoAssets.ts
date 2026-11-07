// Mappa percentuale/materia -> illustrazione del Pupo. Vedi Design/PUPO.md per la scheda.

export function stageImageFor(percent: number) {
  if (percent <= 25) return require('../assets/images/pupo/crescita/pupo-appena-nato-0-25.png');
  if (percent <= 60) return require('../assets/images/pupo/crescita/pupo-che-prende-appunti-26-60.png');
  if (percent <= 90) return require('../assets/images/pupo/crescita/pupo-sicuro-di-se-61-90.png');
  return require('../assets/images/pupo/crescita/pupo-pronto-per-l-esame-91-100.png');
}

const SUBJECT_VARIANTS: { match: RegExp; image: ReturnType<typeof require> }[] = [
  { match: /mate|analisi|algebra|geometri/i, image: require('../assets/images/pupo/materie/pupo-matematica-blu-con-righello.png') },
  { match: /stori|letter|filosofi/i, image: require('../assets/images/pupo/materie/pupo-storia-terracotta-con-pergamena.png') },
  { match: /biolog|medicin|chimic/i, image: require('../assets/images/pupo/materie/pupo-biologia-verde-salvia-con-provetta.png') },
  { match: /informatic|program|algoritm/i, image: require('../assets/images/pupo/materie/pupo-informatica-grigio-azzurro-con-parentesi-graffe.png') },
  { match: /diritt|econom|giurisprud/i, image: require('../assets/images/pupo/materie/pupo-diritto-bordeaux-con-bilancia.png') },
];

export function subjectImageFor(subject: string) {
  const found = SUBJECT_VARIANTS.find((v) => v.match.test(subject));
  return found ? found.image : require('../assets/images/pupo/espressioni/pupo-neutro.png');
}

export const expressions = {
  curioso: require('../assets/images/pupo/espressioni/pupo-curioso.png'),
  confuso: require('../assets/images/pupo/espressioni/pupo-confuso.png'),
  felice: require('../assets/images/pupo/espressioni/pupo-felice-che-festeggia.png'),
  neutro: require('../assets/images/pupo/espressioni/pupo-neutro.png'),
};
