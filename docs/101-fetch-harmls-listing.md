# US-101: Fetch HAR Listings

## User Story

**As an** agent  
**I want to** fetch active listings from the HAR MLS  
**So that** I can see available properties in my market and match them with buyers

## Priority

**MVP:** Must Have

**Rationale:** Accessing MLS data is the core value proposition of real estate CRMs. Agents need to see current listings to match buyers with properties, prepare for showings, and stay informed about the market. Without MLS data access, the CRM loses significant value.

## Estimated Effort

**Size:** Medium (M) - 3 days

**Breakdown:**
- 2 hours: Implement HAR API client
- 2 hours: Implement OAuth authentication
- 2 hours: Build query for active listings
- 1 hour: Create fetch listings UI
- 1 hour: Add progress indicator
- 2 hours: Cache listings data
- 1 hour: Display fetch results
- 1 hour: Add filtering options
- 2 hours: Test with real HAR API
- 1 hour: Test error handling
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-100 (Configure HAR MLS Credentials)

**Blocks:** US-102 (Search HAR Listings), US-103 (Import HAR Listing), US-104 (View HAR Listing Details)

## Description

Users should be able to fetch active property listings from the HAR MLS using their configured credentials. The fetch should retrieve listings based on optional criteria (city, price range, property type, etc.) and display them in a searchable, browsable format.

The system should handle OAuth authentication automatically, respect HAR API rate limits, cache results to minimize API calls, and provide clear feedback during the fetch process. Errors should be handled gracefully with helpful troubleshooting messages.

## BDD Scenarios

### Scenario 1: Fetch all active listings

```
Given I have configured HAR credentials
  And I am in the MLS section
When I click "Fetch Active Listings"
  And I don't specify criteria
Then the system should fetch all active listings
  And show a progress indicator
  And display the results when complete
```

### Scenario 2: Fetch with criteria

```
Given I am in the MLS section
When I enter criteria:
  - City: Houston
  - Min Price: $300,000
  - Max Price: $500,000
  - Property Type: Single Family
  - Bedrooms: 3+
When I click "Fetch"
Then only matching listings should be retrieved
  And displayed in the results
```

### Scenario 3: Fetch progress indicator

```
Given I am fetching a large number of listings
When the fetch is in progress
Then I should see:
  - A progress bar
  - Number of listings fetched so far
  - Estimated time remaining
  - Ability to cancel (optional)
```

### Scenario 4: Cached results

```
Given I have recently fetched listings
When I view the listings again
Then cached results should be shown
  And I should see when the data was last fetched
  And have the option to refresh
```

### Scenario 5: Authentication error

```
Given my HAR credentials are invalid
When I try to fetch listings
Then I should see a clear error message
  And be directed to update my credentials
  And see troubleshooting tips
```

### Scenario 6: Rate limit error

```
Given I have made too many API calls
When I try to fetch listings
Then I should see a rate limit error
  And be told when I can try again
  And the system should respect rate limits automatically
```

### Scenario 7: No results found

```
Given I search with very specific criteria
When no listings match
Then I should see a "No listings found" message
  And suggestions to broaden the search
```

### Scenario 8: Fetch results are saved

```
Given I have fetched listings
When I close and reopen the application
Then the cached listings should still be available
  And I can see when they were last fetched
```

## Manual Testing Steps

### Test 1: Fetch all active listings

1. Configure HAR credentials
2. Go to MLS section
3. Click "Fetch Active Listings"
4. Verify the progress indicator
5. Wait for completion
6. Verify listings are displayed
7. Check the count of listings

### Test 2: Fetch with criteria

1. Enter specific criteria (city, price, etc.)
2. Click "Fetch"
3. Verify only matching listings are shown
4. Verify the results match the criteria
5. Try different criteria combinations

### Test 3: Test progress indicator

1. Fetch a large number of listings
2. Verify the progress bar updates
3. Verify the count increases
4. Test the cancel button (if implemented)

### Test 4: Test caching

1. Fetch listings
2. Note the fetch time
3. Close and reopen the application
4. View the listings
5. Verify cached results are shown
6. Check the "last fetched" timestamp
7. Click "Refresh" to update

### Test 5: Test authentication error

1. Use invalid HAR credentials
2. Try to fetch listings
3. Verify the error message
4. Verify it directs to credential settings
5. Update credentials and retry

### Test 6: Test rate limit

1. Make many rapid API calls
2. Verify rate limit error appears
3. Check the retry timing
4. Wait and retry
5. Verify it works after the wait period

### Test 7: Test no results

1. Search with very specific criteria
2. Verify "No listings found" message
3. Verify suggestions to broaden search
4. Broaden the criteria
5. Verify results appear

### Test 8: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Can fetch active HAR listings
- [ ] Can fetch with custom criteria
- [ ] Progress indicator shows during fetch
- [ ] Results are cached for performance
- [ ] Cached results show last fetch time
- [ ] Can refresh cached results
- [ ] Authentication errors are handled
- [ ] Rate limits are respected
- [ ] No results state is clear
- [ ] Large result sets are handled well
- [ ] Fetched data persists across restarts
- [ ] Works on Windows, macOS, and Linux
- [ ] Error messages include troubleshooting
- [ ] OAuth authentication works automatically
