I'll create the user story for Notification Preferences/Settings (US-119).

---

# US-119: Notification Preferences and Settings

## User Story

**As a** user of the application  
**I want to** configure my notification preferences in detail  
**So that** I can control which notifications I receive, how I receive them, and when I'm interrupted, ensuring the system works the way I need it to

## Priority

**MVP:** Must Have

**Rationale:** Notification preferences are essential for user control and preventing notification fatigue. Different users have different workflows, tolerances for interruptions, and notification needs. Without granular control, users will either be overwhelmed by notifications or miss critical ones. A well-designed preferences system respects user autonomy, reduces frustration, and ensures the notification system adds value rather than becoming a nuisance. This is foundational to making the entire notification system usable and effective.

## Estimated Effort

**Size:** Medium-Large (M-L) - 4 days

**Breakdown:**
- 2 hours: Design preferences data model and schema
- 3 hours: Create preferences UI/UX mockups
- 4 hours: Build notification settings page
- 3 hours: Implement global notification toggles
- 4 hours: Implement per-category notification settings
- 3 hours: Add per-event-type granular controls
- 3 hours: Implement channel selection (desktop, in-app, email)
- 3 hours: Build timing and scheduling preferences
- 2 hours: Add quiet hours / Do Not Disturb functionality
- 3 hours: Implement frequency limits and throttling
- 3 hours: Create test notification feature
- 2 hours: Add import/export preferences
- 3 hours: Implement preference validation and error handling
- 3 hours: Test and polish UI/UX

## Dependencies

**Depends on:** 
- US-116 (Desktop Notifications for New Leads)
- US-117 (In-App Notifications)
- US-118 (Notification for Showing Reminders)
- US-120 (Notification for Email Received)
- US-084 (Set Task Due Date and Reminder)
- All notification-triggering features

**Blocks:** None (terminal configuration feature)

## Description

The application should provide a comprehensive notification preferences page that allows users to control every aspect of their notification experience. The page should be organized logically with clear sections and intuitive controls.

The preferences page should include:

**1. Global Settings**
- Master enable/disable for all notifications
- Notification sound on/off
- Notification volume control
- Desktop notifications enable/disable
- In-app notifications enable/disable
- Email notifications enable/disable

**2. Per-Category Settings** (with sub-categories)
- **Leads**
  - New lead created
  - Lead assigned to me
  - Lead status changed
  - Lead converted
  - Lead qualification completed
- **Tasks**
  - Task assigned
  - Task due soon (with configurable timeframe)
  - Task overdue
  - Task completed
- **Showings**
  - Showing scheduled
  - Showing reminder (with default times)
  - Showing starting soon
  - Showing completed
  - Showing cancelled
- **Transactions**
  - Transaction created
  - Transaction status changed
  - Closing date approaching
  - Transaction completed
- **Emails**
  - New email received
  - Email sent confirmation
  - Email bounce/failure
- **Contacts**
  - Contact shared with me
  - Contact updated by team member
- **Properties**
  - Property status changed
  - Price changed
  - Property sold
- **System**
  - Backup completed/failed
  - Updates available
  - Security alerts
  - Import/export completed

**3. Channel Selection per Category**
- Desktop notifications (with sound options)
- In-app notifications
- Email notifications
- Push notifications (if applicable)

**4. Timing and Scheduling**
- Quiet hours / Do Not Disturb schedule
- Different schedules for weekdays/weekends
- Time zone selection
- Default reminder times for showings
- Default reminder times for tasks

**5. Frequency and Throttling**
- Maximum notifications per hour
- Batch similar notifications
- Digest mode (summary at specific times)
- Minimum interval between notifications

**6. Advanced Settings**
- Notification priority levels
- Override system Do Not Disturb
- Show notification content in preview
- Notification duration on screen
- Snooze duration options
- Auto-dismiss after time

**7. Testing and Diagnostics**
- Send test notification
- Preview notification sound
- View notification delivery statistics
- Reset to defaults

