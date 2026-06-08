I'll create the user story for In-App Notifications (US-117).

---

# US-117: In-App Notifications

## User Story

**As a** user of the application  
**I want to** see a centralized feed of notifications within the app  
**So that** I can stay informed about important events, track recent activities, and never miss critical updates even if I miss desktop notifications

## Priority

**MVP:** Must Have

**Rationale:** Desktop notifications are transient and easy to miss, especially when the user is away from their computer. An in-app notification center provides a persistent, searchable record of all important events. This is essential for daily workflow management, audit trails, and ensuring users can catch up on what happened while they were away. It complements desktop notifications and provides a reliable fallback when notifications are disabled or unavailable.

## Estimated Effort

**Size:** Medium-Large (M-L) - 4 days

**Breakdown:**
- 2 hours: Design notification data model and database schema
- 3 hours: Create notification service/manager
- 2 hours: Design notification bell icon with badge counter
- 3 hours: Implement notification dropdown panel
- 4 hours: Build full notification center page with filters
- 3 hours: Implement mark as read/unread functionality
- 2 hours: Implement bulk actions (mark all as read, clear all)
- 3 hours: Add notification categories and types
- 3 hours: Implement notification generation triggers
- 2 hours: Add notification preferences integration
- 3 hours: Implement real-time updates
- 3 hours: Add search and filter capabilities
- 3 hours: Test and polish UI/UX

## Dependencies

**Depends on:** 
- US-116 (Desktop Notifications for New Leads)
- US-119 (Notification Preferences/Settings)
- US-030 (Create a New Lead)
- US-056 (Schedule a Showing)
- US-080 (Create a Task)
- US-070 (Send Email to Contact)

**Blocks:** 
- US-118 (Notification for Showing Reminders)
- US-120 (Notification for Email Received)
- US-121 (Notification for Task Reminders - if separated from US-084)

## Description

The application should include a comprehensive in-app notification system that captures and displays important events and activities. A notification bell icon with an unread count badge should be visible in the main navigation/header at all times. Clicking the bell opens a dropdown panel showing the most recent notifications (typically 10-20), with quick actions to mark as read, dismiss, or navigate to the related item.

A full notification center page should also be available, accessible from the dropdown panel, that provides:
- Complete notification history (paginated)
- Filtering by notification type (leads, tasks, showings, emails, system)
- Filtering by read/unread status
- Search functionality
- Bulk actions (mark all as read, delete all, etc.)
- Date range filtering
- Grouping by date (Today, Yesterday, This Week, Earlier)

Notifications should be generated for various events:
- **New Leads**: Lead created, imported, or assigned
- **Lead Updates**: Status changes, qualification results, conversion
- **Tasks**: Task assigned, due soon, overdue, completed
- **Showings**: Showing scheduled, upcoming, completed, cancelled
- **Transactions**: Status changes, closing dates approaching, completed
- **Emails**: New email received, email sent, bounce/failure
- **System**: Updates available, backup completed, security alerts
- **AI**: Qualification completed, insights available

Each notification should include:
- Icon indicating notification type
- Title and description
- Timestamp (relative and absolute)
- Read/unread status
- Action button to navigate to related item
- Dismiss/delete option
- Optional: context preview (e.g., lead name, property address)

Notifications should respect user preferences for which types of notifications to receive. The notification count badge should update in real-time as new notifications arrive. Notifications should persist across app restarts and be tied to the user account.

## BDD Scenarios

### Scenario 1: Notification bell with badge counter

```
Given I am logged in and using the application
  And I have 3 unread notifications
When I view the main interface
Then I should see a notification bell icon in the header
  And a red badge with the number "3" should be displayed on the bell
  And the badge should be visible but not obstruct the icon
```

### Scenario 2: Open notification dropdown

```
Given I have unread notifications
When I click the notification bell icon
Then a dropdown panel should appear
  And it should show the 10 most recent notifications
  And each notification should display:
    - Type icon
    - Title and description
    - Relative timestamp
    - Read/unread indicator
  And there should be a "View All" link to see the full notification center
  And there should be a "Mark All as Read" option
```

