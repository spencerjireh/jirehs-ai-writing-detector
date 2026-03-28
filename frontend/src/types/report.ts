export interface TextStats {
  char_count: number;
  word_count: number;
  avg_word_length: number;
  sentence_count: number;
}

export interface LinguisticFactor {
  name: string;
  value: number;
  score_contribution: number;
  explanation: string;
}

export interface PatternDetection {
  category: string;
  occurrences: number;
  score_contribution: number;
  details: string[];
  explanation: string;
}

export interface AnalyzeResponse {
  score: number;
  classification: string;
  stats: TextStats;
  linguistic_factors: LinguisticFactor[];
  pattern_detections: PatternDetection[];
  warnings: string[];
  timestamp: string;
}
