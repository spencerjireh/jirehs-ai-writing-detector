# Unit Test Execution

## Current State
No frontend unit tests exist in this project. The redesign preserved all existing component interfaces, so no new unit tests were added as part of this visual-only change.

## Recommended Future Unit Tests

### ThemeToggle Component
```
- Renders sun icon in light mode
- Renders moon icon in dark mode
- Toggles dark class on html element
- Persists theme to localStorage
- Reads initial theme from localStorage
- Falls back to system preference when no stored theme
```

### ScoreGauge Component
```
- Renders SVG arc with correct viewBox
- Displays score value in data-testid="score-value"
- Clamps score between 0 and 100
- Shows correct label for low/moderate/high scores
- Applies correct color for score thresholds (<30, 30-60, >60)
```

### App Component
```
- Renders header with title and theme toggle
- Shows TextInput in initial state
- Shows loading indicator during analysis
- Shows ReportView after successful analysis
- Shows error message on analysis failure
- Reset returns to input view
```

## Running Tests (When Implemented)
```bash
# Install test dependencies first:
npm install -D vitest @testing-library/react @testing-library/jest-dom jsdom

# Run tests:
npx vitest run

# Run with coverage:
npx vitest run --coverage
```
