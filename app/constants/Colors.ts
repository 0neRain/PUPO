// Palette del Pupo: vedi Design/PUPO.md.
const tintColorLight = '#7B5CFF'; // viola caldo (corpo del Pupo)
const tintColorDark = '#FFB800'; // giallo-arancio (ciuffo)

export const pupoPalette = {
  purple: '#7B5CFF',
  yellow: '#FFB800',
  mint: '#2ED3A0', // barra di carica, successo
  coral: '#FF6B6B', // confusione, errore
  pink: '#FF8FB3',
  navy: '#1E1B3A',
};

export default {
  light: {
    text: '#000',
    background: '#fff',
    tint: tintColorLight,
    tabIconDefault: '#ccc',
    tabIconSelected: tintColorLight,
  },
  dark: {
    text: '#fff',
    background: '#000',
    tint: tintColorDark,
    tabIconDefault: '#ccc',
    tabIconSelected: tintColorDark,
  },
};
