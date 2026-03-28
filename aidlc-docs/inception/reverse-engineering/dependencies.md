# Dependencies

## Internal Dependencies

```
Frontend SPA
    |
    +-- src/App.tsx (root component)
    |       |
    |       +-- src/api/client.ts (API communication)
    |       +-- src/components/TextInput.tsx
    |       +-- src/components/ReportView.tsx
    |               |
    |               +-- src/components/ScoreGauge.tsx
    |               +-- src/components/ClassificationBadge.tsx
    |               +-- src/components/LinguisticFactors.tsx
    |               +-- src/components/PatternBreakdown.tsx
    |
    +-- src/types/report.ts (shared by api/client.ts and all report components)
```

### App.tsx depends on TextInput, ReportView, api/client
- **Type**: Compile
- **Reason**: Root component orchestrates views and data flow

### ReportView depends on ScoreGauge, ClassificationBadge, LinguisticFactors, PatternBreakdown
- **Type**: Compile
- **Reason**: Composes the full report display from sub-components

### All report components depend on types/report.ts
- **Type**: Compile
- **Reason**: TypeScript interfaces for AnalyzeResponse and sub-types

## External Dependencies

### react (^19.2.4)
- **Purpose**: UI component rendering
- **License**: MIT

### react-dom (^19.2.4)
- **Purpose**: React DOM rendering
- **License**: MIT

### tailwindcss (^4.2.2)
- **Purpose**: Utility-first CSS framework
- **License**: MIT

### vite (^8.0.1)
- **Purpose**: Build tool and dev server
- **License**: MIT

### typescript (~5.9.3)
- **Purpose**: Type safety and compilation
- **License**: Apache-2.0