Users should be able to:
- Access preferences from settings menu
- See all preferences on a single page or organized tabs
- Save changes with a single "Save" button or auto-save
- Reset all preferences to defaults
- Export/import preferences for backup
- Preview how a notification will look before saving settings

## BDD Scenarios

### Scenario 1: Access notification preferences

```
Given I am logged into the application
When I navigate to Settings > Notifications
Then the notification preferences page should open
  And it should display all available preference categories
  And it should show my current settings
  And it should have clear organization with sections or tabs
```

### Scenario 2: Master notification toggle

```
Given I am on the notification preferences page
  And all notifications are currently enabled
When I toggle the master "Enable All Notifications" switch to OFF
  And I save my preferences
Then all notification types should be disabled
  And no notifications should be delivered through any channel
  And the setting should persist across app restarts
  And I should see a warning about missing important updates
```

### Scenario 3: Re-enable master toggle

```
Given all notifications are currently disabled
When I toggle the master switch to ON
  And I save my preferences
Then notifications should be re-enabled
  And all individual category settings should be restored to their previous values
  And the categories should show as enabled
```

### Scenario 4: Enable desktop notifications

```
Given I am on the notification preferences page
When I check the "Desktop Notifications" checkbox
  And I save my preferences
Then desktop notifications should be enabled
  And the system should verify notification permissions
  And if permissions are not granted, show a permission request
```

### Scenario 5: Configure per-category settings

```
Given I am on the notification preferences page
  And I expand the "Leads" category
When I see the lead notification options:
  - New lead created
  - Lead assigned
  - Lead status changed
  - Lead converted
Then I should be able to individually enable/disable each option
  And select delivery channels for each
  And the changes should be saved when I click Save
```

### Scenario 6: Select notification channels per event

```
Given I am configuring notifications for "New Lead Created"
When I see the channel options:
  - Desktop notification
  - In-app notification
  - Email notification
Then I should be able to select one or multiple channels
  And each channel should be independently toggleable
  And the selection should be saved
```

### Scenario 7: Configure quiet hours

```
Given I am on the notification preferences page
When I enable "Quiet Hours" / "Do Not Disturb"
  And I set the start time to 10:00 PM
  And I set the end time to 8:00 AM
  And I select which days apply (weeknights)
  And I save my preferences
Then during quiet hours:
  - No desktop notifications should appear
  - No sounds should play
  - Notifications should still be logged in the notification center
  - Critical notifications (e.g., security alerts) may override (configurable)
```

### Scenario 8: Critical notifications override quiet hours

```
Given I have quiet hours enabled from 10 PM to 8 AM
  And I have enabled "Allow critical notifications during quiet hours"
When a critical notification occurs (e.g., security alert) during quiet hours
Then the notification should be delivered despite quiet hours
  And it should be marked as critical
  And it should use a distinct sound/style
```

### Scenario 9: Set default showing reminder times

```
Given I am on the notification preferences page
  And I expand the "Showings" category
When I click "Configure Default Reminder Times"
  And I add reminder times: 24 hours, 2 hours, 30 minutes before
  And I save
Then all future showings should use these default reminder times
  And existing showings should retain their original reminder times
  And the preferences should apply globally
```

### Scenario 10: Configure task reminder timing

```
Given I am on the notification preferences page
When I set "Notify me X hours before task is due" to 24
  And I set "Notify me when task is overdue by Y hours" to 1
  And I save
Then task due reminders should be sent 24 hours before the due date
  And overdue notifications should be sent 1 hour after the due time
  And these settings should apply to all tasks
```

### Scenario 11: Enable notification sounds

```
Given I am on the notification preferences page
When I toggle "Notification Sounds" to ON
  And I select a sound from the available options
  And I adjust the volume slider
  And I save
Then notifications should play the selected sound at the specified volume
  And the changes should take effect immediately for new notifications
```

### Scenario 12: Disable notification sounds

```
Given notification sounds are currently enabled
When I toggle "Notification Sounds" to OFF
  And I save
Then future notifications should not play any sound
  And visual notifications should still appear
  And the change should persist
```

