# US-097: Desktop Notifications for New Leads

## User Story

**As an** agent  
**I want to** receive desktop notifications when new leads come in  
**So that** I can respond quickly and not miss potential clients

## Priority

**MVP:** Must Have

**Rationale:** Speed-to-lead is critical in real estate. The faster an agent responds to a new lead, the higher the conversion rate. Desktop notifications ensure agents are alerted immediately when new leads arrive, even if they're working in another application.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design notification system
- 1 hour: Implement desktop notification for new leads
- 1 hour: Add notification content (lead name, source, action)
- 1 hour: Test notification delivery
- 1 hour: Test on all platforms
- 1 hour: Handle notification permissions

## Dependencies

**Depends on:** US-150 (Desktop Notifications Setup), US-030 (Create a New Lead)

**Blocks:** US-098 (In-App Notifications), US-099 (Notification Preferences)

## Description

When a new lead is created in OurCRM (manually or from a lead source), the system should display a desktop notification on the agent's computer. The notification should include key information: lead name, source, and a quick action to open the lead.

Desktop notifications work across the operating system and appear even when OurCRM is minimized or in the background. They use the native OS notification system for a familiar, integrated experience.

## BDD Scenarios

### Scenario 1: Receive notification for new lead

```
Given a new lead is created
  (manually, from website, from import, etc.)
When the lead is saved to the database
Then I should receive a desktop notification
  With the lead's name
  And the source (if available)
  And a quick action to open the lead
```

### Scenario 2: Notification content

```
Given I receive a notification for a new lead
When I look at the notification
Then it should show:
  - Title: "New Lead: [Lead Name]"
  - Body: "From [Source]" or "Manually added"
  - Icon: OurCRM icon
  - Action button: "Open Lead"
```

### Scenario 3: Click notification to open lead

```
Given I have received a desktop notification
When I click on the notification (or the action button)
Then OurCRM should open (or come to focus)
  And navigate to the new lead
  And show the lead's details
```

### Scenario 4: Notification when app is minimized

```
Given OurCRM is minimized or in the background
When a new lead is created
Then the desktop notification should still appear
  And I should see it in the system tray/notification center
  Even if I'm working in another application
```

### Scenario 5: Multiple notifications

```
Given multiple new leads come in quickly
When notifications are triggered
Then each lead should generate a separate notification
  And they should all be visible in the notification center
  And not overwrite each other
```

### Scenario 6: Notification permissions (first time)

```
Given I am using OurCRM for the first time
When the app tries to send a desktop notification
Then I should be prompted to allow notifications
  (OS-level permission dialog)
  And the choice should be remembered
```

### Test 7: Notification is not sent when disabled

```
Given I have disabled lead notifications in settings
When a new lead is created
Then no desktop notification should appear
  (In-app notification may still show)
```

### Test 8: Notification is logged

```
Given a desktop notification is sent
When the notification appears
Then it should be logged
  So I can review notification history
  And troubleshoot if notifications aren't working
```

## Manual Testing Steps

### Test 1: Basic notification

1. Create a new lead manually
2. Verify the desktop notification appears
3. Check the notification content
4. Verify it shows the lead name and source

### Test 2: Click to open

1. Create a new lead
2. Click on the desktop notification
3. Verify OurCRM opens or comes to focus
4. Verify it navigates to the new lead
5. Verify the lead details are shown

### Test 3: Test when minimized

1. Minimize OurCRM
2. Create a new lead (from another window or via import)
3. Verify the notification appears
4. Click the notification
5. Verify OurCRM comes to focus

### Test 4: Test multiple notifications

1. Create 3 new leads quickly
2. Verify 3 separate notifications appear
3. Check the notification center
4. Verify all 3 are listed

### Test 5: Test permissions

1. On first use, verify the OS permission prompt
2. Allow notifications
3. Create a lead
4. Verify the notification appears
5. Test denying permissions
6. Verify notifications don't appear

### Test 6: Test with notifications disabled

1. Go to Notification settings
2. Disable lead notifications
3. Create a new lead
4. Verify no desktop notification appears
5. Re-enable notifications
6. Verify they work again

### Test 7: Test on all platforms

1. Test on Windows
2. Verify the notification works
3. Test on macOS
4. Verify the notification works
5. Test on Linux
6. Verify the notification works
7. Document any platform-specific issues

### Test 8: Test notification logging

1. Create several leads with notifications
2. Check the log file
3. Verify notification events are logged
4. Verify the logs include lead names and timestamps

## Acceptance Criteria

- [ ] Desktop notification appears when new lead is created
- [ ] Notification shows lead name and source
- [ ] Notification has OurCRM icon
- [ ] Clicking notification opens the lead
- [ ] Notifications work when app is minimized
- [ ] Multiple notifications don't overwrite each other
- [ ] OS permission is requested on first use
- [ ] Notifications can be disabled in settings
- [ ] Notifications are logged
- [ ] Works on Windows, macOS, and Linux
- [ ] Notifications are timely and not delayed
- [ ] Notification content is accurate
- [ ] Quick action works correctly
- [ ] No performance impact from notifications
