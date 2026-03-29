# Iteration 2 Requirements - Text Visibility in Report View

## Intent Analysis
- **User Request**: "i would like to see the text even in the analyzed screen"
- **Request Type**: Enhancement
- **Scope**: Single component area (frontend only -- App.tsx, ReportView, TextInput)
- **Complexity**: Simple-to-Moderate (state lifting + layout restructure)

## Functional Requirements

### FR-1: Persistent Text Display
The analyzed text MUST remain visible in the report view at all times after analysis completes. The text appears in a read-only block that is always visible (not hidden behind a toggle or collapsible panel).

### FR-2: Inline Editing and Re-Analysis
The user MUST be able to edit the displayed text directly in the report view and trigger a re-analysis without navigating back to the input screen. This requires:
- An editable textarea in the report view
- A re-analyze button/action
- Loading state handling during re-analysis
- Report updates in-place when new results arrive

### FR-3: Full-Width Responsive Layout
The layout MUST expand to use the full viewport width with appropriate padding, replacing the current narrow max-w-2xl constraint. This accommodates the additional text content alongside the analysis results. On mobile, content stacks vertically.

### FR-4: Preserve "Analyze Another" Flow
The existing "Analyze Another" button MUST be retained, allowing users to clear both the text and report to start completely fresh.

## Non-Functional Requirements

### NFR-1: Editorial Aesthetic Continuity
The current visual design system MUST be preserved:
- Playfair Display (display font)
- Source Serif 4 (body font)
- JetBrains Mono (monospace)
- Warm color palette (vermillion, emerald, amber)
- Grain overlay texture
- Staggered fade-in-up animations

### NFR-2: Responsive Design
- Mobile: single-column stacked layout (text above report)
- Desktop: full-width with appropriate padding and spacing
- Smooth transitions between states

### NFR-3: Preserved Test IDs
All existing data-testid attributes MUST be preserved for test compatibility:
- text-input, text-counter, analyze-button
- score-gauge, score-value, classification-badge
- stats-bar, linguistic-factors, pattern-breakdown
- report-view, reset-button, loading-indicator
- theme-toggle, error-message

## Technical Approach (High-Level)
1. Lift text state from TextInput up to App.tsx
2. Pass text + setText to both TextInput and ReportView
3. Add textarea + re-analyze button to ReportView
4. Change App.tsx layout container from max-w-2xl to full-width responsive
5. Handle re-analysis loading state within report view

## Out of Scope
- Backend changes (API remains unchanged)
- New components or pages
- Changes to scoring, detection, or analysis logic
