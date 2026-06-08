# US-037: Mark Lead as Converted

## User Story

**As an** agent  
**I want to** mark a lead as converted to a client  
**So that** I can track successful conversions and move them to active client status

## Priority

**MVP:** Must Have

**Rationale:** Converting a lead to a client is the ultimate goal of the sales process. Agents need to track conversion rates, celebrate wins, and transition leads into ongoing client relationships. This is a key milestone in the lead lifecycle.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design conversion UI
- 1 hour: Implement "Mark as Converted" action
- 1 hour: Add conversion date tracking
- 1 hour: Move lead to "Closed" or "Converted" stage
- 1 hour: Create or link to client record
- 1 hour: Add conversion success message
- 1 hour: Test conversion flow
- 1 hour: Test that converted leads are tracked
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-035 (Move Lead Through Pipeline)

**Blocks:** US-038 (View Converted Leads), US-039 (Track Conversion Rate)

## Description

Users should be able to mark a lead as converted when they become an active client (closed a deal or started working together). The conversion should be a significant event that's tracked with a timestamp. Converted leads should be moved to a special stage (Closed-Converted or similar) and should be distinguishable from lost leads.

The system should track:
- When the lead was converted
- What they converted to (buyer client, seller client, etc.)
- The conversion value (sale price, commission, etc.) - optional
- A conversion celebration or acknowledgment

## BDD Scenarios

### Scenario 1: Mark lead as converted

```
Given I am viewing a lead that has become a client
When I click "Mark as Converted"
Then a conversion dialog should appear
  And I can confirm the conversion
  And optionally enter conversion details (sale price, type, etc.)
```

### Scenario 2: Lead moves to converted stage

```
Given I have confirmed a lead conversion
When the conversion is saved
Then the lead should be moved to the "Closed-Converted" stage
  And it should be visually distinct from active leads
  And a conversion timestamp should be recorded
```

### Scenario 3: Conversion date is tracked

```
Given I converted a lead on a specific date
When I view the lead's history (if implemented)
Then I should see the conversion date
  And how long the conversion process took
```

### Scenario 4: Converted lead celebration

```
Given I have just converted a lead
When the conversion is saved
Then I should see a success message
  And the message should celebrate the conversion
  And it should be encouraging
```

### Scenario 5: Cannot accidentally unconvert

```
Given a lead has been marked as converted
When I try to change its status
Then the system should warn that this is a converted lead
  And ask for confirmation
```

### Scenario 6: View converted leads

```
Given I have converted several leads
When I filter or search for converted leads
Then I should be able to see all converted leads
  And their conversion dates
```

### Scenario 7: Conversion details can be edited

```
Given I have converted a lead
When I need to update the conversion details
Then I should be able to edit the conversion information
  And the changes should be saved
```

## Manual Testing Steps

### Test 1: Mark lead as converted

1. Create a lead
2. Move it through the pipeline to a late stage
3. Click "Mark as Converted"
4. Verify the conversion dialog appears
5. Enter conversion details (optional)
6. Confirm the conversion
7. Verify the lead moves to the converted stage

### Test 2: Test conversion stage

1. Convert a lead
2. View the pipeline
3. Verify the lead is in the "Closed-Converted" stage
4. Verify it's visually distinct (maybe with a checkmark or special color)
5. Verify the conversion date is displayed

### Test 3: Test conversion date tracking

1. Convert a lead
2. Note the conversion date
3. View the lead's history
4. Verify the conversion date is recorded
5. Verify it's accurate

### Test 4: Test conversion celebration

1. Convert a lead
2. Verify the success message appears
3. Verify it's encouraging and celebratory
4. Check that it doesn't feel spammy or annoying

### Test 5: Test accidental unconvert protection

1. Convert a lead
2. Try to change its status
3. Verify a warning appears
4. Confirm the warning is clear
5. Test canceling the status change

### Test 6: Test viewing converted leads

1. Convert several leads
2. Filter or search for converted leads
3. Verify they all appear
4. Verify conversion dates are shown
5. Verify they're easy to find

### Test 7: Test conversion details editing

1. Convert a lead
2. Edit the conversion details
3. Save the changes
4. Verify the updates are saved
5. Verify they're reflected in the lead's information

### Test 8: Test on all platforms

1. Test conversion on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] "Mark as Converted" action is available for leads
- [ ] Conversion dialog appears with confirmation
- [ ] Optional conversion details can be entered
- [ ] Converted lead moves to special stage
- [ ] Conversion date is tracked
- [ ] Success message celebrates the conversion
- [ ] Converted leads are visually distinct
- [ ] Cannot accidentally unconvert without warning
- [ ] Converted leads can be found via search/filter
- [ ] Conversion details can be edited later
- [ ] Works on Windows, macOS, and Linux
- [ ] Conversion tracking is accurate
- [ ] The feature feels rewarding to use