# 39 - View Notes List

**Capability:** App Shell
**Milestone:** Secure Shell
**Status:** Not Done
**GitHub Issue:** #39

## User Story

As a real estate agent, I want to view a list of all my standalone notes so that I can browse and re-open information I have captured.

## Dependencies

- #38 — Create a Standalone Note

## Acceptance Criteria

1. The Notes section displays all notes with title, creation date, content preview (first line of the note body), and linked entity label (if linked) on each row
2. Notes are sorted by creation date, newest first, by default; an alternative sort by title (A–Z) is available
3. Clicking a note row opens the note detail view showing the full content
4. When no notes exist, the section shows "No notes yet" with a "New Note" button
5. Notes list reflects notes created in #27 without requiring a page reload

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/shell.feature`.

```gherkin
@story_39
Scenario: Notes list shows title, date, content preview, and linked entity for each note
  Given notes "Market update" (content "Prices rising…", linked to no entity) and "Alice reminder" (content "Call re: contract", linked to contact "Alice Smith") exist
  When the user opens the Notes section
  Then "Market update" is listed with a preview "Prices rising…" and no linked entity
  And "Alice reminder" is listed with a preview "Call re: contract" and linked to "Alice Smith"

@story_39
Scenario: Notes are sorted newest first by default
  Given notes created at different times exist
  When the user opens the Notes section
  Then the most recently created note appears at the top

@story_39
Scenario: User can sort notes alphabetically by title
  Given multiple notes with different titles exist
  When the user selects the "Title A–Z" sort option
  Then notes are listed in alphabetical order by title

@story_39
Scenario: Empty state appears when no notes have been created
  Given no notes exist
  When the user opens the Notes section
  Then the message "No notes yet" is shown with a "New Note" button
```

## Manual Tests

**Story:** [#39 — View Notes List](39-view-notes-list.md)
### Notes list shows correct columns
1. Create two notes — one linked to a contact, one standalone
2. Navigate to the Notes section
3. Confirm each row shows title, creation date, and first line of content
4. Confirm the linked note shows the contact's name; the standalone note shows nothing in the entity column

### Default sort is newest first
1. Create note A then note B
2. Open the Notes section
3. Confirm note B appears above note A

### Sort by title works
1. Create notes titled "Zebra", "Alpha", "Market"
2. Select "Title A–Z" sort
3. Confirm the order is Alpha, Market, Zebra

### Clicking a note opens its detail view
1. Click any note row
2. Confirm the full note content is shown

### Empty state when no notes exist
1. Ensure no notes have been created
2. Open the Notes section
3. Confirm "No notes yet" and "New Note" button are shown

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_notes_list.py` |
| Manual tests | `tests/manual/shell/notes_list.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
