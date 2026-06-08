I'll create the user story for Notification for Showing Reminders (US-118).

---

# US-118: Notification for Showing Reminders

## User Story

**As a** real estate agent  
**I want to** receive timely reminders for upcoming showings  
**So that** I never miss an appointment, arrive prepared, and provide professional service to my clients

## Priority

**MVP:** Must Have

**Rationale:** Missing a showing is one of the most costly mistakes a real estate agent can make. It damages client relationships, wastes the seller's time, and can result in lost listings. Showings are time-sensitive appointments that require preparation and punctuality. Automated reminders ensure agents are aware of upcoming showings with enough lead time to prepare, travel, and handle any last-minute issues. This feature directly impacts client satisfaction, professional reputation, and business success.

## Estimated Effort

**Size:** Medium (M) - 3 days

**Breakdown:**
- 2 hours: Research scheduling and notification APIs
- 3 hours: Design reminder timing configuration system
- 3 hours: Implement reminder scheduling service
- 4 hours: Build desktop notification integration
- 3 hours: Implement in-app notification generation
- 3 hours: Add email reminder option (optional)
- 3 hours: Create reminder management UI
- 2 hours: Implement reminder preferences
- 3 hours: Add calendar integration for reminders
- 2 hours: Implement snooze functionality
- 3 hours: Handle recurring showings
- 3 hours: Test and edge cases (time zones, cancellations, etc.)

## Dependencies

**Depends on:** 
- US-056 (Schedule a Showing)
- US-057 (View Upcoming Showings)
- US-116 (Desktop Notifications for New Leads)
- US-117 (In-App Notifications)
- US-119 (Notification Preferences/Settings)
- US-058 (Mark Showing as Completed)
- US-059 (Add Notes to a Showing)

**Blocks:** None (terminal feature for showing notifications)

## Description

The system should automatically generate reminders for scheduled showings at configurable time intervals before the showing. When a showing is scheduled, the system should create a series of reminders based on user preferences (e.g., 24 hours before, 2 hours before, 30 minutes before).

Each reminder should include:
- Property address and basic details
- Contact/client name
- Showing date and time
- Duration
- Any special instructions or notes
- Quick actions (view details, get directions, call contact, mark as completed)

Reminders should be delivered through multiple channels based on user preferences:
- **Desktop notifications** (primary)
- **In-app notifications** (always, as backup)
- **Email reminders** (optional, for important showings)
- **Calendar alerts** (integrated with system calendar)

The system should handle:
- Reminder timing based on user-configured intervals
- Automatic rescheduling if showing time changes
- Cancellation of reminders if showing is cancelled
- Different reminder urgency levels (high priority for imminent showings)
- Snooze functionality (e.g., remind me again in 15 minutes)
- Time zone awareness (if showing is in different time zone)
- Conflict detection (overlapping showings)

Users should be able to:
- Configure default reminder times
- Set custom reminders for individual showings
- Snooze reminders
- Dismiss reminders
- View all upcoming reminders
- Enable/disable showing reminders globally
- Choose notification channels for reminders

## BDD Scenarios

### Scenario 1: Schedule reminder when creating showing

```
Given I am scheduling a new showing for tomorrow at 2:00 PM
  And my default reminder times are 24 hours, 2 hours, and 30 minutes before
When I save the showing
Then the system should schedule three reminders:
  - One for tomorrow at 2:00 PM (24 hours before)
  - One for tomorrow at 12:00 PM (2 hours before)
  - One for tomorrow at 1:30 PM (30 minutes before)
  And each reminder should include the showing details
```

### Scenario 2: Desktop notification for upcoming showing

```
Given I have a showing scheduled in 2 hours
  And I have desktop notifications enabled for showing reminders
When the 2-hour reminder time arrives
Then a desktop notification should appear
  And the title should be "Showing in 2 hours: [Property Address]"
  And the body should include:
    - Contact name
    - Full address
    - Time
    - Duration
  And action buttons should be available (View, Directions, Snooze)
```

### Scenario 3: In-app notification for showing reminder

```
Given I have a showing scheduled in 30 minutes
  And I have the application open
When the 30-minute reminder time arrives
Then an in-app notification should appear
  And it should be added to the notification center
  And the notification bell badge should update
  And the notification should have a high-priority indicator
```

### Scenario 4: Reminder with preparation details

```
Given I have a showing scheduled for tomorrow
  And I have added notes to the showing (e.g., "Client interested in 3-bedrooms, bring comps")
When the reminder is triggered
Then the notification should include the notes as context
  And it should show any attached documents
  And it should show the contact's phone number for quick access
```

