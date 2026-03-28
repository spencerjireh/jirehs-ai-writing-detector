# Units of Work

## Unit 1: Backend Foundation

**Purpose**: Project scaffolding, configuration, shared models, text preprocessing, API skeleton

**Components**:
- `app/main.py` -- FastAPI app, CORS, lifespan
- `app/core/config.py` -- YAML config loader/validator
- `app/core/models.py` -- All Pydantic schemas (TextAnalysis, TextStats, AnalyzeRequest, AnalyzeResponse, DetectorResult, ScoredResult, MatchDetail, LinguisticFactor, PatternDetection, AggregatedScore)
- `app/preprocessing.py` -- Sentence/word tokenization, stats computation
- `app/detectors/base.py` -- BaseDetector abstract class
- `app/api/routes.py` -- POST /api/analyze endpoint (stub returning placeholder)
- `config/detectors.yaml` -- Full configuration file
- `requirements.txt` / `pyproject.toml` -- Dependencies (FastAPI, uvicorn, pydantic, PyYAML, nltk, wordfreq)

**Tests**:
- `tests/test_config.py` -- Config loading and validation
- `tests/test_preprocessing.py` -- Tokenization, stats computation, edge cases
- `tests/conftest.py` -- Shared fixtures, sample texts, config fixture

**Deliverables**:
- Working FastAPI app that starts and responds to health check
- Config loaded and validated at startup
- preprocess() produces correct TextAnalysis from sample text
- All Pydantic models importable and validated

**Code Organization (Greenfield)**:
```
backend/
  app/
    __init__.py
    main.py
    preprocessing.py
    api/
      __init__.py
      routes.py
    core/
      __init__.py
      config.py
      models.py
    detectors/
      __init__.py
      base.py
    analyzers/
      __init__.py
    scoring/
      __init__.py
    report/
      __init__.py
  config/
    detectors.yaml
  tests/
    __init__.py
    conftest.py
    test_config.py
    test_preprocessing.py
```

---

## Unit 2: Pattern Detectors

**Purpose**: Implement all 4 pattern detectors with auto-discovery registry

**Components**:
- `app/detectors/vocabulary.py` -- AI vocabulary detector (Step 2)
- `app/detectors/structural.py` -- Structural pattern detector (Step 3)
- `app/detectors/vague_language.py` -- Vague language detector (Step 4)
- `app/detectors/emphasis.py` -- Emphasis detector (Step 5)
- `app/detectors/registry.py` -- Auto-discovery registry

**Tests**:
- `tests/test_vocabulary.py` -- Positive/negative detection, cap, weight, edge cases
- `tests/test_structural.py` -- Rule-of-three, parallelism, conclusion, false range
- `tests/test_vague_language.py` -- Attributions, superficial, overgeneralisation
- `tests/test_emphasis.py` -- Undue, promotional, elegant variation
- `tests/test_registry.py` -- Auto-discovery, instantiation

**Deliverables**:
- All 4 detectors pass unit tests
- Registry discovers and instantiates all detectors from config
- Cap and weight enforcement verified for each detector

**Dependencies**: Unit 1 (models, config, preprocessing, base detector)

---

## Unit 3: Analyzers & Scoring

**Purpose**: Statistical linguistic analyzers, score aggregation, and report assembly

**Components**:
- `app/analyzers/linguistic.py` -- All statistical sub-analyzers (lexical diversity, sentence variation, passive voice, transition density, punctuation, rare words)
- `app/analyzers/readability.py` -- Flesch-Kincaid grade level
- `app/scoring/aggregator.py` -- Sum, normalize, classify
- `app/report/builder.py` -- Assemble full AnalyzeResponse

**Tests**:
- `tests/test_linguistic.py` -- Each sub-analyzer with known inputs
- `tests/test_readability.py` -- Grade level calculation
- `tests/test_aggregator.py` -- Sum, normalization, classification thresholds
- `tests/test_report.py` -- Report assembly, timestamp, warnings field

**Deliverables**:
- All analyzers produce correct LinguisticFactor outputs
- Aggregator normalizes correctly when sum > 100
- Classification thresholds match config
- Report builder produces valid AnalyzeResponse
- Full API pipeline wired: request -> preprocess -> detect -> analyze -> aggregate -> report -> response

**Dependencies**: Unit 1 (models, config, preprocessing), Unit 2 (detectors, registry)

---

## Unit 4: Frontend

**Purpose**: React SPA with text input and analysis report views

**Components**:
- `src/App.tsx` -- Root component, state management (input/loading/report)
- `src/components/TextInput.tsx` -- Textarea, live counts, analyze button
- `src/components/ScoreGauge.tsx` -- Color-coded 0-100 gauge
- `src/components/ClassificationBadge.tsx` -- Classification label
- `src/components/LinguisticFactors.tsx` -- Factor cards with bar indicators
- `src/components/PatternBreakdown.tsx` -- Detection table/cards
- `src/components/ReportView.tsx` -- Full report layout
- `src/api/client.ts` -- Typed fetch wrapper
- `src/types/report.ts` -- TypeScript interfaces
- `package.json` -- Dependencies (React, Vite, TypeScript, Tailwind CSS)
- `vite.config.ts` -- Vite configuration with API proxy
- `tailwind.config.js` -- Tailwind configuration

**Tests**:
- Component rendering tests via React Testing Library (optional for prototype)

**Deliverables**:
- Working SPA that submits text and displays analysis report
- Color-coded score gauge with correct thresholds
- Responsive layout with Tailwind CSS
- API proxy configured for development

**Dependencies**: Unit 3 (working backend API)

---

## Unit 5: Integration & Docker

**Purpose**: Containerization, integration tests, end-to-end validation

**Components**:
- `Dockerfile` (backend)
- `Dockerfile` (frontend)
- `docker-compose.yml`
- `tests/test_api.py` -- Integration tests via TestClient
- `tests/corpus/` -- Test corpus files (2 AI + 2 human essays)

**Tests**:
- `tests/test_api.py`:
  - AI-written text scores >= 60
  - Human-written text scores < 30
  - Empty text returns 422
  - Response schema matches Pydantic model
- End-to-end manual QA via Docker Compose

**Deliverables**:
- `docker-compose up` starts both backend and frontend
- Integration tests pass with corpus texts
- Coverage >= 85% on backend/app/

**Dependencies**: Unit 3 (backend), Unit 4 (frontend)
