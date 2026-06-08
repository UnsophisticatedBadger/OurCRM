# US-056: Schedule a Showing

## User Story

**As an** agent  
**I want to** schedule a showing (property viewing) for a contact  
**So that** I can track property viewings and manage my calendar

## Priority

**MVP:** Must Have

**Rationale:** Showings are a core activity for real estate agents. They need to schedule property viewings with buyers, track when showings happen, and manage their calendar. This is essential daily work that the CRM must support.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design showing creation form
- 2 hours: Create form UI with showing fields
- 1 hour: Link to contact and property
- 1 hour: Add date/time picker
- 1 hour: Implement form validation
- 1 hour: Save showing to database
- 1 hour: Test showing creation
- 1 hour: Test validation
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-015 (Create the First Window), US-014 (Create Encrypted Database)

**Blocks:** US-057 (View Upcoming Showings), US-058 (Mark Showing as Completed), US-059 (Add Showing Notes)

## Description

A user should be able to schedule a showing (property viewing) by selecting a contact (the buyer), a property, and a date/time. The showing should be added to the calendar and should be associated with both the contact and the property.

The showing creation form should allow:
- Selecting an existing contact or creating a new one
- Selecting an existing property or creating a new one
- Choosing a date and time
- Setting duration
- Adding notes (e.g., "First time viewing", "Bring pre-approval letter")

## BDD Scenarios

### Scenario 1: Open showing creation form

```
Given I am in the Calendar section or on a property/contact details
When I click "Schedule Showing"
Then a showing creation form should open
  And the form should have fields for:
    - Contact (buyer)
    - Property
    - Date
    - Start time
    - Duration (30/60/90/120 minutes)
    - Notes
```

### Scenario 2: Schedule showing with all details

```
Given the showing form is open
When I select a contact
  And I select a property
  And I choose a date and time
  And I set a duration
  And I add notes
  And I click "Save"
Then the showing should be saved
  And it should appear in the calendar
  And it should be associated with the contact and property
```

### Scenario 3: Schedule from contact details

```
Given I am viewing a contact's details
When I click "Schedule Showing"
Then the showing form should open
  And the contact should be pre-selected
  And I just need to choose the property and time
```

### Scenario 4: Schedule from property details

```
Given I am viewing a property's details
When I click "Schedule Showing"
Then the showing form should open
  And the property should be pre-selected
  And I just need to choose the contact and time
```

### Scenario 5: Validate date and time

```
Given I am scheduling a showing
When I try to schedule in the past
  Or I don't select a date/time
Then I should see a validation error
  And the showing should not be saved
```

### Scenario 6: Showing appears in calendar

```
Given I have scheduled a showing
When I view the calendar
Then the showing should be visible at the scheduled date/time
  And it should show the contact and property names
```

### Scenario 7: Conflict detection

```
Given I am scheduling a showing
When I choose a time that conflicts with another showing
Then I should see a warning
  And I can choose to proceed or reschedule
```

### Scenario 8: Duration validation

```
Given I am scheduling a showing
When I set a very long duration (e.g., 8 hours)
Then I should see a warning
  And I can choose a more reasonable duration
```

## Manual Testing Steps

### Test 1: Open showing form

1. Navigate to Calendar or a contact/property
2. Click "Schedule Showing"
3. Verify the form opens
4. Verify all expected fields are present

### Test 2: Schedule a complete showing

1. Open the showing form
2. Select a contact
3. Select a property
4. Choose a date and time
5. Set duration to 60 minutes
6. Add notes
7. Click "Save"
8. Verify the success message
9. Verify it appears in the calendar

### Test 3: Schedule from contact

1. Open a contact's details
2. Click "Schedule Showing"
3. Verify the contact is pre-selected
4. Select a property
5. Choose a time
6. Save the showing
7. Verify it's associated with the contact

### Test 4: Schedule from property

1. Open a property's details
2. Click "Schedule Showing"
3. Verify the property is pre-selected
4. Select a contact
5. Choose a time
6. Save the showing
7. Verify it's associated with the property

### Test 5: Test validation

1. Try to schedule a showing in the past
2. Verify the validation error
3. Try without selecting a contact
4. Verify the error
5. Try without selecting a property
6. Verify the error

### Test 6: Test calendar integration

1. Schedule a showing
2. View the calendar
3. Verify the showing appears
4. Verify the date/time is correct
5. Click on the showing
6. Verify the details are shown

### Test 7: Test conflict detection

1. Schedule a showing at 2:00 PM
2. Try to schedule another showing at 2:00 PM
3. Verify the conflict warning
4. Choose to proceed or reschedule

### Test 8: Test on all platforms

1. Test showing scheduling on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] "Schedule Showing" button is accessible from multiple places
- [ ] Form opens with all showing fields
- [ ] Can link to existing contact
- [ ] Can link to existing property
- [ ] Date and time can be selected
- [ ] Duration can be set
- [ ] Notes can be added
- [ ] Validation prevents past dates
- [ ] Showing appears in calendar
- [ ] Conflict detection warns of overlapping showings
- [ ] Can be scheduled from contact details
- [ ] Can be scheduled from property details
- [ ] Data persists across restarts
- [ ] Works on Windows, macOS, and Linux
- [ ] Form is intuitive and easy to use