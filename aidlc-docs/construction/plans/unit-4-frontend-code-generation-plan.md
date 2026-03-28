# Code Generation Plan -- Unit 4: Frontend

## Unit Context
- **Unit**: Frontend
- **Requirements**: FR-08 (React SPA, input/report views, gauge, patterns table)
- **Dependencies**: Unit 3 (working backend API at POST /api/analyze)
- **Code Location**: `frontend/` directory at workspace root

## Generation Steps

### Step 1: Project Scaffolding
- [x] Create Vite + React + TypeScript project in `frontend/`
- [x] Install and configure Tailwind CSS v4
- [x] Configure Vite API proxy to backend (localhost:8000)
- [x] Create `frontend/package.json`, `frontend/vite.config.ts`, `frontend/tsconfig.json`, `frontend/tailwind.config.js`, `frontend/postcss.config.js`, `frontend/index.html`

### Step 2: TypeScript Types
- [x] Create `frontend/src/types/report.ts` -- TypeScript interfaces matching backend Pydantic schemas (AnalyzeResponse, TextStats, LinguisticFactor, PatternDetection)

### Step 3: API Client
- [x] Create `frontend/src/api/client.ts` -- typed fetch wrapper for POST /api/analyze with loading/error handling

### Step 4: TextInput Component
- [x] Create `frontend/src/components/TextInput.tsx` -- textarea with live character/word count, Analyze button (disabled when empty or loading), data-testid attributes

### Step 5: ScoreGauge Component
- [x] Create `frontend/src/components/ScoreGauge.tsx` -- large color-coded 0-100 gauge (green < 30, yellow 30-59, red >= 60) with animated fill

### Step 6: ClassificationBadge Component
- [x] Create `frontend/src/components/ClassificationBadge.tsx` -- classification label with matching background color

### Step 7: LinguisticFactors Component
- [x] Create `frontend/src/components/LinguisticFactors.tsx` -- card grid showing each factor with labeled bar/percentage, score contribution, and explanation

### Step 8: PatternBreakdown Component
- [x] Create `frontend/src/components/PatternBreakdown.tsx` -- table/cards grouped by category showing occurrence count, score contribution, matched details, explanation

### Step 9: ReportView Component
- [x] Create `frontend/src/components/ReportView.tsx` -- full report layout composing ScoreGauge, ClassificationBadge, stats bar, LinguisticFactors, PatternBreakdown, timestamp, "Analyze Another" button

### Step 10: App Component
- [x] Create `frontend/src/App.tsx` -- root SPA component managing view state (input/loading/report), error handling, handleAnalyze/handleReset
- [x] Create `frontend/src/App.css` -- Tailwind imports
- [x] Create `frontend/src/main.tsx` -- React entry point

### Step 11: Verify Build
- [x] Run `npm run build` to verify the frontend compiles without errors

### Step 12: Documentation Summary
- [x] Create `aidlc-docs/construction/unit-4-frontend/code/summary.md`

## Total: 12 steps
