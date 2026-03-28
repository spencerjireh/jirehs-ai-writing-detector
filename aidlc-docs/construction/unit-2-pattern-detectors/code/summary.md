# Unit 2: Pattern Detectors -- Code Summary

## Files Created

| File | Purpose |
|------|---------|
| `backend/app/detectors/vocabulary.py` | AI vocabulary detector -- word boundary + substring matching |
| `backend/app/detectors/structural.py` | Structural detector -- rule-of-three, negative parallelism, outline conclusion, false range |
| `backend/app/detectors/vague_language.py` | Vague language detector -- attributions, superficial hedging, overgeneralisation |
| `backend/app/detectors/emphasis.py` | Emphasis detector -- undue superlatives, promotional language, elegant variation |
| `backend/app/detectors/registry.py` | Auto-discovery registry -- finds BaseDetector subclasses, instantiates with config |
| `backend/tests/test_vocabulary.py` | Vocabulary detector tests (11 tests) |
| `backend/tests/test_structural.py` | Structural detector tests (10 tests) |
| `backend/tests/test_vague_language.py` | Vague language detector tests (9 tests) |
| `backend/tests/test_emphasis.py` | Emphasis detector tests (10 tests) |
| `backend/tests/test_registry.py` | Registry tests (4 tests) |

## Files Modified

| File | Change |
|------|--------|
| `backend/app/detectors/base.py` | Added score_all() method for compound detector support |

## Design Note: score_all() Pattern
Compound detectors (structural, vague_language, emphasis) contain sub-detectors with independent weight/cap/points. The score_all() method returns one ScoredResult per sub-detector, enabling per-pattern breakdown in the report. Simple detectors (vocabulary) inherit the default implementation which returns a single-element list.

## Test Results
- **68 total tests** (24 Unit 1 + 44 Unit 2), all passing
- Vocabulary: 11 tests (positive/negative detection, case-insensitive, cap, weight, multiple occurrences)
- Structural: 10 tests (all 4 sub-detectors, cap enforcement, combined scoring)
- Vague Language: 9 tests (all 3 sub-categories, cap, case-insensitive)
- Emphasis: 10 tests (undue, promotional, elegant variation proximity, cap)
- Registry: 4 tests (discovery, names, config, scoring)