### Scenario 3: Unread notification styling

```
Given I have a mix of read and unread notifications
When I view the notification dropdown
Then unread notifications should be visually distinct (e.g., bold text, blue dot, highlighted background)
  And read notifications should have a lighter/gray appearance
```

### Scenario 4: Click notification to navigate

```
Given I have a notification about a new lead
When I click on that notification
Then the notification should be marked as read
  And I should be navigated to the related item (e.g., lead details page)
  And the dropdown should close
  And the badge count should decrease by 1
```

### Scenario 5: Mark individual notification as read

```
Given I have an unread notification in the dropdown
When I hover over the notification
  And I click the "mark as read" icon
Then the notification should be marked as read
  And the badge count should update
  And the visual styling should change to "read" state
```

### Scenario 6: Mark all as read

```
Given I have multiple unread notifications
When I click "Mark All as Read" in the dropdown
Then all notifications should be marked as read
  And the badge counter should disappear or show 0
  And a confirmation message should appear
```

### Scenario 7: Dismiss/delete notification

```
Given I have a notification in the dropdown
When I click the dismiss (X) icon on that notification
Then the notification should be removed from the dropdown
  And it should be deleted from the notification center
  And the badge count should update if it was unread
```

### Scenario 8: Real-time notification arrival

```
Given I am using the application with the notification dropdown closed
When a new notification is generated (e.g., new lead assigned)
Then the badge count should increment immediately
  And if the dropdown is open, the new notification should appear at the top
  And a subtle animation should draw attention to the new notification
```

### Scenario 9: Open full notification center

```
Given I have the notification dropdown open
When I click "View All Notifications" or "See All"
Then I should be navigated to a full notification center page
  And the page should show all notifications in reverse chronological order
  And it should include filters and search
  And it should be paginated or use infinite scroll
```

### Scenario 10: Filter notifications by type

```
Given I am in the full notification center
  And I have notifications of various types
When I click the "Leads" filter
Then only lead-related notifications should be displayed
  And the count should update to show "X Lead Notifications"
  And other type filters should be available
```

### Scenario 11: Filter by read/unread status

```
Given I am in the full notification center
When I select "Unread" from the status filter
Then only unread notifications should be displayed
  And the badge count should match the displayed count
  And I should be able to switch between All, Read, and Unread
```

### Scenario 12: Search notifications

```
Given I am in the full notification center
When I type "lead" in the search box
Then notifications containing "lead" in title, description, or context should be displayed
  And the search should be case-insensitive
  And results should update as I type
```

### Scenario 13: Notification grouping by date

```
Given I am in the full notification center
When I view the notification list
Then notifications should be grouped by date:
  - Today
  - Yesterday
  - This Week
  - Earlier
  And each group should have a header label
```

### Scenario 14: Notification for new lead

```
Given a new lead is created (manually or via import)
When the lead is successfully saved
Then an in-app notification should be generated
  And the title should be "New Lead Added"
  And the description should include the lead's name
  And clicking it should open the lead details page
```

### Scenario 15: Notification for task due soon

```
Given I have a task with a due date tomorrow
When the system processes notifications (e.g., on app start or hourly)
Then a notification should be generated: "Task Due Tomorrow: [Task Name]"
  And it should be marked with the task icon
  And clicking it should open the task
```

### Scenario 16: Notification for overdue task

```
Given I have a task that was due yesterday
When the task becomes overdue
Then a notification should be generated: "Task Overdue: [Task Name]"
  And it should be highlighted (e.g., red icon or warning indicator)
  And clicking it should open the task
```

### Scenario 17: Notification for showing reminder

```
Given I have a showing scheduled for tomorrow
When the system processes notifications
Then a notification should be generated: "Showing Tomorrow: [Property Address]"
  And it should include the time and contact name
  And clicking it should open the showing details
```

### Scenario 18: Notification for email received

