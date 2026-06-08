# US-127: Change Master Password

## User Story

**As a** user  
**I want to** change my master password  
**So that** I can update my credentials if I suspect compromise or want to improve security

## Priority

**MVP:** Must Have

**Rationale:** Users need the ability to change their master password for security reasons. This is a standard security feature expected in any application handling sensitive data. Without this, users are stuck with their initial password forever.

## Estimated Effort

**Size:** Medium (M) - 3-5 days

**Breakdown:**
- 2 hours: Design password change UI
- 3 hours: Implement password change form with validation
- 4 hours: Implement database re-encryption with new password
- 2 hours: Implement key derivation with new password
- 2 hours: Update OS keyring with new hash
- 2 hours: Test password change flow
- 2 hours: Test database re-encryption
- 2 hours: Test on all platforms

## Dependencies

**Depends on:** US-010 (Create Master Password), US-014 (Create Encrypted Database)

**Blocks:** None

## Description

Users should be able to change their master password from the Security settings. The process requires:
1. Entering the current password (verification)
2. Entering a new password (meeting all complexity requirements)
3. Confirming the new password
4. Re-encrypting the database with the new password
5. Updating the stored hash in the OS keyring

The database must be re-encrypted because the encryption key is derived from the master password. This is a sensitive operation that should be atomic (all or nothing) to prevent data corruption.

## BDD Scenarios

### Scenario 1: Change password successfully

Given I am logged in to OurCRM And I am in Security settings When I click "Change Master Password" And I enter my current password And I enter a new valid password And I confirm the new password And I click "Change Password" Then the password should be changed And the database should be re-encrypted And the new hash should be stored in the OS keyring And I should see a success message


### Scenario 2: Current password verification fails

Given I am changing my master password When I enter an incorrect current password And I click "Change Password" Then I should see an error message And the password should not be changed And the database should not be re-encrypted


### Scenario 3: New password doesn't meet requirements

Given I am changing my master password When I enter a new password that doesn't meet complexity requirements And I click "Change Password" Then I should see validation errors And the password should not be changed And specific requirements should be listed


### Scenario 4: New password and confirmation don't match

Given I am changing my master password When I enter a new password And I enter a different password in the confirmation field And I click "Change Password" Then I should see an error message And the error should say "Passwords do not match" And the password should not be changed


### Scenario 5: Database re-encryption is atomic

Given I am changing my master password When the re-encryption process starts And an error occurs mid-process Then the database should remain in its original state And I should be able to try again And no data should be corrupted


### Scenario 6: Must log in with new password

Given I have changed my master password When I close the application And I try to log in Then I should use the new password And the old password should not work


### Scenario 7: Recovery password still works

Given I have changed my master password When I forget the new password And I use the recovery password Then I should be able to recover access And the recovery password should still work


## Manual Testing Steps

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

## Acceptance Criteria

- [ ] "Change Master Password" option is in Security settings
- [ ] Current password must be verified first
- [ ] New password must meet all complexity requirements
- [ ] New password must be confirmed
- [ ] Database is re-encrypted with new password
- [ ] New hash is stored in OS keyring
- [ ] Old password no longer works
- [ ] New password works immediately
- [ ] Recovery password still works after change
- [ ] Re-encryption is atomic (no corruption on failure)
- [ ] Success message shown after change
- [ ] Error messages are clear and helpful
- [ ] Works on Windows, macOS, and Linux
- [ ] All data remains accessible after change