### Scenario 13: Set maximum notifications per hour

```
Given I am on the notification preferences page
When I set "Maximum notifications per hour" to 10
  And I save
Then the system should not deliver more than 10 notifications per hour
  And additional notifications should be batched or queued
  And a summary should be shown at the end of the hour
```

### Scenario 14: Enable digest mode

```
Given I am on the notification preferences page
When I enable "Digest Mode"
  And I set the digest delivery time to 9:00 AM daily
  And I save
Then instead of individual notifications, I should receive a daily summary
  And the summary should be sent at 9:00 AM
  And it should include all notifications from the previous period
  And I can still view real-time notifications in the app
```

### Scenario 15: Batch similar notifications

```
Given I have "Batch similar notifications" enabled
When 5 new leads are imported within a short time
Then I should receive a single notification: "5 New Leads Imported"
  And clicking it should show the list of leads
  And the notification should be marked as a batch
```

### Scenario 16: Send test notification

```
Given I am on the notification preferences page
When I click "Send Test Notification"
Then a test desktop notification should appear
  And it should use my current sound and visual settings
  And I can verify my configuration is working
  And the test notification should be marked as a test
```

### Scenario 17: Test different notification channels

```
Given I am on the notification preferences page
When I click "Test Desktop Notification"
  And then "Test In-App Notification"
  And then "Test Email Notification"
Then each channel should be tested independently
  And I should see the result of each test
  And any failures should be clearly indicated
```

### Scenario 18: Reset to default preferences

```
Given I have customized my notification preferences
When I click "Reset to Defaults"
  And I confirm the action
Then all preferences should be reset to their default values
  And I should see a confirmation message
  And the reset should be logged
```

### Scenario 19: Export preferences

```
Given I have configured my notification preferences
When I click "Export Preferences"
  And I choose a location to save the file
Then a JSON or configuration file should be downloaded
  And the file should contain all my notification settings
  And I can use this file to restore or transfer settings
```

### Scenario 20: Import preferences

```
Given I have a previously exported preferences file
When I click "Import Preferences"
  And I select the file
  And I confirm the import
Then my current preferences should be replaced with the imported ones
  And a confirmation should show "Preferences imported successfully"
  And the changes should take effect immediately
```

### Scenario 21: Auto-save preferences

```
Given I am on the notification preferences page
  And auto-save is enabled
When I change any preference
Then the change should be saved automatically after a short delay
  And a "Saved" indicator should appear briefly
  And I don't need to click a Save button
```

### Scenario 22: Manual save with unsaved changes warning

```
Given I have made changes to my preferences
  And I haven't saved yet
When I try to navigate away from the page
Then I should see a warning: "You have unsaved changes"
  And I can choose to save, discard, or cancel
```

### Scenario 23: Notification permission denied

```
Given I try to enable desktop notifications
  And I previously denied notification permissions at the OS level
When I try to save the preference
Then I should see an error: "Desktop notifications are blocked"
  And I should be guided to enable permissions in system settings
  And the preference should not be saved as enabled
```

### Scenario 24: Time zone selection

```
Given I am on the notification preferences page
When I view the time zone setting
  And I select my time zone from the dropdown
  And I save
Then all time-based notifications should use the selected time zone
  And quiet hours should be interpreted in the selected time zone
  And the change should affect all future notifications
```

### Scenario 25: Different quiet hours for weekdays and weekends

```
Given I am configuring quiet hours
When I set "Weekday Quiet Hours" to 10 PM - 7 AM
  And I set "Weekend Quiet Hours" to 11 PM - 9 AM
  And I save
Then the system should use weekday hours Monday-Friday
  And weekend hours Saturday-Sunday
  And the appropriate schedule should be applied based on the current day
```

### Scenario 26: Notification preview before saving

```
Given I am changing notification settings
When I click "Preview" next to a setting
Then I should see a preview of how the notification will look
  And I can verify the sound, visual style, and content
  And I can adjust settings based on the preview
```

### Scenario 27: Granular control for lead notifications

