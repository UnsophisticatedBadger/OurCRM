# US-128: Password Recovery Using Recovery Password

## User Story

**As a** user  
**I want to** recover access using my recovery password if I forget my master password  
**So that** I don't lose all my data if I forget my master password

## Priority

**MVP:** Must Have

**Rationale:** Users forget passwords. Without a recovery mechanism, all data would be permanently inaccessible. The recovery password generated during setup (US-012) must actually work to recover access. This is critical for user trust and data safety.

## Estimated Effort

**Size:** Medium (M) - 3-5 days

**Breakdown:**
- 2 hours: Design recovery flow UI
- 3 hours: Implement recovery password verification
- 4 hours: Implement password reset with recovery
- 3 hours: Implement database re-encryption with new password
- 2 hours: Add recovery attempt logging
- 2 hours: Test recovery flow
- 2 hours: Test on all platforms

## Dependencies

**Depends on:** US-010 (Create Master Password), US-012 (Generate Recovery Password), US-014 (Create Encrypted Database)

**Blocks:** None

## Description

When a user forgets their master password, they should be able to use the recovery password (generated during setup) to regain access. The recovery process:
1. User clicks "Forgot Password?" on login screen
2. User enters the recovery password
3. System verifies the recovery password
4. User creates a new master password
5. Database is re-encrypted with new password
6. User can log in with new password

The recovery password is stored as a hash (not plain text) and is separate from the master password. It should only be usable for recovery, not for normal login.

## BDD Scenarios

### Scenario 1: Recover with valid recovery password

Given I have forgotten my master password And I am on the login screen When I click "Forgot Password?" And I enter my recovery password And I enter a new master password And I confirm the new password And I click "Reset Password" Then the password should be reset And the database should be re-encrypted And I should be able to log in with the new password And I should see a success message


### Scenario 2: Recovery password is case-sensitive

Given I am recovering my password When I enter the recovery password with wrong case Then I should see an error message And the recovery should fail


### Scenario 3: Invalid recovery password

Given I am on the recovery screen When I enter an incorrect recovery password And I click "Reset Password" Then I should see an error message And the error should not reveal if password exists And I should be able to try again


### Scenario 4: New password must meet requirements

Given I am recovering my password When I enter a new password that doesn't meet requirements And I click "Reset Password" Then I should see validation errors And the password should not be reset


### Scenario 5: Recovery attempt is logged

Given I attempt password recovery When I submit a recovery attempt Then the attempt should be logged And the timestamp should be recorded And success/failure should be recorded


### Scenario 6: Can recover multiple times

Given I have recovered my password once When I forget the new password And I use the recovery password again Then I should be able to recover again And the recovery password should still work


### Scenario 7: Recovery requires new password confirmation

Given I am recovering my password When I enter a new password And enter a different confirmation And I click "Reset Password" Then I should see an error And the passwords must match to proceed


## Manual Testing Steps

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

## Acceptance Criteria

- [ ] "Forgot Password?" link on login screen
- [ ] Recovery password verification works
- [ ] Recovery password is case-sensitive
- [ ] New password must meet all requirements
- [ ] New password must be confirmed
- [ ] Database is re-encrypted with new password
- [ ] User can log in with new password immediately
- [ ] All data remains accessible after recovery
- [ ] Recovery attempts are logged
- [ ] Recovery password can be used multiple times
- [ ] Error messages don't reveal if recovery password exists
- [ ] Recovery flow is secure and atomic
- [ ] Works on Windows, macOS, and Linux
- [ ] Clear instructions throughout the flow