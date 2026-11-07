// Specchio dei dataclass del backend: vedi backend/pupo/comparison.py e reference_db.py.

export interface TopicProgress {
  topic: string;
  percent: number;
  correct: number;
  wrong: number;
  missing: number;
  total: number;
}

export interface ProgressReport {
  overall_percent: number;
  topics: TopicProgress[];
  days_since_last_review: number | null;
}

export interface MaterialDoc {
  id: number;
  source: string;
  kind: 'upload' | 'transcript';
  created_at: string;
  words: number;
}

export interface SyllabusTopic {
  name: string;
  concepts: string[];
}
