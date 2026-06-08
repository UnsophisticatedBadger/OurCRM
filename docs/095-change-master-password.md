# US-095: Change Master Password

## User Story

**As a** user  
**I want to** change my master password  
**So that** I can update it periodically for security or if I suspect it's compromised

## Priority

**MVP:** Must Have

**Rationale:** Passwords should be changed periodically for security best practices. Users also need to change passwords if they suspect compromise. Without this capability, users would be stuck with the same password indefinitely.

## Estimated Effort

**Size:** Medium (M) - 3 days

**Breakdown:**
- 1 hour: Design password change UI
- 1 hour: Create change password form
- 2 hours: Implement password verification (current password)
- 2 hours: Re-encrypt database with new key
- 1 hour: Update password hash in keyring
- 1 hour: Test password change flow
- 1 hour: Test re-encryption
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-010 (Create Master Password), US-019 (Configure Security Settings)

**Blocks:** US-096 (Password Recovery Flow)

## Description

Users should be able to change their master password through a secure process that requires entering the current password and a new password. The change process should re-encrypt the database with the new key derived from the new password, ensuring that all data remains accessible with the new password.

The system should validate the current password, enforce the same password requirements as during setup (12+ characters, complexity rules), and provide clear feedback throughout the process. The new password should be verified by asking the user to type it twice.

## BDD Scenarios

### Scenario 1: Open change password dialog

```
Given I am logged in and in Security settings
When I click "Change Master Password"
Then a dialog should appear asking for:
  - Current master password
  - New master password
  - Confirm new master password
```

### Scenario 2: Verify current password

```
Given the change password dialog is open
When I enter my current password
  And I click "Continue"
Then the system should verify the current password
  And proceed if correct
  Or show an error if incorrect
```

### Scenario 3: Enter new password

```
Given the current password has been verified
When I enter a new password that meets requirements
  And I confirm the new password
  And I click "Change Password"
Then the system should:
  - Validate the new password meets requirements
  - Verify both entries match
  - Re-encrypt the database with the new key
  - Update the password hash in the keyring
```

### Scenario 4: New password validation

```
Given I am entering a new password
When I enter a password that doesn't meet requirements
  (too short, missing characters, etc.)
Then I should see validation errors
  And the password should not be accepted
```

### Scenario 5: Passwords don't match

```
Given I am entering a new password
When I enter different passwords in the two fields
Then I should see an error "Passwords do not match"
  And the password should not be changed
```

### Scenario 6: Re-encryption progress

```
Given I have entered a valid new password
When the system is re-encrypting the database
Then I should see a progress indicator
  Warning not to close the app
  And the process should take a reasonable time
```

### Scenario 7: Password change success

```
Given the password has been changed successfully
When the process completes
Then I should see a success message
  And I should be logged out
  And I need to log in with the new password
```

### Scenario 8: Log in with new password

```
Given I have changed my master password
When I try to log in with the new password
Then login should be successful
  And all my data should be accessible
  And the old password should no longer work
```

## Manual Testing Steps

### Test 1: Open change password

1. Go to Security settings
2. Click "Change Master Password"
3. Verify the dialog appears
4. Verify all required fields are present

### Test 2: Test current password verification

1. Open the change password dialog
2. Enter the wrong current password
3. Try to continue
4. Verify the error
5. Enter the correct current password
6. Verify it proceeds

### Test 3: Change password successfully

1. Open the change password dialog
2. Enter the correct current password
3. Enter a new valid password
4. Confirm the new password
5. Click "Change Password"
6. Verify the re-encryption happens
7. Verify the success message
8. Log in with the new password
9. Verify it works

### Test 4: Test password requirements

1. Try to change to a password that's too short
2. Verify the error
3. Try without uppercase
4. Verify the error
5. Try without numbers
6. Verify the error
7. Try a valid password
8. Verify it works

### Test 5: Test password mismatch

1. Enter a new password
2. Enter a different password in confirm field
3. Try to change
4. Verify the error
5. Correct the confirmation
6. Verify it works

### Test 6: Test re-encryption

1. Change the password
2. Verify the re-encryption progress is shown
3. Verify the app doesn't close
4. Wait for completion
5. Verify the time is reasonable

### Test 7: Verify old password doesn't work

1. Change the password
2. Try to log in with the old password
3. Verify it fails
4. Log in with the new password
5. Verify it works

### Test 8: Test data accessibility

1. Change the password
2. Log in with the new password
3. Verify all contacts are there
4. Verify all leads are there
5. Verify all data is intact
6. Verify nothing is lost

### Test 9: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] "Change Master Password" is accessible from settings
- [ ] Current password is required and verified
- [ ] New password must meet requirements (12+ chars, complexity)
- [ ] New password must be entered twice for confirmation
- [ ] Database is re-encrypted with new key
- [ ] Password hash is updated in keyring
- [ ] Progress indicator shows during re-encryption
- [ ] Success message is displayed
- [ ] User is logged out after change
- [ ] New password works for login
- [ ] Old password no longer works
- [ ] All data remains accessible
- [ ] No data loss during re-encryption
- [ ] Works on Windows, macOS, and Linux
- [ ] Process is secure and reliable
