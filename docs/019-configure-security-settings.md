# US-019: Configure Security Settings

## User Story

**As a** user  
**I want to** configure security settings  
**So that** I can protect my data and control authentication behavior

## Priority

**MVP:** Must Have

**Rationale:** Security settings allow users to configure auto-lock, failed login attempt handling, and other security-related options. These are critical for protecting user data.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Identify security settings to include
- 2 hours: Create UI for each setting
- 1 hour: Implement auto-lock timeout
- 1 hour: Implement session management
- 1 hour: Add validation
- 1 hour: Test immediate vs restart-required changes
- 2 hours: Test all settings work correctly
- 1 hour: Test settings persistence

## Dependencies

**Depends on:** US-017 (Open Settings Window)

**Blocks:** US-020 (Create Contact - requires security foundation)

## Description

The Security settings category allows users to configure security-related options including auto-lock timeout, session management, and failed login attempt handling. These settings control how OurCRM protects user data and responds to potential security threats.

Settings should be loaded when the Settings window opens, and saved when the user clicks "Save". Some settings take effect immediately, while others may require an application restart. The UI should clearly indicate which settings require a restart.

## BDD Scenarios

### Scenario 1: View Security settings

```
Given the Settings window is open
  And the Security category is selected
When I view the Security settings
Then I should see options for:
  - Auto-lock timeout (in minutes, or "Never")
  - Failed login attempt handling (exponential backoff)
  - Session timeout
  - Require password for sensitive actions
```

### Scenario 2: Change auto-lock timeout

```
Given I am in Security settings
  And the current auto-lock timeout is 10 minutes
When I select "15 minutes" from the auto-lock dropdown
  And I click "Save"
Then the auto-lock setting should be saved
  And the new timeout should take effect immediately
```

### Scenario 3: Set auto-lock to Never

```
Given I am in Security settings
  And the current auto-lock timeout is 10 minutes
When I select "Never" from the auto-lock dropdown
  And I click "Save"
Then the auto-lock should be disabled
  And the application should not auto-lock
```

### Scenario 4: Auto-lock triggers after inactivity

```
Given I have set auto-lock to 5 minutes
  And I am logged in to OurCRM
When I do not interact with the application for 5 minutes
Then the application should automatically lock
  And I should be required to enter my password to unlock
```

### Scenario 5: Auto-lock resets on activity

```
Given I have set auto-lock to 5 minutes
  And I am logged in to OurCRM
When I interact with the application
Then the auto-lock timer should reset
  And the lock should not occur
```

### Scenario 6: Settings persist across restarts

```
Given I have changed Security settings
  And I have saved them
When I close the application
  And I restart the application
Then all my Security settings should be restored
  And the application should use my preferred settings
```

### Scenario 7: Failed login backoff is configured

```
Given I am in Security settings
When I view the failed login attempt settings
Then I should see information about the exponential backoff
  And I should see the current backoff timing
  And I should be able to understand how it works
```


## Manual Testing Steps

### Test 1: View all Security settings

1. Open Settings
2. Select Security category
3. Verify all expected settings are present
4. Check that each setting has a clear label
5. Verify settings are organized logically
6. Document any missing settings

### Test 2: Test auto-lock timeout change

1. Open Settings > Security
2. Change auto-lock from 10 minutes to 15 minutes
3. Click Save
4. Verify the setting is saved
5. Wait 15 minutes (or temporarily change to 1 minute for testing)
6. Verify the application auto-locks

### Test 3: Test auto-lock with Never

1. Open Settings > Security
2. Set auto-lock to "Never"
3. Click Save
4. Leave the application idle for a long time
5. Verify it does NOT auto-lock
6. Set back to a specific time
7. Verify auto-lock works again

### Test 4: Test auto-lock timer reset

1. Set auto-lock to 1 minute
2. Interact with the application every 30 seconds
3. Verify the application does NOT lock
4. Stop interacting
5. Wait 1 minute
6. Verify it locks

### Test 5: Test settings persistence

1. Change several Security settings
2. Save and close the application
3. Restart the application
4. Open Settings > Security
5. Verify all your changes are still there
6. Check the configuration file
7. Verify the settings are stored correctly

### Test 6: Test immediate effect

1. Change auto-lock timeout
2. Click Save
3. Verify the change takes effect immediately
4. Test other settings that should take effect immediately
5. Document any settings that require restart

### Test 7: Test default values

1. Delete or reset the configuration file
2. Start OurCRM
3. Open Settings > Security
4. Verify default values are sensible
5. Document the defaults

### Test 8: Test on all platforms

1. Test Security settings on Windows
2. Verify auto-lock works
3. Test on macOS
4. Verify auto-lock works
5. Test on Linux
6. Verify auto-lock works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Security settings category is accessible
- [ ] Auto-lock timeout can be configured
- [ ] Auto-lock can be set to Never
- [ ] Auto-lock takes effect immediately
- [ ] Auto-lock resets on user activity
- [ ] Auto-lock triggers after inactivity
- [ ] Settings persist across application restarts
- [ ] Settings are validated before saving
- [ ] Default values are sensible
- [ ] Failed login backoff is documented
- [ ] Works on Windows, macOS, and Linux
- [ ] Configuration is stored in TOML format