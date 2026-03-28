# Unit 5: Integration & Docker -- Code Summary

## Files Created

| File | Purpose |
|------|---------|
| `backend/tests/corpus/ai_essay_01.txt` | AI-generated essay on AI/technology |
| `backend/tests/corpus/ai_essay_02.txt` | AI-generated essay on sustainable energy |
| `backend/tests/corpus/human_essay_01.txt` | Human-written personal narrative (dog story) |
| `backend/tests/corpus/human_essay_02.txt` | Human-written personal narrative (gas station summer) |
| `backend/Dockerfile` | Python 3.12 slim + uv + nltk data |
| `frontend/Dockerfile` | Multi-stage: Node build + nginx serve |
| `frontend/nginx.conf` | SPA routing + /api proxy to backend |
| `docker-compose.yml` | Backend (8000) + Frontend (3000) |

## Files Modified

| File | Change |
|------|--------|
| `backend/tests/test_api.py` | Added 6 corpus-based integration tests + schema validation |

## Test Results
- **127 total tests**, all passing
- Corpus integration: AI essays score >= 60, human essays score < 30
- Response schema validation passes

## Coverage
- **97% line coverage** on backend/app/ (target: 85%)
- All detectors at 100%
- Lowest: routes.py at 81% (graceful degradation error paths)

## Docker Architecture
```
docker-compose.yml
  backend (port 8000) -- FastAPI + uvicorn
  frontend (port 3000) -- nginx serving static build + /api proxy
```
