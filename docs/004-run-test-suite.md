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

## BDD Scenarios

### Scenario 1: Run all tests successfully

```
Given I am in the project root directory
  And all dependencies are installed
  And all tests are currently passing
When I run the test command
Then all tests should execute
  And all tests should pass
  And the command should exit with status code 0
  And I should see a summary showing the number of tests run
```

### Scenario 2: Run tests with failures

```
Given I am in the project root directory
  And there is at least one failing test
When I run the test command
Then the failing tests should be clearly identified
  And I should see details about why each test failed
  And the command should exit with a non-zero status code
  And the summary should show how many tests passed and failed
```

### Scenario 3: Run a specific test file

```
Given I am in the project root directory
  And there is a test file at tests/test_contacts.py
When I run the test command with the specific file
Then only the tests in that file should run
  And I should see results for those tests only
```

### Scenario 4: Run a specific test function

```
Given I am in the project root directory
  And there is a test function named test_create_contact
When I run the test command with the specific test name
Then only that test should run
  And I should see the result for that test
```

### Scenario 5: Generate coverage report

```
Given I am in the project root directory
When I run the test command with coverage enabled
Then a coverage report should be generated
  And the report should show the percentage of code covered
  And the report should identify which lines are not covered
```

## Manual Testing Steps

### Test 1: Verify test discovery works

1. Create a test file in the tests/ directory
2. Run the test command
3. Verify the new test is discovered and run
4. Verify the test appears in the output
5. Remove the test file

### Test 2: Verify test output is readable

1. Run the test suite
2. Check that passed tests are shown clearly
3. Check that failed tests show enough detail to debug
4. Check that the summary is at the end
5. Check that the output is not overwhelming

### Test 3: Verify coverage report is useful

1. Run tests with coverage
2. Open the coverage report
3. Verify it shows overall coverage percentage
4. Verify it shows coverage per file
5. Verify it highlights uncovered lines
6. Verify the report is easy to navigate

### Test 4: Verify tests can be run in isolation

1. Run a single test file
2. Verify only those tests run
3. Run a single test function
4. Verify only that test runs
5. Verify no side effects from other tests

### Test 5: Verify test suite performance

1. Note the current time
2. Run the full test suite
3. Measure how long it takes
4. Verify it's reasonable for the project size
5. Document the time for future reference

### Test 6: Verify cross-platform test execution

1. Run the test suite on Windows
2. Verify all tests pass
3. Run the test suite on macOS
4. Verify all tests pass
5. Run the test suite on Linux
6. Verify all tests pass
7. Document any platform-specific test failures

## Acceptance Criteria

- [ ] Test suite runs with a single command
- [ ] All tests are discovered automatically
- [ ] Test output clearly shows pass/fail status
- [ ] Failed tests provide enough detail to debug
- [ ] Individual tests or files can be run
- [ ] Coverage report is generated
- [ ] Coverage report shows per-file coverage
- [ ] Coverage report highlights uncovered lines
- [ ] Test suite runs in reasonable time
- [ ] Tests work on Windows, macOS, and Linux
- [ ] Testing workflow is documented in README