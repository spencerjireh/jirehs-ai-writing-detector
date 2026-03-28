# Unit 4: Frontend -- Code Summary

## Files Created

| File | Purpose |
|------|---------|
| `frontend/src/types/report.ts` | TypeScript interfaces matching backend Pydantic schemas |
| `frontend/src/api/client.ts` | Typed fetch wrapper for POST /api/analyze |
| `frontend/src/components/TextInput.tsx` | Textarea with live char/word count, Analyze button |
| `frontend/src/components/ScoreGauge.tsx` | Color-coded 0-100 gauge (green/yellow/red) |
| `frontend/src/components/ClassificationBadge.tsx` | Classification label with color |
| `frontend/src/components/LinguisticFactors.tsx` | Factor cards with bar indicators and explanations |
| `frontend/src/components/PatternBreakdown.tsx` | Detection cards with match details |
| `frontend/src/components/ReportView.tsx` | Full report layout composing all report components |

## Files Modified

| File | Change |
|------|--------|
| `frontend/src/App.tsx` | Replaced Vite scaffold with SPA (input/loading/report states) |
| `frontend/src/main.tsx` | Cleaned up import path |
| `frontend/src/index.css` | Replaced scaffold CSS with Tailwind import |
| `frontend/vite.config.ts` | Added Tailwind plugin and API proxy to localhost:8000 |

## Build Results
- TypeScript type check: passes (zero errors)
- Production build: succeeds (198KB JS gzip 62KB, 18KB CSS gzip 4.5KB)

## Component Data Flow
```
App (state: input/loading/report)
  -> TextInput -> handleAnalyze -> analyzeText (fetch)
  -> ReportView -> ScoreGauge, ClassificationBadge, stats, LinguisticFactors, PatternBreakdown
  -> "Analyze Another" -> handleReset -> back to TextInput
```
