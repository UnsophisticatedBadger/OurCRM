Feature: Leads

  @story_70
  Scenario: User creates a lead and sees it in the lead list
    Given the user is in the Leads section
    When the user clicks "New Lead", fills in name "Sara Lee" and status "Hot", and clicks Save
    Then the lead list shows "Sara Lee" with status "Hot"

  @story_70
  Scenario: User submits the lead form with no name and sees an error
    Given the new lead form is open
    When the user leaves the name empty and clicks Save
    Then an error is shown and the form stays open

  @story_70
  Scenario: User submits the lead form with no status and sees an error
    Given the new lead form is open
    When the user enters name "Sara Lee", leaves status unselected, and clicks Save
    Then an error is shown and the form stays open

  @story_70
  Scenario: User enters a min budget greater than max and sees an error
    Given the new lead form is open
    When the user enters min budget 500000 and max budget 300000 and clicks Save
    Then "Minimum budget cannot be greater than maximum budget" is shown

  @story_70
  Scenario: Creating a lead also creates a linked contact
    Given the user creates a lead "Sara Lee" with email "sara@example.com"
    When the user navigates to the Contacts section
    Then "Sara Lee" appears in the contact list

  @story_70
  Scenario: Creating a lead for an existing contact links to that contact instead of duplicating it
    Given a contact "Sara Lee" already exists with email "sara@example.com"
    When the user creates a lead named "Sara Lee" with email "sara@example.com"
    Then the Contacts section shows exactly one "Sara Lee" contact

  @story_70
  Scenario: User cancels the new lead form and nothing is saved
    Given the new lead form is open
    When the user fills in name "Sara Lee" and clicks Cancel
    Then the lead list does not show "Sara Lee"

  @story_70
  Scenario: Lead persists after an application restart
    Given the user has created a lead "Sara Lee"
    When the application is restarted and the user opens the Leads section
    Then "Sara Lee" appears in the lead list

  @story_71
  Scenario: User with leads sees them in the Leads section
    Given leads "Sara Lee" (Hot) and "Bob Kim" (Cold) exist
    When the user opens the Leads section
    Then the list shows "Sara Lee" and "Bob Kim"
    And "Sara Lee" appears before "Bob Kim" (Hot sorted first)

  @story_71
  Scenario: Lead list shows the expected columns
    Given a lead "Sara Lee" with source, budget, and timeline set exists
    When the user opens the Leads section
    Then the lead list shows columns for name, status, source, budget range, and timeline

  @story_71
  Scenario: Status column is color-coded
    Given leads with Hot, Warm, and Cold statuses exist
    When the user views the lead list
    Then the Hot status indicator is red, Warm is orange, and Cold is blue

  @story_71
  Scenario: User with no leads sees an empty state
    Given no leads exist
    When the user opens the Leads section
    Then "No leads yet" is shown
    And a "Create Your First Lead" button is visible

  @story_71
  Scenario: Clicking a column header sorts the list by that column
    Given leads "Bob Kim" (Cold) and "Sara Lee" (Hot) exist
    When the user clicks the "Name" column header
    Then the leads are sorted alphabetically by name

  @story_71
  Scenario: Clicking the same column header again reverses the sort order
    Given leads "Bob Kim" (Cold) and "Sara Lee" (Hot) exist
    When the user clicks the "Name" column header twice
    Then the leads are sorted in reverse alphabetical order by name

  @story_71
  Scenario: User filters the list to show only Hot leads
    Given leads with Hot and Cold statuses exist
    When the user selects the "Hot" status filter
    Then only Hot leads are shown in the list

  @story_71
  Scenario: User selects "All" to clear the status filter
    Given the user has the "Hot" filter active
    When the user selects the "All" status filter
    Then leads of every status are shown again

  @story_71
  Scenario: Double-clicking a lead opens a read-only details dialog
    Given a lead "Sara Lee" with full details exists
    When the user double-clicks "Sara Lee" in the lead list
    Then a details dialog opens showing "Sara Lee"'s name, status, source, budget range, desired location, property type, timeline, and notes

  @story_71
  Scenario: Status filter is preserved after navigating away and back
    Given the user has the "Hot" filter active
    When the user navigates to Contacts and returns to Leads
    Then only Hot leads are still shown

  @story_71
  Scenario: Sort order is preserved after navigating away and back
    Given the user has sorted the lead list by name
    When the user navigates to Contacts and returns to Leads
    Then the lead list is still sorted by name
