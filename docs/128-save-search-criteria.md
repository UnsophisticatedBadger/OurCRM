# US-128 — Save Search Criteria

**Capability:** App Shell
**Status:** Not Done
**Priority:** Should Have (deferrable to post-MVP)

## User Story

As a real estate agent, I want to save frequently used search filters under a name so that I can re-apply them with one click instead of re-entering the same criteria every time.

## Dependencies

- US-023 — Filter Contacts by Tags
- US-024 — Search Contacts

## Acceptance Criteria

1. After applying any search or filter criteria in the Contacts section, a "Save Search" button is available
2. Clicking "Save Search" prompts for a name; the name must be unique among the user's saved searches — attempting to save with a duplicate name shows an error
3. A "Saved Searches" panel or dropdown in the Contacts section lists all saved searches; clicking one applies its stored criteria immediately and updates the contact list
4. Each saved search can be renamed and deleted; deletion requires a confirmation prompt
5. Saved searches persist across application restarts

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/shell.feature`.

```gherkin
@us132
Scenario: User saves current contact filter as a named search
  Given the contacts list is filtered by tag "VIP" and search text "Smith"
  When the user clicks "Save Search" and names it "VIP Smiths"
  Then "VIP Smiths" appears in the Saved Searches list

@us132
Scenario: Applying a saved search restores its criteria
  Given a saved search "Hot Buyers" exists with its stored filter criteria
  When the user clicks "Hot Buyers" in the Saved Searches list
  Then the contacts list updates to show only contacts matching the saved criteria

@us132
Scenario: Duplicate saved search name is rejected
  Given a saved search named "My Filter" already exists
  When the user tries to save another search with the name "My Filter"
  Then an error is shown and the duplicate is not saved

@us132
Scenario: Deleting a saved search removes it from the list
  Given a saved search "Old Filter" exists
  When the user deletes "Old Filter" and confirms
  Then "Old Filter" no longer appears in the Saved Searches list

@us132
Scenario: Saved searches persist after application restart
  Given the user has saved a search named "Weekly Prospects"
  When the user restarts the application and opens the Contacts section
  Then "Weekly Prospects" is still listed in Saved Searches and applies correctly when clicked
```

## Manual Tests

**Story:** [US-117 — Save Search Criteria](../docs/117-save-search-criteria.md)

### Saving a search with active filters
1. In the Contacts section, apply a search term and one or more tag filters
2. Click "Save Search" and enter a name
3. Confirm the name appears in the Saved Searches list

### Applying a saved search
1. Clear all active filters
2. Click a saved search from the list
3. Confirm the contact list updates to show only contacts matching the saved criteria
4. Confirm the filter controls reflect the stored criteria (search text, tags, etc.)

### Duplicate name is rejected
1. Save a search with any name
2. Attempt to save a second search using the same name
3. Confirm an error is shown and no duplicate is created

### Deleting a saved search
1. Delete a saved search and confirm the prompt
2. Confirm it no longer appears in the list
3. Confirm the contacts list is unaffected (no automatic filter change)

### Saved searches survive a restart
1. Save a search, close the application, and reopen it
2. Confirm the saved search is still listed and applies correctly when clicked

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_saved_searches.py` |
| Manual tests | `tests/manual/shell/saved_searches.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
