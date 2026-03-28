# Component Dependencies

## Backend Dependency Matrix

```
                    config  models  preproc  base_det  detectors  registry  analyzers  aggregator  report  routes  main
config                 -       -       -        -         -          -         -          -          -       -      USE
models                 -       -       -        -         -          -         -          -          -       -       -
preprocessing          -      USE      -        -         -          -         -          -          -       -       -
base_detector          -      USE      -        -         -          -         -          -          -       -       -
vocabulary_det         -      USE      -       EXT        -          -         -          -          -       -       -
structural_det         -      USE      -       EXT        -          -         -          -          -       -       -
vague_lang_det         -      USE      -       EXT        -          -         -          -          -       -       -
emphasis_det           -      USE      -       EXT        -          -         -          -          -       -       -
registry               -       -       -       USE       DISC        -         -          -          -       -       -
linguistic             -      USE      -        -         -          -         -          -          -       -       -
readability            -      USE      -        -         -          -         -          -          -       -       -
aggregator             -      USE      -        -         -          -         -          -          -       -       -
report_builder         -      USE      -        -         -          -         -          -          -       -       -
routes                 -      USE     USE       -         -         USE       USE        USE        USE      -       -
main                  USE      -       -        -         -          -         -          -          -      USE      -
```

Legend: USE = imports/calls, EXT = extends, DISC = discovers

## Data Flow Diagram

```
+------------------+
|   API Request    |
|  { text: str }   |
+--------+---------+
         |
         v
+--------+---------+     +-----------+
|  Preprocessing   |---->| TextAnalysis
|  (nltk tokenize) |     | {text, sentences,
+--------+---------+     |  words, stats}
         |                +-----------+
         |                      |
         v                      |
+--------+---------+            |
| Detector Registry|            |
| (auto-discover)  |            |
+--------+---------+            |
         |                      |
    +----+----+                 |
    |         |                 |
    v         v                 v
+-------+ +-------+    +-------------+
|Det. 1 | |Det. N |    | Linguistic  |
|.score()| |.score()|   | Analyzers   |
+---+---+ +---+---+    +------+------+
    |         |                |
    v         v                v
 list[ScoredResult]    list[LinguisticFactor]
    |         |                |
    +----+----+-------+--------+
         |            |
         v            v
  +------+------------+------+
  |    Score Aggregator      |
  | (sum, normalize, classify)|
  +------+-------------------+
         |
         v
  +------+-------------------+
  |    Report Builder        |
  | (assemble response,      |
  |  add timestamp, warnings)|
  +------+-------------------+
         |
         v
+--------+---------+
|  API Response    |
| AnalyzeResponse  |
+------------------+
```

## Frontend Component Tree

```
App
+-- [view === "input"]
|   +-- TextInput
|       +-- textarea
|       +-- char/word counter
|       +-- Analyze button
|
+-- [view === "loading"]
|   +-- loading indicator
|
+-- [view === "report"]
    +-- ReportView
        +-- ScoreGauge (0-100, color-coded)
        +-- ClassificationBadge
        +-- stats bar (word count, char count, etc.)
        +-- LinguisticFactors
        |   +-- factor card (repeated)
        +-- PatternBreakdown
        |   +-- detection card/row (repeated)
        +-- timestamp
        +-- "Analyze Another" button
```

## Frontend Data Flow

```
TextInput --> handleAnalyze(text)
                  |
                  v
            analyzeText(text)  [api/client.ts]
                  |
                  v
            POST /api/analyze
                  |
                  v
            AnalyzeResponse
                  |
                  v
            setReport(response)
            setView("report")
                  |
                  v
            ReportView renders response data
```

## Key Dependencies (External)

| Component | External Dependency | Purpose |
|-----------|-------------------|---------|
| Preprocessing | nltk | sent_tokenize |
| Linguistic Analyzer | wordfreq | Rare word frequency lookup |
| Core Config | PyYAML | YAML parsing |
| Core Models | Pydantic | Data validation and serialization |
| API Routes | FastAPI | HTTP framework |
| Main | Uvicorn | ASGI server |
| Frontend | React, Vite | UI framework and build tool |
| Frontend | Tailwind CSS | Styling |
