# Build Instructions

## Prerequisites
- **Build Tool**: Vite 8.0.3 with TypeScript 5.9.3
- **Runtime**: Node.js 22+
- **Package Manager**: npm
- **Dependencies**: React 19, Tailwind CSS 4 (dev dependencies only)
- **Environment Variables**: None required for frontend build
- **External Requirements**: Internet access for Google Fonts loading at runtime

## Build Steps

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Build All Units
```bash
npm run build
```
This runs `tsc -b` (TypeScript compilation) followed by `vite build` (production bundling).

### 3. Verify Build Success
- **Expected Output**:
  - `tsc -b` completes with 0 errors
  - Vite reports 3 output files: `index.html`, CSS bundle, JS bundle
  - Build completes in <200ms
- **Build Artifacts**:
  - `frontend/dist/index.html` (~0.89 KB)
  - `frontend/dist/assets/index-*.css` (~25 KB, ~5.5 KB gzipped)
  - `frontend/dist/assets/index-*.js` (~207 KB, ~63 KB gzipped)
- **Common Warnings**: None expected

### 4. Lint Check
```bash
npm run lint
```
Should complete with 0 warnings, 0 errors.

### 5. Preview Production Build
```bash
npm run preview
```
Opens production build at `http://localhost:4173`. Verify:
- Fonts load correctly (Playfair Display, Source Serif 4, JetBrains Mono)
- Page renders with editorial styling
- No console errors

## Troubleshooting

### Fonts Not Loading
- **Cause**: Google Fonts CDN blocked or offline
- **Solution**: Fonts use `font-display: swap` so the UI renders with fallback serif/monospace fonts. Check network tab for blocked requests.

### Build Fails with TypeScript Errors
- **Cause**: Type mismatches or missing imports
- **Solution**: Run `npx tsc --noEmit` for detailed error messages. All components use interfaces from `types/report.ts` which is unchanged.

### Tailwind Classes Not Applied
- **Cause**: Tailwind v4 not processing CSS
- **Solution**: Verify `@tailwindcss/vite` plugin is in `vite.config.ts` and `@import "tailwindcss"` is first line of `index.css`.
