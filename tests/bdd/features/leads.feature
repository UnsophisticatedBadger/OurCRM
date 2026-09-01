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
