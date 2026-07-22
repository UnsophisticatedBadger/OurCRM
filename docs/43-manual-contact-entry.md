# 43 - Manually Add Contact To Call List

**Capability:** contacts
**Milestone:** MVP
**Status:** Done
**GitHub Issue:** #43

## User Story

As a real estate agent, I want to add a property owner to my call list by typing their details directly, so that the app works even when MLS is unavailable or not configured, and I can still log contacts I find through other means.

## Dependencies

- #3 — Create master password on first launch
- #5 — Encrypt database at rest

## Acceptance Criteria

1. A form is accessible from the call list and dashboard to add a contact manually
2. The form requires a name; phone number and property address are optional
3. Submitting a valid form adds the contact immediately; it appears in the call list once it has a phone number (contacts without a phone, e.g. a name and email collected at a showing, are not callable and do not appear there)
4. An invalid phone number format shows a plain-language error and does not save
5. A duplicate phone number shows a warning and asks the user to confirm before saving
6. The manually added contact appears in the contact list and dashboard exactly like a contact added from MLS

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/contacts.feature` |
| BDD step defs | `tests/bdd/test_contacts.py` |
| Unit tests | `tests/unit/contacts/test_manual_contact_entry.py` |
| Manual tests | `tests/manual/contacts/manual_contact_entry.md` |

## Definition of Done

- [x] BDD scenarios pass
- [x] `ruff`, `mypy --strict` clean
- [ ] Contact added manually with name only; contact added with phone and/or address; duplicate phone warning confirmed; contact appears on dashboard
- [x] Wiki documentation written, or marked N/A with a reason
