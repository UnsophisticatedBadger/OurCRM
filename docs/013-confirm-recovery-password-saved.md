# US-013: Confirm Recovery Password Saved

## User Story

**As a** user  
**I want to** confirm that I have saved the recovery password  
**So that** I don't lose access to my data if I forget my master password

## Priority

**MVP:** Must Have

**Rationale:** Users often skip important warnings. Requiring explicit confirmation ensures they understand the importance of saving the recovery password before proceeding.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 2 hours: Create confirmation UI with checkboxes
- 1 hour: Implement three-step confirmation process
- 1 hour: Add visual warnings and emphasis
- 1 hour: Prevent proceeding without confirmation
- 1 hour: Add "Show password again" option (optional)
- 1 hour: Test confirmation flow
- 1 hour: Test cancellation behavior

## Dependencies

**Depends on:** US-012 (Generate Recovery Password)

**Blocks:** US-014 (Encrypted Database - needs setup completion), US-019 (Recover from Master Password)

## Description

After the recovery password is displayed, the user must explicitly confirm that they have saved it before proceeding with setup. This confirmation uses a three-step process where the user must type specific words to ensure they are paying attention and have actually saved the password.

The confirmation requires:
1. Checking a box: "I have written down or saved the master recovery password"
2. Checking a box: "I understand I cannot recover my data without this"
3. Typing "CONFIRM" to finalize

The UI should make it clear that this is a critical step and that proceeding without saving the password could result in permanent data loss. If the user cancels, the setup should not continue.

## BDD Scenarios

### Scenario 1: Confirm with all checkboxes and CONFIRM

```
Given I am viewing the recovery password
  And I have saved the password in a secure location
When I check "I have written down or saved the master recovery password"
  And I check "I understand I cannot recover my data without this"
  And I type "CONFIRM" in the confirmation field
  And I click "Continue"
Then the setup should proceed to the next step
  And the confirmation should be logged
```

### Scenario 2: Cannot proceed without first checkbox

```
Given I am on the confirmation screen
  And I have not checked the first checkbox
When I try to click "Continue"
Then the button should be disabled
  And I should see a message that I need to check the box
```

### Scenario 3: Cannot proceed without second checkbox

```
Given I am on the confirmation screen
  And I have checked the first checkbox
  But I have not checked the second checkbox
When I try to click "Continue"
Then the button should be disabled
```

### Scenario 4: Cannot proceed without typing CONFIRM

```
Given I am on the confirmation screen
  And I have checked both checkboxes
  But I have not typed "CONFIRM"
When I try to click "Continue"
Then the button should be disabled
```

### Scenario 5: Wrong confirmation text

```
Given I am on the confirmation screen
  And I have checked both checkboxes
When I type "confirm" (lowercase) in the confirmation field
Then the "Continue" button should remain disabled
  And I should see that the text must be exactly "CONFIRM"
```

### Scenario 6: Cancel setup from confirmation screen

```
Given I am on the confirmation screen
When I click "Cancel"
Then the setup should be cancelled
  And no data should be saved
  And the application should exit or return to the start
```

### Scenario 7: Visual warnings are prominent

```
Given I am on the confirmation screen
When I view the screen
Then I should see a warning icon or color
  And the warning text should be prominent
  And the consequences of not saving should be clear
```

## Manual Testing Steps

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

## Acceptance Criteria

- [ ] User must check first checkbox to proceed
- [ ] User must check second checkbox to proceed
- [ ] User must type "CONFIRM" exactly to proceed
- [ ] Continue button is disabled until all confirmations are complete
- [ ] Visual warnings are prominent and clear
- [ ] Consequences of not saving are clearly stated
- [ ] User can cancel setup from this screen
- [ ] Cancellation prevents any data from being saved
- [ ] Confirmation is logged for security purposes
- [ ] Works on Windows, macOS, and Linux
- [ ] UI makes the importance of this step clear
- [ ] Difficult to accidentally skip the confirmation