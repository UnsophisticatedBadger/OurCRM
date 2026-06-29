# 98 - Bulk Import MLS Listings As Properties

**Capability:** mls
**Milestone:** v0.5.0 — MVP
**Status:** Not Done
**GitHub Issue:** #98
**Priority:** Post-MVP

## User Story
As an agent, I want to select multiple MLS listings and import them all as properties at once, so that I can populate my property list quickly without importing one at a time.

## Dependencies
- #133 — Import MLS Listing as Property

## Acceptance Criteria
1. In the MLS listings view, each row has a checkbox; a "Select All" checkbox in the header selects all visible listings
2. When one or more listings are selected, an "Import Selected" button appears
3. Clicking "Import Selected" shows a confirmation dialog listing the count of listings to import
4. Confirming imports all selected listings as properties; listings already imported are skipped with a count shown in the result summary
5. A result summary after import shows: imported, skipped (already exists), and failed counts

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/mls.feature`.

```gherkin
@story_98
Scenario: Selecting multiple listings enables the Import Selected button
  Given the MLS listings view shows fetched results
  When the user checks the boxes for three listings
  Then the "Import Selected" button is visible

@story_98
Scenario: Bulk import creates a property for each selected listing
  Given three listings are selected and none are already imported
  When the user confirms the bulk import
  Then three new properties are created

@story_98
Scenario: Already-imported listings are skipped in bulk import
  Given two listings are selected and one was previously imported
  When the user confirms the bulk import
  Then one new property is created and the result summary shows "1 imported, 1 skipped"
```

## Manual Tests
**Story:** [#152 — Bulk Import MLS Listings as Properties](../docs/159-bulk-import-mls-listings.md)

### Selecting listings and importing them
1. Select three listings using the checkboxes
2. Click "Import Selected" and confirm
3. Verify three new properties appear in the Properties list

### Already-imported listings are skipped
1. Select a mix of new and previously imported listings
2. Confirm the import and verify the result summary shows the correct imported and skipped counts

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/mls.feature` |
| BDD step defs | `tests/bdd/test_mls.py` |
| Unit tests | `tests/unit/mls/test_bulk_import.py` |
| Manual tests | `tests/manual/mls/bulk-import-listings.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
