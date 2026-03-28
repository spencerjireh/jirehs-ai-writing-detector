# Code Generation Plan -- Unit 3: Analyzers & Scoring

## Unit Context
- **Unit**: Analyzers & Scoring
- **Requirements**: FR-04, FR-05, FR-06, FR-01 (full API wiring)
- **Dependencies**: Unit 1 (models, config, preprocessing), Unit 2 (detectors, registry)
- **Code Location**: `backend/app/analyzers/`, `backend/app/scoring/`, `backend/app/report/`

## Generation Steps

### Step 1: Readability Analyzer
- [x] Create `backend/app/analyzers/readability.py` -- Flesch-Kincaid grade level calculation (syllable counting, formula), reading_grade_factor() returning LinguisticFactor with score contribution based on ai_threshold

### Step 2: Linguistic Analyzer
- [x] Create `backend/app/analyzers/linguistic.py` -- analyze_linguistics() orchestrator calling 7 sub-analyzers:
  - lexical_diversity: type-token ratio, score if below low_threshold
  - sentence_length_variation: coefficient of variation of sentence lengths, score if below cv_threshold
  - passive_voice: regex-based passive voice detection, score if ratio exceeds ai_threshold
  - transition_density: count transition words / total words, score if exceeds ai_threshold
  - punctuation_analysis: analyze punctuation diversity/patterns
  - rare_word_ratio: use wordfreq to check word frequencies, score if ratio outside human_range
  - reading_grade: delegates to readability.py

### Step 3: Linguistic Analyzer Tests
- [x] Create `backend/tests/test_linguistic.py` -- tests for each sub-analyzer with known inputs, edge cases (empty text, single sentence), threshold enforcement

### Step 4: Readability Tests
- [x] Create `backend/tests/test_readability.py` -- Flesch-Kincaid formula correctness, known-grade texts, edge cases

### Step 5: Score Aggregator
- [x] Create `backend/app/scoring/aggregator.py` -- aggregate() sums all contributions, normalizes proportionally if > 100, classify() maps score to label using config thresholds

### Step 6: Aggregator Tests
- [x] Create `backend/tests/test_aggregator.py` -- sum correctness, normalization when > 100, classification threshold mapping, edge cases (score = 0, score = 100, boundary values 30 and 60)

### Step 7: Report Builder
- [x] Create `backend/app/report/builder.py` -- build_report() assembles AnalyzeResponse from TextAnalysis, ScoredResults, LinguisticFactors, AggregatedScore, optional warnings, UTC timestamp

### Step 8: Report Builder Tests
- [x] Create `backend/tests/test_report.py` -- correct assembly, timestamp present, warnings included, all fields populated

### Step 9: Wire Full API Pipeline
- [x] Modify `backend/app/api/routes.py` -- replace placeholder with full pipeline: preprocess -> discover_detectors -> score_all each -> analyze_linguistics -> aggregate -> build_report. Add per-detector/analyzer error handling (graceful degradation).
- [x] Modify `backend/app/main.py` -- store discovered detectors in app.state during lifespan

### Step 10: Run Full Test Suite
- [x] Run all tests (Unit 1 + 2 + 3) to verify no regressions

### Step 11: Documentation Summary
- [x] Create `aidlc-docs/construction/unit-3-analyzers-scoring/code/summary.md`

## Total: 11 steps
