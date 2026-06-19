"""
Use Cases (Interactors) - Application layer
Following SOLID principles, each use case handles one specific business operation
"""
import time
import logging
from typing import Tuple
from ..domain.entities import TextInput, TextPrediction, Token
from ..domain.repositories import PredictionRepository
from ..infrastructure.nlp.model import INLPModel
from ..infrastructure.nlp.tokenizer import ITokenizer

logger = logging.getLogger(__name__)


class GenerateTextUseCase:
    """Use case for generating text - Single Responsibility Principle"""

    def __init__(
        self,
        nlp_model: INLPModel,
        tokenizer: ITokenizer,
        repository: PredictionRepository,
    ):
        """
        Constructor injection - Dependency Inversion Principle
        All dependencies passed as parameters, not created inside
        """
        self.nlp_model = nlp_model
        self.tokenizer = tokenizer
        self.repository = repository

    def execute(self, text_input: TextInput, max_tokens: int = 50) -> Tuple[TextPrediction, str]:
        """
        Execute the generate text use case
        Returns: (TextPrediction, prediction_id)
        """
        # Validate input
        if not text_input.validate():
            raise ValueError("Invalid text input")

        logger.info(f"Generating text for input: {text_input.content[:50]}...")

        # Measure performance
        start_time = time.time()

        try:
            # Generate text using model
            generated_text, confidence = self.nlp_model.generate(
                text_input.content,
                max_tokens=max_tokens,
            )

            # Tokenize result
            tokens_list = self.tokenizer.tokenize(generated_text)

            # Create token entities
            tokens = [
                Token(
                    value=token,
                    token_id=idx,
                    embedding=self.nlp_model.encode(token),
                    position=idx,
                )
                for idx, token in enumerate(tokens_list)
            ]

            processing_time = (time.time() - start_time) * 1000  # Convert to ms

            # Create prediction entity
            prediction = TextPrediction(
                tokens=tokens,
                confidence_score=confidence,
                processing_time_ms=processing_time,
                model_name="simple-gpt-v1",
            )

            # Persist prediction
            prediction_id = self.repository.save(prediction)
            logger.info(f"Prediction saved with ID: {prediction_id}")

            return prediction, prediction_id

        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            raise


class GetPredictionHistoryUseCase:
    """Use case for retrieving prediction history - Single Responsibility"""

    def __init__(self, repository: PredictionRepository):
        self.repository = repository

    def execute(self, limit: int = 10) -> list[TextPrediction]:
        """Get recent predictions"""
        if limit < 1 or limit > 100:
            raise ValueError("Limit must be between 1 and 100")

        predictions = self.repository.find_recent(limit=limit)
        logger.info(f"Retrieved {len(predictions)} predictions")
        return predictions


class GetPredictionUseCase:
    """Use case for retrieving a specific prediction"""

    def __init__(self, repository: PredictionRepository):
        self.repository = repository

    def execute(self, prediction_id: str) -> TextPrediction:
        """Get a specific prediction"""
        prediction = self.repository.find_by_id(prediction_id)
        if not prediction:
            raise ValueError(f"Prediction not found: {prediction_id}")
        return prediction
