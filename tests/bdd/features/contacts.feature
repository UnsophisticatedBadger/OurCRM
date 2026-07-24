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

  @story_59
  Scenario: User edits a contact's phone and the new value appears in the details view
    Given the user is viewing the details for "Jane Smith" with phone "555-0000"
    When the user clicks Edit, changes the phone to "555-9999", and clicks Save
    Then the details view shows the phone "555-9999"

  @story_59
  Scenario: User cancels an edit and the original data is unchanged
    Given the edit form is open for "Jane Smith" with email "old@example.com"
    When the user changes the email to "new@example.com" and clicks Cancel
    Then the details view still shows "old@example.com"

  @story_59
  Scenario: Edited data persists after an application restart
    Given the user has edited "Jane Smith" phone to "555-9999" and saved
    When the application is restarted and the user opens "Jane Smith"
    Then the phone "555-9999" is shown

  @story_60
  Scenario: User deletes a contact and it is removed from the list
    Given the user is viewing the details for "Jane Smith"
    When the user clicks Delete and confirms
    Then "Jane Smith" no longer appears in the contact list

  @story_60
  Scenario: User cancels deletion and the contact remains
    Given the delete confirmation dialog is open for "Jane Smith" from the details view
    When the user clicks Cancel in the delete confirmation dialog
    Then the details view still shows "Jane Smith"

  @story_60
  Scenario: Deleted contact does not reappear after restart
    Given the user has deleted "Jane Smith"
    When the application is restarted and the user opens the Contacts section
    Then "Jane Smith" is not in the list

  @story_64
  Scenario: Typing in the search box filters the contact list
    Given contacts "John Smith" and "Jane Doe" exist
    When the user types "John" in the search box
    Then only "John Smith" is shown

  @story_64
  Scenario: Search is case-insensitive
    Given a contact "John Smith" exists
    When the user searches for "john"
    Then "John Smith" appears in results

  @story_64
  Scenario: Search supports partial matches
    Given a contact "Johnson" exists
    When the user searches for "John"
    Then "Johnson" appears in results

  @story_64
  Scenario: Searching by email finds the correct contact
    Given a contact with email "jane@example.com" exists
    When the user searches for "jane@example"
    Then that contact is shown in results

  @story_64
  Scenario: Searching by phone finds the correct contact
    Given a contact with phone "555-0100" exists
    When the user searches for "0100"
    Then that contact is shown in results

  @story_64
  Scenario: Searching by street address finds the correct contact
    Given a contact with street address "123 Oak St" exists
    When the user searches for "Oak"
    Then that contact is shown in results

  @story_64
  Scenario: Searching by city finds the correct contact
    Given a contact with city "Austin" exists
    When the user searches for "Austin"
    Then that contact is shown in results

  @story_64
  Scenario: Searching by tag finds the correct contact
    Given a contact tagged "vip" exists
    When the user searches for "vip"
    Then that contact is shown in results

  @story_64
  Scenario: No results shows a helpful message
    Given a contact "John Smith" exists
    When the user searches for "xyz123"
    Then a "No contacts found" message is shown

  @story_64
  Scenario: Clearing the search restores the full contact list
    Given contacts "John Smith" and "Jane Doe" exist and the user has searched for "John"
    When the user clears the search box
    Then all contacts are shown again

  @story_43
  Scenario: User saves a new contact whose phone number matches an existing contact and confirms anyway
    Given a contact "Alice Brown" exists with phone "555-0100" and the new contact form is open
    When fills in first name "Bob" and last name "Carter"
    And fills in phone "555-0100"
    And clicks Save
    Then a duplicate phone warning is shown
    When the user confirms the duplicate phone warning
    Then the contact list shows "Bob Carter"

  @story_43
  Scenario: User saves a new contact whose phone number matches an existing contact and cancels
    Given a contact "Alice Brown" exists with phone "555-0100" and the new contact form is open
    When fills in first name "Bob" and last name "Carter"
    And fills in phone "555-0100"
    And clicks Save
    Then a duplicate phone warning is shown
    When the user cancels the duplicate phone warning
    Then the form stays open
    And "Bob Carter" does not appear in the contact list

  @story_44
  Scenario: User toggles to the Call List and sees only contacts with a phone number
    Given contacts "Ann NoPhone" with no phone and "Bob HasPhone" with phone "555-0100" exist
    When the user clicks the "Call List" toggle
    Then only "Bob HasPhone" is shown

  @story_44
  Scenario: User toggles back to All Contacts and sees every contact again
    Given contacts "Ann NoPhone" with no phone and "Bob HasPhone" with phone "555-0100" exist
    When the user clicks the "Call List" toggle
    And the user clicks the "All Contacts" toggle
    Then the list shows "Ann NoPhone" and "Bob HasPhone"

  @story_44
  Scenario: Call list row shows the contact's phone number and street address
    Given a contact "Bob HasPhone" exists with phone "555-0100" and street address "123 Main St"
    When the user clicks the "Call List" toggle
    Then the row for "Bob HasPhone" shows phone "555-0100" and street "123 Main St"

  @story_44
  Scenario: A newly added contact with a phone number appears in the call list immediately
    Given the user has no contacts and clicks the "Call List" toggle
    When the user clicks "New Contact"
    And fills in first name "Carl" and last name "New"
    And fills in phone "555-0200"
    And clicks Save
    Then "Carl New" appears in the contact list

  @story_44
  Scenario: Clicking the dashboard Call List quick action opens the call list directly
    Given the user is on the dashboard
    When the user clicks the "Call List" quick action
    Then the Contacts section is shown with the Call List toggle active
