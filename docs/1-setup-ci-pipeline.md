# #1 — CI Pipeline

**Capability:** infrastructure
**Milestone:** Foundation
**Status:** Done
**GitHub Issue:** #1

## User Story
As a developer, I want automated checks to run on every push and pull request, so that code quality is enforced consistently without manual intervention.

## Acceptance Criteria
1. Workflow file exists at `.github/workflows/ci.yml` and triggers on push and pull_request to main
2. Pipeline runs on ubuntu-latest with Python 3.14 and installs dependencies via `uv sync` with caching
3. `uv run ruff check .` runs and must pass
4. `uv run ruff format --check .` runs and must pass
5. `uv run mypy src/ scripts/ tests/` runs and must pass
6. `uv run pytest` runs with coverage and must pass
7. Failed steps produce clear error output visible in the GitHub Actions log
8. Pipeline status is shown on pull requests before merge

## Test Locations
| Artifact | Path |
|----------|------|
| Manual tests | `tests/manual/infrastructure/ci-pipeline.md` |

## Definition of Done
- [x] Workflow file exists at `.github/workflows/ci.yml`
- [x] Pipeline triggers on push and pull_request to main
- [x] ruff, mypy, and pytest steps all pass
- [x] uv caching is in place
- [x] Pipeline status visible on PRs
- [x] Wiki documentation: N/A — internal CI/build tooling, no user-visible surface
