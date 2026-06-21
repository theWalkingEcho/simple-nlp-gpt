import pytest

from app.application.use_cases import (
    GenerateTextUseCase,
    GetPredictionHistoryUseCase,
    GetPredictionUseCase,
)
from app.domain.entities import TextInput, TextPrediction
from app.infrastructure.nlp.model import INLPModel
from app.infrastructure.nlp.tokenizer import ITokenizer
from app.infrastructure.repositories import InMemoryPredictionRepository


class DummyModel(INLPModel):
    def generate(self, prompt: str, max_tokens: int = 50):
        return prompt + " continuation", 0.9

    def encode(self, text: str):
        return [1.0, 2.0]


class DummyTokenizer(ITokenizer):
    def tokenize(self, text: str):
        return text.split()

    def detokenize(self, tokens: list[str]):
        return " ".join(tokens)


def test_text_input_validates_content_and_length():
    assert TextInput(content="hello world").validate()
    assert not TextInput(content="").validate()
    assert not TextInput(content="   ").validate()
    assert not TextInput(content="x" * 6000).validate()


def test_text_prediction_confidence_threshold():
    prediction = TextPrediction(
        tokens=[],
        confidence_score=0.75,
        processing_time_ms=10.0,
        model_name="simple-gpt-v1",
    )

    assert prediction.is_confident()
    assert not TextPrediction(
        tokens=[],
        confidence_score=0.69,
        processing_time_ms=10.0,
        model_name="simple-gpt-v1",
    ).is_confident()


def test_in_memory_prediction_repository_save_find_and_delete():
    repository = InMemoryPredictionRepository()
    prediction = TextPrediction(
        tokens=[],
        confidence_score=0.5,
        processing_time_ms=5.0,
        model_name="simple-gpt-v1",
    )

    prediction_id = repository.save(prediction)
    assert repository.find_by_id(prediction_id) is prediction
    assert repository.find_recent(limit=1) == [prediction]
    assert repository.delete(prediction_id)
    assert repository.find_by_id(prediction_id) is None
    assert not repository.delete(prediction_id)


def test_generate_text_use_case_saves_prediction():
    repository = InMemoryPredictionRepository()
    use_case = GenerateTextUseCase(
        nlp_model=DummyModel(),
        tokenizer=DummyTokenizer(),
        repository=repository,
    )

    text_input = TextInput(content="This is a test")
    prediction, prediction_id = use_case.execute(text_input, max_tokens=5)

    assert prediction.confidence_score == 0.9
    assert prediction.model_name == "simple-gpt-v1"
    assert prediction.tokens[0].value == "This"
    assert repository.find_by_id(prediction_id) is prediction


def test_generate_text_use_case_rejects_invalid_input():
    repository = InMemoryPredictionRepository()
    use_case = GenerateTextUseCase(
        nlp_model=DummyModel(),
        tokenizer=DummyTokenizer(),
        repository=repository,
    )

    with pytest.raises(ValueError):
        use_case.execute(TextInput(content=""), max_tokens=5)


def test_get_prediction_history_use_case_validates_limit():
    repository = InMemoryPredictionRepository()
    use_case = GetPredictionHistoryUseCase(repository=repository)

    with pytest.raises(ValueError):
        use_case.execute(limit=0)

    with pytest.raises(ValueError):
        use_case.execute(limit=101)


def test_get_prediction_use_case_raises_when_missing():
    repository = InMemoryPredictionRepository()
    use_case = GetPredictionUseCase(repository=repository)

    with pytest.raises(ValueError):
        use_case.execute("missing-id")
