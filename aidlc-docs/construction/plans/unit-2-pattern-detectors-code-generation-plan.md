# Code Generation Plan -- Unit 2: Pattern Detectors

## Unit Context
- **Unit**: Pattern Detectors
- **Requirements**: FR-03 (all 4 pattern detectors)
- **Dependencies**: Unit 1 (BaseDetector, TextAnalysis, config, models)
- **Code Location**: `backend/app/detectors/` and `backend/tests/`

## Generation Steps

### Step 1: Vocabulary Detector
- [x] Create `backend/app/detectors/vocabulary.py` -- detect AI-characteristic words (case-insensitive word boundary match) and phrases (case-insensitive substring match), award points_per_match per unique match

### Step 2: Vocabulary Detector Tests
- [x] Create `backend/tests/test_vocabulary.py` -- positive detection (delve, robust), phrase detection (delve into, innovative solutions), negative detection (clean text), cap enforcement, weight application, empty text, single word

### Step 3: Structural Detector
- [x] Create `backend/app/detectors/structural.py` -- four sub-detectors: rule_of_three (comma-separated triple patterns), negative_parallelism (regex), outline_conclusion (regex), false_range (regex). Each sub-detector has own weight/cap/points from config. Returns combined DetectorResult.

### Step 4: Structural Detector Tests
- [x] Create `backend/tests/test_structural.py` -- rule-of-three detection, negative parallelism (not only...but also), outline conclusion, false range, negative cases, per-sub-detector cap enforcement

### Step 5: Vague Language Detector
- [x] Create `backend/app/detectors/vague_language.py` -- three sub-detectors: attributions (experts agree, studies show), superficial (it is worth noting, one could argue), overgeneralisation (everyone knows, universal consensus). Each with own config section.

### Step 6: Vague Language Detector Tests
- [x] Create `backend/tests/test_vague_language.py` -- each sub-category positive/negative detection, cap enforcement, combined scoring

### Step 7: Emphasis Detector
- [x] Create `backend/app/detectors/emphasis.py` -- three sub-detectors: undue (superlative words), promotional (phrases), elegant_variation (algorithmic -- check synonym group usage within proximity_sentences window). Each with own config section.

### Step 8: Emphasis Detector Tests
- [x] Create `backend/tests/test_emphasis.py` -- undue detection, promotional detection, elegant variation (synonym proximity), negative cases, cap enforcement

### Step 9: Auto-Discovery Registry
- [x] Create `backend/app/detectors/registry.py` -- discover_detectors() scans detectors package, finds BaseDetector subclasses, instantiates each with config[cls.config_key()], returns ordered list

### Step 10: Registry Tests
- [x] Create `backend/tests/test_registry.py` -- discovers all 4 detectors, correct instantiation, config_key mapping

### Step 11: Run All Tests
- [x] Run full test suite (Unit 1 + Unit 2) to verify no regressions

### Step 12: Documentation Summary
- [x] Create `aidlc-docs/construction/unit-2-pattern-detectors/code/summary.md`

## Total: 12 steps
