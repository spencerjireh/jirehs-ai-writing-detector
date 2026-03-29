# AI Writing Detector — spec.md

## 1. Overview

A rule-based web application that accepts text input and analyzes it across multiple linguistic dimensions to estimate the probability that it was written by an AI rather than a human. The system produces a 0–100 score with a detailed breakdown report.

This project implements Coding Challenge #113 from codingchallenges.substack.com, covering Steps 0 through 8 (core challenge only).

---

## 2. Architecture

### Stack

| Layer    | Technology                        |
|----------|-----------------------------------|
| Backend  | Python 3.12+, FastAPI, Uvicorn    |
| Frontend | React (Vite), TypeScript          |
| Config   | YAML (wordlists, weights, caps)   |
| Testing  | pytest, pytest-cov, React Testing Library |

### Project Structure (monorepo)

```
ai-writing-detector/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI app, CORS, lifespan
│   │   ├── api/
│   │   │   └── routes.py            # POST /analyze endpoint
│   │   ├── core/
│   │   │   ├── config.py            # Load & validate YAML config
│   │   │   └── models.py            # Pydantic request/response schemas
│   │   ├── detectors/
│   │   │   ├── base.py              # Abstract Detector interface
│   │   │   ├── vocabulary.py        # Step 2 — AI vocabulary detector
│   │   │   ├── structural.py        # Step 3 — rule-of-three, negative parallelism, etc.
│   │   │   ├── vague_language.py    # Step 4 — attributions, hedging, overgeneralisation
│   │   │   ├── emphasis.py          # Step 5 — superlatives, promotional, elegant variation
│   │   │   └── registry.py          # Collects all detector instances
│   │   ├── analyzers/
│   │   │   ├── linguistic.py        # Step 6 — lexical diversity, sentence variation, etc.
│   │   │   └── readability.py       # Flesch-Kincaid grade level calculation
│   │   ├── scoring/
│   │   │   └── aggregator.py        # Step 7 — combine scores, normalize, classify
│   │   └── report/
│   │       └── builder.py           # Step 8 — assemble the full report object
│   ├── config/
│   │   └── detectors.yaml           # Wordlists, patterns, weights, caps
│   ├── tests/
│   │   ├── conftest.py              # Shared fixtures, sample texts
│   │   ├── corpus/                  # Test text files (AI-written and human-written)
│   │   │   ├── ai_essay_01.txt
│   │   │   ├── ai_essay_02.txt
│   │   │   ├── human_essay_01.txt
│   │   │   └── human_essay_02.txt
│   │   ├── test_vocabulary.py
│   │   ├── test_structural.py
│   │   ├── test_vague_language.py
│   │   ├── test_emphasis.py
│   │   ├── test_linguistic.py
│   │   ├── test_aggregator.py
│   │   ├── test_report.py
│   │   └── test_api.py              # Integration tests via TestClient
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── TextInput.tsx         # Textarea with live char/word count
│   │   │   ├── ScoreGauge.tsx        # Color-coded 0–100 gauge
│   │   │   ├── ClassificationBadge.tsx
│   │   │   ├── LinguisticFactors.tsx # Factor cards with bar indicators
│   │   │   ├── PatternBreakdown.tsx  # Detected patterns table
│   │   │   └── ReportView.tsx        # Full report layout
│   │   ├── api/
│   │   │   └── client.ts            # Fetch wrapper for POST /analyze
│   │   └── types/
│   │       └── report.ts            # TypeScript interfaces matching backend schemas
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

---

## 3. Configuration Schema (`detectors.yaml`)

All wordlists, regex patterns, per-detector weights, per-detector score caps, and classification thresholds live in a single YAML file. The backend loads and validates this at startup.

```yaml
vocabulary:
  weight: 1.0
  cap: 15
  words:
    - delve
    - navigate
    - robust
    - innovative
    - transformative
    - leverage
    - streamline
    - ecosystem
    # ... extended list
  phrases:
    - "delve into"
    - "innovative solutions"
    - "it's important to note"
    # ... extended list
  points_per_match: 2

structural:
  rule_of_three:
    weight: 1.0
    cap: 10
    points_per_match: 3
  negative_parallelism:
    weight: 1.0
    cap: 8
    patterns:
      - "not only .{1,80} but also"
    points_per_match: 4
  outline_conclusion:
    weight: 1.0
    cap: 8
    patterns:
      - "(?i)despite .{1,60}, .{1,60} offers .{1,60}"
    points_per_match: 5
  false_range:
    weight: 1.0
    cap: 6
    patterns:
      - "from .{1,40} to .{1,40}"
    points_per_match: 3

