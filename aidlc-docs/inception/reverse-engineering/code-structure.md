# Code Structure

## Build System
- **Type**: Vite 8 with TypeScript
- **Configuration**: vite.config.ts (React plugin, Tailwind CSS plugin, API proxy to localhost:8000)

## Key Modules

```
frontend/src/
  main.tsx          -- App entry point, renders React root
  App.tsx           -- Main app component, state management, view routing
  index.css         -- Tailwind CSS import
  types/
    report.ts       -- TypeScript interfaces for API response
  api/
    client.ts       -- API client (fetch wrapper for /api/analyze)
  components/
    TextInput.tsx         -- Text area with char/word counter and analyze button
    ReportView.tsx        -- Report layout: gauge, badge, stats, factors, patterns
    ScoreGauge.tsx        -- Visual semicircular gauge (0-100) with color coding
    ClassificationBadge.tsx -- Colored pill badge for classification label
    LinguisticFactors.tsx -- Grid of factor cards with progress bars
    PatternBreakdown.tsx  -- List of pattern detection cards with detail tags
```

### Existing Files Inventory
- `frontend/src/main.tsx` - React app entry point with StrictMode
- `frontend/src/App.tsx` - Root component with view state machine (input/loading/report)
- `frontend/src/index.css` - Single Tailwind import
- `frontend/src/types/report.ts` - TypeScript interfaces: TextStats, LinguisticFactor, PatternDetection, AnalyzeResponse
- `frontend/src/api/client.ts` - API client function analyzeText()
- `frontend/src/components/TextInput.tsx` - Text input with real-time character/word counting
- `frontend/src/components/ReportView.tsx` - Report layout with StatCard helper
- `frontend/src/components/ScoreGauge.tsx` - CSS-based semicircular gauge with needle
- `frontend/src/components/ClassificationBadge.tsx` - Score-colored classification pill
- `frontend/src/components/LinguisticFactors.tsx` - Factor cards in responsive grid
- `frontend/src/components/PatternBreakdown.tsx` - Pattern detection list with detail chips
- `frontend/index.html` - HTML shell
- `frontend/vite.config.ts` - Vite configuration
- `frontend/package.json` - Dependencies and scripts
- `frontend/Dockerfile` - Multi-stage build (node -> nginx)
- `frontend/nginx.conf` - Production nginx config
- `frontend/public/favicon.svg` - App favicon
- `frontend/public/icons.svg` - Icon sprites

## Design Patterns
### View State Machine
- **Location**: App.tsx
- **Purpose**: Manages UI state transitions between input, loading, and report views
- **Implementation**: React useState with 'input' | 'loading' | 'report' union type

### Score-Based Color Coding
- **Location**: ScoreGauge, ClassificationBadge, LinguisticFactors
- **Purpose**: Consistent visual feedback based on score thresholds (<30 green, 30-60 yellow, >60 red)
- **Implementation**: Helper functions returning Tailwind classes or CSS color values

## Critical Dependencies
### React 19
- **Version**: ^19.2.4
- **Usage**: All UI components
- **Purpose**: UI rendering framework

### Tailwind CSS 4
- **Version**: ^4.2.2
- **Usage**: All styling via utility classes
- **Purpose**: Utility-first CSS framework

### Vite 8
- **Version**: ^8.0.1
- **Usage**: Build system and dev server
- **Purpose**: Fast development and production builds
