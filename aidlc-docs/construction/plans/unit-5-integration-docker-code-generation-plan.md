# Code Generation Plan -- Unit 5: Integration & Docker

## Unit Context
- **Unit**: Integration & Docker
- **Requirements**: NFR-03 (integration tests, corpus, coverage), NFR-04 (Docker Compose)
- **Dependencies**: Unit 3 (backend), Unit 4 (frontend)
- **Code Location**: Workspace root (Dockerfiles, docker-compose.yml), `backend/tests/` (integration tests, corpus)

## Generation Steps

### Step 1: Test Corpus
- [x] Create `backend/tests/corpus/ai_essay_01.txt` -- AI-generated essay on a general topic (produced by LLM)
- [x] Create `backend/tests/corpus/ai_essay_02.txt` -- second AI-generated essay
- [x] Create `backend/tests/corpus/human_essay_01.txt` -- human-written text (pre-2017 public domain or personal)
- [x] Create `backend/tests/corpus/human_essay_02.txt` -- second human-written text

### Step 2: Integration Tests
- [x] Update `backend/tests/test_api.py` with corpus-based integration tests:
  - AI essay 01 scores >= 60
  - AI essay 02 scores >= 60
  - Human essay 01 scores < 30
  - Human essay 02 scores < 30
  - Response schema matches AnalyzeResponse model

### Step 3: Backend Dockerfile
- [x] Create `backend/Dockerfile` -- Python 3.12 slim, install uv, sync dependencies, copy app, download nltk data, expose 8000, run uvicorn

### Step 4: Frontend Dockerfile
- [x] Create `frontend/Dockerfile` -- multi-stage: Node build stage (npm install + build), nginx serve stage (serve dist/, proxy /api to backend)
- [x] Create `frontend/nginx.conf` -- nginx config for SPA routing + API proxy

### Step 5: Docker Compose
- [x] Create `docker-compose.yml` at workspace root -- backend service (port 8000), frontend service (port 3000), depends_on

### Step 6: Run Integration Tests
- [x] Run full test suite including corpus-based integration tests
- [ ] Verify AI essays score >= 60 and human essays score < 30

### Step 7: Coverage Check
- [x] Run pytest with coverage to verify >= 85% on backend/app/

### Step 8: Documentation Summary
- [x] Create `aidlc-docs/construction/unit-5-integration-docker/code/summary.md`

## Total: 8 steps
