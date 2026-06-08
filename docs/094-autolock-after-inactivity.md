# US-094: Auto-Lock After Inactivity

## User Story

**As a** user  
**I want to** the app to automatically lock after a period of inactivity  
**So that** my data is protected if I walk away from my computer

## Priority

**MVP:** Must Have

**Rationale:** Auto-lock is a critical security feature. Without it, an unlocked application sitting idle is vulnerable to anyone with physical access to the computer. Auto-lock protects user data when the user steps away.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design auto-lock mechanism
- 1 hour: Implement activity tracking
- 1 hour: Implement inactivity timer
- 1 hour: Create lock screen
- 1 hour: Implement unlock flow
- 1 hour: Add settings for timeout duration
- 1 hour: Test auto-lock with various timeouts
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-019 (Configure Security Settings), US-011 (Log In with Master Password)

**Blocks:** US-095 (Change Master Password)

## Description

After a configured period of inactivity, the application should automatically lock, requiring the user to enter their master password to unlock it. The inactivity timer should reset on any user activity (keyboard, mouse, clicks).

The lock screen should be simple and secure, showing the OurCRM logo and a password field. The user can configure the timeout duration in settings (or disable auto-lock if they prefer, though this is less secure).

## BDD Scenarios

### Scenario 1: Auto-lock after inactivity

```
Given I am logged in to OurCRM
  And the auto-lock timeout is set to 10 minutes
When I do not interact with the app for 10 minutes
Then the app should automatically lock
  And show the lock screen
  And require my master password to unlock
```

### Scenario 2: Activity resets the timer

```
Given the auto-lock timeout is 10 minutes
When I interact with the app (type, click, etc.)
Then the inactivity timer should reset
  And the app should not lock
```

### Scenario 3: Lock screen appears

```
Given the app has auto-locked
When I look at the screen
Then I should see:
  - A lock screen
  - OurCRM logo or branding
  - Password input field
  - "Unlock" button
```

### Scenario 4: Unlock with correct password

```
Given the app is locked
When I enter my correct master password
  And click "Unlock"
Then the app should unlock
  And return to where I was
  And all my data should be accessible
```

### Scenario 5: Unlock with wrong password

```
Given the app is locked
When I enter an incorrect password
Then I should see an error message
  And exponential backoff should apply
  (Same as initial login)
```

### Scenario 6: Configure auto-lock timeout

```
Given I am in Security settings
When I set the auto-lock timeout
  (5, 10, 15, 30, 60 minutes, or Never)
  And I save the settings
Then the new timeout should be applied
  And the app should lock after that period of inactivity
```

### Scenario 7: Disable auto-lock (not recommended)

```
Given I am in Security settings
When I set auto-lock to "Never"
Then the app should never auto-lock
  And a warning should be shown about security risks
```

### Scenario 8: Auto-lock on system lock

```
Given I lock my computer (Windows+L, Cmd+Ctrl+Q, etc.)
When I unlock the computer and return to OurCRM
Then OurCRM should also be locked
  (Optional but recommended for security)
```

## Manual Testing Steps

### Test 1: Test auto-lock

1. Set auto-lock to 1 minute (for testing)
2. Log in to OurCRM
3. Don't touch the app for 1 minute
4. Verify the app locks
5. Verify the lock screen appears

### Test 2: Test activity reset

1. Set auto-lock to 1 minute
2. Log in
3. Interact with the app every 30 seconds
4. Wait 2 minutes
5. Verify the app did NOT lock
6. Stop interacting
7. Wait 1 minute
8. Verify it locks

### Test 3: Test lock screen

1. Wait for auto-lock
2. Verify the lock screen appears
3. Verify the password field is present
4. Verify the OurCRM branding is shown
5. Verify it looks professional

### Test 4: Test unlock

1. Wait for auto-lock
2. Enter the correct password
3. Click "Unlock"
4. Verify the app unlocks
5. Verify you return to where you were
6. Verify all data is accessible

### Test 5: Test wrong password

1. Wait for auto-lock
2. Enter an incorrect password
3. Verify the error message
4. Verify exponential backoff
5. Try again with correct password
6. Verify it works

### Test 6: Test timeout configuration

1. Go to Security settings
2. Change auto-lock to 5 minutes
3. Save the settings
4. Verify the new timeout is applied
5. Test with different timeouts

### Test 7: Test disable auto-lock

1. Set auto-lock to "Never"
2. Verify a warning is shown
3. Save the settings
4. Wait a long time
5. Verify the app does NOT lock

### Test 8: Test system lock integration

1. Lock your computer
2. Unlock it
3. Return to OurCRM
4. Verify OurCRM is also locked (if implemented)
5. Unlock OurCRM
6. Verify it works

### Test 9: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Auto-lock triggers after configured inactivity period
- [ ] Activity (keyboard, mouse) resets the timer
- [ ] Lock screen is shown when locked
- [ ] Lock screen has password field and unlock button
- [ ] Correct password unlocks the app
- [ ] Wrong password shows error and applies backoff
- [ ] Auto-lock timeout is configurable in settings
- [ ] Auto-lock can be disabled (with warning)
- [ ] Lock screen is professional and secure
- [ ] Unlock returns user to where they were
- [ ] Settings persist across restarts
- [ ] Works on Windows, macOS, and Linux
- [ ] Timer is accurate
- [ ] No way to bypass without password
