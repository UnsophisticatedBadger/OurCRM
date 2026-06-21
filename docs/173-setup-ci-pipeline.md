# US-173: Setup CI Pipeline

## User Story

**As a** developer
**I want to** have automated checks run on every push and pull request
**So that** code quality is enforced consistently without manual intervention

## Priority

**MVP:** Must Have

**Rationale:** Automated CI catches regressions before they reach main and enforces the same quality gates locally and in the pipeline.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Create GitHub Actions workflow file
- 1 hour: Configure uv caching for fast installs
- 1 hour: Wire up ruff, mypy, pytest steps
- 1 hour: Verify pipeline passes on a test PR
- 1 hour: Document the pipeline

## Dependencies

**Depends on:** US-001 (Setup Dev Environment), US-003 (Run Linters), US-004 (Run Test Suite)

**Blocks:** All future slices (CI must be green before merging)

## Description

A GitHub Actions workflow should run automatically on every push and pull request to `main`. The pipeline must pass before a PR can be merged. It runs the same commands developers run locally:

1. `uv sync` — install all dependencies
2. `uv run ruff check .` — lint
3. `uv run ruff format --check .` — formatting check
4. `uv run mypy src/ scripts/` — type checking
5. `uv run pytest` — tests with coverage

The pipeline should use uv caching to keep install times under 60 seconds.

## Acceptance Criteria

- [x] Workflow file exists at `.github/workflows/ci.yml`
- [x] Pipeline triggers on push and pull_request to main
- [x] Pipeline runs on ubuntu-latest with Python 3.14
- [x] uv is installed and dependencies are cached
- [x] ruff check passes
- [x] ruff format --check passes
- [x] mypy src/ scripts/ tests/ passes
- [x] pytest passes with coverage
- [x] Pipeline status is visible on PRs
- [x] Failed steps produce clear error messages
