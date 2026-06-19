/**
 * Dependency Injection Container - Frontend
 * Composition Root for managing dependencies
 */
import { TextGenerationService, ITextGenerationService } from '../infrastructure/services/textGenerationService';
import { GenerateTextUseCase, GetPredictionHistoryUseCase } from './useCases';

export class FrontendDIContainer {
  private textGenerationService: ITextGenerationService;
  private generateTextUseCase: GenerateTextUseCase;
  private getPredictionHistoryUseCase: GetPredictionHistoryUseCase;

  constructor(apiBaseURL?: string) {
    // Initialize services
    this.textGenerationService = new TextGenerationService(apiBaseURL);

    // Initialize use cases
    this.generateTextUseCase = new GenerateTextUseCase(this.textGenerationService);
    this.getPredictionHistoryUseCase = new GetPredictionHistoryUseCase(this.textGenerationService);
  }

  getGenerateTextUseCase(): GenerateTextUseCase {
    return this.generateTextUseCase;
  }

  getGetPredictionHistoryUseCase(): GetPredictionHistoryUseCase {
    return this.getPredictionHistoryUseCase;
  }

  getTextGenerationService(): ITextGenerationService {
    return this.textGenerationService;
  }
}

// Global singleton
let diContainer: FrontendDIContainer;

export function initializeDIContainer(apiBaseURL?: string): FrontendDIContainer {
  diContainer = new FrontendDIContainer(apiBaseURL);
  return diContainer;
}

export function getDIContainer(): FrontendDIContainer {
  if (!diContainer) {
    diContainer = new FrontendDIContainer();
  }
  return diContainer;
}
