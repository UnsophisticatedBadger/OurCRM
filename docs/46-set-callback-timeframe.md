# US-019 — Set Callback Timeframe

**Capability:** contacts
**Milestone:** v0.5.0 — MVP
**Status:** Not Started
**GitHub Issue:** #46

## User Story

As a real estate agent, I want to set a vague callback timeframe when someone asks me to call back later, so that the contact surfaces again at the right time without me having to remember it.

## Dependencies

- #45 — Log call outcome

## Acceptance Criteria

1. When the Call Back outcome is selected, a timeframe picker appears before confirming
2. Timeframe options are: This Week, Next Week, In Two Weeks, This Month
3. Selecting a timeframe saves a target callback date range on the contact
4. The contact is removed from the active call list and placed in the callback queue
5. When the target date range arrives, the contact reappears in the call list sorted above new contacts

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/contacts.feature` |
| BDD step defs | `tests/bdd/test_contacts.py` |
| Unit tests | `tests/unit/contacts/test_callback_timeframe.py` |
| Manual tests | `tests/manual/contacts/set_callback_timeframe.md` |

## Definition of Done

- [ ] BDD scenarios pass
- [ ] `ruff`, `mypy --strict` clean
- [ ] Callback set for next week; contact disappears from active list; after simulating date change contact reappears above new contacts
