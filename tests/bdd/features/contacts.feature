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

  @story_57
  Scenario: User with contacts sees them listed in the Contacts section
    Given the user has created contacts "Alice Brown" and "Bob Carter"
    When the user opens the Contacts section
    Then the list shows "Alice Brown" and "Bob Carter"
    And the list is sorted by last name by default

  @story_57
  Scenario: User with no contacts sees an empty state
    Given the user has no contacts
    When the user opens the Contacts section
    Then "No contacts yet" is shown
    And a "Create Your First Contact" button is visible

  @story_57
  Scenario: User sorts the contact list by clicking a column header
    Given the user is viewing a contact list with multiple contacts
    When the user clicks the "Last Name" column header
    Then the contacts are sorted by last name descending
    When the user clicks the "Last Name" column header again
    Then the contacts are sorted alphabetically by last name ascending

  @story_57
  Scenario: User double-clicks a contact and sees its details
    Given the user is viewing the contact list
    When the user double-clicks "Alice Brown"
    Then the contact details view opens for "Alice Brown"

  @story_57
  Scenario: Sort order is preserved when the user navigates away and back
    Given the user has sorted the contact list by email ascending
    When the user navigates to the Leads section and back to Contacts
    Then the list is still sorted by email ascending
    And the scroll position is unchanged

  @story_58
  Scenario: User opens a contact and sees all stored fields
    Given a contact "Jane Smith" exists with email "jane@example.com" and phone "555-1234"
    When the user double-clicks "Jane Smith"
    Then the details view shows "jane@example.com" and "555-1234"

  @story_58
  Scenario: User sees "Not provided" for empty optional fields
    Given a contact "Bob Carter" exists with only a name
    When the user opens the details for "Bob Carter"
    Then empty optional fields show "Not provided"

  @story_58
  Scenario: User navigates to the next contact
    Given the user is viewing details for "Alice Brown" with "Bob Carter" next in list order
    When the user clicks Next
    Then the details for "Bob Carter" are shown

  @story_58
  Scenario: User navigates to the previous contact
    Given the user is viewing details for "Bob Carter" with "Alice Brown" previous in list order
    When the user clicks Previous
    Then the details for "Alice Brown" are shown

  @story_58
  Scenario: User clicks Next on the last contact and wraps to the first
    Given the user is viewing details for the last contact in list order, "Carol Diaz", with "Alice Brown" first
    When the user clicks Next
    Then the details for "Alice Brown" are shown

  @story_58
  Scenario: User returns to the list and the same contact is still selected
    Given the user is viewing the details for "Alice Brown"
    When the user clicks Back to List
    Then the contact list is shown with "Alice Brown" still selected

  @story_58
  Scenario: User presses Escape and the same contact is still selected
    Given the user is viewing the details for "Alice Brown"
    When the user presses Escape
    Then the contact list is shown with "Alice Brown" still selected
