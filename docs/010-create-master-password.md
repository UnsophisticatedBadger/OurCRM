# US-010: Create Master Password

## User Story

**As a** user  
**I want to** create a master password during setup  
**So that** my data is secure and only I can access it

## Priority

**MVP:** Must Have

**Rationale:** Security is fundamental to the application. The master password protects the encrypted database and all user data. Without it, we cannot meet our security commitments.

## Estimated Effort

**Size:** Medium (M) - 3-5 days

**Breakdown:**
- 2 hours: Design password requirements
- 3 hours: Create password validation logic
- 4 hours: Create setup wizard UI for password creation
- 2 hours: Implement password strength meter
- 3 hours: Hash password with Argon2id
- 2 hours: Store password hash securely
- 2 hours: Write tests for validation
- 2 hours: Test cross-platform behavior

## Dependencies

**Depends on:** US-008 (Create First Test), US-020 (Create Contact - needs security)

**Blocks:** US-011 (Log In), US-012 (Recovery Password), US-013 (Confirm Recovery Password)

## Description

During the initial setup of OurCRM, a user must create a master password. This password must be at least 12 characters long and include uppercase, lowercase, numbers, and special characters. The password should be hashed using Argon2id with parameters calibrated to take approximately 2 seconds to verify.

The user will type this password every time they start OurCRM. It protects the encrypted database and all stored credentials. The password is never stored in plain text - only the Argon2id hash is stored in the OS keyring.

## BDD Scenarios

### Scenario 1: Create valid password

```
Given I am in the setup wizard
  And I am on the password creation step
When I enter a password that meets all requirements
  And I confirm the password
  And I click "Create"
Then the password should be validated
  And the password should be hashed with Argon2id
  And the hash should be stored in the OS keyring
  And I should proceed to the next step
```

### Scenario 2: Reject password that is too short

```
Given I am in the setup wizard
  And I am on the password creation step
When I enter a password with fewer than 12 characters
Then I should see an error message
  And the error should say "Password must be at least 12 characters"
  And I should not be able to proceed
```

### Scenario 3: Reject password missing uppercase

```
Given I am in the setup wizard
When I enter a password with no uppercase letters
Then I should see an error message
  And the error should say "Password must contain at least one uppercase letter"
```

### Scenario 4: Reject password missing lowercase

```
Given I am in the setup wizard
When I enter a password with no lowercase letters
Then I should see an error message
  And the error should say "Password must contain at least one lowercase letter"
```

### Scenario 5: Reject password missing numbers

```
Given I am in the setup wizard
When I enter a password with no numbers
Then I should see an error message
  And the error should say "Password must contain at least one number"
```

### Scenario 6: Reject password missing special characters

```
Given I am in the setup wizard
When I enter a password with no special characters
Then I should see an error message
  And the error should say "Password must contain at least one special character"
```

### Scenario 7: Reject mismatched confirmation

```
Given I am in the setup wizard
When I enter a password
  And I enter a different password in the confirmation field
Then I should see an error message
  And the error should say "Passwords do not match"
```

### Scenario 8: Show password strength

```
Given I am in the setup wizard
When I type a password
Then I should see a strength indicator
  And the indicator should update as I type
  And it should show "Weak", "Medium", or "Strong"
```

### Scenario 9: Hash password with Argon2id

```
Given I have entered a valid password
When the password is hashed
Then it should use Argon2id algorithm
  And the hash should be stored in the OS keyring
  And the original password should not be stored anywhere
```

## Manual Testing Steps

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

## Acceptance Criteria

- [ ] User can create a master password during setup
- [ ] Password must be at least 12 characters
- [ ] Password must include uppercase, lowercase, numbers, and special characters
- [ ] Password is hashed with Argon2id
- [ ] Hash is stored in OS keyring
- [ ] Original password is never stored
- [ ] Password strength meter works
- [ ] Confirmation field validates match
- [ ] Clear error messages for all validation failures
- [ ] Verification takes approximately 2 seconds
- [ ] Works on Windows, macOS, and Linux
- [ ] Password requirements are clearly documented