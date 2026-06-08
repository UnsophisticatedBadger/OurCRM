# US-102: Search HAR Listings

## User Story

**As an** agent  
**I want to** search through HAR listings with specific criteria  
**So that** I can quickly find properties that match my buyers' needs

## Priority

**MVP:** Must Have

**Rationale:** Real estate agents spend significant time searching for properties that match their buyers' criteria. Efficient search functionality is critical for productivity and for providing good service to clients.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design search criteria UI
- 2 hours: Create search form with all criteria fields
- 1 hour: Implement search logic
- 1 hour: Add inline results
- 1 hour: Add advanced search options
- 1 hour: Implement search history
- 1 hour: Test search with various criteria
- 1 hour: Test search performance
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-101 (Fetch HAR Listings), US-100 (Configure HAR MLS Credentials)

**Blocks:** US-103 (Import HAR Listing), US-104 (View HAR Listing Details)

## Description

Users should be able to search through HAR listings using various criteria: city, ZIP code, price range, bedrooms, bathrooms, square footage, property type, and keywords. The search should be fast, support multiple criteria simultaneously, and return relevant results.

The search can work on both cached listings and live API queries, depending on the user's preference. Results should be displayed inline as the user types (for simple searches) or after clicking a search button (for complex queries).

## BDD Scenarios

### Scenario 1: Basic search

```
Given I have fetched HAR listings
When I enter a city name (e.g., "Houston")
  And I click "Search"
Then all listings in Houston should be displayed
  And the results should be sorted by relevance or date
```

### Scenario 2: Search with multiple criteria

```
Given I am searching HAR listings
When I enter:
  - City: Houston
  - Min Price: $300,000
  - Max Price: $500,000
  - Bedrooms: 3
  - Bathrooms: 2
  - Property Type: Single Family
When I click "Search"
Then only listings matching ALL criteria should be shown
```

### Scenario 3: Price range search

```
Given I am searching HAR listings
When I set min price to $300,000 and max price to $500,000
Then only listings in that price range should be shown
  And the results should be sorted by price
```

### Scenario 4: Search by ZIP code

```
Given I am searching HAR listings
When I enter a ZIP code
Then all listings in that ZIP code should be shown
```

### Scenario 5: Keyword search

```
Given I am searching HAR listings
When I enter keywords (e.g., "pool", "garage", "updated")
Then listings with those features in the description should be shown
```

### Scenario 6: Save search criteria

```
Given I have performed a search with specific criteria
When I click "Save Search"
Then I can save the search criteria with a name
  And access it later from "Saved Searches"
```

### Scenario 7: Search results are sortable

```
Given I have search results
When I sort by:
  - Price (low to high, high to low)
  - Square footage
  - Bedrooms
  - Listing date
Then the results should be sorted accordingly
```

### Scenario 8: Search performance

```
Given I have 10,000 listings cached
When I search with specific criteria
Then results should appear within 1 second
  And the UI should remain responsive
```

## Manual Testing Steps

### Test 1: Basic search

1. Fetch HAR listings
2. Enter "Houston" in the city field
3. Click "Search"
4. Verify only Houston listings are shown
5. Verify the count is correct

### Test 2: Multi-criteria search

1. Enter multiple criteria
2. Click "Search"
3. Verify only matching listings are shown
4. Verify the results match all criteria
5. Try different combinations

### Test 3: Price range search

1. Set min and max price
2. Click "Search"
3. Verify results are in the price range
4. Verify prices are within the specified range
5. Sort by price to verify

### Test 4: ZIP code search

1. Enter a ZIP code
2. Click "Search"
3. Verify listings in that ZIP are shown
4. Try different ZIP codes
5. Verify accuracy

### Test 5: Keyword search

1. Enter keywords
2. Click "Search"
3. Verify listings with those features are shown
4. Try different keywords
5. Test with multiple keywords

### Test 6: Save search

1. Perform a search
2. Click "Save Search"
3. Enter a name
4. Save it
5. Access it from Saved Searches later
6. Verify it runs the same search

### Test 7: Test sorting

1. Have search results
2. Sort by various criteria
3. Verify sorting works correctly
4. Test ascending and descending order

### Test 8: Test performance

1. Fetch many listings
2. Search with criteria
3. Measure response time
4. Verify it's under 1 second
5. Test UI responsiveness

### Test 9: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Can search by city
- [ ] Can search by ZIP code
- [ ] Can search by price range
- [ ] Can search by bedrooms/bathrooms
- [ ] Can search by property type
- [ ] Can search by keywords
- [ ] Multiple criteria can be combined
- [ ] Results can be sorted by various fields
- [ ] Search is fast (under 1 second with large datasets)
- [ ] Search results are relevant
- [ ] Can save search criteria
- [ ] Works on Windows, macOS, and Linux
- [ ] UI is intuitive and easy to use
- [ ] No results state is clear
