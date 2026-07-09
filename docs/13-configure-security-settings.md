# #13 — Configure Security Settings

**Capability:** App Shell
**Milestone:** Secure Shell
**Status:** Done
**GitHub Issue:** #13

## User Story

As a real estate agent, I want to configure security preferences such as auto-lock timeout, so that OurCRM locks itself when I step away from my desk.

## Dependencies

- #7 — Auto-Lock After Inactivity *(makes the hard-coded 30-second timeout configurable)*
- #11 — Open the Settings Window

## Acceptance Criteria

1. Auto-lock timeout is configurable in the Security settings panel, including a "Never" option
2. When the timeout is set to Never, no inactivity timer runs
3. Auto-lock triggers after the configured period of inactivity and immediately resets on any user activity
4. Security settings are stored in TOML format and persist across restarts
5. If settings cannot be saved (e.g. a disk error), an error is shown and unsaved changes remain in the form

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/authentication/test_app_config_security.py`, `test_security_settings.py`; `tests/unit/shell/test_security_page.py`, `test_settings_panel_security_wiring.py`, `test_settings_panel_save_error_handling.py`, `test_auto_lock_config_wiring.py`, `test_main_window_autolock.py` |
| Manual tests | `tests/manual/shell/security_settings.md` |

## Definition of Done

- [x] BDD scenarios pass end-to-end
- [x] Feature reachable from the running app
- [x] `ruff`, `mypy --strict` clean
- [x] Manual tests documented and verified
- [x] Wiki documentation written — see [App Shell](https://github.com/UnsophisticatedBadger/OurCRM/wiki/App-Shell)
