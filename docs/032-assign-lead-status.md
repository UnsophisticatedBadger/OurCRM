# US-032: Assign Lead Status

## User Story

**As an** agent  
**I want to** assign a status (Hot, Warm, or Cold) to a lead  
**So that** I can prioritize my follow-ups and know which leads are most likely to convert

## Priority

**MVP:** Must Have

**Rationale:** Lead status is the primary way agents prioritize their work. Hot leads need immediate attention, warm leads need regular follow-up, and cold leads are long-term prospects. Without status, all leads look the same and agents waste time on unqualified prospects.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design status selection UI
- 1 hour: Implement status change in lead details
- 1 hour: Add visual indicators for current status
- 1 hour: Implement quick status change from list
- 1 hour: Add status change history (optional)
- 1 hour: Test status changes
- 1 hour: Test that status updates reflect in list
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-030 (Create a New Lead), US-031 (View Lead List)

**Blocks:** US-035 (Move Lead Through Pipeline), US-036 (View Pipeline)

## Description

Users should be able to assign and change a lead's status (Hot, Warm, or Cold) at any time. The status should be clearly visible in the lead list and details, and should be color-coded for quick identification. Changing a status should be quick and easy, with the option to change it from either the lead details or directly from the lead list.

Each status represents:
- **Hot:** Ready to buy/sell soon, high engagement, pre-approved
- **Warm:** Interested but not ready, needs nurturing
- **Cold:** Long-term prospect, just browsing or early stage

## BDD Scenarios

### Scenario 1: Set status when creating lead

```
Given I am creating a new lead
When I select a status from the status dropdown
  And I save the lead
Then the lead should be saved with the selected status
```

### Scenario 2: Change status from lead details

```
Given I am viewing a lead's details
  And the current status is "Warm"
When I click on the status field
  And I select "Hot"
  And I save the change
Then the lead's status should be updated to "Hot"
  And the visual indicator should change
```

### Scenario 3: Change status from lead list

```
Given I am viewing the lead list
  And I have selected a lead
When I right-click and select "Change Status"
  Or I use a quick action button
Then I should be able to change the status
  And the change should be reflected immediately in the list
```

### Scenario 4: Status is color-coded

```
Given I am viewing a lead with status "Hot"
When I look at the status indicator
Then it should be shown in red
  And it should be clearly visible
```

### Scenario 5: Status persists across restarts

```
Given I have changed a lead's status
When I close the application
  And I restart the application
  And I open the lead
Then the status should be the updated value
```

### Scenario 6: Status change is logged

```
Given I have changed a lead's status multiple times
When I view the lead's activity history (if implemented)
Then I should see when the status was changed
  And what it was changed from and to
```

### Scenario 7: Bulk status change (optional)

```
Given I have selected multiple leads in the list
When I choose "Change Status" from the bulk actions menu
Then I can change the status for all selected leads at once
```

## Manual Testing Steps

### Test 1: Set status when creating

1. Create a new lead
2. Select "Hot" from the status dropdown
3. Save the lead
4. Verify the status is saved
5. Open the lead details
6. Verify the status is "Hot"

### Test 2: Change status from details

1. Open a lead's details
2. Current status is "Warm"
3. Click on the status field
4. Select "Hot"
5. Save the change
6. Verify the status updated
7. Verify the visual indicator changed

### Test 3: Change status from list

1. View the lead list
2. Right-click on a lead
3. Select "Change Status"
4. Choose "Cold"
5. Verify the status changed
6. Verify it reflected in the list immediately

### Test 4: Test color coding

1. Create leads with Hot, Warm, and Cold statuses
2. View the lead list
3. Verify Hot is red
4. Verify Warm is orange
5. Verify Cold is blue
6. Verify colors are clearly distinguishable

### Test 5: Test status persistence

1. Change a lead's status to "Hot"
2. Close the application
3. Restart the application
4. Open the lead
5. Verify the status is still "Hot"

### Test 6: Test quick status change

1. View the lead list
2. Select a lead
3. Use a keyboard shortcut or button to change status
4. Verify the change is quick and easy
5. Verify it saves automatically

### Test 7: Test on all platforms

1. Test status changes on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Status can be set when creating a lead
- [ ] Status can be changed from lead details
- [ ] Status can be changed from lead list
- [ ] Status is color-coded (Hot=red, Warm=orange, Cold=blue)
- [ ] Status changes are saved immediately
- [ ] Status persists across restarts
- [ ] Visual indicators are clear and consistent
- [ ] Status change is quick and easy
- [ ] All three statuses are available
- [ ] Works on Windows, macOS, and Linux
- [ ] Status is clearly visible in list and details
- [ ] No accidental status changes