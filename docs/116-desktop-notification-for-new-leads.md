I'll create a comprehensive user story for Desktop Notifications for New Leads, following the format you provided.

---

# US-116: Desktop Notifications for New Leads

## User Story

**As a** real estate agent  
**I want to** receive desktop notifications when new leads are added or assigned to me  
**So that** I can respond quickly to potential clients and never miss an opportunity

## Priority

**MVP:** Must Have

**Rationale:** Real estate is a time-sensitive business where the speed of lead response dramatically impacts conversion rates. Studies show that responding to a lead within 5 minutes makes you 21x more likely to qualify that lead. Without desktop notifications, agents must constantly check the app manually, which leads to missed opportunities and lost revenue. Desktop notifications enable proactive, real-time awareness without disrupting workflow.

## Estimated Effort

**Size:** Medium (M) - 3 days

**Breakdown:**
- 2 hours: Research native notification APIs (Electron Notification, Windows toast, macOS Notification Center, libnotify)
- 3 hours: Design notification service architecture
- 2 hours: Implement permission request flow
- 3 hours: Implement notification trigger on lead creation
- 3 hours: Implement notification trigger on lead assignment
- 2 hours: Add notification preferences/settings integration
- 2 hours: Implement click-to-open behavior (deep link to lead)
- 2 hours: Handle notification when app is in foreground vs background
- 2 hours: Add notification icons, branding, and styling
- 3 hours: Test on Windows, macOS, and Linux

## Dependencies

**Depends on:** 
- US-030 (Create a New Lead)
- US-032 (Assign Lead Status)
- US-031 (View Lead List)
- Notification Preferences/Settings (to be created as US-119)
- OS notification system availability

**Blocks:** 
- US-117 (In-App Notifications)
- US-118 (Notification for Showing Reminders)
- US-120 (Notification for Email Received)

## Description

When a new lead is created in the system (either manually by the user, imported from CSV, or fetched from a source), the system should display a native desktop notification. The notification should appear regardless of whether the application is in the foreground, minimized, or in the system tray.

The notification should include:
- A clear title indicating a new lead
- The lead's name and source (if available)
- A brief preview of lead details (e.g., budget range, property interest)
- An action to open the lead directly in the application
- An option to dismiss the notification

The user must grant notification permissions on first use. Notification behavior should be configurable through notification preferences, allowing users to:
- Enable/disable desktop notifications globally
- Enable/disable notifications for new leads specifically
- Enable/disable notifications for assigned leads
- Choose notification sound on/off
- Choose whether notifications appear when the app is in focus

Clicking the notification should open the application and navigate directly to the lead's details page. If the app is not running, clicking the notification should launch the app and then navigate to the lead.

## BDD Scenarios

### Scenario 1: First-time permission request

```
Given I am a new user of the application
  And I have just created my first lead
When the system attempts to show a desktop notification
Then I should see an OS-level permission prompt asking if I want to allow notifications
  And if I grant permission, the notification should appear
  And if I deny permission, no notification should appear
  And the system should remember my choice
```

### Scenario 2: Notification on new lead creation

```
Given I have desktop notifications enabled
  And I am on any screen in the application
When I create a new lead
Then a desktop notification should appear within 2 seconds
  And the notification title should be "New Lead Added"
  And the notification body should include the lead's name
  And the notification body should include the lead source (if available)
```

### Scenario 3: Notification on lead import

```
Given I have desktop notifications enabled
  And I am importing leads from a CSV file
When the import is complete
Then a desktop notification should appear with title "X New Leads Imported"
  And the body should show the count of imported leads
  And clicking it should navigate to the lead list filtered to the new imports
```

### Scenario 4: Notification on lead assignment

```
Given I have desktop notifications enabled for lead assignments
  And another team member assigns a lead to me
When the lead is assigned to me
Then a desktop notification should appear
  And the title should be "New Lead Assigned"
  And the body should include the lead's name and the assigner's name
```

### Scenario 5: Click notification to open lead

```
Given a desktop notification is displayed for a new lead
When I click the notification
Then the application should come to the foreground
  And I should be navigated directly to the new lead's details page
  And the notification should be dismissed
```

### Scenario 6: Launch app from notification when closed

```
Given the application is not running
  And a notification was triggered for a new lead
When I click the notification
Then the application should launch
  And after authentication, navigate to the new lead's details page
```

### Scenario 7: Suppress notification when app is in focus and preference is set

```
Given I am actively using the application
  And my preference is set to suppress notifications when app is in focus
When a new lead is created
Then no desktop notification should appear
  But the in-app notification badge/feed should still be updated
```

### Scenario 8: Notification when app is minimized

```
Given the application is minimized to the system tray
  And I have desktop notifications enabled
When a new lead is created
Then a desktop notification should appear
  And clicking it should restore the application window
  And navigate to the new lead
```

