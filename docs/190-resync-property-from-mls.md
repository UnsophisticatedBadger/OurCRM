# US-190 — Re-Sync Property from MLS

**Capability:** mls
**Status:** Not Done
**Priority:** Post-MVP

## User Story
As an agent, I want to refresh a property that was imported from MLS with the latest listing data, so that my property record stays up to date without re-importing manually.

## Dependencies
- US-087 — Import MLS Listing as Property

## Acceptance Criteria
1. A "Refresh from MLS" button appears on the detail view of any property that was originally imported from an MLS listing
2. Clicking it fetches the current listing data from the HAR API using the stored MLS number
3. The following fields are updated from the fetched data: list price, status, description, and photos
4. Fields that were manually edited in OurCRM after import (address, property type, custom notes) are not overwritten
5. If the listing is no longer available on the MLS, an informational message is shown and no fields are changed
6. The property detail shows the date and time of the last MLS sync

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/mls.feature`.

```gherkin
@us203
Scenario: Refresh from MLS updates the list price
  Given a property was imported from MLS with list price $500,000
  And the MLS listing now shows $490,000
  When the user clicks "Refresh from MLS"
  Then the property's list price is updated to $490,000

@us203
Scenario: Manually edited fields are not overwritten by refresh
  Given a property was imported from MLS and the agent edited the notes field
  When the user refreshes from MLS
  Then the notes field retains the agent's edits

@us203
Scenario: Refresh shows a message when the listing is no longer on MLS
  Given a property was imported from MLS but the listing has since been removed
  When the user clicks "Refresh from MLS"
  Then an informational message is shown and no property fields are changed

@us203 @live_mls
Scenario: Real MLS refresh updates a property from a live listing
  Given a property imported from a real MLS listing
  When the user clicks "Refresh from MLS"
  Then the last synced date updates to the current date and time
```

## Manual Tests
**Story:** [US-179 — Re-Sync Property from MLS](../docs/179-resync-property-from-mls.md)

### Refresh from MLS updates the list price
1. Open a property that was imported from MLS
2. Click "Refresh from MLS"
3. Verify the list price, status, and description reflect the latest MLS data
4. Verify the last synced date updates

### Manually edited notes are not overwritten
1. Edit the notes field on an MLS-imported property
2. Refresh from MLS
3. Verify the notes field still contains the manual edits

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/mls.feature` |
| BDD step defs | `tests/bdd/test_mls.py` |
| Unit tests | `tests/unit/mls/test_resync_property.py` |
| Manual tests | `tests/manual/mls/resync-property-from-mls.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
