# US-034: Track Lead Source

## User Story

**As an** agent  
**I want to** track where each lead came from  
**So that** I can measure which marketing channels are most effective

## Priority

**MVP:** Must Have

**Rationale:** Knowing which lead sources produce the best results is critical for business decisions. If Zillow leads convert at 30% but Facebook leads convert at 5%, the agent should focus on Zillow. Without source tracking, agents can't optimize their marketing spend.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design source selection UI (dropdown with common sources)
- 1 hour: Implement source field in lead form
- 1 hour: Add custom source option
- 1 hour: Display source in lead list and details
- 1 hour: Implement source-based filtering
- 1 hour: Create source statistics view (optional)
- 1 hour: Test source tracking
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-030 (Create a New Lead)

**Blocks:** None

## Description

Users should be able to specify where each lead came from. Sources include common real estate lead sources like Zillow, Realtor.com, Realtor, Facebook, Google Ads, Website, Referral, Open House, and Others. Users can also enter custom sources.

The source is displayed in the lead list and details, and can be used for filtering and reporting. Tracking sources helps agents understand which marketing efforts are most effective.

## BDD Scenarios

### Scenario 1: Select source when creating lead

```
Given I am creating a new lead
When I select a source from the source dropdown
  (e.g., Zillow, Realtor.com, Facebook, Referral, etc.)
  And I save the lead
Then the source should be saved with the lead
```

### Scenario 2: Common sources are predefined

```
Given I am creating a lead
When I view the source dropdown
Then I should see common real estate lead sources:
  - Zillow
  - Realtor.com
  - Realtor
  - Facebook
  - Google Ads
  - Website
  - Referral
  - Open House
  - Walk-in
  - Other
```

### Scenario 3: Custom source option

```
Given I am creating a lead
When I select "Other" from the source dropdown
Then a text field should appear
  And I can enter a custom source name
```

### Scenario 4: Source is displayed in lead list

```
Given I am viewing the lead list
When I look at each lead
Then the source should be displayed in a column
  And it should be clearly visible
```

### Scenario 5: Filter leads by source

```
Given I have leads from various sources
When I filter by a specific source (e.g., "Zillow Only")
Then only leads from that source should be displayed
  And the filter should be clearly indicated
```

### Scenario 6: Change source from lead details

```
Given I am viewing a lead's details
When I edit the source field
  And I save the changes
Then the source should be updated
```

### Scenario 7: Source persists across restarts

```
Given I have set a source for a lead
When I close the application
  And I restart the application
  And I open the lead
Then the source should be the same as what I set
```

### Scenario 8: Optional source field

```
Given I am creating a lead
When I leave the source field empty
  And I save the lead
Then the lead should be saved without a source
  And the source should be displayed as "Not specified" or similar
```

## Manual Testing Steps

### Test 1: Select source when creating

1. Create a new lead
2. Click on the source dropdown
3. Verify all common sources are listed
4. Select "Zillow"
5. Save the lead
6. Verify the source is saved
7. Open the lead details
8. Verify "Zillow" is displayed

### Test 2: Test predefined sources

1. View the source dropdown
2. Verify all expected sources are present
3. Test selecting each one
4. Verify they all save correctly

### Test 3: Test custom source

1. Create a lead
2. Select "Other" from the source dropdown
3. Verify a text field appears
4. Enter "Real Estate Conference 2024"
5. Save the lead
6. Verify the custom source is saved

### Test 4: Test source in list

1. Create leads with various sources
2. View the lead list
3. Verify each lead shows its source
4. Check that the source column is clear and readable

### Test 5: Test source filtering

1. Create leads with different sources
2. Filter by "Zillow"
3. Verify only Zillow leads are shown
4. Clear the filter
5. Verify all leads are shown again

### Test 6: Test source change

1. Open a lead's details
2. Change the source from "Zillow" to "Referral"
3. Save the changes
4. Verify the source updated
5. Check the list to verify it's reflected

### Test 7: Test source persistence

1. Set a source for a lead
2. Close the application
3. Restart the application
4. Open the lead
5. Verify the source is still there

### Test 8: Test optional source

1. Create a lead without selecting a source
2. Save the lead
3. Verify it saves successfully
4. View the lead
5. Verify source is shown as "Not specified" or similar

### Test 9: Test on all platforms

1. Test source tracking on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Source dropdown is available in lead form
- [ ] Common real estate sources are predefined
- [ ] Custom source option is available
- [ ] Source is displayed in lead list
- [ ] Source is displayed in lead details
- [ ] Leads can be filtered by source
- [ ] Source can be changed from lead details
- [ ] Source persists across restarts
- [ ] Source field is optional
- [ ] Empty source is handled gracefully
- [ ] Works on Windows, macOS, and Linux
- [ ] Source data is encrypted in database
- [ ] Source tracking is accurate and reliable