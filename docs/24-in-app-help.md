# 24 - In-App Help

**Capability:** App Shell
**Milestone:** MVP
**Status:** Not Done
**GitHub Issue:** #24

## User Story

As a real estate agent, I want to access help and documentation from inside OurCRM, so that I can learn features and find keyboard shortcuts without leaving the app.

## Dependencies

- #10 — Navigate Between Sections

## Acceptance Criteria

1. The Help menu opens a Help window containing a user guide and a keyboard shortcuts reference
2. The About dialog shows the application version, copyright, and support links
3. Help content is available offline (embedded, not fetched from the internet)

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_help_window.py`, `test_help_entry_points.py` |
| Manual tests | `tests/manual/shell/help.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
