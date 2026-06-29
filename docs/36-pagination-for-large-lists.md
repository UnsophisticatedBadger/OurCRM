# 36 - Pagination For Large Lists

**Capability:** shell
**Milestone:** v0.2.0 — Secure Shell
**Status:** Not Done
**GitHub Issue:** #36
**Priority:** Post-MVP

## User Story
As an agent, I want large record lists to be displayed in pages, so that the app stays responsive when I have thousands of contacts, leads, or properties.

## Dependencies
- #44 — View Contact List
- #63 — View Lead List

## Acceptance Criteria
1. All record list views (Contacts, Leads, Properties, Transactions, Tasks) display records in pages of 100 by default
2. Pagination controls below the list show: Previous, Next, current page number, total page count, and total record count (e.g. "Page 2 of 12 — 1,150 records")
3. The user can jump directly to a specific page by entering a page number in the page control
4. The user can change the page size from Settings → General; options are 25, 50, 100, and 200
5. Active filters and sort order are preserved when navigating between pages
6. Navigating to a new page scrolls the list back to the top

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/shell.feature`.

```gherkin
@story_142
Scenario: Contact list is paginated when there are more records than the page size
  Given 250 contacts exist and the page size is 100
  When the user opens the Contacts list
  Then the first 100 contacts are shown
  And pagination controls show "Page 1 of 3 — 250 records"

@story_142
Scenario: Next and Previous buttons navigate between pages
  Given the user is on page 1 of the Contacts list
  When the user clicks "Next"
  Then page 2 is displayed
  When the user clicks "Previous"
  Then page 1 is displayed again

@story_142
Scenario: Jumping to a specific page navigates directly there
  Given the Contacts list has 5 pages
  When the user enters "4" in the page number field
  Then page 4 is displayed

@story_142
Scenario: Active filters are preserved when changing pages
  Given a status filter is applied to the Leads list showing results across 3 pages
  When the user navigates to page 2
  Then the status filter is still active and only filtered records are shown

@story_142
Scenario: Page size change applies immediately
  Given the user changes the page size from 100 to 25 in Settings
  When the user views the Contacts list
  Then 25 records are shown per page and the page count updates accordingly
```

## Manual Tests
**Story:** [#93 — Pagination for Large Lists](../docs/144-pagination-for-large-lists.md)

### Contacts list shows pagination controls with many records
1. Ensure more than 100 contacts exist
2. Open the Contacts list and verify pagination controls appear below the list
3. Verify the count shows the correct total number of contacts

### Next/Previous and jump-to-page navigation works
1. Click Next to go to page 2 and verify the page indicator updates
2. Click Previous to return to page 1
3. Enter a page number directly and verify the list jumps to that page

### Filters are preserved when changing pages
1. Apply a filter to the Leads list
2. Navigate to page 2
3. Verify the filter is still active and only matching records are shown

### Page size setting changes the number of records per page
1. Change page size to 25 in Settings → General
2. Open the Contacts list and verify exactly 25 records are shown

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_pagination.py` |
| Manual tests | `tests/manual/shell/pagination.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
