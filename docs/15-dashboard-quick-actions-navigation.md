# #15 — Dashboard Quick Actions Navigation

**Capability:** shell
**Milestone:** Secure Shell
**Status:** Not Done
**GitHub Issue:** #15

## User Story

As a real estate agent, I want the Quick Actions buttons on the dashboard to take me directly to the right section, so that I can start common tasks with one click instead of hunting through the sidebar.

## Dependencies

- #14 — Home Dashboard
- #10 — Navigate Between Sections

## Acceptance Criteria

1. New Contact, New Lead, New Property, and New Task buttons each navigate to their respective section with one click
2. Navigation is triggered via callback or signal — `DashboardPage` does not import `MainWindow` directly

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_quick_actions.py` |
| Manual tests | `tests/manual/shell/quick_actions.md` |

## Definition of Done

- [x] BDD scenarios pass end-to-end
- [x] Feature reachable from the running app
- [x] `ruff`, `mypy --strict` clean
- [x] Manual tests documented and verified
