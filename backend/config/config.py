"""
Configuration management following SOLID principles
"""
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class AppConfig:
    """Application configuration - Single Responsibility Principle"""
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    FLASK_ENV: str = os.getenv("FLASK_ENV", "development")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "5000"))
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key")


@dataclass
class NLPConfig:
    """NLP model configuration - Single Responsibility Principle"""
    MODEL_NAME: str = os.getenv("NLP_MODEL_NAME", "bert-base-uncased")
    MODEL_PATH: str = os.getenv("NLP_MODEL_PATH", "./models")
    MAX_TOKENS: int = int(os.getenv("NLP_MAX_TOKENS", "512"))
    TEMPERATURE: float = float(os.getenv("NLP_TEMPERATURE", "0.7"))
    VOCABULARY_SIZE: int = int(os.getenv("NLP_VOCAB_SIZE", "30522"))


@dataclass
class APIConfig:
    """API configuration"""
    API_VERSION: str = os.getenv("API_VERSION", "v1")
    API_PREFIX: str = f"/api/{API_VERSION}"
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")


@dataclass
class Config:
    """Main configuration class - Composition Root"""
    app: AppConfig = AppConfig()
    nlp: NLPConfig = NLPConfig()
    api: APIConfig = APIConfig()

    @staticmethod
    def get_config() -> "Config":
        """Factory method to get configuration - Dependency Inversion Principle"""
        return Config()
