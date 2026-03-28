# Requirements Verification Questions

The spec.md is comprehensive. These questions target the open questions listed in Section 8, plus a few gaps the spec does not address.

---

## Question 1
**Sentence Tokenizer** (spec Section 8, Open Question #1): Which approach should be used for sentence tokenization?

A) Regex-based -- minimal dependencies, good enough for English prose, easier to test deterministically
B) nltk.sent_tokenize -- more accurate with abbreviations and edge cases, adds nltk as a dependency
C) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 2
**Rare Word Detection** (spec Section 8, Open Question #2): How should the rare word frequency list be provided?

A) Bundled frequency file (e.g., a top-5000 English word list committed to the repo)
B) Small external package (e.g., wordfreq library)
C) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 3
**Frontend Styling** (spec Section 8, Open Question #4): Which CSS approach for the React frontend?

A) Tailwind CSS -- utility-first, fast prototyping, larger initial setup
B) Plain CSS (or CSS Modules) -- no framework dependency, full control, more manual work
C) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 4
**Python Dependency Management**: The spec lists requirements.txt but does not specify the toolchain. Which approach?

A) pip + requirements.txt (simple, standard)
B) Poetry (lock file, virtual env management, pyproject.toml)
C) uv (fast resolver, drop-in pip replacement, growing ecosystem)
D) Other (please describe after [Answer]: tag below)

[Answer]: C

## Question 5
**Deployment Target**: The spec does not specify how the app will be run. What is the intended deployment?

A) Local development only (run with uvicorn + vite dev server)
B) Docker Compose (containerized backend + frontend, single docker-compose.yml)
C) Cloud deployment (specify provider after [Answer]: tag)
D) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 6
**Minimum Text Length**: The spec requires non-empty text but does not define a minimum length for meaningful analysis. Should there be a minimum word count?

A) No minimum beyond non-empty -- analyze whatever is submitted
B) Minimum ~50 words -- short texts produce unreliable statistical measures (lexical diversity, sentence variation)
C) Minimum ~100 words -- more reliable linguistic analysis
D) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 7: Security Extensions
Should security extension rules be enforced for this project?

A) Yes -- enforce all SECURITY rules as blocking constraints (recommended for production-grade applications)
B) No -- skip all SECURITY rules (suitable for PoCs, prototypes, and experimental projects)
C) Other (please describe after [Answer]: tag below)

[Answer]: B
