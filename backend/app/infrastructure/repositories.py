"""
Repository implementations - Infrastructure layer
Concrete implementation of repository interfaces
"""
from typing import Optional
import json
import uuid
from datetime import datetime
from ..domain.repositories import PredictionRepository
from ..domain.entities import TextPrediction


class InMemoryPredictionRepository(PredictionRepository):
    """In-memory implementation for development"""

    def __init__(self):
        self._store: dict = {}

    def save(self, prediction: TextPrediction) -> str:
        """Save prediction to memory"""
        prediction_id = str(uuid.uuid4())
        self._store[prediction_id] = prediction
        return prediction_id

    def find_by_id(self, prediction_id: str) -> Optional[TextPrediction]:
        """Find prediction by ID"""
        return self._store.get(prediction_id)

    def find_recent(self, limit: int = 10) -> list[TextPrediction]:
        """Find recent predictions sorted by creation date"""
        predictions = sorted(
            self._store.values(),
            key=lambda p: p.created_at,
            reverse=True
        )
        return predictions[:limit]

    def delete(self, prediction_id: str) -> bool:
        """Delete prediction"""
        if prediction_id in self._store:
            del self._store[prediction_id]
            return True
        return False


class FilePredictionRepository(PredictionRepository):
    """File-based persistence for predictions"""

    def __init__(self, storage_path: str = "./data/predictions"):
        self.storage_path = storage_path
        import os
        os.makedirs(storage_path, exist_ok=True)

    def save(self, prediction: TextPrediction) -> str:
        """Save prediction to file"""
        prediction_id = str(uuid.uuid4())
        filepath = f"{self.storage_path}/{prediction_id}.json"
        
        # Convert to dict for JSON serialization
        data = {
            "id": prediction_id,
            "tokens": [(t.value, t.token_id) for t in prediction.tokens],
            "confidence_score": prediction.confidence_score,
            "processing_time_ms": prediction.processing_time_ms,
            "model_name": prediction.model_name,
            "created_at": prediction.created_at.isoformat(),
        }
        
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        
        return prediction_id

    def find_by_id(self, prediction_id: str) -> Optional[TextPrediction]:
        """Find prediction by ID"""
        filepath = f"{self.storage_path}/{prediction_id}.json"
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
                # Reconstruct TextPrediction object
                return TextPrediction(
                    tokens=[],
                    confidence_score=data["confidence_score"],
                    processing_time_ms=data["processing_time_ms"],
                    model_name=data["model_name"],
                )
        except FileNotFoundError:
            return None

    def find_recent(self, limit: int = 10) -> list[TextPrediction]:
        """Find recent predictions"""
        import os
        
        files = os.listdir(self.storage_path)
        predictions = []
        
        for filename in sorted(files, reverse=True)[:limit]:
            prediction_id = filename.replace(".json", "")
            pred = self.find_by_id(prediction_id)
            if pred:
                predictions.append(pred)
        
        return predictions

    def delete(self, prediction_id: str) -> bool:
        """Delete prediction"""
        import os
        filepath = f"{self.storage_path}/{prediction_id}.json"
        try:
            os.remove(filepath)
            return True
        except FileNotFoundError:
            return False
