# Integration Test Instructions

## Purpose
Test the frontend-to-backend integration to ensure the redesigned UI correctly communicates with the API and displays results.

## Test Scenarios

### Scenario 1: Full Analysis Flow
- **Description**: Submit text through the UI and verify the complete report renders
- **Setup**: Start backend (`cd backend && uvicorn app.main:app --port 8000`) and frontend dev server (`cd frontend && npm run dev`)
- **Test Steps**:
  1. Open `http://localhost:5173`
  2. Paste sample text into the textarea
  3. Click "Analyze" button
  4. Wait for loading state to appear (animated dots)
  5. Verify report renders with: score gauge, classification badge, stats bar, linguistic factors, pattern detections
- **Expected Results**:
  - Score gauge shows SVG arc with animated fill
  - Classification badge shows label with correct color
  - Stats bar shows 4 stat cards (words, characters, sentences, avg length)
  - Linguistic factors section renders if factors present
  - Pattern detections section renders if detections present
- **Cleanup**: None

### Scenario 2: Theme Switching
- **Description**: Verify dark/light mode works across all views
- **Test Steps**:
  1. Click theme toggle (sun/moon icon in header)
  2. Verify background changes from warm white to charcoal
  3. Verify all text remains readable
  4. Submit text and verify report renders correctly in dark mode
  5. Toggle back to light mode and verify
  6. Refresh page and verify theme persists
- **Expected Results**: Smooth transition, all content readable in both modes, localStorage preserves preference

### Scenario 3: Error Handling
- **Description**: Verify error display when backend is unavailable
- **Test Steps**:
  1. Stop the backend server
  2. Submit text via the frontend
  3. Verify error message appears with editorial styling
- **Expected Results**: Red-styled error banner with descriptive message, returns to input view

### Scenario 4: Responsive Layout
- **Description**: Verify layout on mobile and desktop viewports
- **Test Steps**:
  1. Open browser DevTools, toggle device toolbar
  2. Test at 320px, 768px, and 1280px widths
  3. Navigate through input -> loading -> report at each width
- **Expected Results**: All content readable, no horizontal overflow, stats grid collapses to 2 columns on mobile

## Setup Integration Test Environment

### 1. Start Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 2. Start Frontend Dev Server
```bash
cd frontend
npm install
npm run dev
```

### 3. Alternative: Docker Compose
```bash
docker-compose up --build
# Frontend at http://localhost (port 80)
```
