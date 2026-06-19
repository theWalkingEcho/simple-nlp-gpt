"""
Dependency Injection Container - Application layer
Composes all dependencies following the Composition Root pattern
"""
from ..infrastructure.nlp.model import SimpleNLPModel, INLPModel
from ..infrastructure.nlp.tokenizer import SimpleTokenizer, ITokenizer
from ..infrastructure.repositories import InMemoryPredictionRepository
from ..domain.repositories import PredictionRepository
from .use_cases import GenerateTextUseCase, GetPredictionHistoryUseCase, GetPredictionUseCase
from ...config.config import NLPConfig


class DIContainer:
    """Dependency Injection Container - Inversion of Control"""

    def __init__(self, nlp_config: NLPConfig):
        self.nlp_config = nlp_config
        self._nlp_model: INLPModel = None
        self._tokenizer: ITokenizer = None
        self._repository: PredictionRepository = None

    def get_nlp_model(self) -> INLPModel:
        """Factory method for NLP model - Lazy initialization"""
        if self._nlp_model is None:
            # You can switch between different model implementations here
            self._nlp_model = SimpleNLPModel(vocab_size=self.nlp_config.VOCABULARY_SIZE)
            # For production with transformers:
            # self._nlp_model = TransformerNLPModel(self.nlp_config.MODEL_NAME)
        return self._nlp_model

    def get_tokenizer(self) -> ITokenizer:
        """Factory method for tokenizer"""
        if self._tokenizer is None:
            self._tokenizer = SimpleTokenizer()
            # For BERT tokenizer:
            # self._tokenizer = BertTokenizer(self.nlp_config.MODEL_NAME)
        return self._tokenizer

    def get_repository(self) -> PredictionRepository:
        """Factory method for repository"""
        if self._repository is None:
            self._repository = InMemoryPredictionRepository()
            # For file-based storage:
            # self._repository = FilePredictionRepository()
        return self._repository

    def get_generate_text_use_case(self) -> GenerateTextUseCase:
        """Get configured generate text use case"""
        return GenerateTextUseCase(
            nlp_model=self.get_nlp_model(),
            tokenizer=self.get_tokenizer(),
            repository=self.get_repository(),
        )

    def get_get_prediction_history_use_case(self) -> GetPredictionHistoryUseCase:
        """Get configured get history use case"""
        return GetPredictionHistoryUseCase(repository=self.get_repository())

    def get_get_prediction_use_case(self) -> GetPredictionUseCase:
        """Get configured get prediction use case"""
        return GetPredictionUseCase(repository=self.get_repository())