### Scenario 5: Snooze a reminder

```
Given I have received a showing reminder
  And the showing is in 2 hours
When I click "Snooze" and select "15 minutes"
Then the notification should dismiss
  And a new reminder should be scheduled for 15 minutes later
  And the snooze should be limited to prevent infinite snoozing
```

### Scenario 6: Reminder cancellation when showing is cancelled

```
Given I have a showing scheduled with reminders set
When I cancel the showing
Then all pending reminders should be automatically cancelled
  And a confirmation should show "X reminders cancelled"
  And the showing should be removed from upcoming showings
```

### Scenario 7: Reminder rescheduling when showing time changes

```
Given I have a showing scheduled for tomorrow at 2:00 PM
  And reminders are set for 24h, 2h, and 30min before
When I reschedule the showing to tomorrow at 4:00 PM
Then all existing reminders should be cancelled
  And new reminders should be scheduled based on the new time
  And I should see a confirmation of the rescheduled reminders
```

### Scenario 8: Default reminder times configuration

```
Given I am in notification preferences
When I set default showing reminder times to "1 day before" and "1 hour before"
  And I save the preferences
Then all future showings should use these default times
  And the preferences should apply to new showings only
  And existing showings should retain their original reminder times
```

### Scenario 9: Custom reminder for individual showing

```
Given I am creating or editing a showing
When I click "Add Custom Reminder"
  And I set a custom time (e.g., 3 hours before)
Then this reminder should be added in addition to default reminders
  And it should be specific to this showing only
  And it should not affect the default settings
```

### Scenario 10: High-priority reminder for imminent showing

```
Given I have a showing in 15 minutes
When the reminder is triggered
Then it should be marked as high priority
  And the notification should be persistent (require dismissal)
  And it should use attention-grabbing styling (red icon, bold text)
  And the notification should appear even if "suppress when in focus" is enabled
```

### Scenario 11: Reminder for showing happening now

```
Given I have a showing scheduled for the current time
When the showing time arrives
Then a "Showing Starting Now" notification should appear
  And it should include a direct link to mark the showing as in progress
  And it should provide quick access to the contact and property details
```

### Scenario 12: Email reminder for showing

```
Given I have email reminders enabled for showings
  And I have a showing scheduled for tomorrow at 2:00 PM
When the 24-hour reminder time arrives
Then an email should be sent to my registered email address
  And the email should include all showing details
  And the email should have a link to open the showing in the app
  And the email should be professionally formatted
```

### Scenario 13: Reminder with directions

```
Given I have received a showing reminder
  And the property address is known
When I click the "Directions" action
Then my default maps application should open
  And it should show directions from my current location to the property
  And the address should be pre-filled
```

### Scenario 14: Quick call action from reminder

```
Given I have received a showing reminder for a client's showing
When I click the "Call Contact" action
Then my default phone/dialer should open
  And it should be pre-filled with the contact's phone number
  And the contact name should be displayed
```

### Scenario 15: Conflict detection warning

```
Given I have a showing scheduled from 2:00 PM to 3:00 PM
  And I schedule another showing from 2:30 PM to 3:30 PM
When I try to save the second showing
Then I should see a conflict warning
  And the reminder for the overlapping time should highlight the conflict
  And I should be advised to adjust the schedule
```

### Scenario 16: Reminder for recurring showings

```
Given I have scheduled a recurring showing (e.g., every Saturday for 4 weeks)
When the showings are created
Then reminders should be scheduled for each occurrence
  And each reminder should be independent
  And cancelling one occurrence should not affect others
```

### Scenario 17: Reminder preferences override

```
Given I have global showing reminders disabled
  And I enable reminders for a specific important showing
When the reminder time arrives for that specific showing
Then the reminder should be delivered
  And it should be marked as a manual override
  And other showings should not generate reminders
```

### Scenario 18: Reminder log and history

```
Given I have received and dismissed several showing reminders
When I view the notification history
Then I should see all past reminders
  And they should be marked as "delivered" and "dismissed"
  And I should be able to see which reminders were snoozed and when
```

### Scenario 19: Reminder for showing preparation checklist

```
Given I have a showing scheduled for tomorrow
  And I have set up a preparation checklist (e.g., "Print comps", "Prepare listing presentation")
When the 24-hour reminder is triggered
Then the notification should include the checklist
  And I should be able to check off items as I complete them
  And the checklist should be saved for reference
```

### Scenario 20: Time zone handling for reminders

