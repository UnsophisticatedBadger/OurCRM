# US-010 — Navigate Between Sections

**Capability:** App Shell
**Status:** Not Done

## User Story

As a real estate agent, I want to move between the main sections of OurCRM from a sidebar, so that I can switch between contacts, leads, calendar, and other tools without losing my place.

## Dependencies

- US-015 — Wire Encrypted Database into Application Startup

## Acceptance Criteria

1. All major sections (Contacts, Leads, Properties, Transactions, Calendar, Tasks, Settings) are reachable from the sidebar
2. The currently active section is visually highlighted in the sidebar
3. Keyboard shortcuts navigate to sections (e.g., Ctrl+1 through Ctrl+N)

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_main_window_layout.py`, `test_section_navigation.py` |
| Manual tests | `tests/manual/shell/section_navigation.md` |

## Definition of Done

- [x] BDD scenarios pass end-to-end
- [x] Feature reachable from the running app
- [x] `ruff`, `mypy --strict` clean
- [x] Manual tests documented and verified
