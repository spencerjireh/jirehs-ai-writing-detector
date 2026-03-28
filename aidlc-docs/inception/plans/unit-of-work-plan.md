# Unit of Work Plan

## Plan Overview
Decompose the AI Writing Detector into balanced implementation units. The component dependency chain is strictly linear (config -> preprocessing -> detectors -> analyzers -> scoring -> report -> API -> frontend), so units must be built sequentially.

## Artifacts to Generate
- [x] unit-of-work.md -- Unit definitions, responsibilities, and code organization
- [x] unit-of-work-dependency.md -- Unit dependency matrix and build order
- [x] unit-of-work-story-map.md -- Mapping of spec requirements to units
- [x] Validate unit boundaries and dependencies

## Proposed Decomposition

Based on the 15 backend + 9 frontend components defined in Application Design, I propose **5 units**:

| Unit | Name | Components | Spec Phases |
|------|------|------------|-------------|
| 1 | Backend Foundation | config, models, preprocessing, base detector, API skeleton | 0, 1 |
| 2 | Pattern Detectors | vocabulary, structural, vague language, emphasis detectors + registry | 2, 3, 4, 5 |
| 3 | Analyzers & Scoring | linguistic analyzers, readability, aggregator, report builder | 6, 7, 8 |
| 4 | Frontend | React app, all UI components, API client, types | 9 |
| 5 | Integration & Docker | Integration tests, Docker Compose, end-to-end validation | 10 |

Build order: 1 -> 2 -> 3 -> 4 -> 5 (strictly sequential)

## Questions

### Question 1
Does this 5-unit decomposition match your expectations, or would you prefer a different granularity?

A) 5 units as proposed above -- good balance of testability and efficiency
B) 3 units (backend, frontend, Docker) -- faster iteration, fewer approval gates
C) Follow the spec's 10 phases exactly -- maximum granularity, more checkpoints
D) Other (please describe after [Answer]: tag below)

[Answer]: A
