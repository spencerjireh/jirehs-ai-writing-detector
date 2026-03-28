# Component Inventory

## Application Packages
- **frontend** - React SPA for text input and report display
- **backend** - FastAPI text analysis engine

## Infrastructure Packages
- **frontend/Dockerfile** - Docker - Multi-stage build (node:22-slim -> nginx:alpine)
- **frontend/nginx.conf** - Nginx - Production reverse proxy and static serving
- **backend/Dockerfile** - Docker - Backend container (if exists)

## Shared Packages
- **frontend/src/types/report.ts** - TypeScript type definitions shared across frontend components

## Test Packages
- **backend/tests/** - Backend unit and integration tests
- **frontend** - No frontend tests exist

## Total Count
- **Total Packages**: 2
- **Application**: 2 (frontend, backend)
- **Infrastructure**: 2 (Dockerfiles)
- **Shared**: 1 (types)
- **Test**: 1 (backend only)
