# US-013 — Configure Security Settings

**Capability:** App Shell
**Status:** Not Done
**GitHub Issue:** #13

## User Story

As a real estate agent, I want to configure security preferences such as auto-lock timeout, so that OurCRM locks itself when I step away from my desk.

## Dependencies

- #11 — Open the Settings Window

## Acceptance Criteria

1. Auto-lock timeout is configurable in the Security settings panel, including a "Never" option
2. Auto-lock triggers after the configured period of inactivity and immediately resets on any user activity
3. Security settings are stored in TOML format and persist across restarts

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_app_config_security.py`, `test_security_settings_page.py`, `test_security_settings.py`, `test_settings_panel_security_wiring.py` |
| Manual tests | `tests/manual/shell/security_settings.md` |

## Definition of Done

- [x] BDD scenarios pass end-to-end
- [x] Feature reachable from the running app
- [x] `ruff`, `mypy --strict` clean
- [x] Manual tests documented and verified
