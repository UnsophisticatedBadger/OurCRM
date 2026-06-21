# US-009: Configure Code Quality Tools

## User Story

**As a** developer  
**I want to** configure linters, formatters, and type checkers  
**So that** code quality is enforced automatically and consistently

## Priority

**MVP:** Must Have

**Rationale:** Consistent code quality tools prevent style debates, catch common errors early, and make code reviews focus on logic rather than style. This is essential for a maintainable codebase.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Configure ruff in pyproject.toml
- 1 hour: Configure mypy in pyproject.toml
- 1 hour: Set up pre-commit hooks (optional)
- 2 hours: Test configuration on sample code
- 1 hour: Document configuration
- 1 hour: Add to development workflow

## Dependencies

**Depends on:** US-001 (Setup Development Environment), US-007 (Create Initial Project Structure)

**Blocks:** US-003 (Run Linters), all feature development

## Description

A developer should configure ruff for linting and formatting, and mypy for type checking. These tools should be configured in pyproject.toml with project-specific rules. The configuration should be strict enough to catch issues but not so strict that it becomes annoying.

The configuration should establish baseline rules that all code must follow. These tools will run automatically as part of the development workflow and in CI/CD (when we set that up).

## Acceptance Criteria

- [x] Ruff is configured in pyproject.toml
- [x] Mypy is configured in pyproject.toml
- [x] Configuration targets Python 3.14
- [x] Ruff catches common style issues
- [x] Ruff can auto-format code
- [x] Mypy catches type errors
- [x] Configuration is documented with comments
- [x] Tools work on the actual OurCRM codebase
- [x] Usage is documented in README
- [x] Tools are part of the development workflow
- [x] Configuration is not too strict or too lenient