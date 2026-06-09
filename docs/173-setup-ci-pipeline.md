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

## BDD Scenarios

### Scenario 1: Pipeline passes on clean code

```
Given a push is made to a branch with all checks passing
When the CI pipeline runs
Then all steps complete successfully
  And the pipeline reports green
```

### Scenario 2: Pipeline fails on lint error

```
Given a push is made with a ruff violation
When the CI pipeline runs
Then the ruff step fails
  And the pipeline reports red
  And the failure message identifies the violation
```

### Scenario 3: Pipeline fails on type error

```
Given a push is made with a mypy error
When the CI pipeline runs
Then the mypy step fails
  And the pipeline reports red
```

### Scenario 4: Pipeline fails on test failure

```
Given a push is made with a failing test
When the CI pipeline runs
Then the pytest step fails
  And the pipeline reports red
```

## Manual Testing Steps

### Test 1: Verify pipeline triggers on push

1. Push a commit to a feature branch
2. Open GitHub Actions tab
3. Verify the workflow starts automatically
4. Verify all steps run

### Test 2: Verify pipeline fails correctly

1. Introduce an intentional ruff violation
2. Push the commit
3. Verify the ruff step fails
4. Verify the error message is clear
5. Revert the violation

### Test 3: Verify caching works

1. Trigger the pipeline twice
2. Compare the install step duration
3. Verify the second run is faster due to caching

## Acceptance Criteria

- [ ] Workflow file exists at `.github/workflows/ci.yml`
- [ ] Pipeline triggers on push and pull_request to main
- [ ] Pipeline runs on ubuntu-latest with Python 3.13
- [ ] uv is installed and dependencies are cached
- [ ] ruff check passes
- [ ] ruff format --check passes
- [ ] mypy src/ scripts/ passes
- [ ] pytest passes with coverage
- [ ] Pipeline status is visible on PRs
- [ ] Failed steps produce clear error messages
