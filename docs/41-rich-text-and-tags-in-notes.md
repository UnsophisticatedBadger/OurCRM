# 41 - Rich Text And Tags In Notes

**Capability:** shell
**Milestone:** Secure Shell
**Status:** Not Done
**GitHub Issue:** #41
**Priority:** Post-MVP

## User Story
As an agent, I want to format my notes with basic rich text and tag them with keywords, so that my notes are easier to read and easier to find later.

## Dependencies
- #27 — Create Note

## Acceptance Criteria
1. The note editor includes a toolbar with Bold, Italic, Bulleted List, and Numbered List formatting
2. Notes are stored and rendered with formatting preserved
3. A tag input below the note body allows the user to add one or more tags; tags are free-form text, not from a fixed list
4. Tags appear as badges below the note in the notes list
5. The notes list can be filtered by tag: selecting a tag shows only notes with that tag

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/shell.feature`.

```gherkin
@story_41
Scenario: Bold formatting is applied in the note editor
  Given the user is editing a note
  When the user selects text and clicks Bold
  Then the selected text appears bold in the editor and is saved with bold formatting

@story_41
Scenario: Adding a tag to a note displays it as a badge
  Given the user adds the tag "buyer" to a note
  When the note is saved
  Then a "buyer" badge appears below the note in the notes list

@story_41
Scenario: Filtering notes by tag shows only matching notes
  Given notes tagged "buyer" and "seller" exist
  When the user selects the "buyer" tag filter
  Then only notes tagged "buyer" are shown
```

## Manual Tests
**Story:** [#30 — Rich Text and Tags in Notes](../docs/149-rich-text-and-tags-in-notes.md)

### Bold and list formatting is preserved
1. Create a note with bold text and a bulleted list
2. Save and reopen the note
3. Verify the formatting is preserved

### Tags appear as badges and are filterable
1. Add a tag "urgent" to a note and save
2. Verify the "urgent" badge appears below the note
3. Click the "urgent" tag filter and verify only notes tagged "urgent" are shown

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_note_rich_text.py` |
| Manual tests | `tests/manual/shell/rich-text-notes.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
