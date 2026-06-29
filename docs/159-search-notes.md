# US-159 — Search Notes

**Capability:** App Shell
**Status:** Not Done

## User Story

As a real estate agent, I want to search through my notes by keyword so that I can quickly find specific information without scrolling through the full list.

## Dependencies

- US-147 — View Notes List

## Acceptance Criteria

1. A search field is available at the top of the Notes section
2. Typing a keyword filters the notes list in real time to show only notes whose title or content contains the keyword (case-insensitive)
3. Clearing the search field restores the full notes list
4. When no notes match the search term, the section shows "No notes found for '…'"

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/shell.feature`.

```gherkin
@us109
Scenario: Keyword in title matches and filters the list
  Given notes "Market update" and "Call Alice" exist
  When the user types "market" in the search field
  Then only "Market update" is shown

@us109
Scenario: Keyword in note content matches and filters the list
  Given a note "Procedure" exists with content "Always submit offer by fax"
  When the user types "fax" in the search field
  Then "Procedure" is shown

@us109
Scenario: Clearing the search restores the full list
  Given the search field contains "market" and one note is shown
  When the user clears the search field
  Then all notes are shown again

@us109
Scenario: No matching notes shows an empty-results message
  Given no note contains the word "rhinoceros"
  When the user types "rhinoceros" in the search field
  Then the message "No notes found for 'rhinoceros'" is shown
```

## Manual Tests

**Story:** [US-148 — Search Notes](../docs/170-search-notes.md)

### Search filters by title
1. Create notes "Market observation" and "Client follow-up"
2. Type "market" in the search field
3. Confirm only "Market observation" is shown

### Search filters by content
1. Create a note titled "Misc" with content "Remember to call the title company"
2. Search for "title company"
3. Confirm "Misc" appears in the results

### Search is case-insensitive
1. Create a note titled "URGENT reminder"
2. Search for "urgent"
3. Confirm the note appears

### Clearing search restores the full list
1. Perform a search that filters to one note
2. Clear the search field
3. Confirm all notes are shown again

### No-results state
1. Search for a word that appears in no note
2. Confirm the message "No notes found for '…'" is shown

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_notes_search.py` |
| Manual tests | `tests/manual/shell/notes_search.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