```
Given I am expanding the "Leads" category
When I see the sub-options:
  - New lead created (enabled, desktop + in-app)
  - Lead assigned to me (enabled, desktop + in-app + email)
  - Lead status changed (disabled)
  - Lead converted (enabled, in-app only)
Then I can independently configure each option
  And each has its own channel selection
  And changes are saved per-option
```

### Scenario 28: Email notification settings

```
Given I am configuring email notifications
When I enable "Email Notifications"
  And I select which events should send emails
  And I configure my email address
  And I save
Then the selected events should trigger email notifications
  And the emails should be sent to the configured address
  And I should receive a test email to verify
```

### Scenario 29: Notification priority levels

```
Given I am on the notification preferences page
When I configure priority levels for different notification types
  (e.g., showing reminders = high, new lead = medium, system updates = low)
Then notifications should be delivered with the configured priority
  And high-priority notifications should override quiet hours
  And low-priority notifications should respect quiet hours
```

### Scenario 30: Notification content preview settings

```
Given I am on the notification preferences page
When I configure "Show notification content in preview":
  - Always show full content
  - Show sender only, hide message
  - Hide all content (private mode)
Then notifications should display according to the setting
  And sensitive information should be hidden if configured
  And the setting should apply to all channels
```

### Scenario 31: Auto-dismiss duration

```
Given I am on the notification preferences page
When I set "Auto-dismiss notifications after" to 30 seconds
  And I save
Then desktop notifications should automatically disappear after 30 seconds
  And the user can still interact with them before they dismiss
  And critical notifications should not auto-dismiss
```

### Scenario 32: Snooze duration options

```
Given I am configuring snooze behavior
When I set available snooze durations to: 5 min, 15 min, 1 hour, 4 hours
  And I save
Then when snoozing a notification, only these options should appear
  And the user cannot enter custom snooze times
  And the configuration should apply to all snoozable notifications
```

### Scenario 33: Notification statistics

```
Given I am on the notification preferences page
When I click "View Notification Statistics"
Then I should see:
  - Total notifications received this week/month
  - Breakdown by type
  - Most active notification types
  - Snooze frequency
  And I can use this data to optimize my settings
```

### Scenario 34: Validation of preferences

```
Given I am saving notification preferences
When I enter invalid values (e.g., end time before start time for quiet hours)
Then I should see validation errors
  And the preferences should not be saved
  And I should be guided to correct the errors
```

### Scenario 35: Preferences search

```
Given I am on the notification preferences page
  And there are many preference options
When I type "email" in the search box
Then only email-related preferences should be displayed
  And other sections should be collapsed or hidden
  And clearing the search should show all preferences again
```

## Manual Testing Steps

### Test 1: Access notification preferences

1. Log into the application
2. Navigate to Settings
3. Click on "Notifications"
4. Verify the notification preferences page opens
5. Verify all sections are visible
6. Verify current settings are displayed correctly

### Test 2: Master toggle functionality

1. Note current notification behavior
2. Go to notification preferences
3. Toggle "Enable All Notifications" to OFF
4. Save
5. Trigger various events (create lead, schedule showing, etc.)
6. Verify no notifications are delivered
7. Toggle back to ON
8. Verify notifications work again

### Test 3: Global notification toggles

1. Go to notification preferences
2. Toggle off "Desktop Notifications"
3. Save
4. Create a new lead
5. Verify no desktop notification appears
6. Verify in-app notification still works
7. Toggle off "In-App Notifications"
8. Save
9. Create another lead
10. Verify no notifications appear anywhere
11. Re-enable both

### Test 4: Per-category settings

1. Go to notification preferences
2. Expand "Leads" category
3. Disable "New lead created"
4. Save
5. Create a new lead
6. Verify no notification for new lead
7. Verify other lead events still trigger notifications
8. Re-enable and verify it works

### Test 5: Channel selection per event

1. Go to "Leads > New lead created"
2. Enable only "Email" channel
3. Disable desktop and in-app
4. Save
5. Create a new lead
6. Verify email is sent
7. Verify no desktop notification
8. Verify no in-app notification
9. Add desktop channel
10. Verify both desktop and email are sent

