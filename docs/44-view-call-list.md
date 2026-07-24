# 44 - View Call List

**Capability:** contacts
**Milestone:** MVP
**Status:** Done
**GitHub Issue:** #44

## User Story

As a real estate agent, I want to see all my contacts sorted by who needs to be called first, so that I always work the most overdue callbacks before starting new contacts.

## Dependencies

- #43 — Manually add contact to call list

## Acceptance Criteria

1. A toggle on the Contacts page switches between "All Contacts" and "Call List" views
2. The call list view shows all contacts in the system that have a phone number
3. Each row in the call list shows the contact's name, phone number, and property address
4. The list updates immediately when a new contact is added
5. A "Call List" quick action on the dashboard navigates directly to the call list view

Priority sorting by callback urgency is Acceptance Criterion 6 on [#46 — Set Callback Timeframe](46-set-callback-timeframe.md); updating the list when an outcome is logged, and excluding contacts logged "Not Interested," are Acceptance Criteria 4 and 5 on [#45 — Log Call Outcome](45-log-call-outcome.md). Both depend on data this story doesn't yet have (callback dates, logged outcomes), so they're built there instead of here.

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/contacts.feature` |
| BDD step defs | `tests/bdd/test_contacts.py` |
| Unit tests | `tests/unit/contacts/test_call_list_sorting.py` |
| Manual tests | `tests/manual/contacts/view_call_list.md` |

## Definition of Done

- [x] BDD scenarios pass
- [x] `ruff`, `mypy --strict` clean
- [x] Toggling to Call List on the Contacts page shows only contacts with a phone number, with name, phone, and address; newly added contact appears immediately; dashboard "Call List" quick action opens the call list view directly
- [x] Wiki documentation written, or marked N/A with a reason
