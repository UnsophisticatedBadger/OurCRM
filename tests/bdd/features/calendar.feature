Feature: Calendar

  @us-060
  Scenario: Calendar section shows a month grid
    Given I am logged in
    When I navigate to the Calendar section
    Then I should see a month grid
    And today's date should be highlighted
    And the current month and year should be displayed

  @us-060
  Scenario: Events appear as indicators on their date
    Given I have created an event on a specific date
    When I view the calendar
    Then that date should show an indicator
    And dates without events should show no indicator

  @us-060
  Scenario: Clicking a date with events shows a list for that day
    Given I have events on a date
    When I click that date on the calendar
    Then a list of events for that day should appear
    And each event should show its title, start time, and end time

  @us-060
  Scenario: Clicking a date with no events shows an empty list
    Given I have no events on a date
    When I click that date on the calendar
    Then an empty event list should appear

  @us-060
  Scenario: New Event button opens the creation form
    Given I am viewing the Calendar section
    When I click "New Event"
    Then the event creation form should open
    And the form should have a title field
    And the form should have a date field
    And the form should have a start time field
    And the form should have an end time field
    And the form should have a description field
    And the form should have a location field
    And the form should be empty

  @us-060
  Scenario: Create an event with full details
    Given the event creation form is open
    When I enter a title, date, start time, end time, description, and location
    And I click "Save"
    Then the event should be saved to the database
    And the calendar should show an indicator on the event's date
    And clicking the event's date should show the event in the list

  @us-060
  Scenario: Create a quick event with only required fields
    Given the event creation form is open
    When I enter only a title, date, start time, and end time
    And I click "Save"
    Then the event should be saved
    And it should appear in the day list with no description or location

  @us-060
  Scenario: Validation blocks save when end time is before start time
    Given the event creation form is open
    When I set start time to 3:00 PM and end time to 2:00 PM
    And I click "Save"
    Then I should see a validation error
    And the event should not be saved

  @us-060
  Scenario: Duration warning shown and user proceeds to save
    Given the event creation form is open
    When I set a duration longer than 24 hours
    And I click "Save"
    Then I should see a duration warning
    When I choose to proceed
    Then the event should be saved

  @us-060
  Scenario: Duration warning shown and user cancels
    Given the event creation form is open
    When I set a duration longer than 24 hours
    And I click "Save"
    Then I should see a duration warning
    When I choose to cancel
    Then the event should not be saved

  @us-060
  Scenario: Past date warning shown and user proceeds to save
    Given the event creation form is open
    When I set the date to a date in the past
    And I click "Save"
    Then I should see a past date warning
    When I choose to proceed
    Then the event should be saved

  @us-060
  Scenario: Past date warning shown and user cancels
    Given the event creation form is open
    When I set the date to a date in the past
    And I click "Save"
    Then I should see a past date warning
    When I choose to cancel
    Then the event should not be saved

  @us-060
  Scenario: Navigate to previous month
    Given I am viewing the calendar
    When I click the previous month button
    Then the calendar should show the previous month
    And events for that month should be indicated

  @us-060
  Scenario: Navigate to next month
    Given I am viewing the calendar
    When I click the next month button
    Then the calendar should show the next month
    And events for that month should be indicated

  @us-060
  Scenario: Today button returns to current month
    Given I have navigated away from the current month
    When I click "Today"
    Then the calendar should return to the current month
    And today's date should be highlighted and selected

  @us-060
  Scenario: Calendar state is preserved when switching sections
    Given I am viewing a non-current month on the calendar
    When I navigate to the Contacts section
    And I navigate back to Calendar
    Then the calendar should still show the same month

  @us-059
  Scenario: Switch to week view
    Given I am viewing the calendar
    When I click the "Week" view button
    Then I should see the week view

  @us-059
  Scenario: Switch to day view
    Given I am viewing the calendar
    When I click the "Day" view button
    Then I should see the day view

  @us-059
  Scenario: Switch back to month view from week view
    Given I am viewing the calendar
    When I click the "Week" view button
    And I click the "Month" view button
    Then I should see a month grid

  @us-059
  Scenario: Click event in day list shows details
    Given I have events on a date
    When I click that date on the calendar
    And I click on an event in the day list
    Then the event detail dialog should open
    And the dialog should show the event title

  @us-059
  Scenario: Week view state preserved when switching sections
    Given I am viewing the calendar in week view on a different week
    When I navigate to the Contacts section
    And I navigate back to Calendar
    Then the calendar should still be in week view

  @us-059
  Scenario: Events are color-coded by type
    Given I have events of different types on a date
    When I click that date on the calendar
    Then events of different types should have different colors in the list

  @us-059
  Scenario: Navigate to previous week in week view
    Given I am viewing the calendar in week view
    When I click the previous month button
    Then the calendar should show the previous week

  @us-059
  Scenario: Navigate to next week in week view
    Given I am viewing the calendar in week view
    When I click the next month button
    Then the calendar should show the next week

  @us-059
  Scenario: Today button resets week view to current week
    Given I am viewing the calendar in week view on a different week
    When I click "Today"
    Then the week view should show the current week

  @us-059
  Scenario: Navigate to previous day in day view
    Given I am viewing the calendar in day view
    When I click the previous month button
    Then the calendar should show the previous day

  @us-059
  Scenario: Navigate to next day in day view
    Given I am viewing the calendar in day view
    When I click the next month button
    Then the calendar should show the next day

  @us-059
  Scenario: Today button resets day view to today
    Given I am viewing the calendar in day view on a different day
    When I click "Today"
    Then the day view should show today

  @us-059
  Scenario: Day view state preserved when switching sections
    Given I am viewing the calendar in day view on a different day
    When I navigate to the Contacts section
    And I navigate back to Calendar
    Then the calendar should still be in day view

  @us-059
  Scenario: Event detail dialog shows full event details
    Given I have a detailed event on today
    When I click that date on the calendar
    And I click on an event in the day list
    Then the event detail dialog should open
    And the dialog should show the event date
    And the dialog should show the event time range
    And the dialog should show the event type
    And the dialog should show the event description
    And the dialog should show the event location

  @us-059
  Scenario: Events appear in week view
    Given I have an event this week in the calendar
    When I click the "Week" view button
    Then the event should appear in the week view

  @us-059
  Scenario: Events appear in day view time slots
    Given I have an event today in the calendar
    When I click the "Day" view button
    Then the event should appear in the day view
