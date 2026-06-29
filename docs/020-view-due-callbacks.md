# US-020 — View Due Callbacks

**Capability:** contacts
**Milestone:** v0.5.0 — MVP
**Status:** Not Started

## User Story

As a real estate agent, I want to see at a glance which callbacks are due this week, so that I know exactly who to prioritise when I sit down to make calls.

## Dependencies

- US-019 — Set callback timeframe

## Acceptance Criteria

1. A "Due This Week" filter or tab is available on the call list
2. The filtered view shows only contacts whose callback timeframe falls within the current week
3. Overdue callbacks (timeframe passed without a follow-up call) are highlighted and listed first
4. Each contact shows how many days overdue or how many days remain
5. Clearing the filter returns to the full call list

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/contacts.feature` |
| BDD step defs | `tests/bdd/test_contacts.py` |
| Unit tests | `tests/unit/contacts/test_due_callbacks.py` |
| Manual tests | `tests/manual/contacts/view_due_callbacks.md` |

## Definition of Done

- [ ] BDD scenarios pass
- [ ] `ruff`, `mypy --strict` clean
- [ ] Contacts with callbacks due this week visible in filtered view; overdue contacts appear before upcoming ones with days displayed
