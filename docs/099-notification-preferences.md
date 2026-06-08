# US-099: Notification Preferences

## User Story

**As a** user  
**I want to** configure which notifications I receive and how  
**So that** I'm not overwhelmed by notifications and can focus on what matters

## Priority

**MVP:** Must Have

**Rationale:** Different users have different notification needs. Some want to be notified about everything, others only about critical events. Giving users control over their notification preferences ensures they get the right amount of information without being overwhelmed.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design notification preferences UI
- 1 hour: Create preferences form
- 1 hour: Implement notification type toggles
- 1 hour: Add delivery method selection
- 1 hour: Test preferences
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-097 (Desktop Notifications for New Leads), US-098 (In-App Notifications)

**Blocks:** None

## Description

Users should be able to configure their notification preferences in a dedicated Notification section in the Settings window. They should be able to:

1. Enable/disable notifications by type (new leads, task reminders, showing reminders, emails, etc.)
2. Choose delivery methods (desktop, in-app, both, or none)
3. Set quiet hours (do not disturb times)
4. Configure notification sound
5. Choose which events trigger notifications

The preferences should be granular enough to be useful but not so complex that they're overwhelming.

## BDD Scenarios

### Scenario 1: Open notification preferences

```
Given the Settings window is open
When I click on the "Notifications" category
Then I should see notification configuration options:
  - Notification types (with toggles)
  - Delivery methods
  - Quiet hours
  - Sound settings
```

### Scenario 2: Enable/disable notification types

```
Given I am in Notification preferences
When I see the list of notification types
Then I should be able to toggle each:
  - New leads (on/off)
  - Task reminders (on/off)
  - Showing reminders (on/off)
  - Email received (on/off)
  - Property updates (on/off)
  - System updates (on/off)
  - etc.
```

### Scenario 3: Choose delivery method

```
Given I am configuring a notification type
When I select the delivery method
Then I can choose:
  - Desktop notification only
  - In-app notification only
  - Both desktop and in-app
  - No notification
```

### Scenario 4: Set quiet hours

```
Given I am in Notification preferences
When I configure quiet hours
Then I can set:
  - Start time (e.g., 9:00 PM)
  - End time (e.g., 7:00 AM)
  And during quiet hours, notifications are silenced
  But still logged in the notification center
```

### Scenario 5: Notification sound

```
Given I am in Notification preferences
When I configure sound
Then I can:
  - Enable/disable notification sounds
  - Choose a sound (if multiple available)
  - Adjust volume (if possible)
```

### Scenario 6: Test notification

```
Given I am in Notification preferences
When I click "Send Test Notification"
Then a test notification should be sent
  Using my current settings
  And I can verify it works correctly
```

### Scenario 7: Preferences persist across restarts

```
Given I have configured notification preferences
When I close the application
  And I restart the application
  And I trigger a notification
Then the notification should use my saved preferences
```

### Scenario 8: Granular event settings

```
Given I am in Notification preferences
When I configure events
Then I can choose specific events:
  - New lead from website (on/off)
  - New lead from manual entry (on/off)
  - Task due in 1 hour (on/off)
  - Task overdue (on/off)
  - etc.
```

## Manual Testing Steps

### Test 1: Open notification preferences

1. Go to Settings
2. Click "Notifications"
3. Verify all options are present
4. Check that the UI is clear

### Test 2: Toggle notification types

1. Toggle various notification types on/off
2. Trigger events for each type
3. Verify only enabled types trigger notifications
4. Verify disabled types don't

### Test 3: Test delivery methods

1. Set different delivery methods for different types
2. Trigger events
3. Verify the correct delivery method is used
4. Test desktop only, in-app only, both, and none

### Test 4: Test quiet hours

1. Set quiet hours (e.g., 9 PM to 7 AM)
2. Trigger a notification during quiet hours
3. Verify it's silenced (no desktop notification)
4. Verify it's still logged in the notification center
5. Trigger outside quiet hours
6. Verify the notification appears normally

### Test 5: Test sound

1. Enable notification sound
2. Trigger a notification
3. Verify the sound plays
4. Disable sound
5. Trigger another
6. Verify no sound plays

### Test 6: Test notification

1. Click "Send Test Notification"
2. Verify a test notification appears
3. Verify it uses current settings
4. Test with different settings to see the effect

### Test 7: Test persistence

1. Configure preferences
2. Close the application
3. Restart the application
4. Trigger a notification
5. Verify the saved preferences are used

### Test 8: Test granular settings

1. Configure specific events
2. Trigger those events
3. Verify only configured events trigger notifications
4. Test with various combinations

### Test 9: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Notification preferences are accessible from settings
- [ ] Can enable/disable notifications by type
- [ ] Can choose delivery method (desktop, in-app, both, none)
- [ ] Can set quiet hours
- [ ] Can enable/disable notification sound
- [ ] Can send test notification
- [ ] Preferences persist across restarts
- [ ] Granular event settings are available
- [ ] Preferences are easy to configure
- [ ] Changes take effect immediately
- [ ] Works on Windows, macOS, and Linux
- [ ] UI is intuitive and well-organized
- [ ] Preferences are saved securely
- [ ] Default preferences are sensible
