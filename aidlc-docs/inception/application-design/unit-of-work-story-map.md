# Unit of Work -- Requirements Map

Since User Stories were skipped, this document maps spec requirements (from requirements.md) to units.

## Requirements to Unit Mapping

| Requirement | Description | Unit | Spec Phase |
|-------------|-------------|------|------------|
| FR-01 | Text Analysis API (endpoint definition) | Unit 1 (skeleton), Unit 3 (full wiring) | 0, 1, 8 |
| FR-02 | Text Preprocessing (nltk tokenization, stats) | Unit 1 | 1 |
| FR-03 | Pattern Detectors (vocabulary, structural, vague, emphasis) | Unit 2 | 2, 3, 4, 5 |
| FR-04 | Linguistic Analyzers (7 statistical analyzers) | Unit 3 | 6 |
| FR-05 | Score Aggregation (sum, normalize, classify) | Unit 3 | 7 |
| FR-06 | Report Builder (assemble response) | Unit 3 | 8 |
| FR-07 | Configuration (YAML loading, validation) | Unit 1 | 0 |
| FR-08 | Frontend (React SPA, input/report views) | Unit 4 | 9 |
| FR-09 | No Minimum Text Length | Unit 1 (validation) | 0 |
| NFR-01 | Technology Stack | Unit 1 (backend), Unit 4 (frontend) | - |
| NFR-02 | Project Structure (monorepo) | Unit 1 | 0 |
| NFR-03 | Testing (corpus, coverage) | Unit 2 + 3 (unit tests), Unit 5 (integration) | - |
| NFR-04 | Deployment (Docker Compose) | Unit 5 | 10 |
| NFR-05 | Security (basic Pydantic validation) | Unit 1 | - |
| NFR-06 | CORS | Unit 1 | 0 |

## Coverage Verification

All 9 functional requirements and 6 non-functional requirements are assigned to at least one unit. No orphaned requirements.

## Unit Workload Estimate

| Unit | Requirements | Components | Test Files | Relative Size |
|------|-------------|------------|------------|---------------|
| 1 | FR-01 (partial), FR-02, FR-07, FR-09, NFR-01-02, NFR-05-06 | 8 | 3 | Medium |
| 2 | FR-03 | 5 | 5 | Large |
| 3 | FR-04, FR-05, FR-06, FR-01 (full wiring) | 4 | 4 | Large |
| 4 | FR-08, NFR-01 (frontend) | 9 | 0-1 | Medium |
| 5 | NFR-03 (integration), NFR-04 | 4 | 1 | Small |
