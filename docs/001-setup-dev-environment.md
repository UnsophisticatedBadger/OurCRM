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

## Acceptance Criteria

- [x] Project structure follows the agreed layout
- [x] pyproject.toml is configured correctly
- [x] Dependencies install without errors
- [x] Tests run and pass
- [x] Application launches successfully
- [x] Code quality tools work
- [x] README has clear setup instructions
- [ ] Setup works on Windows, macOS, and Linux — see tests/manual/infrastructure.md
- [ ] Setup takes less than 15 minutes — see tests/manual/infrastructure.md
- [ ] Error messages are clear and helpful — see tests/manual/infrastructure.md