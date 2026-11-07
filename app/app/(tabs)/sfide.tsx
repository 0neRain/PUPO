import { Image, ScrollView, StyleSheet, View } from 'react-native';

import { pupoPalette } from '@/constants/Colors';
import { Text } from '@/components/Themed';
import { expressions } from '@/lib/pupoAssets';

// Mock statico: solo per mostrare l'idea nel pitch, nessuna logica reale.
const MOCK_CHALLENGES = [
  { opponent: 'Marco', subject: 'Limiti (Analisi 1)', you: 67, them: 54 },
  { opponent: 'Sara', subject: 'Derivate (Analisi 1)', you: 20, them: 71 },
  { opponent: 'Luca', subject: 'Basi di dati', you: 88, them: 90 },
];

export default function SfideScreen() {
  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Image source={expressions.felice} style={styles.hero} />
      <Text style={styles.title}>Sfide amichevoli</Text>
      <Text style={styles.subtitle}>
        Duelli tra Pupi sullo stesso argomento, senza classifiche pubbliche: ci si confronta,
        non si gareggia per il voto.
      </Text>

      {MOCK_CHALLENGES.map((c) => (
        <View key={c.opponent} style={styles.card}>
          <Text style={styles.cardTitle}>Tu vs {c.opponent}</Text>
          <Text style={styles.cardSubject}>{c.subject}</Text>
          <Text style={styles.cardScore}>
            Tu {c.you}% · {c.opponent} {c.them}%
          </Text>
        </View>
      ))}

      <View style={[styles.button, styles.buttonDisabled]}>
        <Text style={styles.buttonText}>Sfida amichevole — prossimamente</Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: 16, gap: 12, alignItems: 'center' },
  hero: { width: 100, height: 128, resizeMode: 'contain' },
  title: { fontSize: 20, fontWeight: '800' },
  subtitle: { textAlign: 'center', opacity: 0.7, marginBottom: 8 },
  card: {
    width: '100%',
    padding: 14,
    borderRadius: 14,
    backgroundColor: pupoPalette.yellow + '18',
    gap: 4,
  },
  cardTitle: { fontWeight: '700' },
  cardSubject: { opacity: 0.7, fontSize: 13 },
  cardScore: { fontWeight: '600' },
  button: {
    marginTop: 12,
    paddingVertical: 12,
    paddingHorizontal: 20,
    borderRadius: 10,
  },
  buttonDisabled: { backgroundColor: pupoPalette.navy + '22' },
  buttonText: { fontWeight: '700', opacity: 0.6 },
});
