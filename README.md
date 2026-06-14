# Simple GPT - A Lightweight NLP Text Generation Service

> The simple GPT-like system uses Python NLP backend and TypeScript React frontend, following Clean Architecture and SOLID principles.

## 🎯 Project Overview

This project demonstrates how to built a modern AI/ML application with:

- **Python Backend**: NLP model inference using transformers, following Clean Architecture
- **TypeScript Frontend**: React UI with clean dependency injection and proper separation of concerns
- **Security**: Environment-based configuration with no secrets committed to Git
- **Scalability**: SOLID principles ensuring extensibility and maintainability

## 📋 Architecture

### Clean Architecture Layers

```
┌─────────────────────────────────────────┐
│        Presentation Layer               │
│  (API Routes, Controllers, Serializers) │
├─────────────────────────────────────────┤
│        Application Layer                │
│     (Use Cases, Interactors, DI)        │
├─────────────────────────────────────────┤
│        Domain Layer                     │
│  (Entities, Repositories Interfaces)    │
├─────────────────────────────────────────┤
│        Infrastructure Layer             │
│  (DB, APIs, ML Models, Implementations) │
└─────────────────────────────────────────┘
```

### SOLID Principles Applied

- **S**ingle Responsibility: Each class has one reason to change
- **O**pen/Closed: Open for extension, closed for modification
- **L**iskov Substitution: Use interfaces for polymorphism
- **I**nterface Segregation: Small, focused interfaces
- **D**ependency Inversion: Depend on abstractions, not concretions

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
cd backend

# Copy environment template
cp .env.example .env

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Flask server
python main.py
```

Backend will start at `http://localhost:5000`

### Frontend Setup

```bash
cd frontend

# Copy environment template
cp .env.example .env.local

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will start at `http://localhost:5173` or `http://localhost:3000`

## 📁 Project Structure

```
simple-gpt/
├── backend/
│   ├── app/
│   │   ├── domain/              # Business logic core
│   │   │   ├── entities.py      # Domain entities
│   │   │   └── repositories.py  # Repository interfaces
│   │   ├── application/         # Use cases & business rules
│   │   │   ├── use_cases.py     # Application use cases
│   │   │   └── di_container.py  # Dependency injection
│   │   ├── infrastructure/      # External services & data
│   │   │   ├── nlp/             # NLP model implementations
│   │   │   │   ├── tokenizer.py
│   │   │   │   └── model.py
│   │   │   └── repositories.py  # Repository implementations
│   │   └── presentation/        # API endpoints
│   │       ├── routes.py        # Flask routes
│   │       └── serializers.py   # Response serialization
│   ├── config/
│   │   └── config.py            # Configuration management
│   ├── main.py                  # Flask app entry point
│   ├── requirements.txt         # Python dependencies
│   └── .env.example             # Environment template
│
├── frontend/
│   ├── src/
│   │   ├── domain/              # Business models
│   │   │   └── models.ts        # TypeScript interfaces
│   │   ├── application/         # Use cases & hooks
│   │   │   ├── useCases.ts
│   │   │   ├── hooks/
│   │   │   └── diContainer.ts
│   │   ├── infrastructure/      # API services
│   │   │   └── services/
│   │   │       └── textGenerationService.ts
│   │   ├── presentation/        # React components
│   │   │   ├── components/
│   │   │   ├── pages/
│   │   │   └── styles/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── public/
│   │   └── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── .env.example
│
└── .gitignore
```

## 🔐 Environment Configuration

### Backend Configuration (`.env`)

```env
# Flask
FLASK_ENV=development
DEBUG=True
PORT=5000
SECRET_KEY=your-secret-key

# NLP Model
NLP_MODEL_NAME=bert-base-uncased
NLP_TEMPERATURE=0.7

# API
CORS_ORIGINS=http://localhost:3000
```

### Frontend Configuration (`.env.local`)

```env
VITE_API_BASE_URL=http://localhost:5000/api/v1
```

## 🔌 API Endpoints

### Generate Text
```bash
POST /api/v1/generate
Content-Type: application/json

{
  "content": "Hello world",
  "max_tokens": 50,
  "language": "en"
}

# Response
{
  "success": true,
  "prediction_id": "uuid",
  "data": {
    "tokens": [...],
    "confidence_score": 0.85,
    "processing_time_ms": 125.4,
    "model_name": "simple-gpt-v1",
    "created_at": "2024-01-01T12:00:00"
  }
}
```

### Get Prediction History
```bash
GET /api/v1/predictions?limit=10
```

### Get Specific Prediction
```bash
GET /api/v1/predictions/{prediction_id}
```

### Health Check
```bash
GET /api/v1/health
```

## 🧪 Testing

### Backend
```bash
cd backend
pytest
```

### Frontend
```bash
cd frontend
npm run test
```

## 📖 Documentation

### Backend Documentation
See `backend/README.md` for detailed backend architecture

### Frontend Documentation
See `frontend/README.md` for detailed frontend architecture

## 🔗 Resources

- [Clean Architecture by Robert Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [Transformers Library](https://huggingface.co/transformers/)
- [React Best Practices](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
