# Business Overview

## Business Context Diagram

```
+------------------+      +-----------------------+      +-------------------+
|                  |      |                       |      |                   |
|  End User        +----->+  Frontend (React SPA) +----->+  Backend (FastAPI)|
|  (Writer/Editor) |      |  Text Input & Report  |      |  Text Analysis    |
|                  |<-----+  Display              |<-----+  Engine           |
+------------------+      +-----------------------+      +-------------------+
```

## Business Description
- **Business Description**: AI Writing Detector is a web application that analyzes submitted text to estimate the probability it was written by AI. It provides a detailed report with a score, classification, linguistic factors, and pattern detections.
- **Business Transactions**:
  1. **Text Analysis** - User submits text, system analyzes it for AI writing indicators and returns a comprehensive report with score (0-100), classification, linguistic factors, and pattern detections
  2. **Report Review** - User reviews the analysis report including score gauge, classification badge, text statistics, linguistic factors breakdown, and pattern detection details
- **Business Dictionary**:
  - **Score**: Numeric value 0-100 indicating probability of AI authorship (higher = more likely AI)
  - **Classification**: Human-readable label derived from the score (e.g., "Likely Human", "Mixed", "Likely AI")
  - **Linguistic Factors**: Measurable text properties (vocabulary diversity, sentence structure, readability) that contribute to the overall score
  - **Pattern Detections**: Specific textual patterns commonly associated with AI-generated writing (structural patterns, emphasis patterns, vocabulary choices, vague language)
  - **Score Contribution**: How much each factor or pattern adds to the overall AI probability score

## Component Level Business Descriptions
### Frontend (React SPA)
- **Purpose**: Provides the user interface for submitting text and viewing analysis reports
- **Responsibilities**: Text input with character/word counting, API communication, report visualization with score gauge, classification badges, linguistic factor charts, and pattern breakdowns

### Backend (FastAPI)
- **Purpose**: Performs the actual text analysis using linguistic analyzers and pattern detectors
- **Responsibilities**: Text preprocessing, linguistic analysis (readability, vocabulary), pattern detection (structural, emphasis, vocabulary, vague language), score aggregation, report generation
