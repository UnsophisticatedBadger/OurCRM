# US-018 — Log Call Outcome

**Capability:** contacts
**Milestone:** v0.5.0 — MVP
**Status:** Not Started

## User Story

As a real estate agent, I want to log what happened after I call a contact, so that I have a record of every call and know what to do next.

## Dependencies

- US-017 — View call list

## Acceptance Criteria

1. Tapping a contact in the call list opens their detail view with a Log Outcome button
2. The outcome options are: No Answer, Call Back, Became Client, Not Interested
3. Selecting an outcome and confirming saves it with a timestamp
4. After logging, the contact's last-contacted date and outcome are updated in the call list
5. A contact logged as Not Interested disappears from the call list immediately
6. A contact logged as Became Client is marked with a client badge and remains visible until moved to the client section
7. Multiple outcomes can be logged over time; all are stored as history

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/contacts.feature` |
| BDD step defs | `tests/bdd/test_contacts.py` |
| Unit tests | `tests/unit/contacts/test_call_outcome.py` |
| Manual tests | `tests/manual/contacts/log_call_outcome.md` |

## Definition of Done

- [ ] BDD scenarios pass
- [ ] `ruff`, `mypy --strict` clean
- [ ] All four outcomes logged on real contacts; Not Interested removes from list; Became Client shows badge; history visible on second visit
