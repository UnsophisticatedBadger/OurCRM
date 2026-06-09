# OurCRM — Claude Code Guide

## Project
Desktop CRM for real estate agents. Python 3.14 desktop app (PySide6).

## Tech Stack
- **Package manager:** uv (`uv sync` to install, `uv add` to add deps)
- **Linter/formatter:** ruff (replaces black + isort + flake8)
- **Type checker:** mypy strict
- **Testing:** pytest + pytest-bdd + pytest-cov
- **Architecture:** Vertical slices with dependency injection

## Essential Commands

```powershell
uv run ourcrm                          # launch the app
uv run pytest                          # run all tests with coverage
uv run ruff check .                    # lint
uv run ruff format .                   # format
uv run mypy src/                       # type check
uv run pre-commit run --all-files      # run all hooks
```

## Project Layout

```
docs/slices/          # slice definitions — each file groups related user stories
docs/NNN-*.md         # individual user story files

src/ourcrm/
├── main.py           # entry point (ourcrm.main:main)
├── core/             # shared primitives (models, exceptions, config, DI container)
├── database/         # SQLite + encryption layer
├── ui/               # main window, navigation shell
├── crm/              # contacts, leads, transactions, showings
├── ai/               # lead qualification, AI settings
├── integrations/     # HARMLS MLS, email, calendar
└── lead_generation/  # lead pipeline

tests/
├── unit/             # fast, no I/O
├── integration/      # database + real filesystem
└── bdd/              # pytest-bdd .feature files
```

## Architecture Rules

1. **No story, no code.** Every feature must reference a User Story in `docs/`.
2. **Strict typing.** All code must pass `mypy --strict`. No `Any` without justification.
3. **Slice isolation.** Imports flow inward: slices may import from `core/`, never from each other.
4. **Dependency injection.** Dependencies are injected, never instantiated internally. Services receive their dependencies via constructor injection. The DI container lives in `core/`.
5. **BDD first.** Write the `.feature` file before the implementation.

## What Is a Slice

A slice is a collection of related user stories defined in `docs/slices/SliceN.md`. Each slice file contains a table of story numbers, titles, effort estimates, and layers. Slices are the unit of planning and delivery — a slice is done when all its stories are implemented and coverage gates are met.

## Coverage Gates

| Gate | Target | Meaning |
|------|--------|---------|
| Start of slice | 50% | Tests exist and are meaningful before building |
| End of slice | 85% | Slice is complete and well-covered |

## Development Workflow (Double-Loop TDD)

Every change follows these steps in strict order. No step is skipped or compressed.

### Step 1 — Plan
- Read the user story and review its BDD scenarios and manual tests for viability and coverage gaps
- Explain the planned changes
- Answer questions → wait for explicit confirmation before proceeding

### Step 2 — BDD Red
- Write the `.feature` file
- Write step definitions for every step in the feature file
- Run them to confirm they all fail
- Answer questions → wait for explicit confirmation before proceeding

### Step 3 — Inner Loop (repeat for each unit until the BDD step turns Green)

#### 3a — Unit Red
- Write a failing unit test for the smallest unit needed by the current BDD step
- Run it to confirm it fails
- Answer questions → wait for explicit confirmation before proceeding

#### 3b — Unit Green
- Write the minimum code to make the unit test pass
- Run the unit test to confirm it passes

#### 3c — Unit Refactor
- Explain what refactorings can and should be done
- Answer questions → wait for explicit confirmation before proceeding
- Apply the agreed refactorings
- Re-run tests to confirm nothing broke

#### 3d — BDD step check
- If the BDD step now passes with the units built so far, mark it Green and move to the next step
- Otherwise return to 3a for the next unit

### Step 4 — Slice complete
- All BDD steps are Green
- Run `ruff`, `mypy`, and coverage to confirm the 85% gate is met

## User Stories
All stories live in `docs/NNN-story-name.md`. Always read the relevant story before starting.
All slices live in `docs/slices/SliceN.md`. Always check the slice table to understand scope.