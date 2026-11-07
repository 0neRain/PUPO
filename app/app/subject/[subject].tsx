import { useCallback, useEffect, useState } from 'react';
import { Image, Pressable, ScrollView, StyleSheet, TextInput, View } from 'react-native';
import { Stack, useLocalSearchParams } from 'expo-router';

import { ProgressBar } from '@/components/ProgressBar';
import { Chat } from '@/components/Chat';
import { pupoPalette } from '@/constants/Colors';
import { Text } from '@/components/Themed';
import {
  addMaterialText,
  ApiError,
  createSyllabus,
  getProgress,
  listMaterial,
  quiz,
  teach,
} from '@/lib/api';
import { stageImageFor } from '@/lib/pupoAssets';
import { useStudent } from '@/lib/student';
import type { MaterialDoc, ProgressReport, SyllabusTopic } from '@/lib/types';

const REVIEW_REMINDER_DAYS = 3;
type Section = 'materiale' | 'insegna' | 'interroga' | 'preparazione';

export default function SubjectScreen() {
  const { subject } = useLocalSearchParams<{ subject: string }>();
  const { student, loading } = useStudent();
  const [section, setSection] = useState<Section>('materiale');

  if (loading || !subject) return null;

  return (
    <>
      <Stack.Screen options={{ title: subject }} />
      <View style={styles.tabs}>
        {(['materiale', 'insegna', 'interroga', 'preparazione'] as Section[]).map((s) => (
          <Pressable
            key={s}
            style={[styles.tabButton, section === s && styles.tabButtonActive]}
            onPress={() => setSection(s)}>
            <Text style={[styles.tabText, section === s && styles.tabTextActive]}>
              {sectionLabel(s)}
            </Text>
          </Pressable>
        ))}
      </View>
      <View style={styles.content}>
        {section === 'materiale' && <MaterialeSection subject={subject} student={student} />}
        {section === 'insegna' && <InsegnaSection subject={subject} student={student} />}
        {section === 'interroga' && <InterrogaSection subject={subject} student={student} />}
        {section === 'preparazione' && <PreparazioneSection subject={subject} student={student} />}
      </View>
    </>
  );
}

function sectionLabel(s: Section) {
  return { materiale: 'Materiale', insegna: 'Insegna', interroga: 'Interroga', preparazione: 'Preparazione' }[s];
}

function MaterialeSection({ subject, student }: { subject: string; student: string }) {
  const [text, setText] = useState('');
  const [source, setSource] = useState('');
  const [docs, setDocs] = useState<MaterialDoc[] | null>(null);
  const [topics, setTopics] = useState<SyllabusTopic[] | null>(null);
  const [status, setStatus] = useState<string | null>(null);

  const refresh = useCallback(() => {
    listMaterial(subject, student).then(setDocs).catch(() => setDocs([]));
  }, [subject, student]);

  useEffect(refresh, [refresh]);

  return (
    <ScrollView contentContainerStyle={styles.section}>
      <Text style={styles.label}>Incolla appunti o sbobinatura</Text>
      <TextInput
        style={styles.textarea}
        value={text}
        onChangeText={setText}
        multiline
        placeholder="Testo della lezione…"
      />
      <TextInput
        style={styles.input}
        value={source}
        onChangeText={setSource}
        placeholder="nome del documento (es. lezione1.txt)"
      />
      <Pressable
        style={styles.button}
        onPress={async () => {
          if (!text.trim()) return;
          setStatus('Carico…');
          try {
            await addMaterialText(subject, student, text, source || 'appunti.txt');
            setText('');
            setSource('');
            setStatus('Caricato.');
            refresh();
          } catch (e) {
            setStatus(e instanceof Error ? e.message : 'Errore');
          }
        }}>
        <Text style={styles.buttonText}>Carica</Text>
      </Pressable>

      <Text style={styles.label}>Materiale già caricato</Text>
      {(docs ?? []).length === 0 ? <Text style={styles.muted}>Niente ancora.</Text> : null}
      {(docs ?? []).map((d) => (
        <Text key={d.id} style={styles.docRow}>
          {d.source} — {d.kind}, {d.words} parole
        </Text>
      ))}

      <Pressable
        style={styles.button}
        onPress={async () => {
          setStatus('Creo il programma…');
          try {
            const t = await createSyllabus(subject, student);
            setTopics(t);
            setStatus(null);
          } catch (e) {
            setStatus(e instanceof Error ? e.message : 'Errore');
          }
        }}>
        <Text style={styles.buttonText}>Crea programma</Text>
      </Pressable>
      {status ? <Text style={styles.muted}>{status}</Text> : null}
      {topics ? (
        <Text style={styles.muted}>
          Argomenti trovati: {topics.map((t) => `${t.name} (${t.concepts.length})`).join(', ')}
        </Text>
      ) : null}
    </ScrollView>
  );
}