```
Given I am in New York (EST)
  And I schedule a showing for a property in Los Angeles (PST) at 2:00 PM PST
When the reminder is scheduled
Then the system should account for the 3-hour time difference
  And the reminder should be sent at the correct local time
  And the notification should display times in the property's local time zone
  And it should also show my local time for reference
```

## Manual Testing Steps

### Test 1: Schedule showing with default reminders

1. Configure default reminder times (e.g., 24h, 2h, 30min)
2. Schedule a new showing for tomorrow at 2:00 PM
3. Save the showing
4. Verify in the notification settings that 3 reminders are scheduled
5. Verify the reminder times are calculated correctly
6. Check the showing details page for scheduled reminders

### Test 2: Desktop notification delivery

1. Schedule a showing for 5 minutes from now
2. Set a reminder for "5 minutes before"
3. Wait for the reminder time
4. Verify desktop notification appears
5. Verify all showing details are included
6. Verify the notification is high-priority styled
7. Click the notification
8. Verify it opens the showing details

### Test 3: In-app notification for reminder

1. Schedule a showing for 2 hours from now
2. Set a 2-hour reminder
3. Keep the app open
4. Wait for the reminder
5. Verify in-app notification appears
6. Verify notification bell badge updates
7. Verify notification in the notification center
8. Click to view showing details

### Test 4: Multiple reminder times

1. Schedule a showing for tomorrow
2. Set reminders for 24h, 2h, and 30min before
3. Fast-forward system time (or use test mode) to trigger each reminder
4. Verify each reminder is delivered at the correct time
5. Verify each contains appropriate urgency styling

### Test 5: Snooze functionality

1. Receive a showing reminder
2. Click "Snooze" and select "15 minutes"
3. Verify the notification dismisses
4. Wait 15 minutes
5. Verify the reminder reappears
6. Test snooze limits (e.g., max 2 snoozes)
7. Verify the limit is enforced

### Test 6: Cancel showing cancels reminders

1. Schedule a showing with 3 reminders
2. Verify reminders are scheduled
3. Cancel the showing
4. Verify all reminders are cancelled
5. Check the notification center
6. Verify no reminders are delivered for the cancelled showing

### Test 7: Reschedule showing updates reminders

1. Schedule a showing for tomorrow at 2:00 PM
2. Note the scheduled reminder times
3. Reschedule the showing to tomorrow at 5:00 PM
4. Verify old reminders are cancelled
5. Verify new reminders are scheduled for the new time
6. Verify the new reminder times are correct

### Test 8: Custom reminder for individual showing

1. Schedule a new showing
2. Add a custom reminder for 3 hours before
3. Save the showing
4. Verify both default and custom reminders are scheduled
5. Verify the custom reminder is specific to this showing
6. Schedule another showing
7. Verify the new showing only has default reminders

### Test 9: High-priority styling for imminent showing

1. Schedule a showing for 10 minutes from now
2. Wait for the reminder
3. Verify the notification has high-priority styling
4. Verify it's persistent (requires manual dismissal)
5. Verify it appears even with "suppress when in focus" enabled
6. Verify the visual indicators (red icon, bold text)

### Test 10: Email reminder delivery

1. Enable email reminders in preferences
2. Configure SMTP settings
3. Schedule a showing for tomorrow
4. Set a 24-hour reminder
5. Fast-forward to trigger the reminder
6. Verify email is sent to registered address
7. Check email content for showing details
8. Click the link in the email
9. Verify it opens the app to the showing

### Test 11: Directions action

1. Receive a showing reminder
2. Click the "Directions" action
3. Verify default maps application opens
4. Verify the property address is pre-filled
5. Verify directions are calculated
6. Test on Windows (Maps app)
7. Test on macOS (Maps app)
8. Test on Linux (web-based maps)

### Test 12: Quick call action

1. Have a showing reminder with a contact
2. Click "Call Contact" action
3. Verify the dialer/phone app opens
4. Verify the contact's phone number is pre-filled
5. Test with mobile numbers
6. Test with office numbers

### Test 13: Conflict detection

1. Schedule a showing from 2:00 PM to 3:00 PM tomorrow
2. Try to schedule another showing from 2:30 PM to 3:30 PM
3. Verify conflict warning appears
4. Verify the warning shows both showings
5. Adjust the time to avoid conflict
6. Verify no warning appears
7. Save successfully

### Test 14: Reminder preferences configuration

1. Go to Settings > Notifications > Showing Reminders
2. Set default reminder times (e.g., 1 day, 2 hours)
3. Save preferences
4. Schedule a new showing
5. Verify the new defaults are applied
6. Change preferences to different times
7. Schedule another showing
8. Verify the new defaults are used