### Test 6: Quiet hours configuration

1. Go to notification preferences
2. Enable "Quiet Hours"
3. Set start time to current time + 1 minute
4. Set end time to current time + 5 minutes
5. Save
6. Wait for quiet hours to start
7. Create a new lead
8. Verify no desktop notification appears
9. Verify the notification is still in the in-app notification center
10. Wait for quiet hours to end
11. Verify notifications resume normally

### Test 7: Critical notifications override quiet hours

1. Enable quiet hours
2. Enable "Allow critical notifications during quiet hours"
3. Trigger a critical event (e.g., security alert)
4. Verify the notification is delivered despite quiet hours
5. Verify it's marked as critical
6. Test with non-critical events
7. Verify they respect quiet hours

### Test 8: Default reminder times

1. Go to "Showings > Default Reminder Times"
2. Set times to 48 hours, 4 hours, 1 hour before
3. Save
4. Schedule a new showing
5. Verify the showing has these reminder times
6. Schedule another showing
7. Verify it also uses these times
8. Change the defaults
9. Schedule a third showing
10. Verify it uses the new defaults

### Test 9: Task reminder timing

1. Go to "Tasks > Reminder Timing"
2. Set "Hours before due" to 48
3. Set "Hours after overdue" to 2
4. Save
5. Create a task due in 48 hours
6. Verify reminder is scheduled
7. Create a task that will be overdue in 2 hours
8. Verify overdue notification is scheduled

### Test 10: Notification sounds

1. Go to notification preferences
2. Enable notification sounds
3. Select a sound
4. Adjust volume
5. Save
6. Create a lead
7. Verify sound plays at correct volume
8. Disable sounds
9. Create another lead
10. Verify no sound plays
11. Verify visual notification still appears

### Test 11: Maximum notifications per hour

1. Set "Maximum notifications per hour" to 3
2. Save
3. Create 5 leads in quick succession
4. Verify only 3 desktop notifications appear
5. Verify a batch notification appears for the remaining 2
6. Or verify they are queued/delivered later
7. Wait an hour
8. Verify normal delivery resumes

### Test 12: Digest mode

1. Enable "Digest Mode"
2. Set delivery time to 1 minute from now
3. Save
4. Create 3 leads
5. Verify no individual notifications appear
6. Wait for digest time
7. Verify a summary notification/email appears
8. Verify it includes all 3 leads
9. Verify the in-app notification center still has individual notifications

### Test 13: Batch similar notifications

1. Enable "Batch similar notifications"
2. Import 10 leads from CSV
3. Verify a single batch notification appears: "10 New Leads Imported"
4. Click the notification
5. Verify it shows the list of leads
6. Verify the notification is marked as a batch

### Test 14: Test notification

1. Go to notification preferences
2. Click "Send Test Notification"
3. Verify a test desktop notification appears
4. Verify it uses current sound settings
5. Verify it's clearly marked as a test
6. Click "Test In-App Notification"
7. Verify in-app notification appears
8. Click "Test Email Notification"
9. Verify test email is sent and received

### Test 15: Reset to defaults

1. Customize several notification preferences
2. Save changes
3. Click "Reset to Defaults"
4. Confirm the action
5. Verify all preferences are reset
6. Verify a confirmation message appears
7. Verify the reset is logged

### Test 16: Export preferences

1. Configure various notification preferences
2. Save changes
3. Click "Export Preferences"
4. Choose a save location
5. Verify a file is downloaded
6. Open the file and verify it contains the settings
7. Verify the format is readable (JSON or similar)

### Test 17: Import preferences

1. Have a previously exported preferences file
2. Change current preferences
3. Click "Import Preferences"
4. Select the file
5. Confirm the import
6. Verify preferences are replaced with imported ones
7. Verify a success message appears
8. Verify the changes take effect immediately

### Test 18: Auto-save behavior

