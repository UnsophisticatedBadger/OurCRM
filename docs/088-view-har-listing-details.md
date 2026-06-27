# US-088 — View HAR Listing Details

**Capability:** MLS Integration
**Status:** Not Done

## User Story

As a real estate agent, I want to view the full details of a specific HAR listing so that I can evaluate the property before showing it to buyers or importing it into my Properties.

## Dependencies

- US-085 — Fetch HAR MLS Listings

## Acceptance Criteria

1. Clicking a listing row opens a detail view that displays all available MLS fields: full address, price, bedrooms, bathrooms, square footage, lot size, year built, property type, MLS number, listing date, days on market, listing agent name, and listing brokerage
2. If the listing has photos, a horizontal thumbnail strip is shown; clicking a thumbnail opens the image in the OS default image viewer
3. If the listing has no photos, the photos section shows "No photos available"
4. The full property description is displayed as readable text
5. Features and amenities from the HAR API response are shown as a list
6. Days on market is calculated from the listing date (today minus listing date, in whole days) and labelled "N days on market"
7. An "Import as Property" button is present and triggers the import flow defined in US-087
8. A "Schedule Showing" button is present and navigates to the showing creation form with the listing address pre-filled
9. A Back button returns to the listings list, preserving the previous scroll position and any active search criteria

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/mls.feature`.

```gherkin
@us104
Scenario: Clicking a listing row opens the detail view with all MLS fields
  Given a cached listing with MLS#77001, address "456 Pine Ave", price $320,000, 3 beds, 2 baths, 1,800 sqft, listed 24 days ago
  When the user clicks the MLS#77001 listing row
  Then the detail view shows address "456 Pine Ave", price $320,000, 3 beds, 2 baths, 1,800 sqft, and "24 days on market"

@us104
Scenario: Detail view shows a thumbnail strip when photos are available
  Given a cached listing has 5 photo URLs provided by the HAR API
  When the user views that listing's detail
  Then 5 photo thumbnails are displayed in a horizontal strip

@us104
Scenario: Detail view shows no-photos message when a listing has no photos
  Given a cached listing has no photo URLs
  When the user views that listing's detail
  Then the photos section shows "No photos available"

@us104
Scenario: Import as Property button starts the import flow
  Given the user is viewing a HAR listing's detail
  When the user clicks "Import as Property"
  Then the import flow defined in US-087 begins for that listing

@us104
Scenario: Back button returns to the listings list at the same scroll position
  Given the user scrolled to listing row 15 and opened its detail view
  When the user clicks Back
  Then the listings list is shown at the same scroll position with any active search criteria still applied
```

## Manual Tests

**Story:** [US-088 — View HAR Listing Details](../docs/088-view-har-listing-details.md)

### All MLS fields are displayed
1. Fetch listings and click any listing row
2. Confirm the detail view shows: full address, price, beds, baths, sqft, lot size, year built, property type, MLS number, listing date, days on market, agent name, and brokerage

### Photos load as thumbnails
1. Click a listing that has photos
2. Confirm thumbnails appear in a horizontal strip
3. Click a thumbnail and confirm it opens in the OS default image viewer

### No-photos state
1. View a listing with no photos (or use a stub with an empty photos list)
2. Confirm "No photos available" is shown

### Days on market is calculated correctly
1. Note the listing date shown in the detail view
2. Count the days from that date to today
3. Confirm the displayed "N days on market" matches

### Import as Property
1. View a listing's detail and click "Import as Property"
2. Confirm the import flow starts (per US-087 — a success confirmation appears)

### Schedule Showing
1. View a listing's detail and click "Schedule Showing"
2. Confirm the showing creation form opens with the address pre-filled

### Back navigation preserves list state
1. Fetch listings and scroll partway down the list
2. Click a listing to open its detail
3. Click Back
4. Confirm the list is at the same scroll position with any search criteria still applied

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/mls.feature` |
| BDD step defs | `tests/bdd/test_mls.py` |
| Unit tests | `tests/unit/mls/test_listing_detail.py` |
| Manual tests | `tests/manual/mls/listing_detail.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
