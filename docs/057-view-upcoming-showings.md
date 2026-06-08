# US-057: View Upcoming Showings

## User Story

**As an** agent  
**I want to** view all my upcoming showings  
**So that** I can see what's on my schedule and prepare accordingly

## Priority

**MVP:** Must Have

**Rationale:** Agents need to see their upcoming showings at a glance to prepare for the day, know which properties to visit, and which buyers to meet. This is essential for daily operations and time management.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design upcoming showings view
- 1 hour: Create list/calendar view of upcoming showings
- 1 hour: Display showing details (contact, property, time, notes)
- 1 hour: Sort by date/time
- 1 hour: Group by day
- 1 hour: Add filtering options
- 1 hour: Test with various data
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-056 (Schedule a Showing)

**Blocks:** US-058 (Mark Showing as Completed), US-059 (Add Showing Notes)

## Description

Users should be able to view all their upcoming showings in a clear, organized view. This can be a list view sorted by date/time, or a calendar view. The view should show key information for each showing: date, time, contact name, property address, and any notes.

Upcoming showings should be sorted chronologically (soonest first) and can be grouped by day for easy scanning. The view should help agents prepare for their day and week.

## BDD Scenarios

### Scenario 1: View upcoming showings list

```
Given I have scheduled several showings
  And some are in the past, some are upcoming
When I view the upcoming showings section
Then I should see only future showings
  And they should be sorted by date/time (soonest first)
  And each showing should show:
    - Date and time
    - Contact name
    - Property address
    - Duration
    - Notes
```

### Scenario 2: Group showings by day

```
Given I have multiple showings on different days
When I view the upcoming showings
Then they should be grouped by day
  And each day should be a section with a date header
  And showings within that day should be listed in time order
```

### Scenario 3: Showings for today are highlighted

```
Given I have showings scheduled for today
When I view the upcoming showings
Then today's showings should be highlighted or at the top
  And they should be easy to identify
```

### Scenario 4: View showing details

```
Given I am viewing upcoming showings
When I click on a showing
Then the showing details should open
  And I can see full information
  And I can take actions (edit, complete, add notes)
```

### Scenario 5: Empty state for no upcoming showings

```
Given I have no upcoming showings
When I view the upcoming showings section
Then I should see an empty state message
  And it should be encouraging
  Like "No showings scheduled - time to prospect!"
```

### Scenario 6: Filter by date range

```
Given I have showings over several weeks
When I filter by "This Week"
Then only this week's showings should be shown
  And the filter should be clearly indicated
```

### Scenario 7: Showings are sorted chronologically

```
Given I have showings at various times
When I view the list
Then they should be in chronological order
  And the soonest showing should be at the top
```

### Scenario 8: Quick actions on showings

```
Given I am viewing upcoming showings
When I hover over or right-click a showing
Then I should see quick actions:
  - Mark as completed
  - Edit
  - Cancel
  - Add notes
```

## Manual Testing Steps

### Test 1: View upcoming showings

1. Schedule several showings (some past, some future)
2. Navigate to the Calendar or Showings section
3. Verify only future showings are shown
4. Verify they're sorted by date/time
5. Verify all information is displayed

### Test 2: Test day grouping

1. Schedule showings on different days
2. View the upcoming showings
3. Verify they're grouped by day
4. Verify each day has a date header
5. Verify showings within a day are in time order

### Test 3: Test today's highlight

1. Schedule a showing for today
2. View the upcoming showings
3. Verify today's showings are highlighted
4. Verify they're at the top
5. Verify they're easy to identify

### Test 4: Test showing details

1. View upcoming showings
2. Click on a showing
3. Verify the details open
4. Verify all information is shown
5. Test the action buttons

### Test 5: Test empty state

1. Delete or complete all upcoming showings
2. View the upcoming showings
3. Verify the empty state message
4. Verify it's encouraging

### Test 6: Test date filtering

1. Schedule showings over several weeks
2. Filter by "This Week"
3. Verify only this week's showings are shown
4. Test other date ranges

### Test 7: Test quick actions

1. View upcoming showings
2. Right-click on a showing
3. Verify quick actions are available
4. Test each action
5. Verify they work correctly

### Test 8: Test on all platforms

1. Test upcoming showings on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Upcoming showings view is accessible
- [ ] Only future showings are shown
- [ ] Showings are sorted chronologically (soonest first)
- [ ] Showings are grouped by day
- [ ] Today's showings are highlighted
- [ ] Each showing shows date, time, contact, property, notes
- [ ] Clicking a showing opens its details
- [ ] Empty state is encouraging
- [ ] Date range filtering works
- [ ] Quick actions are available
- [ ] Works on Windows, macOS, and Linux
- [ ] Performance is good even with many showings
- [ ] View is intuitive and easy to scan