function InsegnaSection({ subject, student }: { subject: string; student: string }) {
  return (
    <View style={styles.section}>
      <Text style={styles.muted}>Spiega l&apos;argomento al Pupo con parole tue.</Text>
      <Chat placeholder="Spiega qui…" onSend={(text) => teach(subject, student, text)} />
    </View>
  );
}

function InterrogaSection({ subject, student }: { subject: string; student: string }) {
  return (
    <View style={styles.section}>
      <Text style={styles.muted}>Fai domande per vedere cosa ha capito il Pupo.</Text>
      <Chat placeholder="Fai una domanda…" onSend={(text) => quiz(subject, student, text)} />
    </View>
  );
}

function PreparazioneSection({ subject, student }: { subject: string; student: string }) {
  const [report, setReport] = useState<ProgressReport | null>(null);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(() => {
    setError(null);
    getProgress(subject, student)
      .then(setReport)
      .catch((e) => setError(e instanceof ApiError ? e.message : 'Errore'));
  }, [subject, student]);

  // eslint-disable-next-line react-hooks/set-state-in-effect -- avvia il fetch del progresso al montaggio
  useEffect(refresh, [refresh]);

  const needsReview =
    report?.days_since_last_review !== null &&
    report?.days_since_last_review !== undefined &&
    report.days_since_last_review >= REVIEW_REMINDER_DAYS;

  return (
    <ScrollView contentContainerStyle={styles.section}>
      {report && <Image source={stageImageFor(report.overall_percent)} style={styles.stageImage} />}
      {needsReview && (
        <Text style={styles.reviewBanner}>
          Non ripassi questa materia da {report?.days_since_last_review} giorni.
        </Text>
      )}
      {error && <Text style={styles.muted}>{error}</Text>}
      {report && (
        <>
          <ProgressBar percent={report.overall_percent} label="Totale" />
          {report.topics.map((t) => (
            <ProgressBar key={t.topic} percent={t.percent} label={t.topic} />
          ))}
        </>
      )}
      <Pressable style={styles.button} onPress={refresh}>
        <Text style={styles.buttonText}>Aggiorna</Text>
      </Pressable>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  tabs: { flexDirection: 'row', flexWrap: 'wrap', gap: 6, padding: 12 },
  tabButton: {
    paddingVertical: 6,
    paddingHorizontal: 12,
    borderRadius: 999,
    backgroundColor: pupoPalette.navy + '14',
  },
  tabButtonActive: { backgroundColor: pupoPalette.purple },
  tabText: { fontSize: 13, fontWeight: '600' },
  tabTextActive: { color: '#fff' },
  content: { flex: 1, paddingHorizontal: 12 },
  section: { gap: 10, paddingBottom: 24 },
  label: { fontWeight: '700', marginTop: 8 },
  muted: { opacity: 0.65, fontSize: 13 },
  docRow: { fontSize: 13 },
  textarea: {
    borderWidth: 1,
    borderColor: pupoPalette.navy + '33',
    borderRadius: 10,
    padding: 10,
    minHeight: 100,
  },
  input: {
    borderWidth: 1,
    borderColor: pupoPalette.navy + '33',
    borderRadius: 10,
    padding: 10,
  },
  button: {
    alignSelf: 'flex-start',
    backgroundColor: pupoPalette.purple,
    borderRadius: 10,
    paddingHorizontal: 16,
    paddingVertical: 10,
  },
  buttonText: { color: '#fff', fontWeight: '700' },
  stageImage: { width: 90, height: 115, resizeMode: 'contain', alignSelf: 'center' },
  reviewBanner: {
    backgroundColor: pupoPalette.coral,
    color: '#fff',
    fontWeight: '700',
    padding: 10,
    borderRadius: 10,
    textAlign: 'center',
  },
});
