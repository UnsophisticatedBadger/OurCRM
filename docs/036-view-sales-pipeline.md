# US-036: View Sales Pipeline

## User Story

**As an** agent  
**I want to** view my sales pipeline visually  
**So that** I can see where all my leads are and understand my business at a glance

## Priority

**MVP:** Must Have

**Rationale:** A visual pipeline view helps agents understand their business at a glance. Instead of looking at a list, they can see which stages have many leads (potential bottlenecks) and which are empty (need more leads). This is a critical business intelligence feature.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Choose pipeline visualization (kanban vs list)
- 2 hours: Design pipeline layout
- 2 hours: Implement kanban board view
- 1 hour: Add stage counts
- 1 hour: Add lead cards with key info
- 1 hour: Implement drag-and-drop between stages
- 1 hour: Add filtering and search within pipeline
- 1 hour: Test pipeline visualization
- 1 hour: Test performance with many leads
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-031 (View Lead List), US-035 (Move Lead Through Pipeline)

**Blocks:** None

## Description

The pipeline view provides a visual representation of all leads organized by their current stage in the sales process. This can be implemented as a kanban board (columns for each stage with lead cards) or a list view with stage indicators. The visualization should make it easy to see the overall health of the sales pipeline.

The pipeline view should show:
- Each stage as a column or section
- All leads in each stage
- Count of leads per stage
- Key information for each lead (name, budget, days in stage)
- Ability to move leads between stages (drag-and-drop or buttons)

## BDD Scenarios

### Scenario 1: Switch to pipeline view

```
Given I am in the Leads section
  And I am viewing the list view
When I click on "Pipeline View" or a similar toggle
Then the view should change to the pipeline visualization
  And I should see all stages as columns or sections
```

### Scenario 2: View leads in each stage

```
Given I have leads in various stages
When I view the pipeline
Then each stage should display the leads in that stage
  And each lead should show:
    - Name
    - Budget range
    - Status (Hot/Warm/Cold)
    - Days in current stage
```

### Scenario 3: Stage counts are displayed

```
Given I have leads in various stages
When I view the pipeline
Then each stage should show the count of leads
  And the count should be clearly visible
```

### Scenario 4: Drag lead between stages

```
Given I am viewing the pipeline
When I drag a lead card from "Contacted" to "Qualified"
Then the lead should be moved to the "Qualified" stage
  And the change should be saved
  And the counts should update
```

### Scenario 5: Click lead to view details

```
Given I am viewing the pipeline
When I click on a lead card
Then the lead details should open
  And I can view full information
```

### Scenario 6: Pipeline shows empty stages

```
Given I have no leads in "Under Contract" stage
When I view the pipeline
Then the "Under Contract" column should be shown
  And it should indicate "No leads in this stage"
```

### Scenario 7: Filter pipeline by status

```
Given I am viewing the pipeline
When I filter to show only "Hot" leads
Then only Hot leads should be shown in their respective stages
  And Cold and Warm leads should be hidden
```

### Scenario 8: Pipeline performance

```
Given I have 200 leads across various stages
When I view the pipeline
Then it should load in under 3 seconds
  And drag-and-drop should be smooth
  And the UI should remain responsive
```

## Manual Testing Steps

### Test 1: Switch to pipeline view

1. Navigate to the Leads section
2. Click on "Pipeline View" toggle
3. Verify the view changes to kanban board
4. Verify all stages are shown as columns
5. Verify the layout is clear and organized

### Test 2: View leads in stages

1. Create leads in various stages
2. Switch to pipeline view
3. Verify leads are organized by stage
4. Verify each lead card shows the expected information
5. Check that the information is readable

### Test 3: Test stage counts

1. Create 3 leads in "New Lead"
2. Create 2 leads in "Contacted"
3. Create 1 lead in "Qualified"
4. View the pipeline
5. Verify counts are correct
6. Verify counts are clearly visible

### Test 4: Test drag-and-drop

1. View the pipeline
2. Drag a lead from one column to another
3. Verify it moves to the new stage
4. Verify the change is saved
5. Close and reopen the pipeline
6. Verify the change persisted

### Test 5: Test lead details from pipeline

1. View the pipeline
2. Click on a lead card
3. Verify the lead details open
4. Close the details
5. Verify you return to the pipeline

### Test 6: Test empty stages

1. View the pipeline
2. Find a stage with no leads
3. Verify it shows a message like "No leads in this stage"
4. Verify the stage is still visible

### Test 7: Test filtering

1. View the pipeline
2. Filter to show only Hot leads
3. Verify only Hot leads are shown
4. Clear the filter
5. Verify all leads are shown again

### Test 8: Test performance

1. Create 200 leads across various stages
2. Open the pipeline view
3. Measure load time
4. Verify it's under 3 seconds
5. Test drag-and-drop performance
6. Verify it's smooth

### Test 9: Test on all platforms

1. Test pipeline on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Pipeline view is accessible from Leads section
- [ ] All pipeline stages are shown as columns
- [ ] Leads are organized by their current stage
- [ ] Each lead card shows key information
- [ ] Stage counts are displayed
- [ ] Leads can be moved between stages via drag-and-drop
- [ ] Clicking a lead opens its details
- [ ] Empty stages are handled gracefully
- [ ] Pipeline can be filtered by status
- [ ] Pipeline loads quickly with many leads
- [ ] Drag-and-drop is smooth
- [ ] Works on Windows, macOS, and Linux
- [ ] Visual design is intuitive and professional