vague_language:
  attributions:
    weight: 1.0
    cap: 10
    phrases:
      - "experts agree"
      - "studies show"
      - "research indicates"
      - "industry insiders"
    points_per_match: 3
  superficial:
    weight: 1.0
    cap: 8
    phrases:
      - "it is worth noting"
      - "significant developments"
      - "one could argue"
      - "various sources indicate"
    points_per_match: 2
  overgeneralisation:
    weight: 1.0
    cap: 8
    phrases:
      - "everyone knows"
      - "it is well established"
      - "universal consensus"
    points_per_match: 3

emphasis:
  undue:
    weight: 1.0
    cap: 10
    words:
      - tremendous
      - remarkable
      - groundbreaking
      - extraordinary
    points_per_match: 2
  promotional:
    weight: 1.0
    cap: 10
    phrases:
      - "game-changer"
      - "revolutionary"
      - "impressive features"
      - "transformative potential"
    points_per_match: 3
  elegant_variation:
    weight: 1.0
    cap: 8
    # This detector is algorithmic, not pattern-based.
    # Config holds synonym groups to watch for.
    synonym_groups:
      - ["company", "organisation", "firm", "enterprise"]
      - ["method", "approach", "technique", "strategy"]
    proximity_sentences: 4
    points_per_match: 3

linguistic:
  # These are statistical analyzers, not pattern detectors.
  # They contribute to the report but feed into the overall score
  # via their own weight/cap.
  lexical_diversity:
    weight: 1.0
    cap: 8
    low_threshold: 0.4
    high_threshold: 0.8
  sentence_length_variation:
    weight: 1.0
    cap: 10
    cv_threshold: 0.35
  passive_voice:
    weight: 1.0
    cap: 8
    human_range: [0.05, 0.10]
    ai_threshold: 0.15
  transition_density:
    weight: 1.0
    cap: 8
    ai_threshold: 0.20
    words:
      - furthermore
      - moreover
      - consequently
      - additionally
      - nevertheless
  reading_grade:
    weight: 1.0
    cap: 6
    ai_threshold: 14
  punctuation:
    weight: 1.0
    cap: 6
  rare_words:
    weight: 1.0
    cap: 6
    ai_threshold: 0.12
    human_range: [0.03, 0.08]

scoring:
  classification:
    likely_human: 30
    possibly_ai: 60
    # >= 60 is "Likely AI-Generated"
```

---

## 4. Backend Design

### 4.1 API

A single analysis endpoint:

```
POST /api/analyze
Content-Type: application/json

{
  "text": "string (required, non-empty)"
}
```

**Response** (`200 OK`):

```json
{
  "score": 72,
  "classification": "Likely AI-Generated",
  "stats": {
    "char_count": 2341,
    "word_count": 387,
    "avg_word_length": 5.2,
    "sentence_count": 24
  },
  "linguistic_factors": [
    {
      "name": "Lexical Diversity",
      "value": 0.42,
      "score_contribution": 6,
      "explanation": "Type-token ratio of 0.42 is below the typical human range..."
    }
  ],
  "pattern_detections": [
    {
      "category": "AI Vocabulary",
      "occurrences": 7,
      "score_contribution": 14,
      "details": ["delve into (x2)", "robust (x1)", ...],
      "explanation": "Found 7 distinct AI-characteristic terms."
    }
  ],
  "timestamp": "2026-03-28T14:32:00Z"
}
```

**Error** (`422`): empty text or missing field.

### 4.2 Detector Interface

Every pattern detector implements a common abstract base:

```python
class BaseDetector(ABC):
    def __init__(self, config: dict): ...

    @abstractmethod
    def detect(self, text: str, sentences: list[str]) -> DetectorResult:
        """Return matches found and raw score (before weight/cap)."""

    def score(self, text: str, sentences: list[str]) -> ScoredResult:
        """Calls detect(), then applies weight and cap from config."""
