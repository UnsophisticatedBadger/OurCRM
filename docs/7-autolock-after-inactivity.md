# #7 — Auto-Lock After Inactivity

**Capability:** Authentication & Security
**Milestone:** Secure Shell
**Status:** Not Done
**GitHub Issue:** #7

## User Story

As a real estate agent, I want OurCRM to lock itself after I've been away from my desk, so that my clients' data stays protected if I forget to lock my computer.

## Dependencies

- #6 — Log In with Master Password *(password verification on unlock)*

## Notes

The inactivity period is hard-coded to 30 seconds for this story — short on purpose, to fail fast during initial development and testing. #13 (Configure Security Settings) later makes this value configurable and adds a "Never" option.

## Acceptance Criteria

1. After 30 seconds of inactivity, the lock screen is shown — any keyboard or mouse activity resets the timer
2. Correct password on the lock screen returns the user to the section they were viewing before the lock
3. Wrong password shows an error on the lock screen without dismissing it

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/authentication.feature` |
| BDD step defs | `tests/bdd/test_authentication.py` |
| Unit tests | `tests/unit/authentication/test_inactivity_timer.py`, `test_lock_screen.py`, `test_autolock_wiring.py` |
| Manual tests | `tests/manual/authentication/autolock.md` |

## Definition of Done

- [x] BDD scenarios pass end-to-end
- [x] Feature reachable from the running app
- [x] `ruff`, `mypy --strict` clean
- [x] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
