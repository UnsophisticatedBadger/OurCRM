# US-003: Run Linters and Formatters

## User Story

**As a** developer  
**I want to** run linters and formatters on my code  
**So that** code style is consistent and I catch common errors

## Priority

**MVP:** Must Have

**Rationale:** Consistent code style and early error detection are essential for maintainable code, especially in a collaborative open-source project.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Configure ruff in pyproject.toml
- 1 hour: Configure mypy in pyproject.toml
- 1 hour: Test that tools run successfully
- 2 hours: Document usage in README
- 1 hour: Add to development workflow documentation

## Dependencies

**Depends on:** US-001 (Setup Development Environment)

**Blocks:** US-004 (Run Test Suite), US-020 (Create Contact)

## Description

A developer should be able to run linting and formatting tools with simple commands. The tools should check for code style issues, common errors, and type safety problems. The tools should be configured to work with the OurCRM codebase out of the box.

Linters catch syntax errors, unused imports, undefined variables, and style violations. Type checkers catch type mismatches before runtime. Running these tools frequently prevents small issues from accumulating.

## Acceptance Criteria

- [x] Linter runs with a simple command
- [x] Formatter runs with a simple command
- [x] Type checker runs with a simple command
- [x] Tools catch common style issues
- [x] Tools catch common type errors
- [ ] Tools work on Windows, macOS, and Linux — see tests/manual/infrastructure.md
- [x] Configuration is documented in README
- [x] Tools can be run individually or all at once
- [x] Exit codes properly indicate success or failure
- [x] Error messages are clear and actionable