```

`DetectorResult` holds a list of matches (with positions/text) and a raw point total. `ScoredResult` adds the capped, weighted contribution and metadata for the report.

### 4.3 Text Preprocessing

A shared preprocessing module provides:

- Sentence tokenization (regex-based, handling abbreviations and edge cases)
- Word tokenization
- Basic stats (char count, word count, sentence count, avg word length)

All detectors and analyzers receive the original text plus the pre-tokenized sentences and words, avoiding redundant work.

### 4.4 Scoring Aggregation (Step 7)

1. Collect `score_contribution` from every detector and analyzer.
2. Sum all contributions.
3. If the raw sum exceeds 100, normalize each contribution proportionally so the total equals 100.
4. Classify based on thresholds from config.

### 4.5 Report Builder (Step 8)

Assembles the full response object from all detector/analyzer outputs, stats, and the aggregated score. Adds the UTC timestamp.

---

## 5. Frontend Design

### 5.1 Pages / Flow

Single-page app with two states:

1. **Input state** — large textarea with a live character/word counter below it. An "Analyze" button submits to the backend. Empty input disables the button.
2. **Report state** — displays the full analysis. An "Analyze Another" button returns to the input state.

### 5.2 Report Layout

- **Header**: overall score displayed as a large color-coded gauge (green < 30, yellow 30–59, red >= 60) with the classification label.
- **Stats bar**: word count, character count, avg word length, sentence count.
- **Linguistic Factors section**: a card for each factor showing a labeled bar/percentage, the score contribution, and a one-line explanation.
- **Pattern Detections section**: a table or card list grouped by category, showing occurrence count, score contribution, matched details, and explanation.
- **Timestamp** at the bottom.

### 5.3 API Client

A thin wrapper around `fetch` that calls `POST /api/analyze`, handles loading/error states, and returns typed data.

---

## 6. Testing Strategy

### 6.1 Test Corpus

Maintain a `tests/corpus/` directory with at least:

- 2 AI-generated essays (produced by an LLM on a general topic)
- 2 human-written essays (sourced from personal writing or public-domain text predating 2017)

These are loaded via a pytest fixture and reused across tests.

### 6.2 Unit Tests (per detector / analyzer)

Each detector gets its own test file. Tests cover:

- **Positive detection**: crafted sentences known to trigger the detector.
- **Negative detection**: clean sentences that should not trigger.
- **Cap enforcement**: saturated input should hit the cap and stop accumulating.
- **Weight application**: verify that the configured weight multiplier is applied.
- **Edge cases**: empty string, single word, very long input, unicode.

Example:

```python
def test_vocabulary_detects_delve(config):
    detector = VocabularyDetector(config["vocabulary"])
    result = detector.detect("We need to delve into the root cause.", ...)
    assert any("delve" in m.text for m in result.matches)

def test_vocabulary_cap(config):
    # text with 20+ AI vocab terms
    result = detector.score(saturated_text, ...)
    assert result.score_contribution <= config["vocabulary"]["cap"]
```

### 6.3 Aggregator Tests

- Verify that individual contributions sum correctly.
- Verify normalization kicks in when raw total > 100.
- Verify classification thresholds map to the correct labels.

### 6.4 Integration Tests

Use FastAPI's `TestClient`:

- `POST /api/analyze` with valid AI-written text returns score >= 60.
- `POST /api/analyze` with valid human-written text returns score < 30.
- `POST /api/analyze` with empty text returns 422.
- Response schema matches the Pydantic model.

### 6.5 Coverage Target

Aim for >= 85% line coverage on the `backend/app/` package. Detectors and the aggregator should be near 100%.

---

## 7. Implementation Order

| Phase | What                                  | Steps Covered |
|-------|---------------------------------------|---------------|
| 1     | Project scaffolding, config loader, preprocessing, basic stats, API skeleton | 0, 1 |
| 2     | Vocabulary detector + tests           | 2             |
| 3     | Structural detectors + tests          | 3             |
| 4     | Vague language detectors + tests      | 4             |
| 5     | Emphasis detectors + tests            | 5             |
| 6     | Linguistic analyzers + tests          | 6             |
| 7     | Score aggregator + classification + tests | 7         |
| 8     | Report builder, full API response + integration tests | 8 |
| 9     | React frontend (input, gauge, report) | All           |
| 10    | End-to-end manual QA with corpus      | All           |

---

## 8. Open Questions / Decisions to Revisit

- **Sentence tokenizer**: regex vs. a lightweight library like `nltk.sent_tokenize`. Regex keeps dependencies minimal; nltk is more accurate. Decide in Phase 1.
- **Rare word detection** (Step 6): needs a word frequency list. Options include a bundled frequency file (e.g., top 5000 English words) or a small external package. Decide in Phase 6.
- **Elegant variation detector**: the synonym-group approach is a simplified heuristic. May need tuning once tested against real samples.
- **Frontend styling**: no CSS framework specified. Tailwind or plain CSS are both reasonable; decide when starting Phase 9.
