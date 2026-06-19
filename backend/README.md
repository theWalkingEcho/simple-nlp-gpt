# Backend - Python NLP Service

## Overview

The backend is built with Flask and follows Clean Architecture principles with SOLID design patterns.

## Architecture Layers

### 1. Domain Layer (`app/domain/`)
Core business logic independent of frameworks.

- **entities.py**: Domain objects (TextInput, Token, TextPrediction)
- **repositories.py**: Repository interfaces (contracts for data access)

### 2. Application Layer (`app/application/`)
Use cases and business logic orchestration.

- **use_cases.py**: Application use cases (GenerateTextUseCase, GetPredictionHistoryUseCase)
- **di_container.py**: Dependency Injection container managing all dependencies

### 3. Infrastructure Layer (`app/infrastructure/`)
External services and technical implementations.

- **nlp/**: NLP implementations
  - `tokenizer.py`: ITokenizer interface and implementations (SimpleTokenizer, BertTokenizer)
  - `model.py`: INLPModel interface and implementations (SimpleNLPModel, TransformerNLPModel)
- **repositories.py**: Repository implementations (InMemoryPredictionRepository, FilePredictionRepository)

### 4. Presentation Layer (`app/presentation/`)
HTTP API endpoints and serialization.

- **routes.py**: Flask routes using dependency injection
- **serializers.py**: Domain entity to JSON serialization

## Configuration (`config/`)

- **config.py**: Environment-based configuration using dataclasses
  - AppConfig: Flask configuration
  - NLPConfig: Model configuration
  - APIConfig: API configuration
  - Composition root for dependency management

## Running the Service

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your settings
# IMPORTANT: Change SECRET_KEY for production!

# Run development server
python main.py

# Run with Flask CLI
flask run

# Run with Gunicorn (production)
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

## Adding a New Use Case

1. Create domain entities if needed in `app/domain/entities.py`
2. Create use case class in `app/application/use_cases.py`:
   ```python
   class MyNewUseCase:
       def __init__(self, dependency1, dependency2):
           self.dep1 = dependency1
           self.dep2 = dependency2
       
       def execute(self, input_data):
           # Business logic here
           pass
   ```
3. Register in DI container (`app/application/di_container.py`)
4. Add route in `app/presentation/routes.py`

## Adding a New NLP Model

1. Implement `INLPModel` interface in `app/infrastructure/nlp/model.py`
2. Add to DI container factory method
3. Switch implementations based on environment variable

Example:
```python
class MyCustomModel(INLPModel):
    def generate(self, prompt: str, max_tokens: int) -> Tuple[str, float]:
        # Implementation
        pass
    
    def encode(self, text: str) -> List[float]:
        # Implementation
        pass
```

## Database Integration

To add database persistence:

1. Create repository implementation in `app/infrastructure/repositories.py`
2. Update DI container to use the new repository
3. Example with SQLAlchemy:
   ```python
   class SQLAlchemyPredictionRepository(PredictionRepository):
       def __init__(self, session):
           self.session = session
       
       def save(self, prediction: TextPrediction) -> str:
           # Save to database
           pass
   ```

## Testing

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=app
```

## Performance Considerations

- Models are lazy-loaded in DI container
- Consider caching frequently used tokens/embeddings
- For production, use model quantization
- Monitor API response times with logging

## Security Checklist

- [ ] Change SECRET_KEY in production
- [ ] Set CORS_ORIGINS to specific domains
- [ ] Use environment variables for all secrets
- [ ] Validate all inputs
- [ ] Rate limit API endpoints
- [ ] Use HTTPS in production
- [ ] Keep dependencies updated

## Troubleshooting

### Import Errors
Ensure virtual environment is activated and dependencies installed

### Model Loading Issues
Check NLP_MODEL_PATH exists and has write permissions

### CORS Errors
Verify CORS_ORIGINS in .env matches frontend URL

### Out of Memory
Consider using smaller models or enable model quantization
