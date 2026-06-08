# US-011: Log In with Master Password

## User Story

**As a** user  
**I want to** log in with my master password  
**So that** I can access my encrypted data

## Priority

**MVP:** Must Have

**Rationale:** Every time the user starts OurCRM, they need to authenticate to unlock the encrypted database. This is the primary authentication mechanism.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 2 hours: Create login UI
- 2 hours: Implement password verification with Argon2id
- 1 hour: Implement exponential backoff for failed attempts
- 2 hours: Create Result objects for authentication outcomes
- 2 hours: Write tests for login flow
- 2 hours: Test cross-platform behavior
- 1 hour: Add logging for login attempts

## Dependencies

**Depends on:** US-010 (Create Master Password), US-014 (Encrypted Database)

**Blocks:** US-002 (Run Application - requires authentication), all user features

## Description

When a user starts OurCRM, they should be prompted to enter their master password. The password is verified using Argon2id, which takes approximately 2 seconds. If the password is correct, the encrypted database is unlocked and the user can access their data. If incorrect, the user must wait an increasing amount of time before trying again (exponential backoff).

The login screen should be simple and clear, with a password field and a submit button. Failed attempts should be logged for security purposes. After successful login, the user should see the main application window.

## BDD Scenarios

### Scenario 1: Successful login

```
Given I have created a master password
  And I have started OurCRM
  And I am on the login screen
When I enter my correct master password
  And I click "Log In"
Then the password should be verified
  And the encrypted database should be unlocked
  And the main application window should open
  And the login attempt should be logged as successful
```

### Scenario 2: Failed login with wrong password

```
Given I am on the login screen
When I enter an incorrect password
  And I click "Log In"
Then the password verification should fail
  And I should see an error message "Incorrect password"
  And I should not be able to access the application
  And the failed attempt should be logged
```

### Scenario 3: Exponential backoff after first failure

```
Given I have failed to log in once
When I try to log in again
Then I should be required to wait 2 seconds before the next attempt
```

### Scenario 4: Exponential backoff after multiple failures

```
Given I have failed to log in 3 times
When I try to log in again
Then I should be required to wait 8 seconds before the next attempt
```

### Scenario 5: Successful login after failures

```
Given I have failed to log in several times
  And the wait time has passed
When I enter my correct password
Then I should be able to log in successfully
  And the failure count should be reset
```

### Scenario 6: Empty password rejected

```
Given I am on the login screen
When I leave the password field empty
  And I click "Log In"
Then I should see an error message
  And the error should say "Password is required"
```

### Scenario 7: Password verification takes approximately 2 seconds

```
Given I am on the login screen
When I enter my password and click "Log In"
Then the verification should take approximately 2 seconds
  And I should see a "Verifying..." indicator during this time
```

## Manual Testing Steps

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

## Acceptance Criteria

- [ ] User can log in with correct master password
- [ ] Incorrect password shows clear error message
- [ ] Failed login attempts trigger exponential backoff
- [ ] Wait time doubles after each failure (2s, 4s, 8s, 16s, etc.)
- [ ] Successful login resets the failure count
- [ ] Password field masks the input
- [ ] Password is not stored or logged in plain text
- [ ] Verification takes approximately 2 seconds
- [ ] Login attempt is logged (success or failure)
- [ ] Works on Windows, macOS, and Linux
- [ ] Clear UI with password field and submit button
- [ ] Cannot proceed with empty password
- [ ] Database is unlocked after successful login