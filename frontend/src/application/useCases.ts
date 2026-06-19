/**
 * Use Case - Application Layer
 * Business logic for text generation
 * Single Responsibility - handles one use case
 */
import { ITextGenerationService } from '../../infrastructure/services/textGenerationService';
import { GenerateRequest, TextPrediction, GenerateResponse } from '../../domain/models';

export interface IGenerateTextUseCase {
  execute(request: GenerateRequest): Promise<{ prediction: TextPrediction; predictionId: string }>;
}

export class GenerateTextUseCase implements IGenerateTextUseCase {
  constructor(private textGenerationService: ITextGenerationService) {}

  async execute(request: GenerateRequest): Promise<{ prediction: TextPrediction; predictionId: string }> {
    if (!request.content || request.content.trim().length === 0) {
      throw new Error('Content cannot be empty');
    }

    if (request.content.length > 5000) {
      throw new Error('Content exceeds maximum length of 5000 characters');
    }

    const response = await this.textGenerationService.generateText(request);
    return {
      prediction: response.data,
      predictionId: response.prediction_id,
    };
  }
}

export interface IGetPredictionHistoryUseCase {
  execute(limit?: number): Promise<TextPrediction[]>;
}

export class GetPredictionHistoryUseCase implements IGetPredictionHistoryUseCase {
  constructor(private textGenerationService: ITextGenerationService) {}

  async execute(limit: number = 10): Promise<TextPrediction[]> {
    if (limit < 1 || limit > 100) {
      throw new Error('Limit must be between 1 and 100');
    }
    return this.textGenerationService.getPredictionHistory(limit);
  }
}
