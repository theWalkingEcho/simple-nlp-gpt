"""
NLP Tokenizer implementation - Infrastructure layer
Handles text tokenization and preprocessing
"""
from typing import List
from abc import ABC, abstractmethod


class ITokenizer(ABC):
    """Tokenizer interface - Dependency Inversion"""

    @abstractmethod
    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into tokens"""
        pass

    @abstractmethod
    def detokenize(self, tokens: List[str]) -> str:
        """Convert tokens back to text"""
        pass


class SimpleTokenizer(ITokenizer):
    """Simple tokenizer implementation"""

    def tokenize(self, text: str) -> List[str]:
        """Simple whitespace and punctuation tokenizer"""
        # Remove extra whitespace
        text = text.strip()
        # Basic tokenization by splitting on whitespace
        tokens = text.split()
        return tokens

    def detokenize(self, tokens: List[str]) -> str:
        """Join tokens back together"""
        return " ".join(tokens)


class BertTokenizer(ITokenizer):
    """BERT tokenizer wrapper - requires transformers library"""

    def __init__(self, model_name: str = "bert-base-uncased"):
        try:
            from transformers import AutoTokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        except ImportError:
            raise ImportError(
                "transformers library not installed. Run: pip install transformers"
            )

    def tokenize(self, text: str) -> List[str]:
        """Tokenize using BERT tokenizer"""
        tokens = self.tokenizer.tokenize(text)
        return tokens

    def detokenize(self, tokens: List[str]) -> str:
        """Convert BERT tokens back to text"""
        text = self.tokenizer.convert_tokens_to_string(tokens)
        return text
