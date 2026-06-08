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

## BDD Scenarios

### Scenario 1: Ruff catches style violations

```
Given I have configured ruff
  And I have code with style violations
When I run ruff
Then it should report the violations
  And the violations should include file names and line numbers
```

### Scenario 2: Ruff auto-formats code

```
Given I have configured ruff
  And I have code with formatting issues
When I run ruff format
Then the code should be reformatted automatically
  And the changes should follow the style guidelines
```

### Scenario 3: Mypy catches type errors

```
Given I have configured mypy
  And I have code with type errors
When I run mypy
Then it should report the type errors
  And the errors should include file names, line numbers, and explanations
```

### Scenario 4: Ruff and mypy pass on clean code

```
Given I have configured both tools
  And all code follows the rules
When I run both tools
Then both should pass with no errors
```

### Scenario 5: Configuration is in pyproject.toml

```
Given I have configured the tools
When I examine pyproject.toml
Then I should see a [tool.ruff] section
  And I should see a [tool.mypy] section
  And the configuration should be clearly commented
```

## Manual Testing Steps

### Test 1: Verify ruff configuration

1. Open pyproject.toml
2. Verify there is a [tool.ruff] section
3. Check that target-version is set to "py314"
4. Check that line-length is configured
5. Check that rule sets are enabled (E, W, F, I, etc.)
6. Verify the configuration is documented with comments

### Test 2: Test ruff on sample code

1. Create a file with intentional style violations:
   - Unused import
   - Undefined variable
   - Wrong indentation
   - Line too long
2. Run `ruff check .`
3. Verify all violations are caught
4. Run `ruff format .`
5. Verify formatting issues are fixed
6. Clean up the test file

### Test 3: Verify mypy configuration

1. Open pyproject.toml
2. Verify there is a [tool.mypy] section
3. Check that Python version is set to 3.14
4. Check that strict mode is configured (or appropriate level)
5. Check that warnings are configured appropriately
6. Verify the configuration is documented

### Test 4: Test mypy on sample code

1. Create a file with intentional type errors:
   - Function with wrong return type
   - Variable assigned wrong type
   - Missing type hints where required
2. Run `mypy src/`
3. Verify all type errors are caught
4. Fix the errors
5. Run mypy again
6. Verify it passes
7. Clean up the test file

### Test 5: Test configuration with project code

1. Run ruff on the actual OurCRM codebase
2. Verify it passes (or only reports intentional issues)
3. Run mypy on the actual OurCRM codebase
4. Verify it passes
5. Fix any issues that are reported
6. Document any configuration adjustments needed

### Test 6: Verify tools integrate with development workflow

1. Document how to run the tools manually
2. Document how the tools will be used in CI/CD
3. Add the tools to the README
4. Add the tools to any contribution guidelines
5. Make sure new developers know to run these tools

## Acceptance Criteria

- [ ] Ruff is configured in pyproject.toml
- [ ] Mypy is configured in pyproject.toml
- [ ] Configuration targets Python 3.14
- [ ] Ruff catches common style issues
- [ ] Ruff can auto-format code
- [ ] Mypy catches type errors
- [ ] Configuration is documented with comments
- [ ] Tools work on the actual OurCRM codebase
- [ ] Usage is documented in README
- [ ] Tools are part of the development workflow
- [ ] Configuration is not too strict or too lenient