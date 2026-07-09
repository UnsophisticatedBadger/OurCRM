# #11 — Open the Settings Window

**Capability:** App Shell
**Milestone:** Secure Shell
**Status:** Not Done
**GitHub Issue:** #11

## User Story

As a real estate agent, I want to open a Settings window, so that I can configure OurCRM to match my workflow and preferences.

## Dependencies

- #10 — Navigate Between Sections

## Acceptance Criteria

1. Settings window opens from the sidebar navigation, the File menu, and the Ctrl+, keyboard shortcut
2. Settings categories (General, Security, AI, MLS, Email, Calendar, Notifications) are listed in a left-hand panel
3. Clicking Save persists changes; clicking Cancel discards them

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_settings_window.py`, `test_settings_entry_points.py` |
| Manual tests | `tests/manual/shell/settings_window.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
