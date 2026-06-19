/**
 * Custom React Hook for Text Generation
 * Presentation Layer - handles UI state management
 */
import { useState, useCallback } from 'react';
import { TextPrediction } from '../domain/models';

interface UseTextGenerationState {
  prediction: TextPrediction | null;
  loading: boolean;
  error: Error | null;
  predictionId: string | null;
}

interface UseTextGenerationActions {
  generateText: (content: string, maxTokens?: number) => Promise<void>;
  clearPrediction: () => void;
  clearError: () => void;
}

export function useTextGeneration(generateUseCase: any): UseTextGenerationState & UseTextGenerationActions {
  const [state, setState] = useState<UseTextGenerationState>({
    prediction: null,
    loading: false,
    error: null,
    predictionId: null,
  });

  const generateText = useCallback(
    async (content: string, maxTokens: number = 50) => {
      setState((prev) => ({ ...prev, loading: true, error: null }));
      try {
        const result = await generateUseCase.execute({
          content,
          max_tokens: maxTokens,
        });
        setState((prev) => ({
          ...prev,
          prediction: result.prediction,
          predictionId: result.predictionId,
          loading: false,
        }));
      } catch (error) {
        setState((prev) => ({
          ...prev,
          error: error instanceof Error ? error : new Error('Unknown error'),
          loading: false,
        }));
      }
    },
    [generateUseCase]
  );

  const clearPrediction = useCallback(() => {
    setState((prev) => ({ ...prev, prediction: null, predictionId: null }));
  }, []);

  const clearError = useCallback(() => {
    setState((prev) => ({ ...prev, error: null }));
  }, []);

  return {
    ...state,
    generateText,
    clearPrediction,
    clearError,
  };
}
