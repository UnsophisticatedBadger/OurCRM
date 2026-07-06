Feature: Authentication

  @story_3
  Scenario: Accept a password that meets all requirements
    Given the password validator is available
    When I validate the password "SecureP@ssw0rd!2024"
    Then the password should be accepted

  @story_3
  Scenario Outline: Reject a password that violates a requirement
    Given the password validator is available
    When I validate the password "<password>"
    Then the errors should include "<error>"

    Examples:
      | password           | error                                                |
      | Short1!A           | Password must be at least 12 characters              |
      | nouppercase1!xx    | Password must contain at least one uppercase letter  |
      | NOLOWERCASE1!XX    | Password must contain at least one lowercase letter  |
      | NoNumbersHere!!    | Password must contain at least one number            |
      | NoSpecialChars12   | Password must contain at least one special character |

  @story_3
  Scenario: Reject mismatched password confirmation
    Given the password validator is available
    When I validate "SecureP@ssw0rd!2024" with confirmation "WrongConfirm1!"
    Then the errors should include "Passwords do not match"

  @story_3
  Scenario Outline: Evaluate password strength
    Given the password hasher is available
    When I evaluate the strength of "<password>"
    Then the strength should be "<strength>"

    Examples:
      | password             | strength |
      | password12345678     | Weak     |
      | MyPassword123456     | Medium   |
      | SecureP@ssw0rd!2024  | Strong   |

  @story_3
  Scenario: Hash a password using Argon2id
    Given the password hasher is available
    When I hash the password "SecureP@ssw0rd!2024"
    Then the hash should start with "$argon2id$"
    And the original password "SecureP@ssw0rd!2024" should verify against the hash

  @story_3
  Scenario: Store only the hash in the OS keyring on master password creation
    Given a clean in-memory keyring
    When I create the master password "SecureP@ssw0rd!2024"
    Then the keyring should contain an Argon2id hash for "master_password_hash"
    And the plain password should not be in the keyring

  @story_4
  Scenario: User's recovery password is 32 characters long with no ambiguous characters
    Given the recovery password setup screen is open
    Then the recovery password is 32 characters long
    And the recovery password contains no ambiguous characters

  @story_4
  Scenario: The recovery password is displayed grouped with dashes and round-trips to the raw password
    Given the recovery password setup screen is open
    Then the displayed recovery password is grouped with dashes every 5 characters
    And the displayed recovery password with dashes removed matches the recovery password

  @story_4
  Scenario: Reopening the setup screen generates a different recovery password
    Given the recovery password setup screen is open
    When the recovery password setup screen is opened again
    Then the two recovery passwords are different

  @story_4
  Scenario: User copies the recovery password to the clipboard
    Given the recovery password setup screen is open
    When the user clicks Copy to Clipboard
    Then the clipboard contains the recovery password with no dashes

  @story_4
  Scenario: Continue button starts disabled when the setup screen opens
    Given the recovery password setup screen is open
    Then the Continue button is disabled

  @story_4
  Scenario: Checking only the first checkbox keeps Continue disabled
    Given the recovery password setup screen is open
    When the user checks the first confirmation checkbox
    Then the Continue button is disabled

  @story_4
  Scenario: Checking only the second checkbox keeps Continue disabled
    Given the recovery password setup screen is open
    When the user checks the second confirmation checkbox
    Then the Continue button is disabled

  @story_4
  Scenario: Checking both checkboxes without typing CONFIRM keeps Continue disabled
    Given the recovery password setup screen is open
    When the user checks both checkboxes
    Then the Continue button is disabled

  @story_4
  Scenario Outline: Typing anything other than exact CONFIRM keeps Continue disabled
    Given the recovery password setup screen is open
    When the user checks both checkboxes
    And the user types "<text>" in the recovery confirmation field
    Then the Continue button is disabled

    Examples:
      | text     |
      | confirm  |
      | Confirm  |
      | CONFIRM! |
      | confirm! |

  @story_4
  Scenario: Checking both checkboxes and typing CONFIRM enables Continue
    Given the recovery password setup screen is open
    When the user checks both checkboxes
    And the user types "CONFIRM" in the recovery confirmation field
    Then the Continue button is enabled

  @story_4
  Scenario: Clicking Continue accepts the recovery password setup screen
    Given the recovery password setup screen is open
    When the user checks both checkboxes
    And the user types "CONFIRM" in the recovery confirmation field
    And the user clicks Continue
    Then the recovery password setup screen is accepted

  @story_4
  Scenario: Closing the setup screen warns that progress will be lost
    Given the recovery password setup screen is open
    When the user closes the recovery password setup screen
    Then a warning explains the master password and database will be deleted

  @story_4
  Scenario: Confirming exit deletes the database and clears the master password
    Given the recovery password setup screen is open for a freshly created database
    When the user closes the recovery password setup screen and confirms exit
    Then the database file no longer exists
    And the master password is cleared from the keyring

  @story_4
  Scenario: Declining to exit keeps the setup screen open
    Given the recovery password setup screen is open
    When the user closes the recovery password setup screen and declines to exit
    Then the recovery password setup screen is still open

  @story_5
  Scenario: Schema is initialized after database creation
    Given an in-memory database manager
    When I initialize the schema
    Then the alembic_version table should exist

  @story_5
  Scenario: Session key is stored in keyring when session starts
    Given a clean in-memory keyring
    And an in-memory database manager
    When I start a session with key "mysessionkey123456789012345678901"
    Then the keyring should contain the session key under "db_session_key"

  @story_5
  Scenario: Session key is removed from keyring when session closes
    Given a clean in-memory keyring
    And an in-memory database manager
    When I start a session with key "mysessionkey123456789012345678901"
    And I close the session
    Then the keyring should not contain a session key

  @story_5
  @story_6
  Scenario: Closing the main window closes the database session
    Given a temporary data directory
    And a clean in-memory keyring
    And the main window is open with an active encrypted database
    When the user closes the main window
    Then the encrypted database is closed and written to disk
    And the keyring should not contain a session key

  @story_5
  Scenario: Database file is created at the given path
    Given a temporary data directory
    When I create a database at that path
    Then a database file should exist at that path

  @story_5
  Scenario: Encrypted database file is not readable as plain SQLite
    Given a temporary data directory
    And an encrypted database for that directory
    When I create and close a new encrypted database with password "SecureP@ssw0rd!2024"
    Then the database file should not contain the SQLite magic bytes

  @story_5
  Scenario: Encrypted database can be reopened with the correct password
    Given a temporary data directory
    And an encrypted database for that directory
    When I create and close a new encrypted database with password "SecureP@ssw0rd!2024"
    And I open the encrypted database with password "SecureP@ssw0rd!2024"
    Then the schema should be accessible through the encrypted database

  @story_5
  Scenario: Opening with wrong password fails
    Given a temporary data directory
    And an encrypted database for that directory
    When I create and close a new encrypted database with password "SecureP@ssw0rd!2024"
    Then opening the encrypted database with "WrongP@ssw0rd!9999" should fail

  @story_5
  Scenario: Tampered database file is rejected
    Given a temporary data directory
    And an encrypted database for that directory
    When I create and close a new encrypted database with password "SecureP@ssw0rd!2024"
    And the database file is tampered with
    Then opening the encrypted database with "SecureP@ssw0rd!2024" should fail

  @story_5
  Scenario: Data written after a mid-session save is persisted
    Given a temporary data directory
    And an encrypted database for that directory
    When I create a new encrypted database with password "SecureP@ssw0rd!2024"
    And I save the encrypted database
    And I write a marker value to the database
    And I close the encrypted database
    And I open the encrypted database with password "SecureP@ssw0rd!2024"
    Then the marker value should be present in the database

  @story_7
  Scenario: App locks when the inactivity timer fires
    Given the main window is open with auto-lock enabled
    When the inactivity timer fires
    Then the lock screen is shown

  @story_7
  Scenario: Lock screen has required elements
    Given the main window is open with auto-lock enabled
    When the inactivity timer fires
    Then the lock screen shows the "OurCRM" branding
    And the lock screen has a password field
    And the lock screen has an "Unlock" button

  @story_7
  Scenario: Unlock with correct password returns to prior section
    Given the main window is open with auto-lock enabled
    And I have navigated to the "Contacts" section
    When the inactivity timer fires
    And I enter the correct password and click "Unlock"
    Then the lock screen is gone
    And the "Contacts" section is shown

  @story_7
  Scenario: Wrong password shows error and keeps the lock screen
    Given the main window is open with auto-lock enabled
    When the inactivity timer fires
    And I enter an incorrect password and click "Unlock"
    Then an error message is shown on the lock screen
    And the lock screen is still shown

  @story_7
  Scenario: Activity resets the inactivity timer
    Given the main window is open with auto-lock enabled
    When I interact with the app
    Then the inactivity timer is reset

  @story_7
  Scenario: No timer runs when auto-lock is set to Never
    Given the main window is open with auto-lock set to Never
    Then the inactivity timer is not running

  @story_8
  Scenario: Change password successfully
    Given the auth service is set up with master password "SecureP@ssw0rd!2024"
    When I change the password from "SecureP@ssw0rd!2024" to "NewP@ssw0rd!2025" confirmed with "NewP@ssw0rd!2025"
    Then the change should succeed
    And logging in with "NewP@ssw0rd!2025" should succeed
    And logging in with "SecureP@ssw0rd!2024" should fail

  @story_8
  Scenario: Current password verification fails
    Given the auth service is set up with master password "SecureP@ssw0rd!2024"
    When I change the password from "WrongCurrentP@ss1!" to "NewP@ssw0rd!2025" confirmed with "NewP@ssw0rd!2025"
    Then the change should fail
    And the change error should be "Incorrect current password"

  @story_8
  Scenario: New password does not meet requirements
    Given the auth service is set up with master password "SecureP@ssw0rd!2024"
    When I change the password from "SecureP@ssw0rd!2024" to "weak" confirmed with "weak"
    Then the change should fail
    And the change error should contain "Password must be at least 12 characters"

  @story_8
  Scenario: New password and confirmation do not match
    Given the auth service is set up with master password "SecureP@ssw0rd!2024"
    When I change the password from "SecureP@ssw0rd!2024" to "NewP@ssw0rd!2025" confirmed with "DifferentP@ss1!"
    Then the change should fail
    And the change error should be "Passwords do not match"

  @story_9
  Scenario: Recover with valid recovery password
    Given the auth service has master password "SecureP@ssw0rd!2024" and recovery password "RecoveryTestP@ssABCDEFGHIJ123456"
    When I recover using "RecoveryTestP@ssABCDEFGHIJ123456" setting new password "NewP@ssw0rd!2025" confirmed with "NewP@ssw0rd!2025"
    Then the recovery should succeed
    And logging in with "NewP@ssw0rd!2025" should succeed
    And logging in with "SecureP@ssw0rd!2024" should fail

  @story_9
  Scenario: Recovery password is case-sensitive
    Given the auth service has master password "SecureP@ssw0rd!2024" and recovery password "RecoveryTestP@ssABCDEFGHIJ123456"
    When I recover using "recoverytestp@ssabcdefghij123456" setting new password "NewP@ssw0rd!2025" confirmed with "NewP@ssw0rd!2025"
    Then the recovery should fail
    And the recovery error should be "Invalid recovery password"

  @story_9
  Scenario: Incorrect recovery password fails without revealing existence
    Given the auth service has master password "SecureP@ssw0rd!2024" and recovery password "RecoveryTestP@ssABCDEFGHIJ123456"
    When I recover using "WrongRecoveryP@ss!ABCDEFGHIJ12345" setting new password "NewP@ssw0rd!2025" confirmed with "NewP@ssw0rd!2025"
    Then the recovery should fail
    And the recovery error should be "Invalid recovery password"

  @story_9
  Scenario: New password must meet requirements
    Given the auth service has master password "SecureP@ssw0rd!2024" and recovery password "RecoveryTestP@ssABCDEFGHIJ123456"
    When I recover using "RecoveryTestP@ssABCDEFGHIJ123456" setting new password "weak" confirmed with "weak"
    Then the recovery should fail
    And the recovery error should contain "Password must be at least 12 characters"

  @story_9
  Scenario: New password and confirmation must match
    Given the auth service has master password "SecureP@ssw0rd!2024" and recovery password "RecoveryTestP@ssABCDEFGHIJ123456"
    When I recover using "RecoveryTestP@ssABCDEFGHIJ123456" setting new password "NewP@ssw0rd!2025" confirmed with "DifferentP@ss1!"
    Then the recovery should fail
    And the recovery error should be "Passwords do not match"

  @story_9
  Scenario: Recovery password can be used multiple times
    Given the auth service has master password "SecureP@ssw0rd!2024" and recovery password "RecoveryTestP@ssABCDEFGHIJ123456"
    When I recover using "RecoveryTestP@ssABCDEFGHIJ123456" setting new password "FirstNewP@ss!2025" confirmed with "FirstNewP@ss!2025"
    When I recover using "RecoveryTestP@ssABCDEFGHIJ123456" setting new password "SecondNewP@ss!2026" confirmed with "SecondNewP@ss!2026"
    Then the recovery should succeed
    And logging in with "SecondNewP@ss!2026" should succeed

  @story_6
  Scenario: Logout via File menu shows login screen
    Given the main window is open and the user is logged in
    When I click File > Logout
    Then the login screen is shown

  @story_6
  Scenario: Logout via toolbar button shows login screen
    Given the main window is open and the user is logged in
    When I click the Logout toolbar button
    Then the login screen is shown

  @story_6
  Scenario: Application remains open after logout
    Given the main window is open and the user is logged in
    When I click File > Logout
    Then the main window is still open
    And the login screen is shown

  @story_6
  Scenario: Session is cleared after logout
    Given the main window is open and the user is logged in
    When I click File > Logout
    Then the auth service shows the user as logged out

  @story_6
  Scenario: Wrong password on login screen shows error and keeps login screen
    Given the main window is open and the user is logged in
    When I click File > Logout
    And I enter an incorrect password on the login screen
    Then an error message is shown on the login screen
    And the login screen is shown

  @story_6
  Scenario: Wrong password on the login screen shows the backoff wait time and disables Login
    Given the main window is open and the user is logged in
    When I click File > Logout
    And I enter an incorrect password on the login screen
    Then an error message is shown on the login screen
    And the login button is disabled

  @story_6
  Scenario: Can log back in after logout
    Given the main window is open and the user is logged in
    When I click File > Logout
    And I enter the correct password on the login screen
    Then the login screen is gone
    And the Dashboard section is active

  @story_6
  Scenario: Logging out closes the encrypted database session
    Given a clean in-memory keyring
    And the main window is open and logged in with an active encrypted database
    When I click File > Logout
    Then the encrypted database is closed
    And the keyring should not contain a session key

  @story_6
  Scenario: Logging back in reopens the encrypted database
    Given a clean in-memory keyring
    And the main window is open and logged in with an active encrypted database
    When I click File > Logout
    And I log back in with the correct password
    Then the encrypted database is open
    And the keyring should contain the session key under "db_session_key"

  @story_6
  Scenario: Keyring failure during account creation shows an error instead of crashing
    Given a temporary data directory
    And the keyring backend raises an error
    And the startup dialog is open in create-password mode for that path
    When the user submits a valid new password and matching confirmation
    Then startup does not complete
    And an error dialog is shown explaining the problem
    And no database file was created

  @story_6
  Scenario: Keyring failure during login shows an error instead of crashing
    Given an existing encrypted database at that path with password "SecureP@ssw0rd!2024"
    And the keyring backend raises an error
    And the startup dialog is open in enter-password mode for that path
    When the user submits the password "SecureP@ssw0rd!2024"
    Then startup does not complete
    And an error dialog is shown explaining the problem

  @story_6
  Scenario: Keyring failure during logout still locks the app instead of crashing
    Given a clean in-memory keyring
    And the main window is open and logged in with an active encrypted database
    And the keyring backend raises an error
    When I click File > Logout
    Then an error dialog is shown explaining the problem
    And the login screen is shown

  @story_3
  Scenario: First launch shows create-password dialog
    Given the startup dialog is open in create mode
    Then the dialog title is "Create Master Password"
    And the submit button is labelled "Create"

  @story_3
  Scenario: First launch detects missing database and shows create-password mode
    Given no database file exists
    When I build the startup dialog for that path
    Then the dialog title is "Create Master Password"
    And the submit button is labelled "Create"

  @story_3
  @story_5
  Scenario: Correct password on first launch creates the database and opens the main window
    Given no database file exists
    And a clean in-memory keyring
    And the startup dialog is open in create-password mode for that path
    When the user submits a valid new password and matching confirmation
    Then startup completes successfully
    And a database file should exist at that path
    And the keyring should contain the session key under "db_session_key"

  @story_3
  Scenario: Closing the startup dialog on first launch exits the application
    Given no database file exists
    And the startup dialog is open in create-password mode for that path
    When the user closes the dialog before submitting
    Then startup does not complete
    And no database file was created

  @story_6
  Scenario: Subsequent launch detects existing database and shows enter-password mode
    Given a database file already exists at that path
    When I build the startup dialog for that path
    Then the dialog title is "Enter Master Password"
    And the submit button is labelled "Open"

  @story_6
  Scenario: Correct password on a subsequent launch opens the database and proceeds
    Given an existing encrypted database at that path with password "SecureP@ssw0rd!2024"
    And the startup dialog is open in enter-password mode for that path
    When the user submits the password "SecureP@ssw0rd!2024"
    Then startup completes successfully

  @story_6
  Scenario: Wrong password on a subsequent launch is rejected and the dialog stays open
    Given an existing encrypted database at that path with password "SecureP@ssw0rd!2024"
    And the startup dialog is open in enter-password mode for that path
    When I type "WrongP@ssw0rd!9999" in the startup password field
    And I click the startup dialog submit button
    Then the startup dialog is not accepted
    And the error label reads "Incorrect password. Please wait 2 seconds before trying again."

  @story_6
  Scenario: Closing the startup dialog on a subsequent launch exits the application
    Given an existing encrypted database at that path with password "SecureP@ssw0rd!2024"
    And the startup dialog is open in enter-password mode for that path
    When the user closes the dialog before submitting
    Then startup does not complete

  @story_3
  Scenario: Submitting matching password and confirmation accepts the dialog
    Given the startup dialog is open in create mode
    When I type "SecureP@ssw0rd!2024" in the startup password field
    And I type "SecureP@ssw0rd!2024" in the startup confirmation field
    And I click the startup dialog submit button
    Then the startup dialog is accepted
    And the submitted password is "SecureP@ssw0rd!2024"

  @story_3
  Scenario: Mismatched confirmation is rejected and the dialog stays open
    Given the startup dialog is open in create mode
    When I type "SecureP@ssw0rd!2024" in the startup password field
    And I type "DifferentP@ss1!" in the startup confirmation field
    And I click the startup dialog submit button
    Then the startup dialog is not accepted
    And the error label reads "Passwords do not match"

  @story_3
  Scenario: An invalid new password is rejected and the dialog stays open
    Given the startup dialog is open in create mode
    When I type "weak" in the startup password field
    And I type "weak" in the startup confirmation field
    And I click the startup dialog submit button
    Then the startup dialog is not accepted
    And the error label reads "Password must be at least 12 characters"

  @story_3
  Scenario: Requirement checklist starts unmet when the create dialog opens
    Given the startup dialog is open in create mode
    Then every requirement label shows as unmet
    And the passwords-match label shows as unmet

  @story_3
  Scenario: Typing a password meeting all requirements turns the checklist to met
    Given the startup dialog is open in create mode
    When I type "SecureP@ssw0rd!2024" in the startup password field
    Then every requirement label shows as met

  @story_3
  Scenario: Typing a matching confirmation turns the passwords-match label to met
    Given the startup dialog is open in create mode
    When I type "SecureP@ssw0rd!2024" in the startup password field
    And I type "SecureP@ssw0rd!2024" in the startup confirmation field
    Then the passwords-match label shows as met

  @story_3
  Scenario: Typing a mismatched confirmation keeps the passwords-match label unmet
    Given the startup dialog is open in create mode
    When I type "SecureP@ssw0rd!2024" in the startup password field
    And I type "DifferentP@ss1!" in the startup confirmation field
    Then the passwords-match label shows as unmet

  @story_3
  Scenario: Clicking Show reveals the password field in plain text
    Given the startup dialog is open in create mode
    When I click the show-password toggle for the password field
    Then the password field echo mode is plain text

  @story_3
  Scenario: Clicking Show again hides the password field
    Given the startup dialog is open in create mode
    When I click the show-password toggle for the password field
    And I click the show-password toggle for the password field
    Then the password field echo mode is masked

