# 51 - Search HAR MLS Listings

**Capability:** MLS Integration
**Milestone:** v0.5.0 — MVP
**Status:** Not Done
**GitHub Issue:** #51

## User Story

As a real estate agent, I want to search through fetched HAR listings by specific criteria so that I can quickly find properties that match a buyer's needs.

## Dependencies

- #131 — Fetch HAR MLS Listings

## Notes

Search operates on the locally cached listings retrieved by #131 — no additional API call is made. If the cache is empty, the search section shows the same "Fetch listings first" prompt as #131.

## Acceptance Criteria

1. The MLS section includes a search form with fields for city, ZIP code, minimum price, maximum price, minimum bedrooms, minimum bathrooms, and property type (Single Family / Condo / Townhouse / Land / Other)
2. Clicking "Search" filters the cached listings to rows matching all entered criteria simultaneously (AND logic)
3. Search results display the same columns as the fetched listings list: MLS number, address, price, bedrooms, bathrooms, square footage
4. Results can be sorted by price (low to high / high to low) or by listing date (newest first)
5. When no cached listings match the criteria, the section shows "No listings match your search"
6. Clearing all criteria and searching again restores the full cached listing set

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/mls.feature`.

```gherkin
@story_51
Scenario: Search by city filters cached listings to that city
  Given 10 cached HAR listings exist, 4 in Houston and 6 in Sugar Land
  When the user enters city "Houston" and clicks "Search"
  Then 4 listings are shown, all in Houston

@story_51
Scenario: Multiple criteria are combined with AND logic
  Given cached listings include properties at various prices and bedroom counts
  When the user enters min price $300,000, max price $500,000, and min bedrooms 3 and clicks "Search"
  Then only listings that satisfy all three criteria are shown

@story_51
Scenario: Search by ZIP code returns only listings in that ZIP
  Given cached listings include properties in multiple ZIP codes
  When the user enters ZIP code "77005" and clicks "Search"
  Then only listings with ZIP code 77005 are shown

@story_51
Scenario: Sorting by price low to high reorders results
  Given search results contain listings at $350,000 and $420,000
  When the user selects sort "Price: Low to High"
  Then the $350,000 listing appears before the $420,000 listing

@story_51
Scenario: No matching listings shows an empty-results message
  Given cached listings contain no 5-bedroom properties
  When the user searches for min bedrooms 5
  Then the message "No listings match your search" is shown

@story_51
Scenario: Clearing criteria and searching restores the full cached set
  Given a filtered search is showing 3 of 10 cached listings
  When the user clears all criteria and clicks "Search"
  Then all 10 cached listings are shown
```

## Manual Tests

**Story:** [#132 — Search HAR MLS Listings](../docs/074-search-harmls-listings.md)

### Search by single criterion
1. Fetch listings so the cache is populated
2. Enter a city name and click "Search"
3. Confirm only listings in that city are shown
4. Check a few rows to verify accuracy

### Search by multiple criteria simultaneously
1. Enter city, a price range, and minimum bedrooms
2. Click "Search"
3. Confirm each result satisfies all three criteria

### Search by ZIP code
1. Enter a ZIP code and click "Search"
2. Confirm all results show that ZIP code

### Sort results
1. Perform a search with several results
2. Sort by "Price: Low to High" and confirm the order
3. Sort by "Price: High to Low" and confirm it reverses
4. Sort by "Listing Date: Newest First" and confirm the order

### No-results state
1. Enter criteria unlikely to match any listing
2. Confirm "No listings match your search" is shown

### Clear criteria restores full list
1. Perform a filtered search
2. Clear all criteria fields and click "Search"
3. Confirm all cached listings are shown again

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/mls.feature` |
| BDD step defs | `tests/bdd/test_mls.py` |
| Unit tests | `tests/unit/mls/test_listing_search.py` |
| Manual tests | `tests/manual/mls/listing_search.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
