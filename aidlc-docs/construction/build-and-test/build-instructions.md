# Build Instructions

## Prerequisites
- **Python**: 3.12+
- **uv**: latest (https://docs.astral.sh/uv/)
- **Node.js**: 22+
- **npm**: 10+
- **Docker** and **Docker Compose**: (optional, for containerized deployment)

## Backend Build

### 1. Install Dependencies
```bash
cd backend
uv sync --all-extras
```

### 2. Download NLTK Data
```bash
uv run python -c "import nltk; nltk.download('punkt_tab', quiet=True)"
```

### 3. Verify Backend Starts
```bash
uv run uvicorn app.main:app --port 8000
# Expected: "Uvicorn running on http://0.0.0.0:8000"
# Ctrl+C to stop
```

## Frontend Build

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Build for Production
```bash
npm run build
```
- **Expected Output**: `dist/` directory with `index.html`, CSS, and JS bundles
- **Acceptable Warnings**: Vite may warn about chunk sizes; this is non-blocking

### 3. Development Server
```bash
npm run dev
# Expected: "Local: http://localhost:5173/"
# API proxy forwards /api to localhost:8000
```

## Docker Build

### 1. Build and Start All Services
```bash
docker compose up --build
```
- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:3000

### 2. Stop Services
```bash
docker compose down
```

## Troubleshooting

### uv not found
- Install: `curl -LsSf https://astral.sh/uv/install.sh | sh`

### nltk punkt_tab download fails
- Ensure internet connectivity
- Alternatively: `uv run python -m nltk.downloader punkt_tab`

### Frontend proxy 502 errors
- Ensure backend is running on port 8000 before starting frontend dev server