1. Go to notification preferences
2. Ensure auto-save is enabled
3. Change a preference
4. Wait 2-3 seconds
5. Verify a "Saved" indicator appears
6. Navigate away from the page
7. Return to the page
8. Verify the change is persisted

### Test 19: Unsaved changes warning

1. Go to notification preferences
2. Disable auto-save
3. Change a preference
4. Try to navigate away
5. Verify a warning dialog appears
6. Choose "Save" and verify the change is saved
7. Make another change
8. Try to navigate away again
9. Choose "Discard" and verify the change is not saved

### Test 20: Permission denied handling

1. Deny desktop notification permissions at the OS level
2. Go to notification preferences
3. Try to enable "Desktop Notifications"
4. Save
5. Verify an error message appears
6. Verify instructions to enable permissions are shown
7. Follow the instructions to enable permissions
8. Return to the app
9. Try again and verify it works

### Test 21: Time zone configuration

1. Go to notification preferences
2. View the time zone setting
3. Change the time zone
4. Save
5. Schedule a showing for a specific time
6. Verify the reminder is scheduled in the correct time zone
7. Change the time zone again
8. Verify all time-based preferences update accordingly

### Test 22: Different quiet hours for weekdays/weekends

1. Configure different quiet hours for weekdays and weekends
2. Save
3. Verify the current day uses the appropriate schedule
4. Test on a weekday
5. Test on a weekend
6. Verify the correct schedule is applied

### Test 23: Notification preview

1. Change a notification setting
2. Click "Preview" next to the setting
3. Verify a preview of the notification appears
4. Verify it uses the current configuration
5. Adjust settings based on the preview
6. Save the final configuration

### Test 24: Granular lead notification control

1. Go to "Leads" category
2. Configure each sub-option independently:
   - New lead: desktop + in-app
   - Lead assigned: email only
   - Lead status changed: in-app only
   - Lead converted: desktop + in-app + email
3. Save
4. Trigger each event
5. Verify each uses the configured channels
6. Verify the configuration is correct

### Test 25: Email notification testing

1. Enable email notifications
2. Configure email address
3. Click "Send Test Email"
4. Verify the test email is received
5. Verify the email content is correct
6. Trigger an event that should send an email
7. Verify the email is received
8. Verify the email is professionally formatted

### Test 26: Priority levels

1. Configure different priority levels for various notification types
2. Save
3. Trigger a high-priority notification
4. Verify it overrides quiet hours
5. Trigger a low-priority notification during quiet hours
6. Verify it respects quiet hours
7. Verify the visual distinction between priorities

### Test 27: Content preview settings

1. Configure "Show notification content" to "Hide all content"
2. Save
3. Receive a notification
4. Verify the content is hidden
5. Verify only generic text is shown
6. Change to "Always show full content"
7. Verify full content is displayed

### Test 28: Auto-dismiss duration

1. Set auto-dismiss to 10 seconds
2. Save
3. Receive a notification
4. Wait 10 seconds without interacting
5. Verify it automatically dismisses
6. Test with critical notification
7. Verify it does not auto-dismiss

### Test 29: Snooze duration options

1. Configure snooze durations: 5 min, 15 min, 1 hour
2. Save
3. Receive a notification
4. Click snooze
5. Verify only the configured options appear
6. Verify custom durations are not allowed
7. Select a duration
8. Verify it works correctly

### Test 30: Notification statistics

1. Go to notification preferences
2. Click "View Statistics"
3. Verify statistics are displayed
4. Verify data is accurate
5. Verify the time period can be changed
6. Verify the breakdown by type is correct
7. Use statistics to optimize settings

### Test 31: Validation testing

1. Try to set quiet hours end time before start time
2. Verify a validation error appears
3. Try to enter invalid email address
4. Verify validation error
5. Try to set negative values for numeric fields
6. Verify validation error
7. Fix all errors and save successfully

### Test 32: Preferences search

1. Go to notification preferences
2. Type "email" in the search box
3. Verify only email-related settings are shown
4. Clear the search
5. Verify all settings return
6. Search for "desktop"
7. Verify correct filtering
8. Test with various search terms

