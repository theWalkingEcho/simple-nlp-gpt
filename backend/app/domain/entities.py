"""
Domain entities following Clean Architecture
Entities represent the business logic core
"""
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class TextInput:
    """Entity representing input text"""
    content: str
    language: str = "en"
    max_length: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)

    def validate(self) -> bool:
        """Validate input text"""
        if not self.content or len(self.content.strip()) == 0:
            return False
        return len(self.content) <= 5000  # Max input length


@dataclass
class Token:
    """Entity representing a single token"""
    value: str
    token_id: int
    embedding: List[float]
    position: int


@dataclass
class TextPrediction:
    """Entity representing model prediction"""
    tokens: List[Token]
    confidence_score: float
    processing_time_ms: float
    model_name: str
    created_at: datetime = field(default_factory=datetime.now)

    def is_confident(self, threshold: float = 0.7) -> bool:
        """Check if prediction meets confidence threshold"""
        return self.confidence_score >= threshold
