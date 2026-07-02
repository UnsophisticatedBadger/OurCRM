# 48 - Dashboard

**Capability:** shell
**Milestone:** MVP
**Status:** Not Started
**GitHub Issue:** #48

## User Story

As a real estate agent, I want to see exactly what I need to do today the moment I open the app, so that I can start working immediately without having to figure out where I left off.

## Dependencies

- #7 — Main window with navigation sidebar
- #11 — View call list sorted by priority
- #14 — Set callback timeframe

## Acceptance Criteria

1. The dashboard is the first screen shown after login
2. A "Call Back Today" section lists contacts whose callback timeframe is due today or overdue, sorted by how overdue they are
3. A "New to Call" section lists contacts added to the call list but not yet called, sorted by date added
4. Each contact in both sections shows name, phone number, and property address
5. A Call button appears next to each contact when a calling interface is configured
6. A count of calls logged today is shown at the top of the screen
7. Tapping a contact opens their detail view where the outcome can be logged

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_dashboard.py` |
| Manual tests | `tests/manual/shell/dashboard.md` |

## Definition of Done

- [ ] BDD scenarios pass
- [ ] `ruff`, `mypy --strict` clean
- [ ] Dashboard opened with real contacts in both sections; due callbacks and new contacts appear correctly; call count updates after logging an outcome
