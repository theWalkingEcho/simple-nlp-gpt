/**
 * Domain Models - TypeScript Frontend
 * Represents core business entities
 */

export interface Token {
  value: string;
  token_id: number;
  position: number;
  embedding_preview: number[];
}

export interface TextPrediction {
  tokens: Token[];
  confidence_score: number;
  processing_time_ms: number;
  model_name: string;
  created_at: string;
}

export interface GenerateRequest {
  content: string;
  max_tokens?: number;
  language?: string;
}

export interface GenerateResponse {
  success: boolean;
  prediction_id: string;
  data: TextPrediction;
}

export interface PredictionHistoryResponse {
  success: boolean;
  count: number;
  data: TextPrediction[];
}
