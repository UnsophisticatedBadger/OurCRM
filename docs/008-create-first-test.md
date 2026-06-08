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

## BDD Scenarios

### Scenario 1: Run a passing test

```
Given I have created a test file with a simple test
When I run the test command
Then the test should be discovered
  And the test should pass
  And I should see a success message
```

### Scenario 2: Run a failing test

```
Given I have created a test that should fail
When I run the test command
Then the test should be discovered
  And the test should fail
  And I should see a failure message with details about why it failed
```

### Scenario 3: Fix a failing test

```
Given I have a failing test
When I fix the code to make the test pass
  And I run the test command again
Then the test should pass
```

### Scenario 4: Run multiple tests

```
Given I have multiple test files
When I run the test command
Then all tests should be discovered
  And all tests should run
  And I should see results for all tests
```

### Scenario 5: Run a specific test

```
Given I have multiple tests
When I run the test command with a specific test name
Then only that test should run
  And I should see results for that test only
```

## Manual Testing Steps

### Test 1: Create and run a simple test

1. Create a file at tests/test_main.py
2. Add a simple test function:
   ```python
   def test_ourcrm_imports():
       """Verify that ourcrm can be imported."""
       import ourcrm
       assert ourcrm is not None
   ```
3. Run the test command
4. Verify the test is discovered
5. Verify the test passes
6. Check the output is clear and readable

### Test 2: Verify test failure handling

1. Create a test that intentionally fails:
   ```python
   def test_intentional_failure():
       """This test should fail."""
       assert 1 == 2
   ```
2. Run the test command
3. Verify the test is discovered
4. Verify the test fails
5. Verify the failure message is clear
6. Verify the test framework shows where the failure occurred
7. Remove the failing test

### Test 3: Test test isolation

1. Create two tests that modify shared state
2. Run them individually
3. Verify they both pass
4. Run them together
5. Verify they both still pass
6. Document any isolation issues

### Test 4: Test test discovery patterns

1. Create test files with different names:
   - test_something.py
   - test_another.py
   - something_test.py
2. Run the test command
3. Verify which files are discovered
4. Verify the naming convention is documented
5. Adjust configuration if needed

### Test 5: Test coverage reporting

1. Run tests with coverage enabled
2. Verify a coverage report is generated
3. Open the coverage report
4. Verify it shows which lines are covered
5. Verify the report is easy to understand
6. Document how to read the report

### Test 6: Test test output formats

1. Run tests with different output formats
2. Try verbose mode
3. Try quiet mode
4. Try JSON output
5. Determine which format is best for OurCRM
6. Document the recommended format

## Acceptance Criteria

- [ ] First test is created and passes
- [ ] Test framework discovers tests automatically
- [ ] Test output is clear and readable
- [ ] Failed tests show enough detail to debug
- [ ] Test coverage is reported
- [ ] Tests can be run individually or all at once
- [ ] Test naming conventions are established
- [ ] Test file structure is documented
- [ ] Testing patterns are documented for future tests
- [ ] Test configuration is in pyproject.toml
- [ ] Tests work on Windows, macOS, and Linux