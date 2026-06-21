/**
 * API Service - Infrastructure Layer
 * Handles HTTP communication with backend
 * Following Dependency Inversion - depends on abstractions
 */
import axios, { AxiosInstance } from 'axios';
import { GenerateRequest, GenerateResponse, PredictionHistoryResponse, TextPrediction } from '../../domain/models';

export interface ITextGenerationService {
  generateText(request: GenerateRequest): Promise<GenerateResponse>;
  getPrediction(predictionId: string): Promise<TextPrediction>;
  getPredictionHistory(limit?: number): Promise<TextPrediction[]>;
}

export class TextGenerationService implements ITextGenerationService {
  private api: AxiosInstance;

  constructor(baseURL: string = 'http://localhost:5000/api/v1') {
    this.api = axios.create({
      baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  async generateText(request: GenerateRequest): Promise<GenerateResponse> {
    const response = await this.api.post<GenerateResponse>('/generate', {
      content: request.content,
      max_tokens: request.max_tokens || 50,
      language: request.language || 'en',
    });
    return response.data;
  }

  async getPrediction(predictionId: string): Promise<TextPrediction> {
    const response = await this.api.get<{ data: TextPrediction }>(`/predictions/${predictionId}`);
    return response.data.data;
  }

  async getPredictionHistory(limit: number = 10): Promise<TextPrediction[]> {
    const response = await this.api.get<PredictionHistoryResponse>('/predictions', {
      params: { limit },
    });
    return response.data.data;
  }
}
