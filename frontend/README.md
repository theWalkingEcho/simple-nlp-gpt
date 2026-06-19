# Frontend - TypeScript React UI

## Overview

The frontend is built with React and TypeScript, following Clean Architecture and SOLID principles for optimal maintainability.

## Architecture Layers

### 1. Domain Layer (`src/domain/`)
Core business models and data structures.

- **models.ts**: TypeScript interfaces for domain entities
  - Token, TextPrediction, GenerateRequest, GenerateResponse

### 2. Application Layer (`src/application/`)
Business logic and use cases.

- **useCases.ts**: Application use cases
  - GenerateTextUseCase: Handles text generation
  - GetPredictionHistoryUseCase: Retrieves history
- **hooks/**: Custom React hooks
  - useTextGeneration: State management for text generation
- **diContainer.ts**: Dependency Injection container
  - Manages service and use case instances

### 3. Infrastructure Layer (`src/infrastructure/`)
External service integration.

- **services/textGenerationService.ts**:
  - ITextGenerationService: Service interface
  - TextGenerationService: HTTP API client
  - Implements axios-based API communication

### 4. Presentation Layer (`src/presentation/`)
React components and UI.

- **components/**: Reusable components
  - TextGenerator: Main input/output component
- **pages/**: Page components
  - Home: Landing page
- **styles/**: CSS files for each component

## Configuration

Frontend configuration uses Vite environment variables:

```env
# .env.local
VITE_API_BASE_URL=http://localhost:5000/api/v1
VITE_APP_NAME=Simple GPT
```

Access in code:
```typescript
const apiUrl = import.meta.env.VITE_API_BASE_URL;
```

## Running the Application

```bash
# Install dependencies
npm install

# Copy environment template
cp .env.example .env.local

# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Type checking
npm run lint
```

## Project Structure Details

### Domain Models (`src/domain/models.ts`)

Define all TypeScript interfaces here. Keep them framework-agnostic.

```typescript
export interface Token {
  value: string;
  token_id: number;
  position: number;
  embedding_preview: number[];
}

export interface TextPrediction {
  tokens: Token[];
  confidence_score: number;
  processing_time_ms: number;
  model_name: string;
  created_at: string;
}
```

### Services (`src/infrastructure/services/`)

Handle external API communication.

```typescript
export interface ITextGenerationService {
  generateText(request: GenerateRequest): Promise<GenerateResponse>;
}

export class TextGenerationService implements ITextGenerationService {
  // Implementation
}
```

### Use Cases (`src/application/useCases.ts`)

Contain business logic independent of UI.

```typescript
export interface IGenerateTextUseCase {
  execute(request: GenerateRequest): Promise<{ prediction: TextPrediction; predictionId: string }>;
}

export class GenerateTextUseCase implements IGenerateTextUseCase {
  constructor(private textGenerationService: ITextGenerationService) {}
  
  async execute(request: GenerateRequest) {
    // Business logic
  }
}
```

### Hooks (`src/application/hooks/`)

React hooks for state management.

```typescript
export function useTextGeneration(generateUseCase) {
  const [state, setState] = useState({
    prediction: null,
    loading: false,
    error: null,
  });
  
  const generateText = async (content: string) => {
    // Use case execution
  };
  
  return { ...state, generateText };
}
```

### Components (`src/presentation/components/`)

React components connected to use cases via props.

```typescript
interface TextGeneratorProps {
  useCase: GenerateTextUseCase;
  onPredictionGenerated?: (predictionId: string) => void;
}

export const TextGenerator: React.FC<TextGeneratorProps> = ({ useCase }) => {
  // Component implementation
};
```

## Adding a New Feature

### Step 1: Add Domain Model
```typescript
// src/domain/models.ts
export interface NewFeature {
  id: string;
  data: string;
}
```

### Step 2: Add Service Method
```typescript
// src/infrastructure/services/textGenerationService.ts
async getNewFeature(id: string): Promise<NewFeature> {
  const response = await this.api.get(`/new-feature/${id}`);
  return response.data;
}
```

### Step 3: Create Use Case
```typescript
// src/application/useCases.ts
export class GetNewFeatureUseCase implements IGetNewFeatureUseCase {
  constructor(private service: ITextGenerationService) {}
  
  async execute(id: string): Promise<NewFeature> {
    return this.service.getNewFeature(id);
  }
}
```

### Step 4: Register in DI Container
```typescript
// src/application/diContainer.ts
getGetNewFeatureUseCase(): GetNewFeatureUseCase {
  return new GetNewFeatureUseCase(this.textGenerationService);
}
```

### Step 5: Create Component
```typescript
// src/presentation/components/NewFeature.tsx
export const NewFeature: React.FC<NewFeatureProps> = ({ useCase }) => {
  // Component implementation
};
```

## Styling Best Practices

- One CSS file per component
- Use BEM naming convention: `.component__element--modifier`
- Keep styles scoped to component
- Use CSS variables for theming

Example:
```css
.text-generator {
  /* Component styles */
}

.text-generator__input {
  /* Element styles */
}

.text-generator__input--focused {
  /* Modifier styles */
}
```

## Type Safety

Always maintain strict TypeScript types:

```bash
# Check types
npm run lint

# In tsconfig.json:
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true
  }
}
```

## Performance Optimization

1. **Lazy Load Components**: Use React.lazy() for code splitting
2. **Memoization**: Use React.memo() for pure components
3. **Use Callbacks**: useMemo and useCallback to prevent rerenders
4. **Image Optimization**: Compress images before adding to public/

## Error Handling

Consistent error handling pattern:

```typescript
try {
  const result = await useCase.execute(data);
  setData(result);
} catch (error) {
  setError(error instanceof Error ? error.message : 'Unknown error');
}
```

## Testing

```bash
# Install testing dependencies
npm install -D vitest @testing-library/react

# Run tests
npm run test
```

## Building for Production

```bash
# Build
npm run build

# Test production build locally
npm run preview

# Deploy dist/ folder to hosting service
```

## Environment-Specific Configuration

### Development
- Hot module reloading enabled
- Source maps enabled
- API pointing to localhost

### Production
- Minified code
- Optimized bundle
- Environment-specific API URL

## Troubleshooting

### TypeScript Errors
Ensure all imports use correct file extensions and paths

### CORS Issues
Check backend CORS configuration and ensure frontend URL is allowed

### Module Not Found
Check that paths in tsconfig.json are correct

### API Connection Issues
Verify VITE_API_BASE_URL environment variable is set correctly
