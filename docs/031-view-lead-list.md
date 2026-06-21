# US-031: View Lead List

## User Story

**As an** agent  
**I want to** view a list of all my leads  
**So that** I can see my sales pipeline at a glance

## Priority

**MVP:** Must Have

**Rationale:** Leads are the primary focus of an agent's daily work. They need to see all their leads, their status, and key information at a glance to know who to follow up with and prioritize their time.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design list layout and columns
- 2 hours: Create list UI with lead-specific columns
- 1 hour: Implement data loading
- 1 hour: Add sorting by columns
- 1 hour: Add status indicators (color-coded)
- 1 hour: Implement empty state
- 1 hour: Add filtering by status
- 1 hour: Test with various data volumes
- 1 hour: Test performance
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-030 (Create a New Lead)

**Blocks:** US-032 (Assign Lead Status), US-035 (Move Lead Through Pipeline), US-036 (View Pipeline)

## Description

The Leads section should display a list of all leads in a table view. Each row represents one lead and shows key information including name, status, source, budget range, and timeline. The status should be color-coded for quick visual identification (hot=red, warm=orange, cold=blue).

The list should support sorting by columns, filtering by status, and should load quickly even with hundreds of leads. When there are no leads, an empty state should be displayed with a helpful message.

## BDD Scenarios

### Scenario 1: View lead list with leads

```
Given I have created several leads
  And I am in the Leads section
When the Leads section loads
Then I should see a list of all my leads
  And each lead should display:
    - Name
    - Status (color-coded)
    - Source
    - Budget range
    - Timeline
  And the leads should be sorted by status (Hot first) by default
```

### Scenario 2: Status is color-coded

```
Given I am viewing the lead list
  And I have leads with different statuses
When I look at the status column
Then Hot leads should be shown in red
  And Warm leads should be shown in orange
  And Cold leads should be shown in blue
  And the colors should be clearly distinguishable
```

### Scenario 3: Empty state with no leads

```
Given I have no leads
  And I am in the Leads section
When the Leads section loads
Then I should see an empty state message
  And the message should say "No leads yet"
  And there should be a button "Create Your First Lead"
```

### Scenario 4: Sort by status

```
Given I am viewing the lead list
  And I have leads with different statuses
When I click on the "Status" column header
Then the leads should be sorted by status (Hot, Warm, Cold)
  And the column header should show a sort indicator
```

### Scenario 5: Filter by status

```
Given I am viewing the lead list
When I click on a status filter (e.g., "Hot Only")
Then only leads with that status should be displayed
  And the filter should be clearly indicated
```

### Scenario 6: Sort by budget

```
Given I am viewing the lead list
When I click on the "Budget" column header
Then the leads should be sorted by budget
  And high-budget leads should appear first (or last, depending on user preference)
```

### Scenario 7: Lead list state is preserved when switching sections

```
Given I am viewing the lead list
  And I have filtered by "Hot" status
When I navigate to the Contacts section
  And I navigate back to Leads
Then only Hot leads should still be displayed
  And the status filter should still be active
```

### Scenario 8: List loads quickly

```
Given I have 200 leads
When I open the Leads section
Then the list should load in under 2 seconds
  And scrolling should be smooth
```

## Manual Testing Steps

### Test 1: View list with leads

1. Create 5-10 leads with various data
2. Navigate to the Leads section
3. Verify all leads are displayed
4. Verify the columns show the expected information
5. Verify the data is accurate
6. Check the visual layout is clean and readable

### Test 2: Test status colors

1. Create leads with Hot, Warm, and Cold statuses
2. Navigate to the Leads section
3. Verify Hot leads are shown in red
4. Verify Warm leads are shown in orange
5. Verify Cold leads are shown in blue
6. Verify the colors are clearly distinguishable

### Test 3: Test empty state

1. Delete all leads (or start with a fresh database)
2. Navigate to the Leads section
3. Verify the empty state message appears
4. Verify the "Create Your First Lead" button is visible
5. Click the button
6. Verify it opens the new lead form

### Test 4: Test sorting

1. Create leads with various names, statuses, and budgets
2. Click on each column header
3. Verify sorting works for each column
4. Click again to reverse order
5. Verify the sort indicator updates

### Test 5: Test status filtering

1. Create leads with different statuses
2. Filter by "Hot Only"
3. Verify only Hot leads are shown
4. Clear the filter
5. Verify all leads are shown again

### Test 6: Test with large dataset

1. Create 200+ leads
2. Open the Leads section
3. Measure load time
4. Verify it's under 2 seconds
5. Test scrolling performance
6. Verify UI remains responsive

### Test 7: Test state preservation when switching sections

1. Navigate to the Leads section
2. Apply the "Hot" status filter
3. Navigate to the Contacts section
4. Navigate back to Leads
5. Verify the "Hot" filter is still active
6. Verify only Hot leads are shown

### Test 8: Test on all platforms

1. Test lead list on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Lead list displays all leads
- [ ] Each lead shows name, status, source, budget, timeline
- [ ] Status is color-coded (Hot=red, Warm=orange, Cold=blue)
- [ ] Leads are sorted by status by default
- [ ] Users can sort by clicking column headers
- [ ] Users can filter by status
- [ ] Empty state is shown when no leads exist
- [ ] List loads in under 2 seconds with 200 leads
- [ ] Scrolling is smooth with large lists
- [ ] UI remains responsive
- [ ] Section state (scroll position, sort column and direction, active status filter) is preserved when navigating away and back
- [ ] Works on Windows, macOS, and Linux
- [ ] Visual design is clean and professional
- [ ] Status colors are consistent and readable