```
Given I have email integration enabled
  And I received a new email from a contact
When the email is synced
Then a notification should be generated: "New Email from [Contact Name]"
  And it should show the email subject
  And clicking it should open the email or contact's timeline
```

### Scenario 19: Notification preferences respected

```
Given I have disabled notifications for "Task Reminders" in preferences
When a task reminder is due
Then no in-app notification should be generated
  And no desktop notification should appear
  And the system should still log the event internally
```

### Scenario 20: Notification for system event

```
Given a system event occurs (e.g., backup completed, update available)
When the event happens
Then a system notification should be generated
  And it should be clearly marked as a "System" notification
  And it should have appropriate priority/styling
```

### Scenario 21: Notification persistence across restarts

```
Given I have unread notifications
When I close and restart the application
Then my unread notifications should still be there
  And the badge count should be restored
  And the notification state should be unchanged
```

### Scenario 22: Bulk delete notifications

```
Given I am in the full notification center
  And I have multiple notifications selected
When I click "Delete Selected"
Then the selected notifications should be removed
  And a confirmation dialog should appear first
  And the action can be undone (optional)
```

## Manual Testing Steps

### Test 1: Notification bell visibility

1. Log into the application
2. Verify the notification bell is visible in the header
3. Verify it's positioned consistently across all pages
4. Test on different screen sizes
5. Verify it doesn't overlap with other UI elements

### Test 2: Badge counter

1. Start with 0 notifications
2. Create a new lead
3. Verify badge appears with "1"
4. Create 2 more leads
5. Verify badge updates to "3"
6. Mark one as read
7. Verify badge updates to "2"
8. Mark all as read
9. Verify badge disappears or shows "0"

### Test 3: Notification dropdown

1. Have multiple notifications (mix of read/unread)
2. Click the bell icon
3. Verify dropdown appears
4. Verify it shows recent notifications
5. Verify read/unread styling is correct
6. Click outside the dropdown
7. Verify it closes

### Test 4: Notification interaction

1. Open notification dropdown
2. Click on a notification
3. Verify it navigates to the correct page
4. Verify the notification is marked as read
5. Verify the dropdown closes
6. Verify the badge count decreased

### Test 5: Mark as read actions

1. Open dropdown with unread notifications
2. Hover over an unread notification
3. Click the mark-as-read icon
4. Verify it becomes read
5. Test "Mark All as Read" button
6. Verify all become read
7. Verify badge clears

### Test 6: Dismiss notifications

1. Open dropdown
2. Click dismiss (X) on a notification
3. Verify it's removed
4. Open full notification center
5. Verify it's also removed from there
6. Verify badge count updated

### Test 7: Real-time updates

1. Keep the app open on any page
2. Trigger an event that creates a notification (e.g., import leads)
3. Verify the badge count updates immediately
4. If dropdown is open, verify new notification appears at top
5. Verify no page refresh is needed

### Test 8: Full notification center page

1. Click "View All" from dropdown
2. Verify navigation to notification center page
3. Verify all notifications are listed
4. Test pagination or infinite scroll
5. Verify date grouping is correct
6. Test back navigation

### Test 9: Filter by type

1. Open notification center
2. Create notifications of different types (lead, task, showing, email)
3. Click "Leads" filter
4. Verify only lead notifications show
5. Click "Tasks" filter
6. Verify only task notifications show
7. Click "All" to reset
8. Verify all notifications show again

### Test 10: Filter by read/unread

1. Have a mix of read and unread notifications
2. Click "Unread" filter
3. Verify only unread show
4. Click "Read" filter
5. Verify only read show
6. Click "All"
7. Verify all show

### Test 11: Search functionality

1. Open notification center
2. Type a keyword in search (e.g., "John" for a contact name)
3. Verify matching notifications appear
4. Clear search
5. Verify all notifications return
6. Test with different keywords
7. Test case-insensitive search

### Test 12: Notification types coverage

