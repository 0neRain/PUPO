// Client HTTP verso backend/api/. Niente logica AI qui: solo chiamate all'API.

import type { MaterialDoc, ProgressReport, SyllabusTopic } from './types';

const API_URL = process.env.EXPO_PUBLIC_API_URL ?? 'http://localhost:8000';

class ApiError extends Error {}

async function request<T>(
  path: string,
  student: string,
  init: RequestInit = {}
): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: { ...init.headers, 'X-Student': student },
  });
  if (!res.ok) {
    const body = await res.json().catch(() => null);
    throw new ApiError(body?.detail ?? `Errore ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export async function addMaterialText(subject: string, student: string, text: string, source: string) {
  const form = new FormData();
  form.append('text', text);
  form.append('source', source);
  return request<{ id: number; source: string }>(`/subjects/${subject}/material`, student, {
    method: 'POST',
    body: form,
  });
}

export async function listMaterial(subject: string, student: string) {
  const { documents } = await request<{ documents: MaterialDoc[] }>(
    `/subjects/${subject}/material`,
    student
  );
  return documents;
}

export async function createSyllabus(subject: string, student: string) {
  const { topics } = await request<{ topics: SyllabusTopic[] }>(`/subjects/${subject}/syllabus`, student, {
    method: 'POST',
  });
  return topics;
}

export async function teach(subject: string, student: string, explanation: string) {
  const { reply } = await request<{ reply: string }>(`/subjects/${subject}/teach`, student, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ explanation }),
  });
  return reply;
}

export async function quiz(subject: string, student: string, question: string) {
  const { reply } = await request<{ reply: string }>(`/subjects/${subject}/quiz`, student, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question }),
  });
  return reply;
}

export async function getProgress(subject: string, student: string) {
  return request<ProgressReport>(`/subjects/${subject}/progress`, student);
}

export { ApiError };
