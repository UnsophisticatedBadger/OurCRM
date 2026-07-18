Feature: Contacts

  @story_56
  Scenario: User creates a contact with a name and sees it in the list
    Given the user is in the Contacts section
    When the user clicks "New Contact"
    And fills in first name "Jane" and last name "Smith"
    And clicks Save
    Then the contact list shows "Jane Smith"

  @story_56
  Scenario: User submits the new contact form with no name and sees an error
    Given the new contact form is open
    When the user leaves both name fields empty and clicks Save
    Then the error "Name is required" is shown
    And the form stays open

  @story_56
  Scenario: User enters an invalid email and sees a validation error
    Given the new contact form is open
    When the user enters "notanemail" in the email field and clicks Save
    Then an inline email format error is shown

  @story_56
  Scenario: User cancels the new contact form and no contact is created
    Given the new contact form is open and the user has entered data
    When the user clicks Cancel
    Then the form closes and the contact does not appear in the contact list

  @story_56
  Scenario: Contact created in one session is visible after restart
    Given the user has created a contact "Jane Smith"
    When the application is restarted and the user opens the Contacts section
    Then "Jane Smith" appears in the contact list
