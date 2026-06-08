# US-012: Generate Recovery Password

## User Story

**As a** user  
**I want to** see a recovery password during setup  
**So that** I can recover my data if I forget my master password

## Priority

**MVP:** Must Have

**Rationale:** Users forget passwords. Without a recovery mechanism, all data would be permanently inaccessible. The recovery password is a critical safety mechanism.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Implement cryptographically secure random number generation
- 2 hours: Create recovery password generator (32 characters)
- 2 hours: Format password for display (with dashes for readability)
- 2 hours: Create UI to display the recovery password
- 1 hour: Add "Copy to Clipboard" functionality
- 1 hour: Implement secure display (clear from screen after confirmation)
- 2 hours: Write tests for generation and formatting
- 1 hour: Document the recovery process

## Dependencies

**Depends on:** US-010 (Create Master Password)

**Blocks:** US-013 (Confirm Recovery Password Saved), US-019 (Recover from Master Password)

## Description

During setup, after creating the master password, the system generates a cryptographically random 32-character recovery password. This password is displayed to the user once and only once. The user must save this password in a secure location (password manager, safe, etc.) because it will be needed if they ever forget their master password.

The recovery password uses a secure character set that excludes ambiguous characters (0, O, I, l, 1) to make it easier to read and write down correctly. The password is formatted with dashes every 5 characters to improve readability.

## BDD Scenarios

### Scenario 1: Generate recovery password

```
Given I am in the setup wizard
  And I have just created my master password
When I proceed to the recovery password step
Then a 32-character recovery password should be generated
  And the password should use cryptographically secure randomness
  And the password should exclude ambiguous characters (0, O, I, l, 1)
```

### Scenario 2: Display recovery password

```
Given a recovery password has been generated
When I view the recovery password screen
Then I should see the password displayed clearly
  And the password should be formatted with dashes every 5 characters
  And I should see a warning that this is the only time it will be shown
```

### Scenario 3: Copy recovery password to clipboard

```
Given I am viewing the recovery password
When I click "Copy to Clipboard"
Then the password should be copied to my system clipboard
  And I should see a confirmation message
```

### Scenario 4: Recovery password is shown only once

```
Given I have completed the setup wizard
  And I have seen the recovery password
When I try to view the recovery password again
Then I should not be able to see it
  And the system should not store the plain text recovery password
```

### Scenario 5: Recovery password is sufficiently long

```
Given a recovery password has been generated
When I examine the password
Then it should be exactly 32 characters long
  And it should contain a mix of uppercase, lowercase, numbers, and special characters
```

### Scenario 6: Multiple generations produce different passwords

```
Given I generate a recovery password
When I generate another recovery password
Then the two passwords should be completely different
  And there should be no pattern or predictability
```

## Manual Testing Steps

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

## Acceptance Criteria

- [ ] Recovery password is 32 characters long
- [ ] Uses cryptographically secure random generation
- [ ] Excludes ambiguous characters (0, O, I, l, 1)
- [ ] Formatted with dashes every 5 characters
- [ ] Displayed clearly during setup
- [ ] Can be copied to clipboard
- [ ] Shown only once
- [ ] Not stored in plain text anywhere
- [ ] Different each time it's generated
- [ ] Contains mix of character types
- [ ] Works on Windows, macOS, and Linux
- [ ] UI clearly warns this is the only time it will be shown