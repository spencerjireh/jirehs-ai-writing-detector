# Service Definitions

## Analysis Pipeline Service

The core orchestration is a single linear pipeline invoked by the API route handler. There is no separate service layer -- the pipeline logic lives directly in the route handler, calling component functions in sequence.

### Pipeline Flow

```
POST /api/analyze { text }
       |
       v
  1. Validate (Pydantic)
       |
       v
  2. preprocess(text) -> TextAnalysis
       |
       v
  3. For each detector from registry:
       try:
           detector.score(analysis) -> ScoredResult
       except:
           log warning, skip detector
       |
       v
  4. analyze_linguistics(analysis, config) -> list[LinguisticFactor]
     (includes readability)
     Per-analyzer error handling: skip on failure, log warning
       |
       v
  5. aggregate(detector_results, linguistic_factors, config) -> AggregatedScore
       |
       v
  6. build_report(analysis, results, factors, aggregated, warnings) -> AnalyzeResponse
       |
       v
  Return JSON response
```

### Orchestration Responsibilities

| Step | Component | Failure Mode |
|------|-----------|--------------|
| Validate | Pydantic / FastAPI | 422 automatic |
| Preprocess | preprocessing.py | 500 -- cannot continue without tokenization |
| Detect | Each detector via registry | Graceful skip -- log warning, continue |
| Analyze | linguistic.py + readability.py | Graceful skip per analyzer -- log warning, continue |
| Aggregate | aggregator.py | 500 -- cannot produce score without aggregation |
| Report | builder.py | 500 -- cannot produce response without builder |

### Startup Service

The FastAPI lifespan context manager handles startup:

```
App startup:
  1. load_config("config/detectors.yaml") -> config
  2. discover_detectors(config) -> detectors
  3. Store config and detectors in app.state
```

These are made available to route handlers via `request.app.state`.

### No Additional Services

This application does not require:
- Database service (no persistence)
- Authentication service (no auth)
- Background task service (synchronous analysis)
- Caching service (each analysis is independent)
