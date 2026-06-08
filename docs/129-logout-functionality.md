# US-129: Logout Functionality

## User Story

**As a** user  
**I want to** log out of the application  
**So that** I can securely end my session when using a shared computer or stepping away

## Priority

**MVP:** Must Have

**Rationale:** Logout is a basic security feature. Users need to be able to end their session and lock the application, especially when using shared computers or in office environments. Without logout, the only option is to close the app entirely.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design logout UI (menu item, button)
- 2 hours: Implement logout functionality
- 1 hour: Clear sensitive data from memory
- 1 hour: Return to login screen
- 1 hour: Clear encryption keys from memory
- 1 hour: Test logout flow
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-011 (Log In with Master Password), US-014 (Create Encrypted Database)

**Blocks:** None

## Description

Users should be able to log out from the application through a menu item (File > Logout) or a logout button. When logging out:
1. Encryption keys are cleared from memory
2. The application returns to the login screen
3. The database is locked
4. No data is accessible without re-authentication

The application remains open (doesn't exit), but requires re-authentication to access data. This is different from closing the app.

## BDD Scenarios

### Scenario 1: Logout from menu

Given I am logged in to OurCRM When I click File > Logout Then I should be returned to the login screen And the encryption keys should be cleared from memory And the database should be locked And no data should be accessible


### Scenario 2: Logout from button

Given I am logged in to OurCRM When I click the Logout button (if available) Then I should be returned to the login screen And I should need to enter my password to access data again


### Scenario 3: Cannot access data after logout

Given I have logged out When I try to access contacts or other data Then I should be prompted to log in first And no data should be visible


### Scenario 4: Application remains open after logout

Given I am logged in When I log out Then the application should remain open And show the login screen And not exit completely


### Scenario 5: Sensitive data cleared from memory

Given I am logged in When I log out Then encryption keys should be cleared from memory And cached data should be cleared And session data should be cleared


### Scenario 6: Can log back in after logout

Given I have logged out When I enter my correct master password Then I should be able to log in successfully And all my data should be accessible again


### Scenario 7: Unsaved changes warning before logout

Given I am editing a contact And I have unsaved changes When I try to log out Then I should be warned about unsaved changes And I can choose to save, discard, or cancel logout


## Manual Testing Steps

### Test 1: Logout from menu

1. Log in to OurCRM
2. Click File > Logout
3. Verify you're returned to login screen
4. Verify the window didn't close
5. Try to access data
6. Verify you must log in first

### Test 2: Test data is inaccessible

1. Log in and view some contacts
2. Log out
3. Try to view contacts without logging in
4. Verify no data is visible
5. Verify database is locked

### Test 3: Test log back in

1. Log out
2. Enter correct password
3. Verify you can log in
4. Verify all data is accessible
5. Verify you're back where you were

### Test 4: Test unsaved changes warning

1. Edit a contact but don't save
2. Try to log out
3. Verify warning appears
4. Test "Save" option
5. Test "Discard" option
6. Test "Cancel" option

### Test 5: Test memory clearing

1. Log in
2. Log out
3. Check memory (if possible)
4. Verify keys are cleared
5. Verify cached data is cleared

### Test 6: Test multiple logout/login cycles

1. Log in
2. Log out
3. Log in again
4. Log out again
5. Log in again
6. Verify it works each time
7. Verify no degradation

### Test 7: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Logout option in File menu
- [ ] Logout button available (optional)
- [ ] Returns to login screen (doesn't exit)
- [ ] Encryption keys cleared from memory
- [ ] Database locked after logout
- [ ] No data accessible without re-authentication
- [ ] Can log back in successfully
- [ ] Unsaved changes warning before logout
- [ ] Session data cleared on logout
- [ ] Works on Windows, macOS, and Linux
- [ ] Logout is immediate
- [ ] No way to bypass login after logout