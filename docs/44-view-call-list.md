# 44 - View Call List

**Capability:** contacts
**Milestone:** v0.5.0 — MVP
**Status:** Not Started
**GitHub Issue:** #44

## User Story

As a real estate agent, I want to see all my contacts sorted by who needs to be called first, so that I always work the most overdue callbacks before starting new contacts.

## Dependencies

- #43 — Manually add contact to call list

## Acceptance Criteria

1. The call list shows all contacts in the system
2. Contacts are sorted in this priority order: overdue callbacks first (most overdue at top), then callbacks due today, then callbacks due this week, then new contacts not yet called, then contacts with no callback set
3. Each row shows the contact's name, phone number, property address, and next callback due date
4. A contact with a logged outcome of "Not Interested" does not appear in the call list
5. The list updates immediately when a new contact is added or an outcome is logged

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/contacts.feature` |
| BDD step defs | `tests/bdd/test_contacts.py` |
| Unit tests | `tests/unit/contacts/test_call_list_sorting.py` |
| Manual tests | `tests/manual/contacts/view_call_list.md` |

## Definition of Done

- [ ] BDD scenarios pass
- [ ] `ruff`, `mypy --strict` clean
- [ ] Call list opened with overdue, due-today, and new contacts present; correct sort order verified by inspection
