# #14 — Home Dashboard

**Capability:** App Shell
**Milestone:** Secure Shell
**Status:** Not Done
**GitHub Issue:** #14

## User Story

As a real estate agent, I want to see a dashboard when I open the app, so that I can get an overview of my business and today's priorities without navigating to each section.

## Dependencies

- #10 — Navigate Between Sections

## Acceptance Criteria

1. Dashboard is the default section shown immediately after login
2. The dashboard page provides three named layout regions — stats, today's schedule, and quick actions — each populated by its own widget story (#16, #108, #15)

## Note

Each region renders placeholder/empty content until its widget story lands.

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_dashboard_page.py`, `test_dashboard_navigation.py` |
| Manual tests | `tests/manual/shell/dashboard.md` |

## Definition of Done

- [x] BDD scenarios pass end-to-end
- [x] Feature reachable from the running app
- [x] `ruff`, `mypy --strict` clean
- [x] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
