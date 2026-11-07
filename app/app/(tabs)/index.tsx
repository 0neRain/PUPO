import { useCallback, useEffect, useState } from 'react';
import { Image, Pressable, ScrollView, StyleSheet, TextInput, View } from 'react-native';
import { router } from 'expo-router';

import { pupoPalette } from '@/constants/Colors';
import { Text } from '@/components/Themed';
import { ApiError, getProgress } from '@/lib/api';
import { stageImageFor } from '@/lib/pupoAssets';
import { useStudent } from '@/lib/student';

const REVIEW_REMINDER_DAYS = 3;

type SubjectStatus = { percent: number; days: number | null } | 'no-syllabus' | 'loading' | 'error';

export default function HomeScreen() {
  const { loading, student, setStudent, subjects, addSubject } = useStudent();
  const [statuses, setStatuses] = useState<Record<string, SubjectStatus>>({});
  const [newSubject, setNewSubject] = useState('');

  const refresh = useCallback(() => {
    for (const subject of subjects) {
      setStatuses((s) => ({ ...s, [subject]: 'loading' }));
      getProgress(subject, student)
        .then((r) =>
          setStatuses((s) => ({
            ...s,
            [subject]: { percent: r.overall_percent, days: r.days_since_last_review },
          }))
        )
        .catch((e) =>
          setStatuses((s) => ({
            ...s,
            [subject]: e instanceof ApiError ? 'no-syllabus' : 'error',
          }))
        );
    }
  }, [subjects, student]);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- avvia il fetch del progresso per materia
    if (!loading) refresh();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [loading, subjects, student]);

  if (loading) return null;

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.heading}>Studente</Text>
      <TextInput
        style={styles.studentInput}
        value={student}
        onChangeText={setStudent}
        placeholder="nome studente"
      />

      <Text style={styles.heading}>Le mie materie</Text>
      {subjects.length === 0 ? <Text style={styles.empty}>Nessuna materia ancora.</Text> : null}
      {subjects.map((subject) => {
        const status = statuses[subject];
        const percent = typeof status === 'object' ? status.percent : 0;
        const needsReview =
          typeof status === 'object' && status.days !== null && status.days >= REVIEW_REMINDER_DAYS;
        return (
          <Pressable
            key={subject}
            style={styles.row}
            onPress={() => router.push({ pathname: '/subject/[subject]', params: { subject } })}>
            <Image source={stageImageFor(percent)} style={styles.rowImage} />
            <View style={styles.rowBody}>
              <Text style={styles.rowTitle}>{subject}</Text>
              {status === 'loading' && <Text style={styles.rowSubtitle}>Carico…</Text>}
              {status === 'no-syllabus' && <Text style={styles.rowSubtitle}>Nessun programma ancora</Text>}
              {status === 'error' && <Text style={styles.rowSubtitle}>Errore nel caricare lo stato</Text>}
              {typeof status === 'object' && <Text style={styles.rowSubtitle}>Preparazione: {status.percent}%</Text>}
              {needsReview && <Text style={styles.reviewBadge}>Ripassa {subject}</Text>}
            </View>
          </Pressable>
        );
      })}

      <Text style={styles.heading}>+ Nuova materia</Text>
      <View style={styles.newRow}>
        <TextInput
          style={styles.newInput}
          value={newSubject}
          onChangeText={setNewSubject}
          placeholder="es. analisi1"
          autoCapitalize="none"
        />
        <Pressable
          style={styles.newButton}
          onPress={() => {
            if (!newSubject.trim()) return;
            addSubject(newSubject.trim());
            setNewSubject('');
          }}>
          <Text style={styles.newButtonText}>Aggiungi</Text>
        </Pressable>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: 16, gap: 10 },
  heading: { fontSize: 16, fontWeight: '700', marginTop: 12 },
  studentInput: {
    borderWidth: 1,
    borderColor: pupoPalette.navy + '33',
    borderRadius: 10,
    padding: 10,
  },
  empty: { opacity: 0.6 },
  row: {
    flexDirection: 'row',
    gap: 12,
    alignItems: 'center',
    padding: 10,
    borderRadius: 14,
    backgroundColor: pupoPalette.purple + '14',
  },
  rowImage: { width: 56, height: 72, resizeMode: 'contain' },
  rowBody: { flex: 1, gap: 2 },
  rowTitle: { fontSize: 16, fontWeight: '700' },
  rowSubtitle: { fontSize: 13, opacity: 0.7 },
  reviewBadge: {
    alignSelf: 'flex-start',
    marginTop: 4,
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 999,
    backgroundColor: pupoPalette.coral,
    color: '#fff',
    fontSize: 12,
    fontWeight: '700',
    overflow: 'hidden',
  },
  newRow: { flexDirection: 'row', gap: 8 },
  newInput: {
    flex: 1,
    borderWidth: 1,
    borderColor: pupoPalette.navy + '33',
    borderRadius: 10,
    padding: 10,
  },
  newButton: {
    backgroundColor: pupoPalette.purple,
    borderRadius: 10,
    paddingHorizontal: 16,
    justifyContent: 'center',
  },
  newButtonText: { color: '#fff', fontWeight: '700' },
});
