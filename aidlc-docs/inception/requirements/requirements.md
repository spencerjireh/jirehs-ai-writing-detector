# Requirements Document -- AI Writing Detector

## Intent Analysis

| Attribute | Value |
|-----------|-------|
| Request Type | New Project (Greenfield) |
| Request Clarity | Clear -- detailed spec provided |
| Scope | System-wide (full-stack monorepo) |
| Complexity | Moderate |
| Requirements Depth | Standard |

**User Request**: Build a rule-based web application that accepts text input and analyzes it across multiple linguistic dimensions to estimate the probability that it was written by an AI. The system produces a 0-100 score with a detailed breakdown report. Implements Coding Challenge #113 (Steps 0-8).

---

## Functional Requirements

### FR-01: Text Analysis API
- Single endpoint: `POST /api/analyze`
- Accepts JSON body with a `text` field (required, non-empty string)
- Returns structured JSON response with score, classification, stats, linguistic factors, pattern detections, and timestamp
- Returns 422 for empty or missing text

### FR-02: Text Preprocessing
- Sentence tokenization via **nltk.sent_tokenize**
- Word tokenization
- Basic statistics: character count, word count, sentence count, average word length
- All detectors/analyzers receive original text plus pre-tokenized sentences and words

### FR-03: Pattern Detectors (Steps 2-5)
Each detector implements a common abstract base (`BaseDetector`) with `detect()` and `score()` methods. Scores are subject to per-detector weight and cap from YAML config.

| Detector | Step | What It Detects |
|----------|------|-----------------|
| Vocabulary | 2 | AI-characteristic words and phrases (delve, navigate, robust, etc.) |
| Structural | 3 | Rule-of-three, negative parallelism, outline conclusions, false range |
| Vague Language | 4 | Vague attributions, superficial hedging, overgeneralisations |
| Emphasis | 5 | Undue superlatives, promotional language, elegant variation |

### FR-04: Linguistic Analyzers (Step 6)
Statistical analyzers that contribute to the overall score:

| Analyzer | Metric |
|----------|--------|
| Lexical Diversity | Type-token ratio |
| Sentence Length Variation | Coefficient of variation |
| Passive Voice | Passive voice ratio |
| Transition Density | Transition word frequency |
| Reading Grade | Flesch-Kincaid grade level |
| Punctuation | Punctuation pattern analysis |
| Rare Words | Rare word ratio (via **wordfreq** library) |

### FR-05: Score Aggregation (Step 7)
- Sum all detector/analyzer score contributions
- Normalize proportionally to 100 if raw sum exceeds 100
- Classify using thresholds from config:
  - < 30: Likely Human-Written
  - 30-59: Possibly AI-Generated
  - >= 60: Likely AI-Generated

### FR-06: Report Builder (Step 8)
- Assemble full response object from all detector/analyzer outputs
- Include stats, linguistic factors, pattern detections, score, classification
- Add UTC timestamp

### FR-07: Configuration
- All wordlists, regex patterns, weights, caps, and thresholds in a single `detectors.yaml`
- Loaded and validated at startup

### FR-08: Frontend
- Single-page React application (Vite, TypeScript, **Tailwind CSS**)
- **Input state**: Large textarea with live character/word count, "Analyze" button (disabled when empty)
- **Report state**: Color-coded score gauge (green < 30, yellow 30-59, red >= 60), classification badge, stats bar, linguistic factors cards, pattern detections table, timestamp
- "Analyze Another" button returns to input state

### FR-09: No Minimum Text Length
- Any non-empty text is accepted for analysis
- Short texts may produce less reliable statistical measures (this is acceptable)

---

## Non-Functional Requirements

### NFR-01: Technology Stack
| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12+, FastAPI, Uvicorn |
| Frontend | React (Vite), TypeScript, Tailwind CSS |
| NLP | nltk (sentence tokenization), wordfreq (rare word frequency) |
| Config | YAML (detectors.yaml) |
| Testing | pytest, pytest-cov, React Testing Library |
| Dependency Management | uv |
| Containerization | Docker Compose |

### NFR-02: Project Structure
- Monorepo with `backend/` and `frontend/` directories
- Structure as defined in spec.md Section 2

### NFR-03: Testing
- Test corpus: minimum 2 AI-generated + 2 human-written essays in `tests/corpus/`
- Per-detector unit tests: positive detection, negative detection, cap enforcement, weight application, edge cases
- Aggregator tests: sum correctness, normalization, classification thresholds
- Integration tests via FastAPI TestClient
- Coverage target: >= 85% on `backend/app/`

### NFR-04: Deployment
- Docker Compose with containerized backend and frontend
- Single `docker-compose.yml` at project root

### NFR-05: Security
- Security extension rules are **not enforced** for this project (prototype/learning project)
- Basic input validation via Pydantic on API endpoints

### NFR-06: CORS
- Backend must configure CORS to allow frontend requests during development

---

## Decisions Log

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Sentence tokenizer | nltk.sent_tokenize | More accurate with abbreviations and edge cases |
| Rare word frequency | wordfreq library | Avoids maintaining a bundled frequency file |
| Frontend CSS | Tailwind CSS | Fast prototyping, utility-first |
| Dependency management | uv | Fast resolver, modern toolchain |
| Deployment | Docker Compose | Containerized dev/demo environment |
| Minimum text length | No minimum | Analyze any non-empty input |
| Security rules | Not enforced | Prototype/learning project |
