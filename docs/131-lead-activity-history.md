# US-131: Lead Activity History

## User Story

**As an** agent  
**I want to** view the complete activity history for a lead  
**So that** I can see all interactions and changes over time

## Priority

**MVP:** Should Have

**Rationale:** Lead activity history provides a complete audit trail of everything that happened with a lead: status changes, notes added, emails sent, showings scheduled, etc. This is essential for understanding the lead's journey and for handoffs between team members.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design activity history UI
- 2 hours: Implement activity tracking for lead events
- 1 hour: Display activity timeline
- 1 hour: Add activity filtering
- 1 hour: Test activity history
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-030 (Create a New Lead), US-031 (View Lead List)

**Blocks:** None

## Description

Every significant action on a lead should be logged in the activity history:
- Lead created
- Status changed (with old/new values)
- Notes added
- Emails sent
- Showings scheduled
- Budget changed
- Source changed
- Converted to client
- Marked as lost

The activity timeline should be chronological (newest first or oldest first) and should show who performed the action (for multi-user systems) and when.

## BDD Scenarios

### Scenario 1: View lead activity history

Given I am viewing a lead's details When I click on "Activity History" or similar tab Then I should see a chronological list of all activities Including: - Lead created - Status changes - Notes added - Emails sent - Showings scheduled - Other significant events


### Scenario 2: Activity shows timestamp

Given I am viewing the activity history When I look at each activity Then I should see when it occurred And it should be in a readable format


### Scenario 3: Activity shows user (if multi-user)

Given I am viewing the activity history And this is a multi-user system When I look at each activity Then I should see who performed the action Or "Me" for single-user systems


### Scenario 4: Status change shows old and new values

Given a lead's status was changed from Warm to Hot When I view the activity history Then I should see: "Status changed from Warm to Hot" With timestamp


### Scenario 5: Activity is chronological

Given I am viewing the activity history When I look at the activities Then they should be in chronological order And I can sort by newest or oldest first


### Scenario 6: Filter activity by type

Given a lead has many activities When I filter by "Status Changes" Then only status change activities should be shown And I can filter by other types too


### Scenario 7: Activity is automatically logged

Given I change a lead's status When I save the change Then the activity should be automatically logged And I don't need to manually create it


### Scenario 8: Activity cannot be deleted

Given there is an activity in the history When I try to delete it Then I should not be able to And it should be permanent for audit purposes


## Manual Testing Steps

### Test 1: View activity history

1. Create a lead
2. Make several changes (status, notes, etc.)
3. Send an email
4. Schedule a showing
5. View the lead's details
6. Click on Activity History
7. Verify all activities are shown

### Test 2: Test timestamps

1. View activity history
2. Verify each activity has a timestamp
3. Verify the format is readable
4. Verify times are accurate

### Test 3: Test status change details

1. Change lead status multiple times
2. View activity history
3. Verify each change shows old and new values
4. Verify timestamps are correct

### Test 4: Test chronological order

1. Create many activities
2. View activity history
3. Verify order is correct
4. Test sorting options

### Test 5: Test filtering

1. Have various activity types
2. Filter by "Status Changes"
3. Verify only status changes shown
4. Filter by "Notes"
5. Verify only notes shown

### Test 6: Test automatic logging

1. Make a change to a lead
2. View activity history
3. Verify it was logged automatically
4. Verify no manual entry needed

### Test 7: Test activity permanence

1. View activity history
2. Try to delete an activity
3. Verify it's not possible
4. Verify this is intentional for audit

### Test 8: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Activity history is viewable for each lead
- [ ] All significant actions are logged automatically
- [ ] Timestamps are shown for each activity
- [ ] User is shown (for multi-user systems)
- [ ] Status changes show old and new values
- [ ] Activities are in chronological order
- [ ] Can sort by newest or oldest first
- [ ] Can filter by activity type
- [ ] Activities cannot be deleted (audit trail)
- [ ] Activity history is read-only
- [ ] Works on Windows, macOS, and Linux
- [ ] UI is clear and easy to read