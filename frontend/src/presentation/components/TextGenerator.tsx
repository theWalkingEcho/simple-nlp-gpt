/**
 * Text Generator Component - Presentation Layer
 * Handles user input and displays predictions
 */
import React, { useState } from 'react';
import { GenerateTextUseCase } from '../../application/useCases';
import '../styles/TextGenerator.css';

interface TextGeneratorProps {
  useCase: GenerateTextUseCase;
  onPredictionGenerated?: (predictionId: string) => void;
}

export const TextGenerator: React.FC<TextGeneratorProps> = ({ useCase, onPredictionGenerated }) => {
  const [input, setInput] = useState('');
  const [maxTokens, setMaxTokens] = useState(50);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [prediction, setPrediction] = useState<any>(null);
  const [predictionId, setPredictionId] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const result = await useCase.execute({
        content: input,
        max_tokens: maxTokens,
      });
      setPrediction(result.prediction);
      setPredictionId(result.predictionId);
      onPredictionGenerated?.(result.predictionId);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="text-generator">
      <h2>Text Generator</h2>

      <form onSubmit={handleSubmit} className="generator-form">
        <div className="form-group">
          <label htmlFor="input">Enter prompt:</label>
          <textarea
            id="input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your prompt here..."
            disabled={loading}
            maxLength={5000}
            rows={4}
          />
          <span className="char-count">{input.length}/5000</span>
        </div>

        <div className="form-group">
          <label htmlFor="maxTokens">Max tokens:</label>
          <input
            id="maxTokens"
            type="number"
            value={maxTokens}
            onChange={(e) => setMaxTokens(parseInt(e.target.value))}
            min={10}
            max={500}
            disabled={loading}
          />
        </div>

        <button type="submit" disabled={loading || !input.trim()}>
          {loading ? 'Generating...' : 'Generate'}
        </button>
      </form>

      {error && (
        <div className="error-message">
          <p>Error: {error}</p>
        </div>
      )}

      {prediction && (
        <div className="prediction-result">
          <h3>Result</h3>
          <div className="prediction-info">
            <p><strong>Confidence:</strong> {(prediction.confidence_score * 100).toFixed(2)}%</p>
            <p><strong>Processing time:</strong> {prediction.processing_time_ms.toFixed(2)}ms</p>
            <p><strong>Model:</strong> {prediction.model_name}</p>
            <p><strong>Tokens:</strong> {prediction.tokens.length}</p>
          </div>
          <div className="tokens">
            <h4>Generated Tokens:</h4>
            <div className="token-list">
              {prediction.tokens.slice(0, 20).map((token: any, idx: number) => (
                <span key={idx} className="token">
                  {token.value}
                </span>
              ))}
              {prediction.tokens.length > 20 && <span className="token-more">...</span>}
            </div>
          </div>
          {predictionId && (
            <p className="prediction-id">ID: {predictionId}</p>
          )}
        </div>
      )}
    </div>
  );
};
