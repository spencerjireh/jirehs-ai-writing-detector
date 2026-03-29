# Iteration 2 - Code Generation Plan

## Unit Context
- **Unit**: Frontend text persistence + inline re-analysis
- **Scope**: 4 files modified, 0 files created
- **Dependencies**: None (frontend-only, backend API unchanged)

## Code Generation Steps

### Step 1: Modify TextInput.tsx - Accept external text state
- [x] Remove local `useState` for text
- [x] Change props interface to accept `text: string` and `onTextChange: (text: string) => void`
- [x] Replace `setText` calls with `onTextChange`
- [x] Preserve all existing styling, `data-testid` attributes, and counter logic
- **File**: `frontend/src/components/TextInput.tsx`
- **Type**: Modify existing

### Step 2: Modify App.tsx - Lift text state and widen layout
- [x] Add `text` and `setText` state at App level
- [x] Pass `text` and `onTextChange` to TextInput
- [x] Pass `text` to ReportView
- [x] Create `handleAnalyze` that uses the lifted text state
- [x] Add re-analysis handler that works from report view
- [x] Change layout container from `max-w-2xl` to full-width responsive with appropriate padding
- [x] Preserve all existing `data-testid` attributes, views, and error handling
- **File**: `frontend/src/App.tsx`
- **Type**: Modify existing

### Step 3: Modify ReportView.tsx - Add editable text area and re-analyze button
- [x] Add `text`, `onTextChange`, and `onReAnalyze` to ReportViewProps
- [x] Add editable textarea section above the score/report content showing the analyzed text
- [x] Add "Re-Analyze" button next to or below the textarea
- [x] Show character/word count for the text (consistent with TextInput)
- [x] Handle loading state during re-analysis (disable button, show indicator)
- [x] Preserve all existing report sections and `data-testid` attributes
- **File**: `frontend/src/components/ReportView.tsx`
- **Type**: Modify existing

### Step 4: Modify index.css - Full-width responsive layout adjustments
- [x] No CSS changes needed -- all layout handled via Tailwind classes (max-w-7xl, grid-cols, lg: breakpoints)
- [x] Editorial aesthetic preserved (no changes to palette, fonts, animations, grain overlay)
- **File**: `frontend/src/index.css`
- **Type**: No changes required

### Step 5: Build verification
- [x] Run TypeScript check (`npx tsc --noEmit`) -- 0 errors
- [x] Run Vite build (`npx vite build`) -- success (26.01 KB CSS, 210.21 KB JS)
- [x] Verify all 14 `data-testid` attributes present in source -- confirmed
- **Type**: Verification

## Files Summary

| File | Action | Key Changes |
|---|---|---|
| `frontend/src/components/TextInput.tsx` | Modify | Controlled component (text from parent) |
| `frontend/src/App.tsx` | Modify | Lift state, full-width layout, re-analysis handler |
| `frontend/src/components/ReportView.tsx` | Modify | Add textarea + re-analyze, receive text props |
| `frontend/src/index.css` | Modify | Responsive layout adjustments |

## Data-testid Preservation Checklist
- [x] text-input
- [x] text-counter
- [x] analyze-button
- [x] score-gauge
- [x] score-value
- [x] classification-badge
- [x] stats-bar
- [x] linguistic-factors
- [x] pattern-breakdown
- [x] report-view
- [x] reset-button
- [x] loading-indicator
- [x] theme-toggle
- [x] error-message
