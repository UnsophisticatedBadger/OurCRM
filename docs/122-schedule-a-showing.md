# 122 - Schedule A Showing

**Capability:** Calendar & Showings
**Milestone:** Extended CRM
**Status:** Not Done
**GitHub Issue:** #122

## User Story

As a real estate agent, I want to schedule a showing for a contact at a property, so that I can track property viewings and keep my calendar organised.

## Dependencies

- #56 — Create a Contact
- #60 — Delete A Contact (contact deletion must respect the showing link introduced by this story)
- #104 — Create a Property Listing

## Acceptance Criteria

1. A "Schedule Showing" action is accessible from the Calendar section, a contact's detail view, and a property's detail view
2. The form collects: contact (required), property (required), date (required), start time (required), duration (30 / 60 / 90 / 120 min, default 60), and notes (optional)
3. When opened from a contact's detail view the contact field is pre-populated with that contact
4. When opened from a property's detail view the property field is pre-populated with that property
5. Attempting to save with a past date or time is rejected with a validation error
6. Attempting to save without contact, property, date, or start time is rejected with a validation error identifying the missing field
7. A saved showing appears in the calendar view at the correct date and time, labelled with the contact's name and property address
8. A saved showing persists across application restarts
9. A contact linked to a showing cannot be deleted while the link exists (extends #60 — Delete A Contact with a showing-tie check, implemented via a DI-injected guard interface so the Contacts capability does not import from Calendar & Showings)

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/calendar.feature`.

```gherkin
@story_122
Scenario: User schedules a showing from the Calendar section
  Given a contact "Alice Smith" and property "123 Oak St" exist
  When the user opens "Schedule Showing" from the Calendar section
  And enters contact "Alice Smith", property "123 Oak St", tomorrow's date, start time 10:00 AM, and duration 60 min
  And clicks Save
  Then the showing appears in the calendar on tomorrow's date at 10:00 AM
  And is labelled with "Alice Smith" and "123 Oak St"

@story_122
Scenario: User opens the showing form from a contact's detail view and contact is pre-populated
  Given a contact "Alice Smith" exists
  When the user clicks "Schedule Showing" from Alice Smith's detail view
  Then the contact field shows "Alice Smith"

@story_122
Scenario: User opens the showing form from a property's detail view and property is pre-populated
  Given a property "123 Oak St" exists
  When the user clicks "Schedule Showing" from the property's detail view
  Then the property field shows "123 Oak St"

@story_122
Scenario: User tries to save a showing with a past date and sees a validation error
  Given the showing form is open
  When the user enters yesterday's date and clicks Save
  Then a validation error is shown and the showing is not saved

@story_122
Scenario: User tries to save without a required field and sees a validation error
  Given the showing form is open with contact and date filled in but no property selected
  When the user clicks Save
  Then a validation error indicates that property is required
```

## Manual Tests

**Story:** [#122 — Schedule a Showing](122-schedule-a-showing.md)
### User schedules a showing from the Calendar section
1. Open the Calendar section
2. Click "Schedule Showing"
3. Fill in contact, property, tomorrow's date, 10:00 AM start time, 60 min duration, and a preparation note
4. Click Save
5. Confirm the showing appears in the calendar at the correct date and time
6. Confirm the label shows the contact name and property address
7. Restart the app and confirm the showing is still there

### Contact is pre-populated when opening from a contact's detail view
1. Open any contact's detail view
2. Click "Schedule Showing"
3. Confirm the contact field already shows that contact's name
4. Fill in the remaining required fields and save successfully

### Property is pre-populated when opening from a property's detail view
1. Open any property's detail view
2. Click "Schedule Showing"
3. Confirm the property field already shows that property's address
4. Fill in the remaining required fields and save successfully

### User is blocked from scheduling in the past
1. Open the showing form
2. Enter yesterday's date
3. Click Save
4. Confirm a validation error appears and no showing is created

### Required field validation
1. Open the showing form
2. Fill in all fields except property, then attempt Save — confirm an error naming the missing field
3. Repeat for contact, date, and start time

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/calendar.feature` |
| BDD step defs | `tests/bdd/test_calendar.py` |
| Unit tests | `tests/unit/calendar/test_showing_scheduling.py` |
| Manual tests | `tests/manual/calendar/showing_scheduling.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
