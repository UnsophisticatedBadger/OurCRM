# US-096: Password Recovery Flow

## User Story

**As a** user  
**I want to** recover access to my data using my master recovery password  
**So that** I can regain access if I forget my master password

## Priority

**MVP:** Must Have

**Rationale:** Users forget passwords. Without a recovery mechanism, all data would be permanently inaccessible. The master recovery password is the safety net that prevents catastrophic data loss. This is critical for user trust and data protection.

## Estimated Effort

**Size:** Medium (M) - 3 days

**Breakdown:**
- 1 hour: Design recovery flow UI
- 1 hour: Create recovery initiation screen
- 1 hour: Implement master recovery password validation
- 2 hours: Re-encrypt database with new master password
- 1 hour: Update encryption key in keyring
- 1 hour: Add recovery confirmation
- 1 hour: Test recovery flow
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-010 (Create Master Password), US-012 (Generate Recovery Password)

**Blocks:** None

## Description

Users should be able to recover access to their data if they forget their master password by using the master recovery password they saved during setup. The recovery process should:

1. Prompt for the master recovery password
2. Validate it against the stored encrypted database key
3. Allow the user to set a new master password
4. Re-encrypt the database with the new master password's derived key
5. Update the encrypted database key in the keyring (encrypted with the new master password)
6. Log the user in with the new master password

The recovery flow should be secure, clear, and provide feedback throughout the process. It should be the ONLY way to access data without the current master password.

## BDD Scenarios

### Scenario 1: Initiate recovery

```
Given I am at the login screen
  And I don't remember my master password
When I click "Forgot Password" or "Recover Access"
Then the recovery flow should start
  And I should be prompted for my master recovery password
```

### Scenario 2: Enter master recovery password

```
Given the recovery flow has started
When I enter my master recovery password
  And I click "Verify"
Then the system should:
  - Decrypt the stored database encryption key
  - Verify it works on the database
  And proceed if successful
  Or show an error if invalid
```

### Scenario 3: Incorrect recovery password

```
Given the recovery flow is active
When I enter an incorrect master recovery password
Then I should see an error "Invalid recovery password"
  And I can try again
  With exponential backoff after multiple failures
```

### Scenario 4: Set new master password

```
Given the master recovery password has been verified
When I see the "Set New Password" screen
Then I should:
  - Enter a new master password
  - Confirm the new master password
  And the system should validate it meets requirements
```

### Scenario 5: Re-encryption with new password

```
Given I have entered a valid new master password
When I click "Recover Access"
Then the system should:
  - Derive a new encryption key from the new password
  - Re-encrypt the entire database with the new key
  - Update the encrypted database key in the keyring
  - Encrypt the database key with the new master password
```

### Scenario 6: Recovery progress

```
Given the recovery is in progress
When the database is being re-encrypted
Then I should see a progress indicator
  With a warning not to close the app
  And estimated time remaining
```

### Scenario 7: Recovery success

```
Given the recovery has completed successfully
When the process finishes
Then I should see a success message
  And I should be automatically logged in
  And I should see a reminder to save my new recovery password
  (Generate a new one and show it)
```

### Scenario 8: New recovery password

```
Given I have successfully recovered access
When the process completes
Then a NEW master recovery password should be generated
  And displayed to me ONCE
  And I must confirm I've saved it
  (Same flow as initial setup)
```

## Manual Testing Steps

### Test 1: Initiate recovery

1. At the login screen
2. Click "Forgot Password"
3. Verify the recovery flow starts
4. Verify it asks for the master recovery password
5. Verify the instructions are clear

### Test 2: Test correct recovery password

1. Start recovery flow
2. Enter the correct master recovery password
3. Click "Verify"
4. Verify it proceeds to the next step
5. Verify the recovery password works

### Test 3: Test incorrect recovery password

1. Start recovery flow
2. Enter an incorrect recovery password
3. Verify the error
4. Try again
5. Verify exponential backoff after multiple failures
6. Verify the system is secure

### Test 4: Set new password

1. Complete recovery password verification
2. Enter a new master password
3. Confirm the new password
4. Verify validation
5. Verify both entries match

### Test 5: Test re-encryption

1. Enter a valid new password
2. Click "Recover Access"
3. Verify the re-encryption happens
4. Verify the progress indicator
5. Wait for completion
6. Verify the time is reasonable

### Test 6: Verify recovery success

1. Complete the recovery flow
2. Verify the success message
3. Verify automatic login
4. Verify all data is accessible
5. Verify the new password works for future logins

### Test 7: Verify new recovery password

1. Complete recovery
2. Verify a new master recovery password is generated
3. Verify it's displayed
4. Verify you must confirm you've saved it
5. Verify the old recovery password no longer works

### Test 8: Test data integrity

1. Recover access
2. Verify all contacts are there
3. Verify all leads are there
4. Verify all properties are there
5. Verify all transactions are there
6. Verify all documents are accessible
7. Verify nothing is lost

### Test 9: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] "Forgot Password" link is available at login
- [ ] Recovery flow asks for master recovery password
- [ ] Correct recovery password allows proceeding
- [ ] Incorrect recovery password shows error
- [ ] Exponential backoff after multiple failures
- [ ] New master password can be set
- [ ] Database is re-encrypted with new password
- [ ] Progress indicator shows during re-encryption
- [ ] Success message is displayed
- [ ] User is automatically logged in
- [ ] All data is accessible after recovery
- [ ] New master recovery password is generated
- [ ] User must confirm new recovery password is saved
- [ ] Works on Windows, macOS, and Linux
- [ ] Process is secure and reliable
- [ ] No data loss during recovery
