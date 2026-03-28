# System Architecture

## System Overview
A two-tier web application: a React SPA frontend served by Vite (dev) or Nginx (production), communicating with a Python FastAPI backend via REST API. The frontend handles all presentation concerns while the backend performs text analysis.

## Architecture Diagram

```
+------------------------------------------------------------------+
|                        Docker Compose                             |
|                                                                   |
|  +----------------------------+   +----------------------------+  |
|  |  Frontend Container        |   |  Backend Container         |  |
|  |  (Nginx on port 80)        |   |  (Uvicorn on port 8000)   |  |
|  |                            |   |                            |  |
|  |  - Static React SPA        |   |  - FastAPI Application     |  |
|  |  - Proxies /api/ to backend|   |  - Analyzers Module        |  |
|  |                            |   |  - Detectors Module        |  |
|  +-------------+--------------+   |  - Scoring Module          |  |
|                |                  |  - Report Builder          |  |
|                +----------------->+                            |  |
|                   POST /api/      +----------------------------+  |
|                   analyze                                         |
+------------------------------------------------------------------+
```

## Component Descriptions

### Frontend SPA
- **Purpose**: User interface for text submission and report display
- **Responsibilities**: Text input, loading states, report visualization
- **Dependencies**: React 19, Tailwind CSS 4, Vite 8
- **Type**: Application

### Backend API
- **Purpose**: Text analysis engine
- **Responsibilities**: Linguistic analysis, pattern detection, scoring, report building
- **Dependencies**: FastAPI, Python analyzers
- **Type**: Application

## Data Flow

```
User --> TextInput --> App.handleAnalyze() --> fetch POST /api/analyze
                                                      |
                                                      v
                                              Backend processes:
                                              1. Preprocess text
                                              2. Run linguistic analyzers
                                              3. Run pattern detectors
                                              4. Aggregate scores
                                              5. Build report
                                                      |
                                                      v
User <-- ReportView <-- App (sets report state) <-- AnalyzeResponse JSON
```

## Integration Points
- **External APIs**: None
- **Databases**: None (stateless analysis)
- **Third-party Services**: None

## Infrastructure Components
- **Docker**: Multi-stage builds for both frontend and backend
- **Nginx**: Production static file serving + API reverse proxy
- **Deployment Model**: Docker Compose with frontend and backend services
