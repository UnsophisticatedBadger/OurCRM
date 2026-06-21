# Manual Tests: Authentication

## Create Master Password — US-010

### Test 1: Test password validation

1. Open the setup wizard
2. Try to enter a password with 8 characters
3. Verify the error message appears
4. Try a password with 12 characters but no numbers
5. Verify the error message appears
6. Try a password that meets all requirements
7. Verify it passes validation

### Test 2: Test password strength meter

1. Enter a weak password (e.g., "password")
2. Verify the strength meter shows "Weak"
3. Enter a medium password (e.g., "MyPassword123")
4. Verify the strength meter shows "Medium"
5. Enter a strong password (e.g., "MyP@ssw0rd!2024")
6. Verify the strength meter shows "Strong"
7. Verify the meter updates in real-time as you type

### Test 3: Test password confirmation

1. Enter a password
2. Enter a different password in the confirmation field
3. Verify the error message appears
4. Enter the same password in both fields
5. Verify the error disappears
6. Verify the "Create" button is enabled

### Test 4: Test password hashing

1. Create a password during setup
2. Complete the setup
3. Check the OS keyring to verify the hash is stored
4. Verify the hash starts with "$argon2id$"
5. Verify the original password is not stored anywhere
6. Verify the hash cannot be reversed to get the password

### Test 5: Test verification time

1. Create a password
2. Try to log in with the correct password
3. Measure how long verification takes
4. Verify it takes approximately 2 seconds
5. Try with an incorrect password
6. Verify it also takes approximately 2 seconds (prevents timing attacks)

### Test 6: Test on all platforms

1. Create a password on Windows
2. Verify it works
3. Create a password on macOS
4. Verify it works
5. Create a password on Linux
6. Verify it works
7. Document any platform-specific issues

### Test 7: Test password requirements are clear

1. Read the setup wizard instructions
2. Verify the requirements are clearly stated
3. Verify examples are provided
4. Verify the UI is intuitive
5. Get feedback from a test user

---

## Log In with Master Password — US-011

### Test 1: Test successful login

1. Start OurCRM
2. Enter the correct master password
3. Verify the application opens
4. Verify the main window appears
5. Verify you can access your data
6. Close the application

### Test 2: Test failed login

1. Start OurCRM
2. Enter an incorrect password
3. Verify the error message appears
4. Verify you cannot access the application
5. Check the log file to verify the failed attempt was logged
6. Close the application

### Test 3: Test exponential backoff

1. Start OurCRM
2. Enter an incorrect password
3. Try to log in again immediately
4. Verify you must wait 2 seconds
5. Try again with wrong password
6. Verify you must wait 4 seconds
7. Try again with wrong password
8. Verify you must wait 8 seconds
9. Document the wait times

### Test 4: Test login after wait period

1. Fail to log in 3 times
2. Wait the required time
3. Enter the correct password
4. Verify you can log in
5. Verify the failure count is reset

### Test 5: Test empty password

1. Start OurCRM
2. Leave the password field empty
3. Click "Log In"
4. Verify the error message appears
5. Verify the login is not attempted
6. Enter a password and try again
7. Verify it works normally

### Test 6: Test password field security

1. Start OurCRM
2. Look at the password field
3. Verify the password is masked (shows dots or asterisks)
4. Verify the password is not visible in the UI
5. Verify you cannot copy the password from the field
6. Check that the password is not logged anywhere

### Test 7: Test verification time

1. Start OurCRM
2. Enter your password
3. Time how long the verification takes
4. Verify it takes approximately 2 seconds
5. Try with a wrong password
6. Verify it also takes approximately 2 seconds
7. Document the actual times

### Test 8: Test on all platforms

1. Test login on Windows
2. Verify it works
3. Test login on macOS
4. Verify it works
5. Test login on Linux
6. Verify it works
7. Document any platform-specific issues

---

## Generate Recovery Password — US-012

### Test 1: Verify password generation

1. Start the setup wizard
2. Create a master password
3. Proceed to the recovery password step
4. Verify a password is displayed
5. Verify the password is 32 characters (not counting dashes)
6. Verify it contains a mix of character types
7. Verify it excludes ambiguous characters (0, O, I, l, 1)
8. Verify the formatting with dashes makes it readable

### Test 2: Test clipboard functionality

