# US-008: Create First Test

## User Story

**As a** developer  
**I want to** create the first test  
**So that** I can verify the testing framework works and establish testing patterns

## Priority

**MVP:** Must Have

**Rationale:** The first test proves that the testing framework is set up correctly and establishes patterns that all future tests will follow. Without a working first test, we cannot verify any code.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Create test file structure
- 1 hour: Write first test
- 1 hour: Run the test and verify it passes
- 1 hour: Write a failing test to verify the framework catches failures
- 1 hour: Document testing patterns
- 1 hour: Set up test configuration

## Dependencies

**Depends on:** US-001 (Setup Development Environment), US-007 (Create Initial Project Structure)

**Blocks:** US-020 (Create Contact), all feature development with tests

## Description

A developer should create the first automated test that verifies a basic piece of functionality. This test should be simple but meaningful, demonstrating the testing framework setup and establishing patterns for future tests. The test should be runnable, should pass, and should provide a foundation for test-driven development.

The first test serves multiple purposes: it verifies that the testing framework is properly configured, it establishes testing patterns and conventions, and it gives developers confidence that the testing infrastructure works.

## Acceptance Criteria

- [x] First test is created and passes
- [x] Test framework discovers tests automatically
- [x] Test output is clear and readable
- [x] Failed tests show enough detail to debug
- [x] Test coverage is reported
- [x] Tests can be run individually or all at once
- [x] Test naming conventions are established
- [x] Test file structure is documented
- [x] Testing patterns are documented for future tests
- [x] Test configuration is in pyproject.toml
- [ ] Tests work on Windows, macOS, and Linux — see tests/manual/infrastructure.md