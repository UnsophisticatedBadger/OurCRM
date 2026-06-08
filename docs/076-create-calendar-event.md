# US-076: Create a Calendar Event

## User Story

**As an** agent  
**I want to** create calendar events (showings, meetings, appointments)  
**So that** I can manage my schedule and not miss important activities

## Priority

**MVP:** Must Have

**Rationale:** Calendar events are the core of an agent's daily schedule. Without the ability to create events, the CRM can't help agents manage their time. This is fundamental functionality for any real estate professional.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design event creation form
- 2 hours: Create form UI with date/time pickers
- 1 hour: Implement form validation
- 1 hour: Save event to database
- 1 hour: Add event to calendar view
- 1 hour: Test event creation
- 1 hour: Test validation
- 1 hour: Test calendar integration
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-015 (Create the First Window), US-014 (Create Encrypted Database)

**Blocks:** US-077 (View Calendar), US-078 (Edit Calendar Event), US-079 (Delete Calendar Event)

## Description

Users should be able to create calendar events for various activities: showings, listing appointments, buyer consultations, team meetings, closings, inspections, and personal appointments. The event creation form should allow specifying the event title, date, start time, end time, description, and optional location.

Events should be saved to the database and displayed in the calendar view. The system should support basic events with a clear time range. Recurring events and complex scheduling are not required for MVP.

## BDD Scenarios

### Scenario 1: Open event creation form

```
Given I am in the Calendar section
When I click "New Event" or click on a date/time
Then the event creation form should open
  And the form should have fields for:
    - Title
    - Date
    - Start time
    - End time
    - Description
    - Location (optional)
```

### Scenario 2: Create event with all details

```
Given the event form is open
When I enter:
  - Title: "Showing - 123 Main St"
  - Date: tomorrow
  - Start time: 2:00 PM
  - End time: 3:00 PM
  - Description: "First viewing with John Smith"
  - Location: "123 Main St, Houston, TX"
  And I click "Save"
Then the event should be saved
  And it should appear in the calendar
  And the time should be blocked out
```

### Scenario 3: Create quick event

```
Given the event form is open
When I enter only the title and date/time
  And I click "Save"
Then the event should be saved with minimal details
  And it should appear in the calendar
```

### Scenario 4: Validate date and time

```
Given I am creating an event
When I try to set an end time before the start time
  Or I don't select a date
Then I should see a validation error
  And the event should not be saved
```

### Scenario 5: Event appears in calendar

```
Given I have created an event
When I view the calendar
Then the event should be visible on the correct date
  And at the correct time
  And it should show the event title
```

### Scenario 6: Click empty time slot to create event

```
Given I am viewing the calendar
When I click on an empty time slot on a specific day
Then the event form should open
  And the date and time should be pre-filled
  Based on where I clicked
```

### Scenario 7: Event duration validation

```
Given I am creating an event
When I set the duration to a very long time (e.g., 24 hours)
Then I should see a warning
  And I can choose to proceed or adjust
```

### Scenario 8: Event in the past

```
Given I am creating an event
When I set a date/time in the past
Then I should see a warning
  And I can choose to proceed (for logging past events)
```

## Manual Testing Steps

### Test 1: Open event form

1. Navigate to the Calendar section
2. Click "New Event"
3. Verify the form opens
4. Verify all expected fields are present
5. Verify the form is clean and empty

### Test 2: Create complete event

1. Open the event form
2. Fill in all fields with valid data
3. Click "Save"
4. Verify the success message
5. View the calendar
6. Verify the event appears

### Test 3: Test quick event

1. Open the event form
2. Enter only title and date/time
3. Save the event
4. Verify it saves successfully
5. Verify it appears in the calendar

### Test 4: Test validation

1. Open the event form
2. Set end time before start time
3. Try to save
4. Verify the validation error
5. Try without a date
6. Verify the error
7. Correct the issues and save

### Test 5: Test calendar integration

1. Create an event
2. View the calendar
3. Verify the event is in the right place
4. Verify the time is correct
5. Verify the title is shown

### Test 6: Test click to create

1. View the calendar
2. Click on an empty time slot
3. Verify the form opens
4. Verify the date/time are pre-filled
5. Enter the event details and save

### Test 7: Test on all platforms

1. Test event creation on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] "New Event" button is accessible from Calendar
- [ ] Clicking an empty time slot opens the form
- [ ] Form has all required fields
- [ ] Date and time pickers work correctly
- [ ] Validation prevents invalid times
- [ ] Events appear in the calendar immediately
- [ ] Events show title, time, and date
- [ ] Events can be created with minimal details
- [ ] Events persist across restarts
- [ ] Form is intuitive and easy to use
- [ ] Works on Windows, macOS, and Linux
- [ ] Calendar integration is smooth