1. View the recovery password
2. Click "Copy to Clipboard"
3. Open a text editor
4. Paste the content
5. Verify the password was copied correctly
6. Verify there are no extra characters or formatting

### Test 3: Verify password is shown only once

1. Complete the setup wizard
2. Try to find the recovery password in the application
3. Verify you cannot view it again
4. Check that it's not stored in the database in plain text
5. Verify it's not in the log files

### Test 4: Test multiple generations

1. Start the setup wizard
2. Create a master password
3. Go back and regenerate the recovery password
4. Verify the new password is different
5. Repeat several times
6. Verify all passwords are unique
7. Verify there are no patterns

### Test 5: Verify character set

1. Generate several recovery passwords
2. Check each one for ambiguous characters
3. Verify no password contains: 0, O, I, l, 1
4. Verify each password has a good mix of:
   - Uppercase letters
   - Lowercase letters
   - Numbers
   - Special characters

### Test 6: Test readability

1. Generate a recovery password
2. Try to read it aloud to someone
3. Verify the formatting with dashes makes it easy to read
4. Try to write it down from the screen
5. Verify the formatting helps prevent errors
6. Get feedback from a test user

### Test 7: Test on all platforms

1. Test recovery password generation on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

---

## Confirm Recovery Password Saved — US-013

### Test 1: Test full confirmation flow

1. Complete the recovery password display
2. Check the first checkbox
3. Verify the Continue button is still disabled
4. Check the second checkbox
5. Verify the Continue button is still disabled
6. Type "CONFIRM" in the confirmation field
7. Verify the Continue button is now enabled
8. Click Continue
9. Verify setup proceeds to the next step

### Test 2: Test that confirmation is required

1. Try to proceed without checking the first checkbox
2. Verify the Continue button is disabled
3. Try to proceed without checking the second checkbox
4. Verify the Continue button is disabled
5. Try to proceed without typing CONFIRM
6. Verify the Continue button is disabled

### Test 3: Test exact text match

1. Check both checkboxes
2. Type "confirm" (lowercase)
3. Verify the Continue button is disabled
4. Type "Confirm" (mixed case)
5. Verify the Continue button is disabled
6. Type "CONFIRM" (uppercase)
7. Verify the Continue button is enabled
8. Type "CONFIRM " (with trailing space)
9. Verify the Continue button is disabled

### Test 4: Test cancellation

1. View the recovery password
2. Click "Cancel"
3. Verify the setup is cancelled
4. Verify no database was created
5. Verify no settings were saved
6. Restart the application
7. Verify it starts from the beginning of setup

### Test 5: Test visual prominence

1. View the confirmation screen
2. Check that warnings are visually prominent
3. Verify the text is large enough to read
4. Verify warning colors are used (red, orange, or yellow)
5. Verify warning icons are present
6. Get feedback from a test user about whether they understood the importance

### Test 6: Test with a test user

1. Have someone unfamiliar with OurCRM go through setup
2. Watch them interact with the confirmation screen
3. Verify they understand they need to save the password
4. Verify they don't just click through
5. Verify they understand the consequences
6. Get feedback on the UI design

### Test 7: Test on all platforms

1. Test the confirmation flow on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

---

## Create Encrypted Database — US-014

### Test 1: Verify database is created

1. Complete the setup wizard
2. Navigate to the data directory (e.g., ~/ourcrm/ on Unix)
3. Verify the database file exists
4. Check the file size (should be reasonable, not suspiciously small or huge)
5. Verify the file has appropriate permissions

### Test 2: Verify database is encrypted

1. Open the database file with a text editor
2. Verify you see only binary/encrypted data
3. Try to search for readable text (names, emails, etc.)
4. Verify no readable data is found
5. Try to open the database with a SQLite browser tool
6. Verify the tool reports the database is encrypted

### Test 3: Verify database opens with password

1. Start OurCRM
2. Enter the correct master password
3. Verify the application opens
4. Verify you can create a contact
5. Verify the contact is saved
6. Close the application
7. Restart and log in again
8. Verify the contact is still there

### Test 4: Test wrong password cannot open database

1. Start OurCRM
2. Enter an incorrect password
3. Verify the login fails
4. Try to access the database file directly
5. Verify the file is unreadable without the correct password

### Test 5: Verify OS keyring storage