### Test 33: Cross-platform testing

1. Test preferences on Windows
2. Verify all controls work
3. Test on macOS
4. Verify all controls work
5. Test on Linux
6. Verify all controls work
7. Document any platform-specific issues

### Test 34: Accessibility testing

1. Navigate preferences using only keyboard
2. Verify all controls are accessible
3. Test with screen reader
4. Verify all options are announced
5. Test with high contrast mode
6. Verify visibility of all controls
7. Test with text scaling enabled
8. Verify layout remains usable

### Test 35: Performance testing

1. Open notification preferences page
2. Verify it loads within 2 seconds
3. Make multiple rapid changes
4. Verify auto-save doesn't cause performance issues
5. Test with many custom preferences
6. Verify filtering and search are responsive

## Acceptance Criteria

- [ ] Notification preferences page is accessible from Settings menu
- [ ] All notification categories are displayed and organized
- [ ] Master toggle enables/disables all notifications
- [ ] Individual category toggles work independently
- [ ] Sub-category settings are configurable (e.g., per lead event type)
- [ ] Channel selection (desktop, in-app, email) works per event
- [ ] Desktop notifications can be enabled/disabled globally and per event
- [ ] In-app notifications can be enabled/disabled globally and per event
- [ ] Email notifications can be enabled/disabled globally and per event
- [ ] Notification sounds can be enabled/disabled
- [ ] Notification volume is adjustable
- [ ] Multiple sound options are available
- [ ] Quiet hours / Do Not Disturb can be configured
- [ ] Quiet hours support different schedules for weekdays and weekends
- [ ] Critical notifications can override quiet hours (configurable)
- [ ] Default reminder times for showings are configurable
- [ ] Default reminder times for tasks are configurable
- [ ] Task due reminder timing is configurable (hours before due)
- [ ] Task overdue notification timing is configurable
- [ ] Maximum notifications per hour can be set
- [ ] Digest mode can be enabled with configurable delivery time
- [ ] Similar notifications can be batched
- [ ] Test notification functionality works for all channels
- [ ] Reset to defaults functionality works
- [ ] Export preferences works and produces valid file
- [ ] Import preferences works and applies settings correctly
- [ ] Auto-save functionality works (if enabled)
- [ ] Manual save with unsaved changes warning works
- [ ] Notification permission denied is handled gracefully
- [ ] Time zone can be configured
- [ ] All time-based preferences respect the configured time zone
- [ ] Notification preview shows how notification will look
- [ ] Granular control available for all event types:
  - [ ] Leads (new, assigned, status changed, converted, qualified)
  - [ ] Tasks (assigned, due soon, overdue, completed)
  - [ ] Showings (scheduled, reminder, starting soon, completed, cancelled)
  - [ ] Transactions (created, status changed, closing, completed)
  - [ ] Emails (received, sent, failure)
  - [ ] Contacts (shared, updated)
  - [ ] Properties (status changed, price changed, sold)
  - [ ] System (backup, updates, security)
- [ ] Email notification address is configurable
- [ ] Email notifications can be tested
- [ ] Notification priority levels are configurable
- [ ] Notification content preview settings work (full, sender only, hidden)
- [ ] Auto-dismiss duration is configurable
- [ ] Critical notifications do not auto-dismiss
- [ ] Snooze duration options are configurable
- [ ] Notification statistics are available and accurate
- [ ] Preference validation prevents invalid configurations
- [ ] Preferences search helps find specific settings
- [ ] All preferences persist across application restarts
- [ ] Preferences page loads within 2 seconds
- [ ] Keyboard navigation works for all controls
- [ ] Screen reader compatibility for all options
- [ ] High contrast mode supported
- [ ] Text scaling doesn't break layout
- [ ] Works on Windows, macOS, and Linux
- [ ] Changes take effect immediately or after save (as designed)
- [ ] No notification is delivered if globally disabled
- [ ] Preferences are stored securely and encrypted
- [ ] Preference changes are logged for audit purposes
