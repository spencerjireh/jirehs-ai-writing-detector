# API Documentation

## REST APIs

### Analyze Text
- **Method**: POST
- **Path**: /api/analyze
- **Purpose**: Analyze submitted text for AI writing probability
- **Request**:
  ```json
  {
    "text": "string (the text to analyze)"
  }
  ```
- **Response** (AnalyzeResponse):
  ```json
  {
    "score": 0-100,
    "classification": "string",
    "stats": {
      "char_count": "number",
      "word_count": "number",
      "avg_word_length": "number",
      "sentence_count": "number"
    },
    "linguistic_factors": [
      {
        "name": "string",
        "value": "number (0-1)",
        "score_contribution": "number",
        "explanation": "string"
      }
    ],
    "pattern_detections": [
      {
        "category": "string",
        "occurrences": "number",
        "score_contribution": "number",
        "details": ["string"],
        "explanation": "string"
      }
    ],
    "warnings": ["string"],
    "timestamp": "ISO 8601 string"
  }
  ```

## Internal APIs (Frontend)

### analyzeText(text: string): Promise<AnalyzeResponse>
- **Location**: src/api/client.ts
- **Purpose**: Sends text to backend for analysis
- **Error Handling**: Throws Error with status code and response body on non-OK response

## Data Models

### AnalyzeResponse
- **score** (number): AI probability score 0-100
- **classification** (string): Human-readable classification label
- **stats** (TextStats): Basic text statistics
- **linguistic_factors** (LinguisticFactor[]): Array of linguistic analysis results
- **pattern_detections** (PatternDetection[]): Array of detected AI-associated patterns
- **warnings** (string[]): Any analysis warnings
- **timestamp** (string): ISO 8601 analysis timestamp

### TextStats
- **char_count** (number): Total character count
- **word_count** (number): Total word count
- **avg_word_length** (number): Average word length
- **sentence_count** (number): Total sentence count

### LinguisticFactor
- **name** (string): Factor name
- **value** (number): Normalized value 0-1
- **score_contribution** (number): Points added to total score
- **explanation** (string): Human-readable explanation

### PatternDetection
- **category** (string): Pattern category name
- **occurrences** (number): Number of matches found
- **score_contribution** (number): Points added to total score
- **details** (string[]): Specific matched patterns
- **explanation** (string): Human-readable explanation
