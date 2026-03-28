# Requirements Document: Frontend UI/UX Redesign

## Intent Analysis
- **User Request**: "Rework the frontend to be more beautiful. Same functionality but better UX/UI."
- **Request Type**: Enhancement - visual/UX redesign of existing frontend
- **Scope**: Multiple Components - all 6 frontend UI components + App shell + CSS
- **Complexity**: Moderate - significant visual overhaul, no business logic changes, no API changes

## Design Direction Summary
- **Aesthetic**: Editorial / Magazine - bold typography, generous whitespace, asymmetric layouts, strong editorial hierarchy
- **Theme**: Adaptive (dark + light modes)
- **Typography**: Maximum readability via Google Fonts - distinctive display font paired with refined body font
- **Motion**: Rich animations - orchestrated page loads, staggered reveals, animated gauge, scroll-triggered effects, hover states
- **Gauge**: SVG arc gauge with smooth animated fill and gradient color transitions
- **Layout**: Single-scroll narrative - continuous flow telling the "story" of the analysis
- **Fonts**: External Google Fonts allowed

---

## Functional Requirements

### FR-01: Preserve All Existing Functionality
All current features must remain fully functional:
- Text input with real-time character/word counting
- Analyze button with disabled state when text is empty
- API call to POST /api/analyze
- Loading state during analysis
- Error display on failure
- Full report display: score, classification, stats, linguistic factors, pattern detections, warnings, timestamp
- "Analyze Another" reset functionality

### FR-02: Adaptive Theme (Dark + Light Mode)
- System must detect user's OS color scheme preference
- Provide toggle for manual dark/light switching
- All components must render correctly in both modes
- Theme preference should persist (localStorage)
- Smooth transition between modes

### FR-03: SVG Arc Gauge
- Replace current CSS needle gauge with SVG-based arc gauge
- Smooth animated fill that transitions based on score (0-100)
- Gradient color transitions: green (low) -> yellow (mid) -> red (high)
- Score number prominently displayed in center
- Animation on initial render (progressive fill from 0 to score value)

### FR-04: Rich Animations
- Staggered entrance animations on page/view transitions
- Score gauge animated fill on report load
- Section-by-section reveal as user scrolls or as data loads
- Hover states on interactive elements (buttons, cards)
- Smooth view transitions between input -> loading -> report
- Loading state: engaging animation beyond a simple spinner

### FR-05: Single-Scroll Narrative Layout
- Report flows as a continuous story: score hero -> classification -> stats -> linguistic factors -> patterns -> reset
- Generous whitespace between sections
- Clear visual hierarchy guiding the eye downward
- No tabs or card grids -- one continuous editorial flow

### FR-06: Editorial Typography
- Load distinctive fonts via Google Fonts
- Display/heading font: bold, characterful, high-impact
- Body font: high-legibility, refined, optimized for reading
- Monospace accent font for data values and scores
- Proper typographic scale with clear hierarchy

### FR-07: Theme Toggle UI
- Accessible toggle control for dark/light mode
- Positioned in the header area
- Clear visual indication of current mode

---

## Non-Functional Requirements

### NFR-01: Performance
- Font loading must not block initial render (font-display: swap)
- Animations must run at 60fps (use CSS transforms/opacity, avoid layout thrashing)
- SVG gauge rendering must be performant
- Total added bundle size from new dependencies should be minimal

### NFR-02: Accessibility
- Maintain semantic HTML structure
- All interactive elements must be keyboard accessible
- Color contrast must meet WCAG AA in both themes
- Animations should respect prefers-reduced-motion
- Score gauge must have appropriate ARIA labels

### NFR-03: Responsiveness
- All layouts must work on mobile (320px+), tablet, and desktop
- Typography must scale appropriately
- SVG gauge must resize fluidly
- Narrative layout must be readable on all screen sizes

### NFR-04: Browser Compatibility
- Must work in modern browsers (Chrome, Firefox, Safari, Edge - latest 2 versions)
- CSS custom properties for theming
- No reliance on bleeding-edge features without fallbacks

### NFR-05: Code Quality
- Maintain existing TypeScript strict mode
- Keep component separation and single-responsibility pattern
- Fix existing loading prop bug (hardcoded false)
- No new external runtime dependencies beyond what's needed for animation (CSS preferred over JS libraries)

---

## Constraints
- **No backend changes** - API contract and backend remain untouched
- **No new routes** - single-page application stays single-page
- **TypeScript interfaces unchanged** - types/report.ts stays the same
- **Existing data-testid attributes preserved** - for any future testing compatibility
- **No functional regressions** - every feature that works today must work after redesign
