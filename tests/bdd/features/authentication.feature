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

  @story_6
  Scenario: Successful login with correct password
    Given the auth service is set up with a stored master password "SecureP@ssw0rd!2024"
    When I attempt to log in with "SecureP@ssw0rd!2024"
    Then the login should succeed
    And the failure count should be reset to 0

  @story_6
  Scenario: Failed login with wrong password
    Given the auth service is set up with a stored master password "SecureP@ssw0rd!2024"
    When I attempt to log in with "WrongPassword1!"
    Then the login should fail
    And the error should be "Incorrect password"

  @story_6
  Scenario: Empty password is rejected
    Given the auth service is set up with a stored master password "SecureP@ssw0rd!2024"
    When I attempt to log in with ""
    Then the login should fail
    And the error should be "Password is required"

  @story_6
  Scenario: Backoff after first failure
    Given the auth service is set up with a stored master password "SecureP@ssw0rd!2024"
    When I attempt to log in with "WrongPassword1!"
    Then the required wait should be 2 seconds

  @story_6
  Scenario: Backoff doubles after each failure
    Given the auth service is set up with a stored master password "SecureP@ssw0rd!2024"
    When I fail to log in 3 times
    Then the required wait should be 8 seconds

  @story_6
  Scenario: Successful login resets failure count
    Given the auth service is set up with a stored master password "SecureP@ssw0rd!2024"
    When I fail to log in 2 times
    And I attempt to log in with "SecureP@ssw0rd!2024"
    Then the login should succeed
    And the required wait should be 0 seconds

  @story_4
  Scenario: Generated password is 32 characters long
    Given the recovery password generator is available
    When I generate a recovery password
    Then the raw password should be exactly 32 characters

  @story_4
  Scenario: Generated password excludes ambiguous characters
    Given the recovery password generator is available
    When I generate a recovery password
    Then the raw password should not contain any of "0OIl1"

  @story_4
  Scenario: Generated password contains only allowed characters
    Given the recovery password generator is available
    When I generate a recovery password
    Then every character should be from the allowed character set

  @story_4
  Scenario: Multiple generations produce unique passwords
    Given the recovery password generator is available
    When I generate two recovery passwords
    Then the two passwords should be different

  @story_4
  Scenario: Formatted password has dashes every 5 characters
    Given the recovery password generator is available
    When I generate and format a recovery password
    Then each group separated by dashes should have at most 5 characters

  @story_4
  Scenario: Formatted password round-trips back to the raw password
    Given the recovery password generator is available
    When I generate and format a recovery password
    Then removing the dashes should give back the raw password

  @story_4
  Scenario: Can proceed when both checkboxes checked and CONFIRM typed
    Given a recovery confirmation
    When I check the first checkbox
    And I check the second checkbox
    And I type "CONFIRM" in the confirmation field
    Then I should be able to proceed

  @story_4
  Scenario: Cannot proceed without first checkbox
    Given a recovery confirmation
    When I check the second checkbox
    And I type "CONFIRM" in the confirmation field
    Then I should not be able to proceed

  @story_4
  Scenario: Cannot proceed without second checkbox
    Given a recovery confirmation
    When I check the first checkbox
    And I type "CONFIRM" in the confirmation field
    Then I should not be able to proceed

  @story_4
  Scenario: Cannot proceed without typing CONFIRM
    Given a recovery confirmation
    When I check the first checkbox
    And I check the second checkbox
    Then I should not be able to proceed

  @story_4
  Scenario Outline: Cannot proceed with incorrect confirmation text
    Given a recovery confirmation
    When I check the first checkbox
    And I check the second checkbox
    And I type "<text>" in the confirmation field
    Then I should not be able to proceed

    Examples:
      | text     |
      | confirm  |
      | Confirm  |
      | CONFIRM! |
      | confirm! |

  @story_4
  Scenario: Fresh confirmation state does not allow proceeding
    Given a recovery confirmation
    Then I should not be able to proceed

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
  Scenario: Can log back in after logout
    Given the main window is open and the user is logged in
    When I click File > Logout
    And I enter the correct password on the login screen
    Then the login screen is gone
    And the Dashboard section is active

  @story_3
  Scenario: First launch shows create-password dialog
    Given the startup dialog is open in create mode
    Then the dialog title is "Create Master Password"
    And the submit button is labelled "Create"

  @story_6
  Scenario: Returning launch shows enter-password dialog
    Given the startup dialog is open in open mode
    Then the dialog title is "Enter Master Password"
    And the submit button is labelled "Open"

  @story_3
  Scenario: Submitting a password accepts the dialog
    Given the startup dialog is open in create mode
    When I type "s3cr3t!" in the startup password field
    And I click the startup dialog submit button
    Then the startup dialog is accepted
    And the submitted password is "s3cr3t!"

  @story_6
  Scenario: Closing the startup dialog rejects it
    Given the startup dialog is open in open mode
    When I close the startup dialog
    Then the startup dialog is rejected

  @story_6
  Scenario: show_error displays an inline error message
    Given the startup dialog is open in open mode
    When show_error is called with "Incorrect password. Please try again."
    Then the error label reads "Incorrect password. Please try again."
