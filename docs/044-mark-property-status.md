# US-044: Mark Property Status

## User Story

**As an** agent  
**I want to** change a property's status (Active, Pending, Sold, Withdrawn)  
**So that** I can track where each property is in the sales process

## Priority

**MVP:** Must Have

**Rationale:** Property status is critical for tracking the sales pipeline. Properties move through statuses: Active (listed and available), Pending (under contract but not closed), Sold (closed), or Withdrawn (taken off market). Without status tracking, agents can't manage their listings effectively.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design status selection UI
- 1 hour: Implement status change in property details
- 1 hour: Add visual indicators for current status
- 1 hour: Implement quick status change from list
- 1 hour: Add status change history (optional)
- 1 hour: Test status changes
- 1 hour: Test that status updates reflect in list
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-040 (Create a New Property Listing), US-041 (View Property List)

**Blocks:** US-045 (Schedule Showing for Property), US-046 (Mark Property as Sold)

## Description

Users should be able to change a property's status at any time. The status options are Active (listed and available), Pending (under contract), Sold (closed), and Withdrawn (taken off market). The status should be clearly visible in the property list and details, and should be color-coded for quick identification.

Changing a status should be quick and easy, with the option to change it from either the property details or directly from the property list. The system should track when the status was last changed.

## BDD Scenarios

### Scenario 1: Set status when creating property

```
Given I am creating a new property
When I select a status from the status dropdown
  And I save the property
Then the property should be saved with the selected status
```

### Scenario 2: Change status from property details

```
Given I am viewing a property's details
  And the current status is "Active"
When I click on the status field
  And I select "Pending"
  And I save the change
Then the property's status should be updated to "Pending"
  And the visual indicator should change
```

### Scenario 3: Change status from property list

```
Given I am viewing the property list
  And I have selected a property
When I right-click and select "Change Status"
  Or I use a quick action button
Then I should be able to change the status
  And the change should be reflected immediately in the list
```

### Scenario 4: Status is color-coded

```
Given I am viewing properties with different statuses
When I look at the status indicators
Then Active should be shown in green
  And Pending should be shown in yellow
  And Sold should be shown in gray
  And Withdrawn should be shown in red
```

### Scenario 5: Status persists across restarts

```
Given I have changed a property's status
When I close the application
  And I restart the application
  And I open the property
Then the status should be the updated value
```

### Scenario 6: Status change is logged

```
Given I have changed a property's status multiple times
When I view the property's history (if implemented)
Then I should see when the status was changed
  And what it was changed from and to
```

### Scenario 7: Mark as Sold requires confirmation

```
Given I am changing a property's status to "Sold"
When I select "Sold"
Then a confirmation dialog should appear
  And I should be asked to confirm this is a closed sale
  And optionally enter the sale price
```

### Scenario 8: Withdrawn status is distinct

```
Given a property is marked as Withdrawn
When I view it in the list
Then it should be visually distinct from active properties
  And it should be clear it's no longer on the market
```

## Manual Testing Steps

### Test 1: Set status when creating

1. Create a new property
2. Select "Active" from the status dropdown
3. Save the property
4. Verify the status is saved
5. Open the property details
6. Verify the status is "Active"

### Test 2: Change status from details

1. Open a property's details
2. Current status is "Active"
3. Click on the status field
4. Select "Pending"
5. Save the change
6. Verify the status updated
7. Verify the visual indicator changed

### Test 3: Change status from list

1. View the property list
2. Right-click on a property
3. Select "Change Status"
4. Choose "Withdrawn"
5. Verify the status changed
6. Verify it reflected in the list immediately

### Test 4: Test color coding

1. Create properties with all four statuses
2. View the property list
3. Verify Active is green
4. Verify Pending is yellow
5. Verify Sold is gray
6. Verify Withdrawn is red
7. Verify colors are clearly distinguishable

### Test 5: Test status persistence

1. Change a property's status to "Pending"
2. Close the application
3. Restart the application
4. Open the property
5. Verify the status is still "Pending"

### Test 6: Test Sold confirmation

1. Open a property
2. Change status to "Sold"
3. Verify a confirmation dialog appears
4. Enter the sale price (if prompted)
5. Confirm
6. Verify the property is now marked as Sold

### Test 7: Test Withdrawn distinction

1. Mark a property as Withdrawn
2. View the property list
3. Verify it's visually distinct (maybe with strikethrough or different color)
4. Verify it's clear it's no longer active

### Test 8: Test on all platforms

1. Test status changes on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Status can be set when creating a property
- [ ] Status can be changed from property details
- [ ] Status can be changed from property list
- [ ] Status is color-coded (Active=green, Pending=yellow, Sold=gray, Withdrawn=red)
- [ ] Status changes are saved immediately
- [ ] Status persists across restarts
- [ ] Visual indicators are clear and consistent
- [ ] Marking as Sold requires confirmation
- [ ] Withdrawn properties are visually distinct
- [ ] All four statuses are available
- [ ] Works on Windows, macOS, and Linux
- [ ] Status is clearly visible in list and details
- [ ] No accidental status changes