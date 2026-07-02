# 78 - Fetch HAR MLS Listings

**Capability:** MLS Integration
**Milestone:** MVP
**Status:** Not Done
**GitHub Issue:** #78

## User Story

As a real estate agent, I want to fetch active property listings from the HAR MLS so that I can browse current inventory and match properties to buyers.

## Dependencies

- #130 — Configure HAR MLS Credentials

## Notes

**Third-party testability:** All scenarios that call the HAR API are tagged `@live_mls` and skipped in CI. Unit tests stub the HTTP response and assert on the parsed listing structure — they verify fields like MLS number, address, price, bedrooms, and status are extracted correctly, not that the live API returns specific listings.

Fetched listings are cached locally. The cache is keyed by the fetch criteria and stores the response alongside a timestamp. Subsequent views of the MLS section load from cache; a "Refresh" action triggers a new API call.

## Acceptance Criteria

1. An MLS section in the main navigation provides a "Fetch Listings" button and optional filter fields: city, minimum price, maximum price, property type (Single Family / Condo / Townhouse / Land / Other)
2. Clicking Fetch Listings calls the HAR API with the entered criteria and displays the returned listings — each row shows MLS number, address, price, bedrooms, bathrooms, and square footage
3. Fetched results are cached locally; the section header shows "Last fetched: [date/time]" and a "Refresh" button
4. If credentials are not configured, the section shows "Configure HAR credentials in Settings before fetching" with a link to Settings → MLS
5. An authentication failure (invalid credentials) shows a clear error message directing the user to Settings → MLS
6. A HAR API rate-limit response shows "Rate limit reached — please wait before fetching again"
7. When no listings match the criteria, the section shows "No listings found for the selected criteria"
8. Cached listings are available after an application restart until a Refresh is performed

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/mls.feature`.

```gherkin
@live_mls
@story_78
Scenario: Fetching with no criteria returns active listings from HAR
  Given valid HAR credentials are configured
  When the user clicks "Fetch Listings" with no criteria entered
  Then a list of active HAR listings is displayed, each showing MLS number, address, price, bedrooms, bathrooms, and square footage

@live_mls
@story_78
Scenario: Fetching with city and price criteria returns filtered results
  Given valid HAR credentials are configured
  When the user enters city "Houston", min price $300,000, max price $500,000 and clicks "Fetch Listings"
  Then only listings in Houston between $300,000 and $500,000 are displayed

@story_78
Scenario: No credentials configured shows a setup prompt
  Given HAR credentials have not been configured
  When the user opens the MLS section
  Then the message "Configure HAR credentials in Settings before fetching" is shown with a link to Settings

@story_78
Scenario: Cached listings are displayed after restart
  Given listings were fetched and cached before the last restart
  When the user opens the MLS section after restarting the application
  Then the previously fetched listings are shown with the original "Last fetched" timestamp

@live_mls
@story_78
Scenario: Invalid credentials show an authentication error
  Given invalid HAR credentials are configured
  When the user clicks "Fetch Listings"
  Then an authentication error is shown directing the user to update credentials in Settings → MLS
```

## Manual Tests

**Story:** [#131 — Fetch HAR MLS Listings](../docs/085-fetch-harmls-listing.md)

### No credentials shows setup prompt
1. Open the MLS section without configuring credentials
2. Confirm a message prompts the user to configure credentials in Settings
3. Click the link and confirm it navigates to Settings → MLS

### Fetch with no criteria returns listings
1. Configure valid HAR credentials
2. Click "Fetch Listings" with no criteria
3. Confirm a list of listings appears with MLS number, address, price, bedrooms, bathrooms, and square footage
4. Confirm the header shows "Last fetched: [today's date and time]"

### Fetch with criteria filters results
1. Enter city "Houston" and a price range
2. Click "Fetch Listings"
3. Confirm results match the criteria (check several listings manually)

### Refresh updates the cache
1. Note the "Last fetched" timestamp
2. Click "Refresh"
3. Confirm the timestamp updates and listings reload

### Authentication error is handled
1. Enter an invalid client secret in Settings → MLS
2. Click "Fetch Listings"
3. Confirm an error message appears and directs to Settings → MLS

### Cached listings survive restart
1. Fetch listings successfully
2. Close and reopen the application
3. Open the MLS section and confirm the listings are still shown with the original timestamp

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/mls.feature` |
| BDD step defs | `tests/bdd/test_mls.py` |
| Unit tests | `tests/unit/mls/test_listing_fetch.py` |
| Manual tests | `tests/manual/mls/listing_fetch.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
