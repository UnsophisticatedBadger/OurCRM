# US-035: Move Lead Through Pipeline

## User Story

**As an** agent  
**I want to** move a lead through the sales pipeline stages  
**So that** I can track their progress and know what stage they're at

## Priority

**MVP:** Must Have

**Rationale:** The sales pipeline is a core concept in real estate. Leads progress through stages from initial contact to closing. Tracking pipeline stages helps agents understand where leads are stuck and forecast their business.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design pipeline stages
- 1 hour: Design pipeline view (kanban or list)
- 2 hours: Implement stage transitions
- 1 hour: Add drag-and-drop (optional)
- 1 hour: Add stage change buttons
- 1 hour: Display current stage clearly
- 1 hour: Track stage history
- 1 hour: Test stage transitions
- 1 hour: Test pipeline view
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-030 (Create a New Lead), US-031 (View Lead List)

**Blocks:** US-036 (View Pipeline), US-037 (Mark Lead as Converted)

## Description

Users should be able to move leads through defined pipeline stages. The typical real estate pipeline includes: New Lead, Contacted, Qualified, Showing Scheduled, Offer Made, Under Contract, Closed, or Lost. Users can move leads forward, backward, or mark them as lost.

The pipeline should be visualized in a way that makes it easy to see where each lead is. This could be a kanban board view (columns for each stage) or a list view with stage indicators. Stage changes should be quick and easy.

## BDD Scenarios

### Scenario 1: View pipeline stages

```
Given I am in the Leads section
When I switch to pipeline view
Then I should see all pipeline stages as columns or sections:
  - New Lead
  - Contacted
  - Qualified
  - Showing Scheduled
  - Offer Made
  - Under Contract
  - Closed
  - Lost
```

### Scenario 2: Move lead to next stage

```
Given I am viewing a lead in the "New Lead" stage
When I click "Move to Next Stage" or drag it to the next column
Then the lead should be moved to "Contacted"
  And the change should be reflected immediately
  And the timestamp should be updated
```

### Scenario 3: Move lead to specific stage

```
Given I am viewing a lead
When I click on the stage field
  And I select a specific stage from a dropdown
Then the lead should be moved to that stage
```

### Scenario 4: Mark lead as lost

```
Given I am viewing a lead
When I click "Mark as Lost"
  And I select a reason (optional)
Then the lead should be moved to the "Lost" stage
  And it should be visually distinct from active leads
```

### Scenario 5: Move lead backward

```
Given a lead is in the "Qualified" stage
When I move it back to "Contacted"
Then the lead should be moved backward in the pipeline
  And the change should be saved
```

### Scenario 6: Pipeline view shows all leads

```
Given I have leads in various stages
When I view the pipeline
Then each stage should show the leads in that stage
  And I should be able to see the count per stage
```

### Scenario 7: Stage change is logged

```
Given I have moved a lead through several stages
When I view the lead's activity history (if implemented)
Then I should see when it was moved between stages
  And what stages it was in
```

### Scenario 8: Cannot skip stages (optional)

```
Given a lead is in "New Lead" stage
When I try to move it directly to "Closed"
Then the system should warn that this is a large jump
  And ask for confirmation
```

## Manual Testing Steps

### Test 1: View pipeline stages

1. Navigate to the Leads section
2. Switch to pipeline view
3. Verify all expected stages are shown
4. Verify each stage is clearly labeled
5. Verify leads are organized by stage

### Test 2: Move lead to next stage

1. Open a lead in "New Lead"
2. Click "Move to Next Stage"
3. Verify it moves to "Contacted"
4. Check the pipeline view
5. Verify the lead appears in the new stage

### Test 3: Move to specific stage

1. Open a lead
2. Click on the stage field
3. Select "Showing Scheduled" from the dropdown
4. Save the change
5. Verify the lead is now in that stage

### Test 4: Mark as lost

1. Open a lead
2. Click "Mark as Lost"
3. Select a reason (if prompted)
4. Confirm
5. Verify the lead is in the "Lost" stage
6. Verify it's visually distinct

### Test 5: Move backward

1. Open a lead in "Qualified" stage
2. Move it back to "Contacted"
3. Verify the change
4. Verify it can be moved forward again

### Test 6: Test drag-and-drop (if implemented)

1. View the pipeline
2. Drag a lead from one column to another
3. Verify it moves to the new stage
4. Verify the change is saved

### Test 7: Test pipeline view

1. Create leads in various stages
2. View the pipeline
3. Verify each stage shows the correct leads
4. Verify counts are accurate
5. Test with many leads in each stage

### Test 8: Test stage persistence

1. Move a lead to a new stage
2. Close the application
3. Restart the application
4. View the lead
5. Verify the stage change persisted

### Test 9: Test on all platforms

1. Test pipeline on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Pipeline view shows all defined stages
- [ ] Leads can be moved to next stage
- [ ] Leads can be moved to any specific stage
- [ ] Leads can be marked as lost
- [ ] Leads can be moved backward
- [ ] Pipeline view shows leads organized by stage
- [ ] Stage changes are saved immediately
- [ ] Stage changes persist across restarts
- [ ] Current stage is clearly displayed
- [ ] Stage history is tracked (optional)
- [ ] Works on Windows, macOS, and Linux
- [ ] Pipeline is intuitive and easy to use
- [ ] Stage transitions are quick and easy