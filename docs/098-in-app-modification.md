# US-098: In-App Notifications

## User Story

**As a** user  
**I want to** see notifications within OurCRM  
**So that** I don't miss important events even when I'm actively using the application

## Priority

**MVP:** Must Have

**Rationale:** While desktop notifications work when OurCRM is in the background, in-app notifications work when the user is actively using the app. They provide a persistent, dismissable record of important events and complement desktop notifications.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design in-app notification system
- 2 hours: Create notification center UI
- 1 hour: Implement notification display (toast/banner)
- 1 hour: Add notification persistence
- 1 hour: Implement notification actions
- 1 hour: Add notification history
- 1 hour: Test notification display
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-097 (Desktop Notifications for New Leads), US-150 (Desktop Notifications Setup)

**Blocks:** US-099 (Notification Preferences)

## Description

OurCRM should display notifications within the application for important events. These can take two forms:
1. **Toast/Banner notifications** - Temporary, auto-dismissing notifications for immediate events
2. **Notification center** - A persistent list of all notifications that users can review

In-app notifications should work alongside desktop notifications and provide a complete notification experience whether the app is active or in the background.

## BDD Scenarios

### Scenario 1: Receive in-app notification

```
Given I am actively using OurCRM
When an important event occurs
  (new lead, task due, showing reminder, etc.)
Then I should see an in-app notification
  As a toast or banner
  That appears at the top or corner of the window
  And auto-dismisses after a few seconds
```

### Scenario 2: Notification content

```
Given I receive an in-app notification
When I look at it
Then it should show:
  - Icon (for the event type)
  - Title (e.g., "New Lead: John Smith")
  - Brief description
  - Timestamp
  - Action button (if applicable)
```

### Scenario 3: Toast notifications auto-dismiss

```
Given a toast notification is displayed
When 5-10 seconds pass
Then the notification should auto-dismiss
  But can be manually dismissed sooner
  And the event is still logged in the notification center
```

### Scenario 4: Notification center

```
Given I have received notifications
When I click the notification bell icon
Then the notification center should open
  Showing a list of all notifications
  With the most recent at the top
  And the ability to scroll through history
```

### Scenario 5: Click notification to take action

```
Given I see a notification in the notification center
When I click on it
Then I should be taken to the related item:
  - New lead → Lead details
  - Task due → Task details
  - Showing reminder → Calendar event
  - Email received → Email/Contact
```

### Scenario 6: Mark notifications as read

```
Given I have unread notifications
When I view the notification center
Then I should see which are read/unread
  And I can mark them as read
  Or mark all as read
  And the count should update
```

### Scenario 7: Notification badge

```
Given I have unread notifications
When I look at the notification bell icon
Then I should see a badge with the count
  E.g., "🔔 (3)" for 3 unread notifications
  And the badge disappears when all are read
```

### Scenario 8: Persistent notification history

```
Given I have received notifications
When I view the notification center
Then I should see notifications from:
  - Today
  - Yesterday
  - This week
  - Earlier
  And the history is searchable and filterable
```

## Manual Testing Steps

### Test 1: Basic toast notification

1. Trigger an event (e.g., create a lead)
2. Verify the toast notification appears
3. Check the content
4. Verify it auto-dismisses
5. Verify the event is logged

### Test 2: Test notification content

1. Trigger various events
2. Verify each notification has correct content
3. Check icons, titles, descriptions
4. Verify they're informative

### Test 3: Test auto-dismiss

1. Trigger a notification
2. Wait 5-10 seconds
3. Verify it auto-dismisses
4. Manually dismiss another one
5. Verify both are logged

### Test 4: Test notification center

1. Trigger several notifications
2. Click the notification bell
3. Verify the center opens
4. Verify all notifications are listed
5. Verify the most recent is at the top

### Test 5: Test click to navigate

1. Click on a notification
2. Verify it navigates to the related item
3. Test with different notification types
4. Verify each works correctly

### Test 6: Test mark as read

1. Have unread notifications
2. Open the notification center
3. Mark one as read
4. Verify the read status updates
5. Mark all as read
6. Verify the badge disappears

### Test 7: Test notification badge

1. Have unread notifications
2. Verify the badge shows the count
3. Mark some as read
4. Verify the badge updates
5. Mark all as read
6. Verify the badge disappears

### Test 8: Test history

1. Create notifications over several days
2. View the notification center
3. Verify they're grouped by date
4. Test filtering by date
5. Test searching notifications

### Test 9: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Toast notifications appear for important events
- [ ] Notifications show icon, title, description, timestamp
- [ ] Toast notifications auto-dismiss after 5-10 seconds
- [ ] Notification center is accessible via bell icon
- [ ] Notification center shows all notifications
- [ ] Most recent notifications appear first
- [ ] Clicking notification navigates to related item
- [ ] Notifications can be marked as read
- [ ] Unread count badge is shown
- [ ] Notification history is persistent
- [ ] History can be filtered and searched
- [ ] Works on Windows, macOS, and Linux
- [ ] Notifications are timely and accurate
- [ ] UI is intuitive and non-intrusive
