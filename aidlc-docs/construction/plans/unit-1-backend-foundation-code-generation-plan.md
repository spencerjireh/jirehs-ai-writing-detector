# Code Generation Plan -- Unit 1: Backend Foundation

## Unit Context
- **Unit**: Backend Foundation
- **Requirements**: FR-01 (skeleton), FR-02, FR-07, FR-09, NFR-01, NFR-02, NFR-05, NFR-06
- **Dependencies**: None (first unit)
- **Workspace Root**: /Users/spencerjireh.cebrian/Projects/jirehs-ai-writing-detector
- **Code Location**: `backend/` directory at workspace root

## Generation Steps

### Step 1: Project Structure Setup
- [x] Create `backend/` directory structure with all `__init__.py` files
- [x] Create `backend/pyproject.toml` with uv-compatible dependencies (FastAPI, uvicorn, pydantic, PyYAML, nltk, wordfreq, pytest, pytest-cov, httpx)
- [x] Create `.python-version` file (3.12)

### Step 2: Configuration File
- [x] Create `backend/config/detectors.yaml` with complete configuration from spec (all wordlists, patterns, weights, caps, thresholds)

### Step 3: Pydantic Models
- [x] Create `backend/app/core/models.py` with all schemas: TextStats, TextAnalysis, MatchDetail, DetectorResult, ScoredResult, LinguisticFactor, PatternDetection, AggregatedScore, AnalyzeRequest, AnalyzeResponse

### Step 4: Config Loader
- [x] Create `backend/app/core/config.py` with load_config() function (YAML loading, key validation)

### Step 5: Text Preprocessing
- [x] Create `backend/app/preprocessing.py` with preprocess() function (nltk.sent_tokenize, word tokenization, TextStats computation, returns TextAnalysis)

### Step 6: Base Detector
- [x] Create `backend/app/detectors/base.py` with BaseDetector ABC (detect abstract method, score template method with weight/cap, config_key classmethod, name property)

### Step 7: API Skeleton
- [x] Create `backend/app/api/routes.py` with POST /api/analyze stub (validates request, calls preprocess, returns placeholder response)
- [x] Create `backend/app/main.py` with FastAPI app, CORS middleware, lifespan context manager (loads config, stores in app.state)

### Step 8: Test Fixtures
- [x] Create `backend/tests/conftest.py` with shared fixtures: sample texts (short, medium, AI-like, human-like), config fixture loading detectors.yaml

### Step 9: Config Tests
- [x] Create `backend/tests/test_config.py` with tests: valid config loads, missing file raises error, required keys validated

### Step 10: Preprocessing Tests
- [x] Create `backend/tests/test_preprocessing.py` with tests: sentence tokenization, word tokenization, stats computation, empty string handling, single word, unicode

### Step 11: API Skeleton Tests
- [x] Create `backend/tests/test_api.py` (skeleton) with tests: endpoint returns 200 for valid text, returns 422 for empty/missing text, response contains expected fields

### Step 12: Documentation Summary
- [x] Create `aidlc-docs/construction/unit-1-backend-foundation/code/summary.md` with list of created files and their purposes

## Total: 12 steps
