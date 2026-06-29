# #4 — Set Up Recovery Password

**Capability:** Authentication & Security
**Milestone:** v0.2.0 — Secure Shell
**Status:** Not Done
**GitHub Issue:** #4

## User Story

As a real estate agent, I want the app to generate a recovery password when I first set up OurCRM and require me to confirm I have saved it, so that I can regain access if I ever forget my master password.

## Dependencies

- #3 — Create Master Password

## Acceptance Criteria

1. Generated password is exactly 32 characters and contains no ambiguous characters (0, O, I, l, 1)
2. Password is formatted with dashes every 5 characters for display; removing the dashes restores the original 32-character string
3. Each generation produces a unique password
4. The Continue button stays disabled until both checkboxes are checked and "CONFIRM" is typed exactly (case-sensitive)
5. Any incomplete state — missing checkbox, wrong text, or no text — prevents proceeding

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/authentication.feature` |
| BDD step defs | `tests/bdd/test_authentication.py` |
| Unit tests | `tests/unit/authentication/test_recovery_password_generation.py`, `test_recovery_confirmation.py` |
| Manual tests | `tests/manual/authentication/recovery_password_generation.md`, `tests/manual/authentication/recovery_confirmation.md` |

## Definition of Done

- [x] BDD scenarios pass end-to-end
- [x] Feature reachable from the running app
- [x] `ruff`, `mypy --strict` clean
- [x] Manual tests documented and verified
