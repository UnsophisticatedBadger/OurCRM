# 38 - Create A Standalone Note

**Capability:** App Shell
**Milestone:** Secure Shell
**Status:** Not Done
**GitHub Issue:** #38

## User Story

As a real estate agent, I want to create a standalone note so that I can capture information that is not tied to a specific contact, lead, or property.

## Dependencies

- #6 — Log In with Master Password

## Notes

**Capability decision:** The canonical capability list has no "notes" group. Standalone notes are an app-level feature with no natural home in contacts, leads, or any other domain capability. Assigned to `shell` pending a decision on whether a dedicated `notes` capability should be added — raise this if the notes feature grows beyond create/view/search.

**Distinction from entity notes:** #61 (Add Notes to Contact) attaches notes to a specific contact record. This story covers a general-purpose Notes section for information that has no specific contact, lead, or property to attach to — market observations, personal reminders, general procedures, and so on.

Optional entity links are supported: a standalone note can be linked to a contact, lead, or property for cross-reference, but the note always lives in the Notes section regardless of that link.

## Acceptance Criteria

1. A Notes section is accessible from the main navigation
2. Clicking "New Note" opens a creation form with a title field and a plain-text content area
3. Title is required; submitting without one shows a validation error
4. An optional "Link to" field allows associating the note with one contact, lead, or property by name
5. Saving creates the note and it appears immediately in the Notes section list
6. The note persists across application restarts

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/shell.feature`.

```gherkin
@story_38
Scenario: User creates a standalone note and it appears in the Notes section
  Given the user is in the Notes section
  When the user clicks "New Note", enters title "Market observation" and content "Prices rising in north district", and saves
  Then the note "Market observation" appears in the Notes section list

@story_38
Scenario: Submitting a note form without a title shows a validation error
  Given the note creation form is open
  When the user leaves the title empty and clicks Save
  Then a validation error is shown and no note is created

@story_38
Scenario: Note with an optional entity link is saved correctly
  Given the user creates a note titled "Reminder" linked to contact "Alice Smith"
  When the user saves the note
  Then the note "Reminder" appears in the Notes section with a link to "Alice Smith"

@story_38
Scenario: Created note persists after application restart
  Given the user has created a note titled "Procedure reminder"
  When the user restarts the application and opens the Notes section
  Then "Procedure reminder" is present
```

## Manual Tests

**Story:** [#27 — Create a Standalone Note](../docs/146-create-note.md)

### Notes section is accessible from navigation
1. Log in to the application
2. Confirm a "Notes" item appears in the main navigation sidebar
3. Click it and confirm the Notes section opens

### Note creation form has the required fields
1. Click "New Note"
2. Confirm the form has a title field and a content (plain text) area
3. Confirm an optional "Link to" field allows selecting a contact, lead, or property

### Saving without a title is rejected
1. Open the note creation form
2. Leave the title blank and click Save
3. Confirm a validation error is shown and the form stays open

### Note is saved and visible immediately
1. Enter a title and some content
2. Click Save
3. Confirm the note appears in the Notes section list with its title

### Optional entity link appears on the note
1. Create a note and link it to an existing contact using the "Link to" field
2. Save the note
3. Confirm the Notes section list shows the linked contact name on that note's row

### Note persists after restart
1. Create a note and close the application
2. Reopen the application and navigate to Notes
3. Confirm the note is present with its title and content

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_note_creation.py` |
| Manual tests | `tests/manual/shell/note_creation.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