1. Log in to OurCRM
2. Open the OS keyring manager (Keychain on macOS, Credential Manager on Windows, etc.)
3. Verify the OurCRM entry is present
4. Verify it contains the encryption key
5. Log out
6. Verify the keyring entry is removed

### Test 6: Test database performance

1. Log in to OurCRM
2. Create 100 contacts
3. Measure how long operations take
4. Verify the encryption doesn't significantly slow down the app
5. Document the performance impact

### Test 7: Test database backup

1. Log in to OurCRM
2. Create a backup
3. Verify the backup file is also encrypted
4. Try to read the backup file
5. Verify it's encrypted

### Test 8: Test on all platforms

1. Test database creation on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

---

## Change Master Password — US-127

### Test 1: Change password successfully

1. Log in to OurCRM
2. Go to Security settings
3. Click "Change Master Password"
4. Enter current password
5. Enter new password (meeting all requirements)
6. Confirm new password
7. Click "Change Password"
8. Verify success message
9. Close the application
10. Log in with new password
11. Verify it works

### Test 2: Test current password verification

1. Go to change password
2. Enter wrong current password
3. Enter new password
4. Click "Change Password"
5. Verify error message
6. Verify password not changed

### Test 3: Test new password validation

1. Go to change password
2. Enter current password
3. Enter weak new password (e.g., "password")
4. Verify validation errors appear
5. Verify specific requirements are listed

### Test 4: Test password mismatch

1. Go to change password
2. Enter current password
3. Enter new password
4. Enter different confirmation
5. Verify error message
6. Verify "Passwords do not match"

### Test 5: Test database re-encryption

1. Change password successfully
2. Create a new contact
3. Close the application
4. Log in with new password
5. Verify the contact is there
6. Verify all data is accessible
7. Verify database is not corrupted

### Test 6: Test old password doesn't work

1. Change password
2. Close application
3. Try to log in with old password
4. Verify it fails
5. Log in with new password
6. Verify it works

### Test 7: Test recovery still works

1. Change password
2. Log out
3. Use recovery password to recover
4. Verify you can set a new password
5. Verify access is restored

### Test 8: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

---

## Password Recovery Using Recovery Password — US-128

### Test 1: Recover with valid recovery password

1. Log out of OurCRM
2. On login screen, click "Forgot Password?"
3. Enter the recovery password from setup
4. Enter a new master password (meeting requirements)
5. Confirm the new password
6. Click "Reset Password"
7. Verify success message
8. Log in with new password
9. Verify all data is accessible

### Test 2: Test invalid recovery password

1. Click "Forgot Password?"
2. Enter wrong recovery password
3. Verify error message
4. Verify you can try again
5. Enter correct recovery password
6. Verify it works

### Test 3: Test case sensitivity

1. Click "Forgot Password?"
2. Enter recovery password with wrong case
3. Verify it fails
4. Enter with correct case
5. Verify it works

### Test 4: Test new password validation

1. Start recovery
2. Enter weak new password
3. Verify validation errors
4. Enter valid password
5. Verify you can proceed

### Test 5: Test data integrity after recovery

1. Create several contacts before forgetting password
2. Recover password
3. Log in with new password
4. Verify all contacts are there
5. Verify all data is intact
6. Verify database is not corrupted

### Test 6: Test recovery logging

1. Attempt recovery with wrong password
2. Check logs
3. Verify attempt is logged
4. Attempt with correct password
5. Verify success is logged

### Test 7: Test multiple recoveries

1. Recover password
2. Log in
3. Log out
4. Recover again
5. Verify it still works
6. Verify recovery password hasn't expired

### Test 8: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

---

## Logout — US-129

### Memory clearing after logout

Automated tests verify `is_logged_in` state is cleared. This test checks the underlying memory.

1. Log in to OurCRM
2. Log out via File > Logout or toolbar button
3. Inspect process memory (e.g. via a debugger or memory profiler)
4. Verify encryption keys are not present in memory
5. Verify cached contact/lead data is cleared

### Cross-platform logout/login cycle

1. On Windows: log in → log out → log back in. Verify toolbar and File menu both work.
2. On macOS: repeat the same cycle. Note any platform-specific menu bar differences.
3. On Linux: repeat the same cycle.
4. Document any platform-specific issues found.
