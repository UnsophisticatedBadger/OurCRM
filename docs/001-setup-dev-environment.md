# US-001: Setup Development Environment

## User Story

**As a** developer  
**I want to** clone the repository and run tests  
**So that** I can start contributing to the project

## Priority

**MVP:** Must Have

**Rationale:** Cannot build anything without a working development environment. This is the foundation for all other work.

## Estimated Effort

**Size:** Small (S) - 1-2 days

**Breakdown:**
- 2 hours: Create project structure
- 2 hours: Configure pyproject.toml
- 1 hour: Set up testing framework
- 1 hour: Write first test
- 2 hours: Document setup process

## Dependencies

**Depends on:** None (this is the first story)

**Blocks:** All other stories (US-002 through US-193)

## Description

A new developer should be able to:
1. Clone the OurCRM repository from GitHub
2. Install Python 3.14 (or have it already)
3. Install UV (the package manager)
4. Run `uv sync` to install dependencies
5. Run `uv run pytest` to verify tests pass
6. Run `uv run ourcrm` to launch the app
7. See an empty window open successfully

The entire setup should take less than 15 minutes for someone familiar with Python development.

## BDD Scenarios

### Scenario 1: Fresh setup on Windows

```
Given I am a new developer on Windows
  And I have Python 3.14 installed
  And I have UV installed
When I clone the repository
  And I run "uv sync"
  And I run "uv run pytest"
Then all tests should pass
  And the command should complete in under 5 minutes
```

### Scenario 2: Fresh setup on macOS

```
Given I am a new developer on macOS
  And I have Python 3.14 installed
  And I have UV installed
When I clone the repository
  And I run "uv sync"
  And I run "uv run pytest"
Then all tests should pass
  And the command should complete in under 5 minutes
```

### Scenario 3: Fresh setup on Linux

```
Given I am a new developer on Linux
  And I have Python 3.14 installed
  And I have UV installed
When I clone the repository
  And I run "uv sync"
  And I run "uv run pytest"
Then all tests should pass
  And the command should complete in under 5 minutes
```

### Scenario 4: Launch the app

```
Given I have completed setup successfully
When I run "uv run ourcrm"
Then the application should launch
  And I should see a window open
  And the window should display "OurCRM" in the title bar
```

### Scenario 5: Verify code quality tools

```
Given I have completed setup successfully
When I run the linter
Then no errors should be found
When I run the type checker
Then no errors should be found
```

## Manual Testing Steps

### Test 1: Verify setup instructions are clear

1. Read the README.md file
2. Follow the setup instructions step-by-step
3. Verify each step works as described
4. Confirm the entire setup takes less than 15 minutes
5. Document any unclear or missing steps

### Test 2: Verify cross-platform setup

1. Test setup on Windows (if available)
2. Test setup on macOS (if available)
3. Test setup on Linux (if available)
4. Verify all platforms work with the same instructions
5. Note any platform-specific issues

### Test 3: Verify error messages are helpful

1. Intentionally skip a step (e.g., don't install UV)
2. Try to run a command that requires it
3. Verify the error message is clear and helpful
4. Verify it tells the user how to fix the problem

## Acceptance Criteria

- [ ] Project structure follows the agreed layout
- [ ] pyproject.toml is configured correctly
- [ ] Dependencies install without errors
- [ ] Tests run and pass
- [ ] Application launches successfully
- [ ] Code quality tools work
- [ ] README has clear setup instructions
- [ ] Setup works on Windows, macOS, and Linux
- [ ] Setup takes less than 15 minutes
- [ ] Error messages are clear and helpful