### Scenario 9: Disable notifications via preferences

```
Given I have desktop notifications currently enabled
When I navigate to notification preferences
  And I toggle off "Desktop Notifications for New Leads"
  And I save my preferences
Then no desktop notifications should appear for new leads
  And the change should persist across application restarts
```

### Scenario 10: Notification with action buttons (optional)

```
Given a desktop notification is displayed for a new lead
When I view the notification
Then I should see action buttons (if supported by OS):
  - "View Lead" - opens the lead
  - "Snooze" - dismisses for 1 hour
  - "Mark as Contacted" - quick action
```

## Manual Testing Steps

### Test 1: First-time permission flow

1. Install the application fresh
2. Create a new lead
3. Verify OS permission prompt appears
4. Click "Allow"
5. Verify notification appears
6. Restart the app and create another lead
7. Verify no prompt appears (already granted)
8. Repeat with "Deny" to test denial flow

### Test 2: New lead notification

1. Ensure notifications are enabled
2. Open the application
3. Create a new lead with full details (name, source, budget)
4. Verify notification appears within 2 seconds
5. Verify all information is correctly displayed
6. Click the notification
7. Verify the lead details page opens

### Test 3: Multiple rapid notifications

1. Create 3 leads in quick succession (within 10 seconds)
2. Verify each notification appears
3. Verify they don't replace each other
4. Click each one to verify they open the correct lead

### Test 4: Notification from import

1. Prepare a CSV with 5 leads
2. Import the CSV
3. Verify a single summary notification appears
4. Click it
5. Verify the lead list opens with the new leads highlighted

### Test 5: Notification when minimized

1. Open the application
2. Create a lead
3. Minimize the application to system tray
4. Create another lead
5. Verify notification appears
6. Click notification
7. Verify app restores to focus

### Test 6: Notification when app is closed

1. Close the application completely
2. Trigger a lead creation through another mechanism (e.g., scheduled import)
3. Wait for notification
4. Click the notification
5. Verify the app launches
6. Log in if required
7. Verify it navigates to the new lead

### Test 7: Click-to-open behavior

1. Create a lead
2. Wait for notification
3. Click the notification body
4. Verify the app opens
5. Verify the correct lead details are shown
6. Test clicking when app is in background
7. Test clicking when app is closed

### Test 8: Disable/enable via preferences

1. Go to Settings > Notifications
2. Toggle off "Desktop Notifications for New Leads"
3. Create a new lead
4. Verify no notification appears
5. Toggle it back on
6. Create another lead
7. Verify notification appears

### Test 9: Suppress when in focus

1. Enable "Suppress notifications when app is in focus"
2. Have the application in focus
3. Create a new lead
4. Verify no desktop notification
5. Verify in-app notification is still recorded
6. Minimize the app
7. Create another lead
8. Verify desktop notification appears

### Test 10: Notification sound

1. Enable notification sounds
2. Create a lead
3. Verify sound plays
4. Disable notification sounds
5. Create another lead
6. Verify no sound plays
7. Verify visual notification still appears

### Test 11: Cross-platform testing

1. Test on Windows 10
2. Test on Windows 11
3. Test on macOS (latest)
4. Test on macOS (older version)
5. Test on Ubuntu Linux
6. Test on Fedora Linux
7. Document any platform-specific issues

### Test 12: Notification persistence

1. Create a lead
2. Wait for notification
3. Do not click it
4. Wait 10 seconds
5. Verify notification still appears in notification center
6. Close notification
7. Verify it disappears

## Acceptance Criteria

- [ ] OS-level permission request is shown on first notification attempt
- [ ] Desktop notification appears within 2 seconds of new lead creation
- [ ] Notification shows lead name and source
- [ ] Notification shows lead budget range (if available)
- [ ] Notification shows property interest (if available)
- [ ] Clicking notification opens the lead details page
- [ ] Clicking notification when app is closed launches the app
- [ ] Clicking notification when app is minimized restores and focuses the app
- [ ] Notifications can be enabled/disabled via preferences
- [ ] Notifications can be suppressed when app is in focus (configurable)
- [ ] Multiple notifications for multiple leads don't replace each other
- [ ] Notification includes app branding/icon
- [ ] Notification sound can be toggled on/off
- [ ] Notification preferences persist across app restarts
- [ ] Works on Windows 10/11
- [ ] Works on macOS
- [ ] Works on Linux (Ubuntu, Fedora)
- [ ] Notifications appear even when app is in system tray
- [ ] Notifications are queued properly during offline/closed state
- [ ] Notification click respects authentication requirements
- [ ] No notification spam (rate limiting for multiple rapid events)
- [ ] Graceful fallback if notification system is unavailable
- [ ] In-app notification feed/center is updated in parallel
