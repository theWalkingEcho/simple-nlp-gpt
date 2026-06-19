"""
Serializers - Presentation layer
Convert domain entities to JSON-serializable format
"""
from typing import List, Dict, Any
from ..domain.entities import TextPrediction, Token


class PredictionSerializer:
    """Serialize TextPrediction to dictionary"""

    @staticmethod
    def to_dict(prediction: TextPrediction) -> Dict[str, Any]:
        """Convert TextPrediction to dictionary"""
        return {
            "tokens": [
                {
                    "value": token.value,
                    "token_id": token.token_id,
                    "position": token.position,
                    "embedding_preview": token.embedding[:10],  # First 10 dims
                }
                for token in prediction.tokens
            ],
            "confidence_score": prediction.confidence_score,
            "processing_time_ms": prediction.processing_time_ms,
            "model_name": prediction.model_name,
            "created_at": prediction.created_at.isoformat(),
        }