1. Create a new lead → verify lead notification
2. Schedule a showing → verify showing notification
3. Create a task with due date → verify task notification
4. Send an email → verify email notification
5. Mark a lead as converted → verify conversion notification
6. Update transaction status → verify transaction notification
7. Verify each type has appropriate icon and styling

### Test 13: Preferences integration

1. Go to notification preferences
2. Disable "Task Notifications"
3. Create a task
4. Verify no task notification appears
5. Re-enable task notifications
6. Create another task
7. Verify notification appears

### Test 14: Persistence

1. Create several notifications
2. Mark some as read
3. Close the application
4. Restart the application
5. Verify notifications are still there
6. Verify read/unread state is preserved
7. Verify badge count is correct

### Test 15: Performance with many notifications

1. Generate 100+ notifications (bulk import leads)
2. Open the notification center
3. Verify the page loads within 2 seconds
4. Scroll through the list
5. Verify smooth scrolling
6. Test filtering performance
7. Test search performance

### Test 16: Bulk actions

1. Open notification center
2. Select multiple notifications
3. Click "Mark as Read"
4. Verify all selected become read
5. Select multiple again
6. Click "Delete"
7. Confirm deletion
8. Verify they're removed

### Test 17: Notification for system events

1. Trigger a backup
2. Verify backup completion notification
3. Simulate an update available
4. Verify update notification
5. Test security alert (e.g., failed login)
6. Verify security notification

### Test 18: Cross-page consistency

1. Navigate to different pages (contacts, leads, properties, etc.)
2. Verify notification bell is always visible
3. Verify badge count is consistent
4. Verify dropdown works from all pages

### Test 19: Accessibility

1. Test keyboard navigation (Tab to bell, Enter to open)
2. Test screen reader compatibility
3. Verify ARIA labels are present
4. Test with high contrast mode
5. Verify focus indicators are visible

### Test 20: Notification clearing

1. Open notification center
2. Click "Clear All" or "Delete All Read"
3. Verify confirmation dialog
4. Confirm action
5. Verify notifications are removed
6. Verify badge updates

## Acceptance Criteria

- [ ] Notification bell icon is visible in the header on all pages
- [ ] Badge counter shows accurate unread count
- [ ] Badge updates in real-time as notifications arrive
- [ ] Badge has visual distinction (color, size, position)
- [ ] Clicking bell opens dropdown with recent notifications
- [ ] Dropdown shows 10-20 most recent notifications
- [ ] Each notification displays type icon, title, description, timestamp
- [ ] Read and unread notifications are visually distinct
- [ ] Clicking notification marks it as read and navigates to related item
- [ ] Dropdown closes when clicking outside
- [ ] "Mark All as Read" functionality works
- [ ] Individual notification dismissal works
- [ ] Full notification center page is accessible from dropdown
- [ ] Notification center shows complete history
- [ ] Notifications are grouped by date (Today, Yesterday, etc.)
- [ ] Filtering by type works (Leads, Tasks, Showings, Emails, System)
- [ ] Filtering by read/unread status works
- [ ] Search functionality works across all notification fields
- [ ] Notifications persist across application restarts
- [ ] Notification preferences are respected
- [ ] Real-time updates work without page refresh
- [ ] Bulk actions (mark as read, delete) work
- [ ] Performance is acceptable with 100+ notifications
- [ ] Notifications are generated for all relevant events:
  - [ ] New leads (created, imported, assigned)
  - [ ] Lead updates (status change, qualification, conversion)
  - [ ] Tasks (assigned, due soon, overdue, completed)
  - [ ] Showings (scheduled, upcoming, completed)
  - [ ] Transactions (status changes, closing dates)
  - [ ] Emails (received, sent, failures)
  - [ ] System events (backups, updates, security)
- [ ] Notifications include appropriate context and deep links
- [ ] Keyboard navigation works
- [ ] Screen reader compatibility
- [ ] Responsive design works on different screen sizes
- [ ] Timestamps are accurate and use relative formatting
- [ ] No notification spam (proper rate limiting and grouping)
