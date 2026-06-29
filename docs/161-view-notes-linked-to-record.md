# US-161 — View Notes Linked to a Record

**Capability:** shell
**Status:** Not Done
**Priority:** Post-MVP

## User Story
As an agent, I want to see notes that are linked to a contact, lead, or property directly on that record's detail view, so that I don't have to go to the Notes section to find relevant context.

## Dependencies
- US-146 — Create Note

## Acceptance Criteria
1. When creating or editing a note, the user can optionally link it to a contact, a lead, or a property via a record picker
2. A "Notes" tab on the contact detail view lists all notes linked to that contact, newest first
3. A "Notes" tab on the lead detail view lists all notes linked to that lead, newest first
4. A "Notes" tab on the property detail view lists all notes linked to that property, newest first
5. Clicking a note in any linked view opens the full note in the Notes section
6. Notes that are not linked to any record are only visible in the standalone Notes section

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/shell.feature`.

```gherkin
@us207
Scenario: A note linked to a contact appears on that contact's Notes tab
  Given the user creates a note linked to contact "Jane Smith"
  When the user opens Jane Smith's contact detail
  Then a Notes tab shows the linked note

@us207
Scenario: A note not linked to any record does not appear on any record's Notes tab
  Given the user creates a standalone note with no record link
  When the user opens any contact, lead, or property detail
  Then the note does not appear in any record's Notes tab

@us207
Scenario: Clicking a linked note opens it in the Notes section
  Given a note is visible in a contact's Notes tab
  When the user clicks the note
  Then the Notes section opens with that note selected
```

## Manual Tests
**Story:** [US-150 — View Notes Linked to a Record](../docs/183-view-notes-linked-to-record.md)

### Linked note appears on the record's Notes tab
1. Create a note and link it to a contact
2. Open that contact's detail view
3. Verify the Notes tab shows the linked note

### Standalone notes don't appear on record detail tabs
1. Create a note with no record link
2. Open any contact, lead, or property
3. Verify the note does not appear in their Notes tabs

### Clicking a linked note opens the Notes section
1. Click a note in a contact's Notes tab
2. Verify the Notes section opens with that note in focus

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_linked_notes.py` |
| Manual tests | `tests/manual/shell/view-notes-linked-to-record.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
