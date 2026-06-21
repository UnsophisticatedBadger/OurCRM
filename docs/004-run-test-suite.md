# US-004: Run Test Suite

## User Story

**As a** developer  
**I want to** run the test suite  
**So that** I can verify my changes don't break existing functionality

## Priority

**MVP:** Must Have

**Rationale:** Automated tests are essential for catching regressions and ensuring code quality. Without tests, refactoring becomes risky and bugs slip through.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Configure pytest in pyproject.toml
- 1 hour: Configure pytest-cov for coverage
- 1 hour: Create test directory structure
- 1 hour: Write example test
- 2 hours: Document testing workflow
- 1 hour: Set up coverage reporting

## Dependencies

**Depends on:** US-001 (Setup Development Environment), US-003 (Run Linters)

**Blocks:** US-020 (Create Contact), all feature development

## Description

A developer should be able to run the entire test suite with a single command. The test suite should execute quickly, provide clear output about which tests passed and failed, and generate a coverage report. Tests should be organized in a logical structure that makes it easy to find and run specific tests.

The test suite should run in under 30 seconds for a small project and provide actionable feedback when tests fail. Coverage reports should show which lines of code are covered by tests and which are not.

## Acceptance Criteria

- [x] Test suite runs with a single command
- [x] All tests are discovered automatically
- [x] Test output clearly shows pass/fail status
- [x] Failed tests provide enough detail to debug
- [x] Individual tests or files can be run
- [x] Coverage report is generated
- [x] Coverage report shows per-file coverage
- [x] Coverage report highlights uncovered lines
- [x] Test suite runs in reasonable time
- [ ] Tests work on Windows, macOS, and Linux — see tests/manual/infrastructure.md
- [x] Testing workflow is documented in README