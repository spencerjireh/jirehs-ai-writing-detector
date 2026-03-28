# Unit Test Execution

## Run All Unit Tests

```bash
cd backend
uv run pytest tests/ -v
```

### Expected Results
- **Total Tests**: 127
- **Passed**: 127
- **Failed**: 0

## Run with Coverage

```bash
uv run pytest tests/ --cov=app --cov-report=term-missing
```

### Expected Coverage
- **Target**: >= 85% on backend/app/
- **Actual**: 97%
- **All detectors**: 100%

## Run Specific Test Files

```bash
# Config tests
uv run pytest tests/test_config.py -v

# Preprocessing tests
uv run pytest tests/test_preprocessing.py -v

# Individual detector tests
uv run pytest tests/test_vocabulary.py -v
uv run pytest tests/test_structural.py -v
uv run pytest tests/test_vague_language.py -v
uv run pytest tests/test_emphasis.py -v

# Analyzer tests
uv run pytest tests/test_linguistic.py -v
uv run pytest tests/test_readability.py -v

# Aggregator and report tests
uv run pytest tests/test_aggregator.py -v
uv run pytest tests/test_report.py -v

# Registry tests
uv run pytest tests/test_registry.py -v

# API and integration tests
uv run pytest tests/test_api.py -v
```

## Test Breakdown by Unit

| Unit | Test File | Tests |
|------|-----------|-------|
| 1 - Backend Foundation | test_config.py | 6 |
| 1 - Backend Foundation | test_preprocessing.py | 12 |
| 2 - Pattern Detectors | test_vocabulary.py | 11 |
| 2 - Pattern Detectors | test_structural.py | 10 |
| 2 - Pattern Detectors | test_vague_language.py | 9 |
| 2 - Pattern Detectors | test_emphasis.py | 10 |
| 2 - Pattern Detectors | test_registry.py | 4 |
| 3 - Analyzers & Scoring | test_linguistic.py | 21 |
| 3 - Analyzers & Scoring | test_readability.py | 11 |
| 3 - Analyzers & Scoring | test_aggregator.py | 10 |
| 3 - Analyzers & Scoring | test_report.py | 9 |
| 5 - Integration | test_api.py | 15 |
| **Total** | | **127** |

## Fix Failing Tests

If tests fail:
1. Read the failure output -- pytest shows the assertion, expected vs actual
2. Check if the failure is in test logic or application code
3. For corpus integration tests: if AI essay scores < 60, review detector config thresholds
4. For corpus integration tests: if human essay scores >= 30, check for accidental AI patterns in corpus text
5. Rerun with `-x` flag to stop on first failure: `uv run pytest tests/ -v -x`
