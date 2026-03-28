# Application Design -- AI Writing Detector (Consolidated)

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Preprocessed data passing | Shared `TextAnalysis` Pydantic model | Single object avoids parameter sprawl; detectors get a consistent context |
| Error handling | Graceful degradation per detector/analyzer | Partial results are more useful than a 500 error; warnings inform the user |
| Detector registration | Auto-discovery via BaseDetector subclasses | Adding a new detector requires only creating a new file -- no registry edits |

---

## Architecture Overview

The system is a linear pipeline with no persistence, no auth, and no background processing.

```
Request -> Preprocess -> [Detectors + Analyzers] -> Aggregate -> Report -> Response
```

- **24 components total**: 15 backend (Python) + 9 frontend (React/TypeScript)
- **1 API endpoint**: POST /api/analyze
- **1 config file**: detectors.yaml (loaded once at startup)
- **No database**: All analysis is stateless and in-memory

---

## Component Summary

### Backend (15 components)

| # | Component | Module | Responsibility |
|---|-----------|--------|---------------|
| 1 | Preprocessing | `app/preprocessing.py` | Tokenize text, compute stats, produce TextAnalysis |
| 2 | Core Config | `app/core/config.py` | Load/validate detectors.yaml |
| 3 | Core Models | `app/core/models.py` | Pydantic schemas (request, response, internal) |
| 4 | Base Detector | `app/detectors/base.py` | Abstract interface: detect() + score() template |
| 5 | Vocabulary Detector | `app/detectors/vocabulary.py` | AI words/phrases (Step 2) |
| 6 | Structural Detector | `app/detectors/structural.py` | Rule-of-three, parallelism, etc. (Step 3) |
| 7 | Vague Language Detector | `app/detectors/vague_language.py` | Attributions, hedging (Step 4) |
| 8 | Emphasis Detector | `app/detectors/emphasis.py` | Superlatives, promotional, elegant variation (Step 5) |
| 9 | Detector Registry | `app/detectors/registry.py` | Auto-discover and instantiate detectors |
| 10 | Linguistic Analyzer | `app/analyzers/linguistic.py` | Statistical analysis (Step 6) |
| 11 | Readability Analyzer | `app/analyzers/readability.py` | Flesch-Kincaid grade level |
| 12 | Score Aggregator | `app/scoring/aggregator.py` | Sum, normalize, classify (Step 7) |
| 13 | Report Builder | `app/report/builder.py` | Assemble response (Step 8) |
| 14 | API Routes | `app/api/routes.py` | POST /api/analyze endpoint + orchestration |
| 15 | FastAPI App | `app/main.py` | App entry, CORS, lifespan |

### Frontend (9 components)

| # | Component | Module | Responsibility |
|---|-----------|--------|---------------|
| 16 | App | `src/App.tsx` | Root SPA, state transitions |
| 17 | TextInput | `src/components/TextInput.tsx` | Textarea + live counts + button |
| 18 | ScoreGauge | `src/components/ScoreGauge.tsx` | Color-coded 0-100 gauge |
| 19 | ClassificationBadge | `src/components/ClassificationBadge.tsx` | Label display |
| 20 | LinguisticFactors | `src/components/LinguisticFactors.tsx` | Factor cards with bars |
| 21 | PatternBreakdown | `src/components/PatternBreakdown.tsx` | Detection table/cards |
| 22 | ReportView | `src/components/ReportView.tsx` | Full report layout |
| 23 | API Client | `src/api/client.ts` | Fetch wrapper |
| 24 | Type Definitions | `src/types/report.ts` | TS interfaces matching backend |

---

## Key Method Signatures

### Pipeline Entry Point
```python
@router.post("/api/analyze")
async def analyze_text(request: AnalyzeRequest) -> AnalyzeResponse
```

### Shared Context Model
```python
class TextAnalysis(BaseModel):
    text: str
    sentences: list[str]
    words: list[str]
    stats: TextStats
```

### Detector Interface
```python
class BaseDetector(ABC):
    @abstractmethod
    def detect(self, analysis: TextAnalysis) -> DetectorResult
    def score(self, analysis: TextAnalysis) -> ScoredResult  # template method
    @classmethod
    def config_key(cls) -> str  # used by auto-discovery
```

### Registry
```python
def discover_detectors(config: dict) -> list[BaseDetector]
```

See `component-methods.md` for complete method catalogue.

---

## Data Flow

```
Request { text }
    |
    v
TextAnalysis { text, sentences, words, stats }
    |
    +---> Detector 1..N .score() ---> list[ScoredResult]
    |
    +---> Analyzer 1..N () ---------> list[LinguisticFactor]
    |
    v
aggregate() ---> AggregatedScore { score, classification }
    |
    v
build_report() ---> AnalyzeResponse { score, classification, stats, factors, detections, timestamp, warnings? }
```

See `component-dependency.md` for full dependency matrix and diagrams.

---

## Service Architecture

No separate service layer. The API route handler orchestrates the pipeline directly. Config and detector instances are loaded once at startup and stored in `app.state`.

Failure modes:
- Preprocessing or aggregation failure: 500 (pipeline cannot continue)
- Individual detector or analyzer failure: graceful skip with warning

See `services.md` for full orchestration details.
