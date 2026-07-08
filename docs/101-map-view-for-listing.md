# 101 - Map View For MLS Listing

**Capability:** mls
**Milestone:** MVP
**Status:** Not Done
**GitHub Issue:** #101
**Priority:** Post-MVP

## User Story
As an agent, I want to see a map showing an MLS listing's location, so that I can quickly judge the property's neighbourhood context without leaving OurCRM.

## Dependencies
- #134 — View MLS Listing Details

## Acceptance Criteria
1. The MLS listing detail view includes a Map tab alongside the Photos tab
2. The Map tab shows an embedded map centred on the property's address, sourced from the OS default map service or an embedded tile renderer
3. The map displays a pin at the property's location with the address as a label
4. If the address cannot be geocoded, the Map tab shows "Location unavailable" instead of a blank map
5. The user can zoom and pan the map within the tab

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/mls.feature`.

```gherkin
@story_101
Scenario: Map tab shows a pin at the listing's address
  Given an MLS listing detail is open for "123 Main St, Houston, TX"
  When the user opens the Map tab
  Then a map is shown centred on 123 Main St with a location pin

@story_101
Scenario: Map tab shows a fallback message when the address cannot be geocoded
  Given an MLS listing has an address that cannot be geocoded
  When the user opens the Map tab
  Then "Location unavailable" is shown instead of a map
```

## Manual Tests
**Story:** [#189 — Map View for MLS Listing](../docs/181-map-view-for-listing.md)

### Map shows the listing location
1. Open an MLS listing detail for a property with a valid address
2. Click the Map tab
3. Verify a map is displayed centred on the property with a pin

### Unavailable address shows fallback message
1. Open an MLS listing with a non-geocodable address (or test with a blank address)
2. Click the Map tab and verify "Location unavailable" is shown

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/mls.feature` |
| BDD step defs | `tests/bdd/test_mls.py` |
| Unit tests | `tests/unit/mls/test_map_view.py` |
| Manual tests | `tests/manual/mls/map-view-for-listing.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
