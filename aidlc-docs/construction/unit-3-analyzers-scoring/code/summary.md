# Unit 3: Analyzers & Scoring -- Code Summary

## Files Created

| File | Purpose |
|------|---------|
| `backend/app/analyzers/readability.py` | Flesch-Kincaid grade level (syllable counting heuristic + formula) |
| `backend/app/analyzers/linguistic.py` | 7 sub-analyzers: lexical diversity, sentence variation, passive voice, transition density, punctuation, rare words, reading grade |
| `backend/app/scoring/aggregator.py` | Score aggregation (sum, normalize to 100, classify) |
| `backend/app/report/builder.py` | Report assembly (AnalyzeResponse with pattern detections, factors, stats, timestamp, warnings) |
| `backend/tests/test_readability.py` | Readability tests (11 tests) |
| `backend/tests/test_linguistic.py` | Linguistic analyzer tests (21 tests) |
| `backend/tests/test_aggregator.py` | Aggregator tests (10 tests) |
| `backend/tests/test_report.py` | Report builder tests (9 tests) |

## Files Modified

| File | Change |
|------|--------|
| `backend/app/api/routes.py` | Replaced placeholder with full pipeline: preprocess -> detect -> analyze -> aggregate -> report. Added graceful degradation. |
| `backend/app/main.py` | Lifespan now calls discover_detectors() and stores in app.state |
| `backend/tests/test_api.py` | Updated for full pipeline (9 tests: clean/AI text scoring, linguistic factors, score range) |

## Test Results
- **121 total tests**, all passing
- Unit 1: 24 tests (unchanged)
- Unit 2: 44 tests (unchanged)
- Unit 3: 53 new tests (readability 11, linguistic 21, aggregator 10, report 9, API updated 2)
- Zero regressions
