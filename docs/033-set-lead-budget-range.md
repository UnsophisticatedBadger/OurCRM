# US-033: Set Lead Budget Range

## User Story

**As an** agent  
**I want to** set a budget range (min and max) for a lead  
**So that** I can match them with properties in their price range and know what they can afford

## Priority

**MVP:** Must Have

**Rationale:** Budget is one of the most critical factors in real estate. Agents need to know what properties a lead can afford to avoid wasting time showing properties outside their range. Budget also helps with lead qualification.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design budget input UI
- 1 hour: Implement min and max budget fields
- 1 hour: Add validation (min <= max)
- 1 hour: Add currency formatting
- 1 hour: Display budget range in lead list and details
- 1 hour: Test budget entry and validation
- 1 hour: Test budget display formatting
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-030 (Create a New Lead)

**Blocks:** US-034 (Track Lead Source), US-037 (Match Lead with Properties)

## Description

Users should be able to set a minimum and maximum budget for each lead. The budget represents the price range the lead is looking for or can afford. The system should validate that the minimum is not greater than the maximum, and should format the budget as currency for display.

The budget range is used for:
- Matching leads with properties in their range
- Filtering and searching leads by budget
- Qualifying leads (do they have realistic expectations?)
- Displaying in lead list and details

## BDD Scenarios

### Scenario 1: Set budget when creating lead

```
Given I am creating a new lead
When I enter a minimum budget (e.g., $300,000)
  And I enter a maximum budget (e.g., $500,000)
  And I save the lead
Then the budget range should be saved
```

### Scenario 2: Validate budget range

```
Given I am entering budget information
When I enter a minimum budget greater than the maximum
  And I try to save
Then I should see an error message
  And the error should say "Minimum budget cannot be greater than maximum budget"
```

### Scenario 3: Display budget as range

```
Given a lead has a budget of $300,000 - $500,000
When I view the lead in the list or details
Then the budget should be displayed as "$300,000 - $500,000"
  Or "$300K - $500K" (depending on space)
```

### Scenario 4: Display budget with proper formatting

```
Given a lead has a budget of $425000
When the budget is displayed
Then it should be formatted with commas and currency symbol
  And it should be easy to read
```

### Scenario 5: Optional budget fields

```
Given I am creating a lead
When I leave the budget fields empty
  And I save the lead
Then the lead should be saved without budget information
  And the budget should be displayed as "Not specified" or similar
```

### Scenario 6: Change budget from lead details

```
Given I am viewing a lead's details
When I edit the budget fields
  And I save the changes
Then the budget should be updated
```

### Scenario 7: Search/filter by budget

```
Given I have leads with various budget ranges
When I search for leads with a specific budget
Then only leads within or matching that range should appear
```

## Manual Testing Steps

### Test 1: Set budget when creating

1. Create a new lead
2. Enter minimum budget: $300,000
3. Enter maximum budget: $500,000
4. Save the lead
5. Verify the budget is saved
6. Open the lead details
7. Verify the budget is displayed correctly

### Test 2: Test budget validation

1. Create or edit a lead
2. Enter minimum: $500,000
3. Enter maximum: $300,000
4. Try to save
5. Verify the validation error appears
6. Correct the values
7. Verify you can save

### Test 3: Test budget formatting

1. Create leads with various budgets
2. View them in the list
3. Verify budgets are formatted with commas
4. Verify currency symbol is shown
5. Check that the formatting is consistent

### Test 4: Test optional budget

1. Create a lead without entering budget
2. Save the lead
3. Verify it saves successfully
4. View the lead
5. Verify budget is shown as "Not specified" or similar

### Test 5: Test budget change

1. Open a lead's details
2. Edit the budget fields
3. Save the changes
4. Verify the budget updated
5. Check the list to verify it's reflected

### Test 6: Test budget search

1. Create leads with various budgets
2. Use the search to find leads in a specific range
3. Verify the search works correctly
4. Test with different budget ranges

### Test 7: Test on all platforms

1. Test budget entry on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Minimum and maximum budget fields are available
- [ ] Budget can be set when creating a lead
- [ ] Budget can be edited from lead details
- [ ] Validation prevents min > max
- [ ] Budget is formatted as currency with commas
- [ ] Budget is displayed in lead list
- [ ] Budget is displayed in lead details
- [ ] Budget fields are optional
- [ ] Empty budget is handled gracefully
- [ ] Budget changes persist across restarts
- [ ] Works on Windows, macOS, and Linux
- [ ] Currency formatting is consistent
- [ ] Budget can be searched/filtered