### Test 15: Enable/disable showing reminders

1. Go to notification preferences
2. Disable all showing reminders
3. Schedule a new showing
4. Verify no reminders are scheduled
5. Re-enable showing reminders
6. Schedule another showing
7. Verify reminders are scheduled

### Test 16: Preparation checklist integration

1. Edit a showing
2. Add preparation items (e.g., "Print comps", "Bring measuring tape")
3. Save the showing
4. When the 24-hour reminder triggers
5. Verify the checklist appears in the notification
6. Check off items
7. Verify they save correctly
8. View the showing details
9. Verify checklist is saved

### Test 17: Time zone handling

1. Set your time zone to EST
2. Schedule a showing for a property in PST at 2:00 PM PST
3. Verify the reminder accounts for the 3-hour difference
4. Verify the notification shows PST time as primary
5. Verify it also shows EST time for reference
6. Test with various time zone combinations
7. Verify DST transitions are handled correctly

### Test 18: Reminder delivery reliability

1. Schedule a showing with reminders
2. Close the application
3. Restart the application
4. Verify the scheduled reminders are still in the queue
5. Wait for the reminder time
6. Verify the reminder is delivered correctly
7. Test with the app offline (verify queuing)
8. Test with the app online (verify delivery)

### Test 19: Snooze limits and escalation

1. Receive a showing reminder
2. Snooze it 2 times
3. Verify the snooze limit is reached
4. Verify the snooze option is disabled
5. Verify the next reminder is more urgent
6. Verify the notification becomes persistent

### Test 20: Recurring showing reminders

1. Schedule a recurring showing (weekly for 4 weeks)
2. Verify all 4 occurrences are created
3. Verify each has independent reminders
4. Cancel one occurrence
5. Verify its reminders are cancelled
6. Verify other occurrences still have their reminders
7. Verify reminders are delivered at the correct times

### Test 21: Cross-platform testing

1. Test reminders on Windows
2. Verify desktop notifications work
3. Test on macOS
4. Verify notification center integration
5. Test on Linux
6. Verify libnotify integration
7. Document any platform-specific issues

### Test 22: Accessibility

1. Test keyboard navigation to reminder actions
2. Verify screen reader announces showing details
3. Test with high contrast mode
4. Verify focus indicators on action buttons
5. Test with text scaling enabled

## Acceptance Criteria

- [ ] Reminders are automatically scheduled when a showing is created
- [ ] Default reminder times are configurable in preferences
- [ ] Users can add custom reminders to individual showings
- [ ] Desktop notifications are delivered at scheduled reminder times
- [ ] In-app notifications are generated for all showing reminders
- [ ] Notifications include all relevant showing details (address, time, contact, notes)
- [ ] High-priority styling for imminent showings (within 1 hour)
- [ ] Notifications are persistent for imminent showings
- [ ] Reminders appear even when "suppress when in focus" is enabled (for high-priority)
- [ ] Snooze functionality works with configurable snooze durations
- [ ] Snooze limits are enforced to prevent infinite snoozing
- [ ] Cancelling a showing cancels all associated reminders
- [ ] Rescheduling a showing updates all reminder times
- [ ] Reminders include quick action buttons (View, Directions, Call, Snooze)
- [ ] Directions action opens default maps application with address
- [ ] Call action opens dialer with contact number
- [ ] Email reminders can be enabled as additional channel
- [ ] Email reminders are professionally formatted with all details
- [ ] Conflict detection warns about overlapping showings
- [ ] Recurring showings have independent reminders for each occurrence
- [ ] Preparation checklists can be attached to showings
- [ ] Checklists appear in reminder notifications
- [ ] Checklist items can be checked off and saved
- [ ] Time zone differences are handled correctly
- [ ] Reminders display times in property's local time zone
- [ ] Reminders persist across application restarts
- [ ] Reminders are queued when app is offline
- [ ] Reminders are delivered when app comes online
- [ ] Reminder preferences are respected (enable/disable per type)
- [ ] Reminder history is maintained in notification center
- [ ] Snoozed reminders are tracked and logged
- [ ] Keyboard navigation works for all reminder actions
- [ ] Screen reader compatibility for all notifications
- [ ] Works on Windows, macOS, and Linux
- [ ] Performance: no impact on app startup or daily use
- [ ] Reminder scheduling is reliable and accurate
- [ ] No duplicate reminders for the same showing
- [ ] Reminders are properly cleaned up after showing completion
- [ ] Reminder delivery times are accurate to within 1 minute
