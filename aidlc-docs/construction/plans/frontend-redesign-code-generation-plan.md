# Code Generation Plan: Frontend UI/UX Redesign

**Unit**: frontend-redesign (single unit)
**Target**: /Users/spencerjireh.cebrian/Projects/jirehs-ai-writing-detector/frontend/

## Design Direction Summary
- **Aesthetic**: Editorial / Magazine -- bold typography, generous whitespace, asymmetric hierarchy
- **Theme**: Adaptive dark + light with CSS custom properties
- **Typography**: Google Fonts -- distinctive display + refined body + monospace accent
- **Motion**: Rich CSS animations + orchestrated reveals
- **Gauge**: SVG arc with animated gradient fill
- **Layout**: Single-scroll narrative

## Code Generation Steps

### Step 1: Foundation -- index.html + Google Fonts
- [x] Modify `frontend/index.html`
  - Add Google Fonts preconnect and stylesheet links
  - Font selections: **Playfair Display** (editorial display), **Source Serif 4** (body/reading), **JetBrains Mono** (data/monospace)
  - Add preload hints for critical font weights
  - Update page title to "AI Writing Detector"

### Step 2: Foundation -- CSS Design System (index.css)
- [x] Modify `frontend/src/index.css`
  - Define CSS custom properties for light and dark themes via `@theme`
  - Color palette: cream/warm white (light) vs deep charcoal (dark) backgrounds
  - Accent colors: editorial ink black, vermillion red, emerald green, amber gold
  - Typography scale using CSS custom properties
  - Base animation keyframes: fadeInUp, slideReveal, arcFill, shimmer
  - `prefers-reduced-motion` media query to disable animations
  - `prefers-color-scheme` media query for system theme detection
  - Smooth scrolling and selection styling
  - Noise/grain texture overlay via CSS for editorial atmosphere

### Step 3: Theme Infrastructure -- ThemeToggle component
- [x] Create `frontend/src/components/ThemeToggle.tsx`
  - Toggle button with sun/moon icons (inline SVG, no dependency)
  - Read initial theme from localStorage, fallback to system preference
  - Toggle `dark` class on `<html>` element
  - Persist preference to localStorage
  - Smooth icon transition animation
  - `data-testid="theme-toggle"` attribute

### Step 4: App Shell -- App.tsx redesign
- [x] Modify `frontend/src/App.tsx`
  - Add ThemeToggle to header
  - Fix loading prop bug (pass actual loading state to TextInput)
  - Editorial header with Playfair Display heading, refined subtitle
  - Staggered entrance animation for header elements
  - View transitions with fade animations between input/loading/report
  - Atmospheric background: subtle gradient mesh or grain overlay
  - Refined error display with editorial styling

### Step 5: TextInput component redesign
- [x] Modify `frontend/src/components/TextInput.tsx`
  - Editorial-styled textarea: generous padding, refined border, warm background
  - Typography: Source Serif 4 for input text (matches analyzed content feel)
  - Character/word counter in monospace (JetBrains Mono)
  - Analyze button: bold editorial style with hover animation
  - Entrance animation: subtle fade-in on mount
  - Dark mode: inverted backgrounds and borders
  - Preserve all data-testid attributes

### Step 6: ScoreGauge component -- SVG arc rewrite
- [x] Modify `frontend/src/components/ScoreGauge.tsx`
  - Full SVG-based semicircular arc gauge
  - SVG gradient definitions: green -> yellow -> red
  - Animated arc fill using stroke-dasharray/stroke-dashoffset CSS animation
  - Large centered score number in Playfair Display
  - "out of 100" label in refined small text
  - Score-based color applied to number and arc
  - CSS animation: arc fills from 0 to score value over ~1.5s with easing
  - `prefers-reduced-motion`: skip animation, show final state
  - Preserve data-testid="score-gauge" and data-testid="score-value"

### Step 7: ClassificationBadge component redesign
- [x] Modify `frontend/src/components/ClassificationBadge.tsx`
  - Editorial pill with refined typography
  - Subtle border with score-based accent color
  - Entrance animation: fade + slight scale
  - Dark mode variant
  - Preserve data-testid="classification-badge"

### Step 8: ReportView component -- narrative layout
- [x] Modify `frontend/src/components/ReportView.tsx`
  - Single-scroll narrative flow with generous section spacing
  - Hero section: ScoreGauge + ClassificationBadge centered with dramatic whitespace
  - Stats bar: editorial stat blocks with JetBrains Mono numbers
  - Section headers: Playfair Display with decorative rule/line
  - Staggered reveal animation: each section fades in sequentially (animation-delay)
  - "Analyze Another" button: editorial ghost button with hover effect
  - Timestamp: refined footnote styling
  - Dark mode variants for all sections
  - Preserve all data-testid attributes

### Step 9: LinguisticFactors component redesign
- [x] Modify `frontend/src/components/LinguisticFactors.tsx`
  - Editorial card layout with refined borders
  - Progress bars: thin, elegant with smooth fill animation
  - Factor name in medium weight, contribution in monospace
  - Explanation text in refined body font
  - Staggered entrance: each factor card appears with delay
  - Dark mode variant
  - Preserve data-testid="linguistic-factors"

### Step 10: PatternBreakdown component redesign
- [x] Modify `frontend/src/components/PatternBreakdown.tsx`
  - Editorial list with clear visual hierarchy
  - Detail chips: refined tag style with subtle background
  - Occurrence count and score contribution in monospace
  - Category names as bold editorial labels
  - Staggered entrance animation
  - Dark mode variant
  - Preserve data-testid="pattern-breakdown"

### Step 11: Verification and Cleanup
- [x] Verify TypeScript compilation: `npm run build` -- PASSED (0 errors)
- [x] Verify all data-testid attributes preserved
- [ ] Verify dark/light theme switching works (visual check needed)
- [ ] Verify responsive layout on narrow viewports (visual check needed)
- [x] Fix any TypeScript errors -- none found

## Files Modified (10)
1. `frontend/index.html` -- font loading
2. `frontend/src/index.css` -- design system, themes, animations
3. `frontend/src/App.tsx` -- shell, theme toggle, transitions
4. `frontend/src/components/TextInput.tsx` -- editorial input
5. `frontend/src/components/ScoreGauge.tsx` -- SVG arc gauge
6. `frontend/src/components/ClassificationBadge.tsx` -- editorial badge
7. `frontend/src/components/ReportView.tsx` -- narrative layout
8. `frontend/src/components/LinguisticFactors.tsx` -- editorial factors
9. `frontend/src/components/PatternBreakdown.tsx` -- editorial patterns

## Files Created (1)
10. `frontend/src/components/ThemeToggle.tsx` -- dark/light toggle

## Unchanged Files
- `frontend/src/types/report.ts` -- no changes
- `frontend/src/api/client.ts` -- no changes
- `frontend/src/main.tsx` -- no changes
- `frontend/vite.config.ts` -- no changes
- `frontend/package.json` -- no new dependencies needed (CSS-only animations)
