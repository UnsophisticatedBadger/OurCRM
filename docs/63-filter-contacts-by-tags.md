# 63 - Filter Contacts By Tags

**Capability:** Contacts
**Milestone:** MVP
**Status:** Not Done
**GitHub Issue:** #63

## User Story

As a real estate agent, I want to filter my contact list by tag, so that I can focus on a specific group — all buyers, all investors, all past clients — without scrolling through everyone.

## Dependencies

- #50 — Tag Contacts
- #44 — View Contact List

## Acceptance Criteria

1. The Contacts section shows a tag filter panel listing every unique tag used across all contacts, each with a count of how many contacts carry it; "All Contacts" with the total count is always shown at the top
2. Clicking a tag shows only contacts with that tag; the selected tag is visually highlighted in the filter panel
3. Clicking "All Contacts" (or the active tag a second time) clears the filter and shows all contacts
4. When a filter is active and no contacts match, "No contacts with this tag" is shown
5. The active filter is preserved when the user navigates away from Contacts and returns
6. Tag counts update immediately when a contact's tags are added or removed

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/contacts.feature`.

```gherkin
@story_63
Scenario: Tag filter panel shows all unique tags with counts
  Given contacts tagged "buyer" (3) and "seller" (2) exist
  When the user opens the Contacts section
  Then the filter panel shows "buyer (3)" and "seller (2)"
  And "All Contacts (5)" is shown at the top

@story_63
Scenario: Clicking a tag shows only matching contacts
  Given the filter panel is visible
  When the user clicks the "buyer" tag
  Then only contacts tagged "buyer" are shown
  And "buyer" is visually highlighted in the filter panel

@story_63
Scenario: Clicking All Contacts clears the filter
  Given the user has filtered by "buyer"
  When the user clicks "All Contacts"
  Then all contacts are shown and no tag is selected

@story_63
Scenario: Empty filter result shows a helpful message
  Given the user filters by a tag that no current contacts carry
  Then "No contacts with this tag" is shown

@story_63
Scenario: Active filter is preserved after navigating away and back
  Given the user has filtered by "buyer"
  When the user navigates to Leads and returns to Contacts
  Then the "buyer" filter is still active and the filtered list is shown
```

## Manual Tests

**Story:** [#51 — Filter Contacts by Tags](../docs/023-filter-contacts-by-tags.md)

### User sees all tags listed with correct counts
1. Create 3 contacts tagged "buyer" and 2 tagged "seller"
2. Open the Contacts section
3. Confirm the filter panel shows "buyer (3)", "seller (2)", and "All Contacts (5)"

### User filters by a tag and sees only matching contacts
1. Click "buyer" in the filter panel
2. Confirm only the 3 buyer contacts appear in the list
3. Confirm "buyer" is visually selected in the panel

### User clears the filter
1. With a filter active, click "All Contacts"
2. Confirm all contacts reappear and no tag is highlighted

### Empty filter result shows a message
1. Remove all contacts with a particular tag (or create a tag with no contacts)
2. Filter by that tag
3. Confirm "No contacts with this tag" appears

### Filter persists after navigating away
1. Apply the "buyer" filter
2. Navigate to Leads, then return to Contacts
3. Confirm the "buyer" filter is still active

### Tag counts update when tags change
1. Filter panel shows "buyer (3)"
2. Open a buyer contact and remove the "buyer" tag
3. Return to the Contacts section
4. Confirm the panel now shows "buyer (2)"

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/contacts.feature` |
| BDD step defs | `tests/bdd/test_contacts.py` |
| Unit tests | `tests/unit/contacts/test_contact_tag_filter.py` |
| Manual tests | `tests/manual/contacts/filter_by_tags.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
