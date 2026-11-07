// Stato locale (AsyncStorage): nessun login, solo un nome studente e l'elenco delle materie
// aperte su questo dispositivo. Il backend non ha un concetto di "elenco materie di uno
// studente": è solo una cartella per materia, quindi la lista resta locale.

import { useCallback, useEffect, useState } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';

const STUDENT_KEY = 'pupo:student';
const SUBJECTS_KEY = 'pupo:subjects';
const DEFAULT_STUDENT = 'demo';
const DEFAULT_SUBJECTS = ['analisi1'];

export function useStudent() {
  const [loading, setLoading] = useState(true);
  const [student, setStudentState] = useState(DEFAULT_STUDENT);
  const [subjects, setSubjects] = useState<string[]>(DEFAULT_SUBJECTS);

  useEffect(() => {
    (async () => {
      try {
        const [savedStudent, savedSubjects] = await Promise.all([
          AsyncStorage.getItem(STUDENT_KEY),
          AsyncStorage.getItem(SUBJECTS_KEY),
        ]);
        if (savedStudent) setStudentState(savedStudent);
        if (savedSubjects) setSubjects(JSON.parse(savedSubjects));
      } catch {
        // storage non disponibile: restano i default
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const setStudent = useCallback((name: string) => {
    const trimmed = name.trim() || DEFAULT_STUDENT;
    setStudentState(trimmed);
    AsyncStorage.setItem(STUDENT_KEY, trimmed).catch(() => {});
  }, []);

  const addSubject = useCallback((name: string) => {
    const trimmed = name.trim();
    if (!trimmed) return;
    setSubjects((prev) => {
      if (prev.includes(trimmed)) return prev;
      const next = [...prev, trimmed];
      AsyncStorage.setItem(SUBJECTS_KEY, JSON.stringify(next)).catch(() => {});
      return next;
    });
  }, []);

  return { loading, student, setStudent, subjects, addSubject };
}
