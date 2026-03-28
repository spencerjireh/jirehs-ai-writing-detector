# Integration Test Instructions

## Purpose
Test the full analysis pipeline end-to-end: API request -> preprocessing -> detectors -> analyzers -> aggregation -> report response.

## Test Scenarios

### Scenario 1: AI-Written Text Detection
- **Description**: Submit AI-generated essays and verify high scores
- **Test**: `test_corpus_ai_essay_01_high_score`, `test_corpus_ai_essay_02_high_score`
- **Expected**: Score >= 60, classification "Likely AI-Generated"
- **Validates**: All 4 detectors + 7 analyzers + aggregator + report builder working together

### Scenario 2: Human-Written Text Detection
- **Description**: Submit human-written essays and verify low scores
- **Test**: `test_corpus_human_essay_01_low_score`, `test_corpus_human_essay_02_low_score`
- **Expected**: Score < 30, classification "Likely Human-Written"
- **Validates**: Detectors correctly ignore natural language patterns

### Scenario 3: Response Schema Validation
- **Description**: Verify API response matches expected structure
- **Test**: `test_corpus_response_schema`
- **Expected**: All fields present with correct types (score: int, classification: str, stats with word_count/char_count/sentence_count/avg_word_length, linguistic_factors and pattern_detections as arrays with required subfields)

### Scenario 4: Error Handling
- **Description**: Submit invalid input
- **Tests**: `test_analyze_empty_text_returns_422`, `test_analyze_missing_text_returns_422`
- **Expected**: 422 status code

### Scenario 5: Score Range Validation
- **Description**: Verify all scores are within 0-100 range
- **Test**: `test_analyze_score_between_0_and_100`
- **Expected**: 0 <= score <= 100 for any input

## Run Integration Tests

```bash
cd backend
uv run pytest tests/test_api.py -v
```

### Expected Results
- **Total**: 15 tests
- **Passed**: 15
- **Failed**: 0

## Manual End-to-End Testing via Docker

### 1. Start Services
```bash
docker compose up --build
```

### 2. Test via curl
```bash
# Test with AI-like text
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "It is important to note that innovative solutions play a crucial role in streamlining operations. Furthermore, experts agree that these transformative tools are remarkable."}'

# Test with human-like text
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "I went to the store and bought some milk. The weather was nice so I walked."}'
```

### 3. Test via Frontend
- Open http://localhost:3000
- Paste AI-like text -> should show high score (red gauge)
- Click "Analyze Another"
- Paste human-like text -> should show low score (green gauge)

### 4. Stop Services
```bash
docker compose down
```
