# #12 — Configure General Settings

**Capability:** App Shell
**Milestone:** v0.2.0 — Secure Shell
**Status:** Not Done
**GitHub Issue:** #12

## User Story

As a real estate agent, I want to configure general preferences such as theme and date format, so that OurCRM feels native to how I work.

## Dependencies

- #11 — Open the Settings Window

## Acceptance Criteria

1. Theme can be switched between Light, Dark, and Auto — change takes effect immediately without restarting
2. Date format and time format (12-hour / 24-hour) can be configured and are applied throughout the app
3. All general settings are stored in TOML format and persist across restarts

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_app_config.py`, `test_general_settings_page.py`, `test_general_settings.py`, `test_theme_switching.py`, `test_settings_panel_wiring.py` |
| Manual tests | `tests/manual/shell/general_settings.md` |

## Definition of Done

- [x] BDD scenarios pass end-to-end
- [x] Feature reachable from the running app
- [x] `ruff`, `mypy --strict` clean
- [x] Manual tests documented and verified
