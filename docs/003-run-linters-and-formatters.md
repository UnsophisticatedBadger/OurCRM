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

## BDD Scenarios

### Scenario 1: Run linter with no errors

```
Given I am in the project root directory
  And all code follows the style guidelines
When I run the linter
Then the command should exit successfully
  And no errors or warnings should be reported
```

### Scenario 2: Run linter with style violations

```
Given I am in the project root directory
  And there is code with style violations
When I run the linter
Then the command should report the violations
  And the violations should include file names and line numbers
  And the command should exit with a non-zero status
```

### Scenario 3: Auto-format code

```
Given I am in the project root directory
  And there is code with formatting issues
When I run the formatter
Then the code should be reformatted automatically
  And the changes should follow the style guidelines
```

### Scenario 4: Run type checker with no errors

```
Given I am in the project root directory
  And all code has correct type hints
When I run the type checker
Then the command should exit successfully
  And no type errors should be reported
```

### Scenario 5: Run type checker with type errors

```
Given I am in the project root directory
  And there is code with type errors
When I run the type checker
Then the command should report the type errors
  And the errors should include file names, line numbers, and explanations
  And the command should exit with a non-zero status
```

## Manual Testing Steps

### Test 1: Verify linter catches common issues

1. Create a temporary file with an unused import
2. Run the linter
3. Verify the unused import is reported
4. Create a file with undefined variable
5. Run the linter
6. Verify the undefined variable is reported
7. Delete the temporary files

### Test 2: Verify formatter works correctly

1. Create a file with inconsistent indentation (mix of tabs and spaces)
2. Run the formatter
3. Verify the indentation is normalized
4. Create a file with inconsistent quote styles
5. Run the formatter
6. Verify quotes are normalized
7. Delete the temporary files

### Test 3: Verify type checker catches type issues

1. Create a function with incorrect type hints
2. Run the type checker
3. Verify the type error is reported
4. Create code that passes wrong type to a function
5. Run the type checker
6. Verify the type mismatch is reported
7. Delete the temporary files

### Test 4: Verify tools work on all platforms

1. Run the linter on Windows
2. Verify it works
3. Run the formatter on Windows
4. Verify it works
5. Repeat for macOS
6. Repeat for Linux
7. Document any platform-specific issues

### Test 5: Verify configuration is documented

1. Read the README.md
2. Verify there are instructions for running the linter
3. Verify there are instructions for running the formatter
4. Verify there are instructions for running the type checker
5. Verify the configuration is explained

## Acceptance Criteria

- [ ] Linter runs with a simple command
- [ ] Formatter runs with a simple command
- [ ] Type checker runs with a simple command
- [ ] Tools catch common style issues
- [ ] Tools catch common type errors
- [ ] Tools work on Windows, macOS, and Linux
- [ ] Configuration is documented in README
- [ ] Tools can be run individually or all at once
- [ ] Exit codes properly indicate success or failure
- [ ] Error messages are clear and actionable