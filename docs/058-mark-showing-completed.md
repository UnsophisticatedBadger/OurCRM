# US-058: Mark Showing as Completed

## User Story

**As an** agent  
**I want to** mark a showing as completed and record the outcome  
**So that** I can track which showings led to interest and which didn't

## Priority

**MVP:** Must Have

**Rationale:** Tracking showing outcomes is critical for understanding buyer interest and making informed decisions. Did the buyer like the property? Are they interested in making an offer? This information helps agents prioritize follow-ups and refine their approach.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design completion UI
- 1 hour: Implement outcome selection (Interested/Not Interested/Maybe/Want to Make Offer)
- 1 hour: Add notes field for showing feedback
- 1 hour: Update showing status
- 1 hour: Add follow-up reminder option
- 1 hour: Test completion flow
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-056 (Schedule a Showing), US-057 (View Upcoming Showings)

**Blocks:** US-059 (Add Showing Notes), US-060 (Schedule Follow-up After Showing)

## Description

Users should be able to mark a showing as completed and record the outcome. The outcome can be: Very Interested, Interested, Neutral, Not Interested, or Want to Make Offer. Optional notes can capture specific feedback from the showing (what the buyer liked, concerns, questions, etc.).

When a showing is marked as completed:
- The showing moves from upcoming to past
- The outcome is saved
- Notes are associated with the showing
- Optionally, a follow-up reminder can be scheduled
- The buyer's lead status may be updated based on outcome

## BDD Scenarios

### Scenario 1: Mark showing as completed

```
Given I have a showing in the past or present
When I click "Mark as Completed"
Then a completion dialog should appear
  And I can select the outcome
  And I can add notes about the showing
```

### Scenario 2: Select showing outcome

```
Given the completion dialog is open
When I select an outcome (e.g., "Very Interested", "Not Interested")
  And I add notes
  And I click "Save"
Then the showing should be marked as completed
  And the outcome should be saved
  And the notes should be associated
```

### Scenario 3: Showing moves to past

```
Given I have completed a showing
When I view the upcoming showings
Then the completed showing should no longer be there
  And it should appear in past showings
```

### Scenario 4: Outcome updates lead status (optional)

```
Given I mark a showing as "Very Interested"
When I save the completion
Then the contact's lead status should update to "Hot"
  Or I should be prompted to update it
```

### Scenario 5: Schedule follow-up

```
Given I have completed a showing
When I mark it as completed
Then I should have the option to schedule a follow-up
  And I can choose when to follow up
  And the follow-up is added to my tasks
```

### Scenario 6: View completed showings

```
Given I have completed several showings
When I view past showings
Then I should see all completed showings
  And their outcomes
  And their notes
```

### Scenario 7: Cannot complete future showings

```
Given I have a showing scheduled for the future
When I try to mark it as completed
Then the system should prevent it
  And explain that the showing hasn't happened yet
```

### Scenario 8: Edit completed showing

```
Given I have marked a showing as completed
When I need to update the outcome or notes
Then I should be able to edit the completion details
  And the changes should be saved
```

## Manual Testing Steps

### Test 1: Mark showing as completed

1. Have a showing that is past or present
2. Click "Mark as Completed"
3. Verify the completion dialog appears
4. Select an outcome
5. Add notes
6. Click "Save"
7. Verify the success message

### Test 2: Test outcome selection

1. Mark a showing as completed
2. Test each outcome option
3. Verify they're all available
4. Add notes for each
5. Save and verify

### Test 3: Test showing moves to past

1. Mark a showing as completed
2. View upcoming showings
3. Verify the completed showing is no longer there
4. View past showings
5. Verify it appears with its outcome

### Test 4: Test lead status update

1. Mark a showing as "Very Interested"
2. Verify the lead status updates (if implemented)
3. Test with other outcomes
4. Verify the behavior

### Test 5: Test follow-up scheduling

1. Mark a showing as completed
2. Choose to schedule a follow-up
3. Select a date for the follow-up
4. Verify the follow-up is added to tasks

### Test 6: Test past showings view

1. Complete several showings
2. View past showings
3. Verify all are shown
4. Verify outcomes and notes are visible
5. Test sorting and filtering

### Test 7: Test cannot complete future showing

1. Try to mark a future showing as completed
2. Verify the system prevents it
3. Verify the explanation is clear

### Test 8: Test edit completed showing

1. Mark a showing as completed
2. Edit the outcome or notes
3. Save the changes
4. Verify the updates are saved

### Test 9: Test on all platforms

1. Test completion on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] "Mark as Completed" action is available for past/present showings
- [ ] Completion dialog appears with outcome options
- [ ] Outcome can be selected from predefined options
- [ ] Notes can be added about the showing
- [ ] Showing moves from upcoming to past when completed
- [ ] Completed showings are saved with outcome and notes
- [ ] Cannot complete future showings
- [ ] Completed showings can be viewed later
- [ ] Completed showing details can be edited
- [ ] Follow-up can be scheduled from completion
- [ ] Lead status may update based on outcome
- [ ] Works on Windows, macOS, and Linux
- [ ] Completion tracking is accurate and useful