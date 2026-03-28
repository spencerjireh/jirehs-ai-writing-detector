# Component Methods

## Preprocessing

```python
def preprocess(text: str) -> TextAnalysis
```
- **Purpose**: Tokenize text and compute basic statistics
- **Input**: Raw text string
- **Output**: TextAnalysis model with text, sentences, words, and stats
- **Notes**: Uses nltk.sent_tokenize for sentence splitting

---

## Core Config

```python
def load_config(path: str = "config/detectors.yaml") -> dict
```
- **Purpose**: Load and validate YAML configuration
- **Input**: Path to YAML file
- **Output**: Validated config dictionary
- **Raises**: ValueError if required keys missing or invalid values

---

## Base Detector

```python
class BaseDetector(ABC):
    def __init__(self, config: dict) -> None

    @abstractmethod
    def detect(self, analysis: TextAnalysis) -> DetectorResult

    def score(self, analysis: TextAnalysis) -> ScoredResult

    @property
    def name(self) -> str

    @classmethod
    def config_key(cls) -> str
```

| Method | Purpose | Notes |
|--------|---------|-------|
| `__init__` | Store config (weight, cap, points_per_match) | Extracts common fields from config dict |
| `detect` | Find matches in text, return raw score | Abstract -- each detector implements |
| `score` | Call detect(), apply weight and cap | Template method -- not overridden |
| `name` | Human-readable detector name for reports | Property derived from class name |
| `config_key` | YAML config section key for this detector | Class method used by registry for auto-instantiation |

---

## Vocabulary Detector

```python
class VocabularyDetector(BaseDetector):
    def detect(self, analysis: TextAnalysis) -> DetectorResult
```
- Scans for words from `config.vocabulary.words` (case-insensitive word match)
- Scans for phrases from `config.vocabulary.phrases` (case-insensitive substring match)
- Awards `points_per_match` per unique match

---

## Structural Detector

```python
class StructuralDetector(BaseDetector):
    def detect(self, analysis: TextAnalysis) -> DetectorResult
```
- Contains sub-detectors for each structural pattern:
  - `_detect_rule_of_three(sentences) -> list[MatchDetail]`
  - `_detect_negative_parallelism(text) -> list[MatchDetail]`
  - `_detect_outline_conclusion(text) -> list[MatchDetail]`
  - `_detect_false_range(text) -> list[MatchDetail]`
- Each sub-detector has its own weight, cap, and points_per_match from config
- Returns combined DetectorResult

---

## Vague Language Detector

```python
class VagueLanguageDetector(BaseDetector):
    def detect(self, analysis: TextAnalysis) -> DetectorResult
```
- Contains sub-detectors:
  - `_detect_attributions(text) -> list[MatchDetail]`
  - `_detect_superficial(text) -> list[MatchDetail]`
  - `_detect_overgeneralisation(text) -> list[MatchDetail]`
- Each sub-category has its own config section

---

## Emphasis Detector

```python
class EmphasisDetector(BaseDetector):
    def detect(self, analysis: TextAnalysis) -> DetectorResult
```
- Contains sub-detectors:
  - `_detect_undue(text) -> list[MatchDetail]`
  - `_detect_promotional(text) -> list[MatchDetail]`
  - `_detect_elegant_variation(sentences) -> list[MatchDetail]`
- Elegant variation is algorithmic: checks synonym groups within proximity_sentences window

---

## Detector Registry

```python
def discover_detectors(config: dict) -> list[BaseDetector]
```
- **Purpose**: Auto-discover BaseDetector subclasses in detectors/ package
- **Input**: Full config dict
- **Output**: Ordered list of instantiated detectors
- **Mechanism**: Import all modules in detectors/, find BaseDetector subclasses, instantiate each with `config[cls.config_key()]`

---

## Linguistic Analyzer

```python
def analyze_linguistics(analysis: TextAnalysis, config: dict) -> list[LinguisticFactor]
```
- **Purpose**: Run all statistical analyzers
- **Returns**: List of LinguisticFactor, each with name, value, score_contribution, and explanation

### Sub-analyzer functions:

```python
def lexical_diversity(words: list[str], config: dict) -> LinguisticFactor
def sentence_length_variation(sentences: list[str], config: dict) -> LinguisticFactor
def passive_voice_ratio(sentences: list[str], config: dict) -> LinguisticFactor
def transition_density(words: list[str], config: dict) -> LinguisticFactor
def punctuation_analysis(text: str, config: dict) -> LinguisticFactor
def rare_word_ratio(words: list[str], config: dict) -> LinguisticFactor
```

---

## Readability Analyzer

```python
def flesch_kincaid_grade(analysis: TextAnalysis) -> float
def reading_grade_factor(analysis: TextAnalysis, config: dict) -> LinguisticFactor
```
- `flesch_kincaid_grade`: Pure calculation returning grade level float
- `reading_grade_factor`: Wraps grade in a LinguisticFactor with score contribution

---

## Score Aggregator

```python
def aggregate(
    detector_results: list[ScoredResult],
    linguistic_factors: list[LinguisticFactor],
    config: dict
) -> AggregatedScore
```
- **Purpose**: Sum contributions, normalize if > 100, classify
- **Output**: AggregatedScore with total score, classification label, normalized contributions

```python
def classify(score: int, config: dict) -> str
```
- Maps score to classification label using config thresholds

---

## Report Builder

```python
def build_report(
    analysis: TextAnalysis,
    detector_results: list[ScoredResult],
    linguistic_factors: list[LinguisticFactor],
    aggregated: AggregatedScore,
    warnings: list[str] | None = None
) -> AnalyzeResponse
```
- **Purpose**: Assemble the full API response
- **Warnings**: Optional list of skipped detector names (graceful degradation)

---

## API Routes

```python
@router.post("/api/analyze")
async def analyze_text(request: AnalyzeRequest) -> AnalyzeResponse
```
- Orchestrates the full pipeline: preprocess -> detect -> analyze -> aggregate -> build report
- Catches per-detector/analyzer exceptions for graceful degradation

---

## Frontend Methods

### API Client
```typescript
async function analyzeText(text: string): Promise<AnalyzeResponse>
```

### App (state management)
```typescript
// State: "input" | "loading" | "report"
const [view, setView] = useState<"input" | "loading" | "report">("input")
const [report, setReport] = useState<AnalyzeResponse | null>(null)
const [error, setError] = useState<string | null>(null)

async function handleAnalyze(text: string): Promise<void>
function handleReset(): void
```
