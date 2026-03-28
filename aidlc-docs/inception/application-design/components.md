# Component Definitions

## Backend Components

### 1. Preprocessing
- **Module**: `app/preprocessing.py`
- **Purpose**: Tokenize raw text into sentences and words, compute basic statistics
- **Responsibilities**:
  - Sentence tokenization (nltk.sent_tokenize)
  - Word tokenization
  - Compute stats: char count, word count, sentence count, avg word length
  - Package all results into a single TextAnalysis model
- **Output**: TextAnalysis (shared context object consumed by all detectors and analyzers)

### 2. Core Config
- **Module**: `app/core/config.py`
- **Purpose**: Load and validate the YAML configuration at startup
- **Responsibilities**:
  - Read detectors.yaml
  - Validate required keys, types, and value ranges
  - Provide typed access to config sections

### 3. Core Models
- **Module**: `app/core/models.py`
- **Purpose**: Pydantic schemas for all data structures
- **Key Models**:
  - `AnalyzeRequest` -- API input (text field)
  - `AnalyzeResponse` -- API output (score, classification, stats, factors, detections, timestamp)
  - `TextAnalysis` -- Preprocessed text context (text, sentences, words, stats)
  - `TextStats` -- Basic text statistics
  - `DetectorResult` -- Raw detection output (matches, raw score)
  - `ScoredResult` -- Capped/weighted detection output with metadata
  - `MatchDetail` -- Individual match (text, position)
  - `LinguisticFactor` -- Analyzer output (name, value, contribution, explanation)
  - `PatternDetection` -- Grouped detection for report (category, occurrences, contribution, details, explanation)
  - `AggregatedScore` -- Final score + classification

### 4. Base Detector
- **Module**: `app/detectors/base.py`
- **Purpose**: Abstract base class defining the detector interface
- **Responsibilities**:
  - Define `detect()` abstract method (returns raw matches + score)
  - Implement `score()` template method (calls detect, applies weight and cap)
  - Store config (weight, cap, points_per_match)

### 5. Vocabulary Detector
- **Module**: `app/detectors/vocabulary.py`
- **Purpose**: Detect AI-characteristic words and phrases (Step 2)
- **Extends**: BaseDetector
- **Config section**: `vocabulary`

### 6. Structural Detector
- **Module**: `app/detectors/structural.py`
- **Purpose**: Detect rule-of-three, negative parallelism, outline conclusions, false range (Step 3)
- **Extends**: BaseDetector
- **Config section**: `structural`

### 7. Vague Language Detector
- **Module**: `app/detectors/vague_language.py`
- **Purpose**: Detect vague attributions, superficial hedging, overgeneralisations (Step 4)
- **Extends**: BaseDetector
- **Config section**: `vague_language`

### 8. Emphasis Detector
- **Module**: `app/detectors/emphasis.py`
- **Purpose**: Detect undue superlatives, promotional language, elegant variation (Step 5)
- **Extends**: BaseDetector
- **Config section**: `emphasis`

### 9. Detector Registry
- **Module**: `app/detectors/registry.py`
- **Purpose**: Auto-discover and instantiate all BaseDetector subclasses
- **Responsibilities**:
  - Scan detectors/ package for modules
  - Find all concrete subclasses of BaseDetector
  - Instantiate each with its config section
  - Return ordered list of detector instances

### 10. Linguistic Analyzer
- **Module**: `app/analyzers/linguistic.py`
- **Purpose**: Statistical text analysis across multiple dimensions (Step 6)
- **Sub-analyzers**: Lexical diversity, sentence length variation, passive voice, transition density, punctuation, rare words
- **Config section**: `linguistic`

### 11. Readability Analyzer
- **Module**: `app/analyzers/readability.py`
- **Purpose**: Flesch-Kincaid grade level calculation
- **Config section**: `linguistic.reading_grade`

### 12. Score Aggregator
- **Module**: `app/scoring/aggregator.py`
- **Purpose**: Combine all score contributions, normalize, classify (Step 7)
- **Responsibilities**:
  - Sum contributions from detectors and analyzers
  - Normalize proportionally if raw sum exceeds 100
  - Classify based on config thresholds

### 13. Report Builder
- **Module**: `app/report/builder.py`
- **Purpose**: Assemble the full API response object (Step 8)
- **Responsibilities**:
  - Combine stats, linguistic factors, pattern detections, score, classification
  - Add UTC timestamp
  - Include warnings for any skipped detectors (graceful degradation)

### 14. API Routes
- **Module**: `app/api/routes.py`
- **Purpose**: FastAPI endpoint definition and request orchestration
- **Endpoints**: `POST /api/analyze`

### 15. FastAPI App
- **Module**: `app/main.py`
- **Purpose**: Application entry point, CORS configuration, lifespan events
- **Responsibilities**:
  - Create FastAPI app
  - Configure CORS middleware
  - Load config on startup via lifespan context manager

---

## Frontend Components

### 16. App
- **Module**: `src/App.tsx`
- **Purpose**: Root SPA component, manages input/report state transitions

### 17. TextInput
- **Module**: `src/components/TextInput.tsx`
- **Purpose**: Textarea with live character/word count, Analyze button

### 18. ScoreGauge
- **Module**: `src/components/ScoreGauge.tsx`
- **Purpose**: Color-coded 0-100 gauge (green < 30, yellow 30-59, red >= 60)

### 19. ClassificationBadge
- **Module**: `src/components/ClassificationBadge.tsx`
- **Purpose**: Display classification label with matching color

### 20. LinguisticFactors
- **Module**: `src/components/LinguisticFactors.tsx`
- **Purpose**: Cards showing each linguistic factor with bar indicator and explanation

### 21. PatternBreakdown
- **Module**: `src/components/PatternBreakdown.tsx`
- **Purpose**: Table/cards grouped by detection category

### 22. ReportView
- **Module**: `src/components/ReportView.tsx`
- **Purpose**: Full report layout composing ScoreGauge, ClassificationBadge, stats, LinguisticFactors, PatternBreakdown

### 23. API Client
- **Module**: `src/api/client.ts`
- **Purpose**: Typed fetch wrapper for POST /api/analyze

### 24. Type Definitions
- **Module**: `src/types/report.ts`
- **Purpose**: TypeScript interfaces matching backend Pydantic schemas
