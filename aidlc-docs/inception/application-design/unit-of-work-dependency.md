# Unit of Work Dependencies

## Dependency Matrix

```
          Unit 1   Unit 2   Unit 3   Unit 4   Unit 5
Unit 1      -        -        -        -        -
Unit 2     DEP       -        -        -        -
Unit 3     DEP      DEP       -        -        -
Unit 4      -        -       DEP       -        -
Unit 5      -        -       DEP      DEP       -
```

Legend: DEP = depends on

## Build Order

```
Unit 1: Backend Foundation
    |
    v
Unit 2: Pattern Detectors
    |
    v
Unit 3: Analyzers & Scoring
    |
    +--------+
    |        |
    v        v
Unit 4    Unit 5*
Frontend  Integration & Docker

* Unit 5 depends on both Unit 3 and Unit 4
```

**Strictly sequential**: 1 -> 2 -> 3 -> 4 -> 5

Units 4 and 5 could theoretically be parallelized (frontend development can start once the API contract is stable after Unit 3), but Unit 5's Docker Compose requires the frontend build, so the practical order remains sequential.

## Dependency Details

### Unit 1 -> Unit 2
- Unit 2 imports `BaseDetector` from `app/detectors/base.py`
- Unit 2 uses `TextAnalysis`, `DetectorResult`, `ScoredResult`, `MatchDetail` from `app/core/models.py`
- Unit 2 reads config sections via `load_config()`
- Unit 2 tests use fixtures from `conftest.py`

### Unit 1 + Unit 2 -> Unit 3
- Unit 3 uses `TextAnalysis`, `LinguisticFactor` from models
- Unit 3's aggregator consumes `ScoredResult` (from detectors) and `LinguisticFactor` (from analyzers)
- Unit 3's report builder needs all model types
- Unit 3 wires the full pipeline in `routes.py` (connects detectors + analyzers + aggregator + builder)

### Unit 3 -> Unit 4
- Unit 4's API client calls the endpoint defined and wired in Unit 3
- Unit 4's TypeScript interfaces mirror the Pydantic models from Unit 1 (but the working API from Unit 3 is needed for development)

### Unit 3 + Unit 4 -> Unit 5
- Unit 5's Docker Compose containerizes the backend (Unit 3) and frontend (Unit 4)
- Unit 5's integration tests hit the full pipeline (Unit 3)
- Unit 5's test corpus validates end-to-end behavior

## Integration Points

| From | To | Interface | Contract |
|------|----|-----------|----------|
| Unit 1 | Unit 2 | BaseDetector ABC | detect(TextAnalysis) -> DetectorResult |
| Unit 1 | Unit 2 | config dict | Config sections keyed by detector config_key() |
| Unit 2 | Unit 3 | list[ScoredResult] | Detector outputs fed to aggregator |
| Unit 1 | Unit 3 | TextAnalysis | Shared context for analyzers |
| Unit 3 | Unit 4 | POST /api/analyze | JSON request/response per AnalyzeRequest/AnalyzeResponse |
| Unit 3+4 | Unit 5 | Docker images | Backend on port 8000, frontend on port 5173/80 |
