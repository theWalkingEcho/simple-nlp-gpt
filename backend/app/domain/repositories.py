"""
Repository interfaces - Dependency Inversion Principle
These define contracts for data access abstraction
"""
from abc import ABC, abstractmethod
from typing import Optional
from .entities import TextPrediction


class PredictionRepository(ABC):
    """Abstract repository for predictions"""

    @abstractmethod
    def save(self, prediction: TextPrediction) -> str:
        """Save prediction and return ID"""
        pass

    @abstractmethod
    def find_by_id(self, prediction_id: str) -> Optional[TextPrediction]:
        """Find prediction by ID"""
        pass

    @abstractmethod
    def find_recent(self, limit: int = 10) -> list[TextPrediction]:
        """Find recent predictions"""
        pass

    @abstractmethod
    def delete(self, prediction_id: str) -> bool:
        """Delete prediction"""
        pass
