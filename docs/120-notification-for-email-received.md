You're right! Let me create US-120 for Notification for Email Received, then we can continue with the Error Handling & Logging stories.

---

# US-120: Notification for Email Received

## User Story

**As a** real estate agent  
**I want to** receive notifications when new emails arrive from my contacts  
**So that** I can respond promptly to client inquiries, maintain professional responsiveness, and never miss important communication

## Priority

**MVP:** Must Have

**Rationale:** Email is a critical communication channel in real estate. Clients expect timely responses to their inquiries, and delays can result in lost opportunities or damaged relationships. Without email notifications, agents must constantly check their email manually, which is inefficient and often leads to delayed responses. Automated email notifications enable proactive, real-time awareness of client communication, ensuring agents can maintain the responsive service that clients expect and that drives business success.

## Estimated Effort

**Size:** Medium (M) - 3 days

**Breakdown:**
- 2 hours: Research email integration approaches
- 3 hours: Design email notification architecture
- 3 hours: Implement email polling/sync mechanism
- 4 hours: Build email notification generation
- 3 hours: Implement contact matching logic
- 3 hours: Add email preview and quick actions
- 3 hours: Implement notification deduplication
- 2 hours: Add notification preferences integration
- 3 hours: Build email grouping and threading
- 2 hours: Implement mark as read functionality
- 3 hours: Add email statistics and tracking
- 3 hours: Test and edge cases

## Dependencies

**Depends on:** 
- US-070 (Send Email to Contact)
- US-072 (View Email History in Contact Timeline)
- US-116 (Desktop Notifications for New Leads)
- US-117 (In-App Notifications)
- US-119 (Notification Preferences/Settings)
- Email integration (Gmail/Outlook OAuth or IMAP/SMTP)

**Blocks:** None (terminal feature for email notifications)

## Description

The application should monitor configured email accounts and generate notifications when new emails are received from contacts in the system. The system should intelligently match incoming emails to existing contacts and provide rich notifications with relevant context.

The email notification system should include:

**1. Email Monitoring**
- Periodic polling of configured email accounts (every 5-15 minutes, configurable)
- Real-time push notifications (if supported by email provider)
- Support for multiple email accounts
- Respect email provider rate limits
- Handle authentication securely
- Background sync that doesn't block the app

**2. Contact Matching**
- Match incoming emails to existing contacts by email address
- Match by name if email doesn't match
- Handle multiple contacts with same email
- Create new contact option if no match found
- Update existing contact with new email address
- Handle email aliases and forwards

**3. Notification Content**
Each email notification should include:
- Sender name and email address
- Email subject
- Email preview (first 100-150 characters)
- Timestamp
- Contact name (if matched)
- Related contact (clickable link)
- Related lead/property (if applicable)
- Attachment indicators
- Priority indicators (VIP contacts, starred, etc.)
- Thread/conversation grouping

**4. Notification Channels**
- Desktop notifications (with sound)
- In-app notifications
- Email digest (optional, for batched notifications)
- System tray badge with unread count

**5. Smart Grouping**
- Group emails from same conversation/thread
- Batch multiple emails from same sender
- Summary notifications for high-volume senders
- Collapse notifications for ongoing threads
- Show thread count for grouped emails

**6. Quick Actions**
- View full email
- Reply to email
- Mark as read/unread
- Archive email
- Delete email
- View related contact
- Add to contact notes
- Create task from email
- Snooze notification
- Mark as spam/junk

**7. Filtering and Rules**
- VIP contacts (always notify)
- Muted contacts (never notify)
- Keyword-based filtering
- Folder-based filtering (only notify for Inbox)
- Time-based filtering (only during business hours)
- Size-based filtering (skip large emails)
- Spam detection and filtering

**8. Privacy and Security**
- Email content is encrypted
- No email content sent to external services
- Secure storage of email credentials
- OAuth tokens stored securely
- No plain text passwords
- Automatic credential refresh

## BDD Scenarios

### Scenario 1: Configure email account for notifications

```
Given I am in notification preferences
  And I have not configured email notifications
When I click "Configure Email Notifications"
  And I select my email provider (Gmail, Outlook, etc.)
  And I authenticate via OAuth
  And I grant the required permissions
Then my email account should be connected
  And I should be able to enable email notifications
  And the system should start monitoring for new emails
```

### Scenario 2: Notification for new email from existing contact

```
Given I have email notifications enabled
  And I have a contact "John Smith" with email "john@example.com"
  And John sends me a new email
When the email is received and synced
Then a desktop notification should appear within 5 minutes
  And the title should be "New Email from John Smith"
  And the body should include:
    - Email subject
    - Email preview (first 100 characters)
    - Contact name
  And clicking it should open the email or contact's timeline
```

### Scenario 3: Notification for email from non-contact

```
Given I have email notifications enabled
  And someone not in my contacts emails me
When the new email is received
Then a notification should appear
  And it should indicate "Unknown Contact"
  And it should offer "Add to Contacts" as a quick action
  And the email should still be accessible
```

### Scenario 4: In-app notification for email

```
Given I have the application open
  And I receive a new email
When the email is synced
Then an in-app notification should appear
  And it should be added to the notification center
  And the notification bell badge should update
  And the email count should be accurate
```

### Scenario 5: Notification with contact link

```
Given I receive an email from a contact
When the notification appears
Then it should include a link to the contact's profile
  And clicking the contact name should open their details
  And I can see their full information
  And I can view their email history
```

### Scenario 6: Grouped notifications for email thread

```
Given I receive multiple emails in the same thread/conversation
When the notifications are generated
Then they should be grouped together
  And I should see "X new emails in this conversation"
  And clicking it should show all emails in the thread
  And the group should be marked with a thread icon
```

### Scenario 7: Batched notifications from same sender

```
Given John Smith sends me 3 emails within 10 minutes
When the notifications are generated
Then they should be batched into a single notification
  And the title should be "3 new emails from John Smith"
  And clicking it should show all 3 emails
  And the most recent email preview should be shown
```

### Scenario 8: VIP contact notification priority

```
Given I have marked "Jane Doe" as a VIP contact
  And Jane sends me an email
When the notification is generated
Then it should have high priority
  And it should use a distinct sound
  And it should override quiet hours
  And it should be visually distinct (e.g., gold star icon)
```

### Scenario 9: Muted contact - no notification

```
Given I have muted notifications for "Spam Sender"
  And this sender emails me
When the email is received
Then no notification should be generated
  And the email should still be available in the email history
  And it should be marked as muted in the logs
```

### Scenario 10: Reply to email from notification

```
Given I receive an email notification
When I click "Reply" in the notification
Then the email compose window should open
  And it should be pre-filled with:
    - Recipient: original sender
    - Subject: "Re: [original subject]"
    - Quoted original message
  And I can type my response
  And send the email
```

### Scenario 11: Quick reply from notification

```
Given I receive an email notification
When I click "Quick Reply"
Then a simple reply field should appear in the notification
  And I can type a brief response
  And send it immediately
  And the full email compose opens for longer replies
```

### Scenario 12: Mark email as read from notification

```
Given I receive an email notification
When I click "Mark as Read"
Then the email should be marked as read
  And the notification should be dismissed
  And the unread count should decrease
  And the email status should sync with the email server
```

### Scenario 13: Archive email from notification

```
Given I receive an email notification
When I click "Archive"
Then the email should be archived
  And the notification should be dismissed
  And the email should be removed from the inbox
  And it should be accessible in the archive folder
```

### Scenario 14: Delete email from notification

```
Given I receive an email notification
When I click "Delete"
Then the email should be deleted
  And I should be asked to confirm
  And the notification should be dismissed
  And the email should be moved to trash
```

### Scenario 15: Snooze email notification

```
Given I receive an email notification
  And I want to deal with it later
When I click "Snooze" and select "1 hour"
Then the notification should dismiss
  And a new notification should appear in 1 hour
  And the email remains unread
  And the snooze is tracked
```

### Scenario 16: Create task from email

```
Given I receive an email notification
  And the email contains an action item
When I click "Create Task"
Then a new task should be created with:
  - Title: derived from email subject
  - Description: email content or link
  - Related contact: the sender
  - Due date: optional, I can set it
And the task should be linked to the email
And the notification should be dismissed
```

### Scenario 17: Add email to contact notes

```
Given I receive an email notification
When I click "Add to Contact Notes"
Then the email should be added to the contact's notes
  And it should be timestamped
  And it should include the email content or summary
  And the contact's timeline should be updated
```

### Scenario 18: Email with attachments notification

```
Given I receive an email with attachments
When the notification is generated
Then it should indicate "X attachments" (e.g., "2 attachments")
  And attachment icons should be shown
  And I can click to view/download attachments
  And the notification should show attachment names
```

### Scenario 19: Email notification with preview

```
Given I receive an email
When the notification appears
Then it should show a preview of the email body
  And the preview should be the first 100-150 characters
  And it should be truncated with "..." if longer
  And line breaks should be handled properly
  And the preview should be plain text (no HTML)
```

### Scenario 20: Full email view from notification

```
Given I receive an email notification
When I click "View Full Email"
Then the full email should open in a viewer
  And it should show:
    - Full headers
    - Complete body
    - Attachments
    - Thread history (if part of conversation)
  And I can reply, forward, or take other actions
```

### Scenario 21: Email notification preferences

```
Given I am in notification preferences
  And I expand the "Emails" category
When I see the email notification options:
  - New email received
  - Email from VIP contact
  - Email from non-contact
  - Email with attachments
Then I can independently configure each
  And select delivery channels
  And set filtering rules
  And save my preferences
```

### Scenario 22: Polling frequency configuration

```
Given I am configuring email notifications
When I set the polling frequency to "Every 5 minutes"
  And I save
Then the system should check for new emails every 5 minutes
  And the frequency should be respected
  And I can change it to "Every 15 minutes" or "Manual only"
  And the setting should persist
```

### Scenario 23: Manual email sync

```
Given I want to check for new emails immediately
When I click "Sync Now" or "Check for New Emails"
Then the system should immediately check for new emails
  And a progress indicator should appear
  And any new emails should generate notifications
  And the sync should complete within a reasonable time
```

### Scenario 24: Multiple email accounts

```
Given I have configured 2 email accounts (work and personal)
  And I receive emails on both accounts
When the emails are synced
Then separate notifications should appear for each account
  And they should be clearly labeled (work/personal)
  And I can filter by account
  And I can enable/disable notifications per account
```

### Scenario 25: Email account authentication failure

```
Given my email account authentication has expired
  And the system tries to sync emails
When the sync fails
Then I should receive a notification about the authentication failure
  And it should guide me to re-authenticate
  And I should be able to update my credentials
  And the system should stop trying until re-authenticated
```

### Scenario 26: Email sync errors

```
Given there is a network error during email sync
When the sync fails
Then I should see a notification about the sync failure
  And the system should retry automatically
  And after multiple failures, it should stop and notify me
  And I can manually retry
```

### Scenario 27: Rate limiting respect

```
Given the email provider has rate limits
  And the system is syncing frequently
When the rate limit is approached
Then the system should automatically reduce sync frequency
  And it should back off appropriately
  And it should not exceed the provider's limits
  And it should resume normal frequency after the limit resets
```

### Scenario 28: Large email handling

```
Given I receive a very large email (e.g., 25 MB with attachments)
When the notification is generated
Then it should still notify me
  And the preview should be limited to avoid loading the full email
  And attachments should be downloaded on demand
  And the notification should show "Large email with attachments"
```

### Scenario 29: Spam email filtering

```
Given I receive an email marked as spam by the provider
When the notification is generated
Then it should be filtered out by default
  And no notification should appear
  And the email should be available in the spam folder
  And I can change the filter to notify for spam
```

### Scenario 30: Keyword-based filtering

```
Given I have configured keyword filters (e.g., notify only for "urgent")
  And I receive an email without those keywords
When the notification is generated
Then it should be filtered out
  And no notification should appear
  And the email should be available in the inbox
  And the filter should be configurable
```

### Scenario 31: Folder-based filtering

```
Given I have configured to monitor only the "Inbox" folder
  And I receive an email in another folder
When the email is synced
Then no notification should be generated
  And only Inbox emails trigger notifications
  And I can configure to monitor multiple folders
  And the setting should be saved
```

### Scenario 32: Business hours filtering

```
Given I have configured business hours (9 AM - 5 PM)
  And I receive an email at 10 PM
When the notification is generated
Then it should respect business hours
  And the email should still be synced
  And notifications can be queued for business hours
  And critical/VIP emails can override
```

### Scenario 33: Email notification sound

```
Given I have email notification sounds enabled
  And I receive a new email
When the notification appears
Then a sound should play
  And it should be different from other notification sounds
  And the volume should respect my preferences
  And I can change the sound in settings
```

### Scenario 34: Email notification badge

```
Given I have unread emails
When I view the application
Then the notification bell should show a badge with the count
  And a separate email icon should show the email-specific count
  And the counts should be accurate
  And they should update in real-time
```

### Scenario 35: Email thread conversation view

```
Given I have multiple emails in a conversation
When I click on a grouped notification
Then I should see the full conversation thread
  And emails should be in chronological order
  And I can reply to the thread
  And I can see all participants
  And the thread is linked to the contact
```

### Scenario 36: Email statistics

```
Given I want to see email notification statistics
When I navigate to notification preferences > Email Statistics
Then I should see:
  - Total emails received this week/month
  - Emails from contacts vs non-contacts
  - Most active contacts (by email volume)
  - Response time statistics
  And I can use this to optimize my email management
```

### Scenario 37: Email notification deduplication

```
Given the same email is detected multiple times during sync
When notifications are generated
Then only one notification should appear
  And duplicates should be prevented
  And the system should track which emails have been notified
  And re-syncing should not create duplicate notifications
```

### Scenario 38: Offline email handling

```
Given I am offline
  And new emails arrive on the server
When I come back online
Then the system should sync and notify for missed emails
  And they should be marked as "received while offline"
  And the notifications should be in chronological order
  And I can configure whether to notify for old emails
```

### Scenario 39: Email content privacy

```
Given I receive a confidential email
When the notification appears
Then the preview should be limited
  And the full content should only be visible after authentication
  And screenshots should be blocked (if configured)
  And the email should not be logged in plain text
```

### Scenario 40: Disconnect email account

```
Given I want to stop email notifications
When I go to email notification settings
  And I click "Disconnect Account"
  And I confirm
Then the email account should be disconnected
  And no more notifications should be generated
  And the credentials should be securely removed
  And I can reconnect later
```

## Manual Testing Steps

### Test 1: Configure email account

1. Go to notification preferences
2. Click "Configure Email Notifications"
3. Select email provider (Gmail, Outlook, etc.)
4. Complete OAuth flow
5. Grant required permissions
6. Verify account is connected
7. Verify email address is shown
8. Enable notifications

### Test 2: Receive notification from contact

1. Have a contact with a known email address
2. Send an email to the configured account from that address
3. Wait for sync (or trigger manual sync)
4. Verify notification appears within 5 minutes
5. Verify all details are correct:
   - Sender name
   - Email subject
   - Preview
   - Contact name
6. Click the notification
7. Verify it opens the email or contact

### Test 3: In-app notification

1. Keep the app open
2. Send an email from a contact
3. Wait for sync
4. Verify in-app notification appears
5. Verify it's in the notification center
6. Verify the badge updates
7. Click to view

### Test 4: Contact linking

1. Send an email from a contact
2. Receive notification
3. Click the contact name in the notification
4. Verify it opens the contact's profile
5. Verify the email appears in their timeline
6. Verify all contact information is shown

### Test 5: Unknown sender

1. Send an email from an address not in contacts
2. Receive notification
3. Verify it shows "Unknown Contact"
4. Click "Add to Contacts"
5. Verify a new contact form opens
6. Fill in details
7. Save
8. Verify the email is linked to the new contact

### Test 6: Email thread grouping

1. Send 3 replies in the same email thread
2. Wait for all to sync
3. Verify they are grouped in one notification
4. Click the grouped notification
5. Verify all 3 emails are shown
6. Verify they're in chronological order
7. Reply to the thread
8. Verify it's added correctly

### Test 7: Batched notifications

1. Send 3 separate emails from the same contact within 5 minutes
2. Wait for sync
3. Verify they are batched into one notification
4. Click it
5. Verify all 3 emails are shown
6. Verify the most recent preview is displayed

### Test 8: VIP contact priority

1. Mark a contact as VIP
2. Send an email from VIP contact
3. Verify notification has high priority
4. Verify distinct sound plays
5. Verify it overrides quiet hours
6. Verify gold star or special icon
7. Compare with regular contact notification

### Test 9: Muted contact

1. Mute a contact
2. Send an email from muted contact
3. Verify no notification appears
4. Check email history
5. Verify the email is there
6. Verify it's marked as muted
7. Unmute the contact
8. Send another email
9. Verify notification appears

### Test 10: Reply from notification

1. Receive an email notification
2. Click "Reply"
3. Verify compose window opens
4. Verify recipient is pre-filled
5. Verify subject has "Re:" prefix
6. Verify original message is quoted
7. Type a response
8. Send
9. Verify it's sent successfully

### Test 11: Quick reply

1. Receive an email notification
2. Click "Quick Reply"
3. Type a brief response
4. Send
5. Verify it's sent
6. Verify the email thread is updated
7. Test with a longer message
8. Verify it opens full compose for long messages

### Test 12: Mark as read

1. Receive an email notification
2. Click "Mark as Read"
3. Verify email is marked as read
4. Verify notification dismisses
5. Verify unread count decreases
6. Check email server
7. Verify the read status synced

### Test 13: Archive from notification

1. Receive an email notification
2. Click "Archive"
3. Verify email is archived
4. Verify notification dismisses
5. Check archive folder
6. Verify email is there
7. Test with multiple emails

### Test 14: Delete from notification

1. Receive an email notification
2. Click "Delete"
3. Confirm deletion
4. Verify email is deleted
5. Verify notification dismisses
6. Check trash folder
7. Verify email is there

### Test 15: Snooze notification

1. Receive an email notification
2. Click "Snooze"
3. Select "1 hour"
4. Verify notification dismisses
5. Wait 1 hour
6. Verify notification reappears
7. Click to view
8. Verify email is still unread

### Test 16: Create task from email

1. Receive an email notification
2. Click "Create Task"
3. Verify task form opens
4. Verify it's pre-filled with email info
5. Verify contact is linked
6. Set due date
7. Save task
8. Verify it's created
9. Verify link to email is maintained

### Test 17: Add to contact notes

1. Receive an email from a contact
2. Click "Add to Contact Notes"
3. Verify it's added to notes
4. Check the contact's timeline
5. Verify it's timestamped
6. Verify the email content is included
7. Verify it's properly formatted

### Test 18: Email with attachments

1. Send an email with 2 attachments
2. Receive notification
3. Verify "2 attachments" is shown
4. Click to view
5. Verify attachments are listed
6. Click an attachment
7. Verify it opens/downloads
8. Test with different file types

### Test 19: Email preview

1. Send a long email
2. Receive notification
3. Verify preview is limited to ~100 characters
4. Verify it's truncated with "..."
5. Click "View Full Email"
6. Verify the complete email is shown
7. Test with HTML email
8. Verify formatting is handled

### Test 20: Notification preferences

1. Go to notification preferences
2. Expand "Emails" category
3. Verify all sub-options are shown
4. Configure each independently
5. Save preferences
6. Test each configuration
7. Verify they work as configured

### Test 21: Polling frequency

1. Go to email settings
2. Set polling to "Every 5 minutes"
3. Save
4. Send an email
5. Wait 5 minutes
6. Verify notification appears
7. Change to "Every 15 minutes"
8. Send another email
9. Verify it takes ~15 minutes

### Test 22: Manual sync

1. Set polling to "Manual only"
2. Send an email
3. Verify no automatic notification
4. Click "Sync Now"
5. Verify manual sync starts
6. Verify progress indicator
7. Verify notification appears for the email
8. Verify sync completes

### Test 23: Multiple email accounts

1. Configure 2 email accounts
2. Send emails to both accounts
3. Verify separate notifications for each
4. Verify they're labeled (work/personal)
5. Filter by account
6. Verify filtering works
7. Disable notifications for one account
8. Verify only the other notifies

### Test 24: Authentication failure

1. Revoke email account access
2. Wait for sync attempt
3. Verify authentication failure notification
4. Click to re-authenticate
5. Complete OAuth flow again
6. Verify account is reconnected
7. Verify sync resumes

### Test 25: Network error handling

1. Disconnect from internet
2. Wait for sync attempt
3. Verify failure is handled gracefully
4. Verify retry attempts
5. Reconnect
6. Verify sync resumes
7. Verify missed emails are synced
8. Verify notifications for them

### Test 26: Rate limiting

1. Configure very frequent sync (every 1 minute)
2. Monitor sync behavior
3. Verify rate limits are respected
4. Verify backoff is implemented
5. Verify it resumes after limit resets
6. Check for any errors or blocks

### Test 27: Large email handling

1. Send a large email (20+ MB with attachments)
2. Receive notification
3. Verify it notifies despite size
4. Verify preview is limited
5. Click to view
6. Verify attachments download on demand
7. Test with multiple large emails

### Test 28: Spam filtering

1. Send an email marked as spam
2. Verify it's filtered out
3. Check spam folder
4. Verify the email is there
5. Change filter settings
6. Enable spam notifications
7. Send another spam email
8. Verify notification appears

### Test 29: Keyword filtering

1. Configure keyword filter: "urgent"
2. Send an email with "urgent" in subject
3. Verify notification appears
4. Send an email without the keyword
5. Verify no notification
6. Change keywords
7. Test different keywords
8. Verify filtering works

### Test 30: Folder monitoring

1. Configure to monitor only "Inbox"
2. Send email to Inbox
3. Verify notification
4. Move an email to another folder
5. Send email to that folder
6. Verify no notification for that email
7. Change to monitor multiple folders
8. Verify notifications for all monitored folders

### Test 31: Business hours

1. Configure business hours: 9 AM - 5 PM
2. Send an email at 10 PM
3. Verify no immediate notification
4. Check at 9 AM next day
5. Verify queued notification appears
6. Mark a contact as VIP
7. Send email at 10 PM from VIP
8. Verify it overrides business hours

### Test 32: Notification sound

1. Enable email notification sounds
2. Select a sound
3. Send an email
4. Verify sound plays
5. Verify it's different from other sounds
6. Adjust volume
7. Verify volume is respected
8. Disable sounds
9. Verify no sound plays

### Test 33: Email badge

1. Have multiple unread emails
2. Check notification bell
3. Verify badge count
4. Check email icon
5. Verify email-specific count
6. Mark some as read
7. Verify counts update
8. Verify real-time updates

### Test 34: Conversation view

1. Have a multi-email conversation
2. Click grouped notification
3. Verify full thread is shown
4. Verify chronological order
5. Verify all participants shown
6. Reply to thread
7. Verify it's added correctly
8. Test with long conversations

### Test 35: Email statistics

1. Go to email statistics
2. Verify counts are accurate
3. Check most active contacts
4. Check response times
5. Change date range
6. Verify statistics update
7. Export statistics (if available)
8. Verify export works

### Test 36: Deduplication

1. Trigger multiple syncs
2. Verify no duplicate notifications
3. Check notification center
4. Verify each email appears once
5. Manually trigger sync
6. Verify no duplicates
7. Test with rapid successive syncs

### Test 37: Offline handling

1. Disconnect from internet
2. Send emails to the account
3. Wait
4. Reconnect
5. Verify sync happens
6. Verify notifications for all emails
7. Verify chronological order
8. Verify they're marked as received while offline

### Test 38: Privacy mode

1. Enable privacy mode for notifications
2. Send an email
3. Verify preview is limited
4. Verify authentication is required for full content
5. Try to screenshot
6. Verify it's blocked (if configured)
7. Check logs
8. Verify no plain text content

### Test 39: Disconnect account

1. Go to email settings
2. Click "Disconnect Account"
3. Confirm
4. Verify account is disconnected
5. Send an email to that account
6. Verify no notification
7. Check credentials are removed
8. Reconnect
9. Verify it works again

### Test 40: Cross-platform testing

1. Test on Windows
2. Verify email sync works
3. Test on macOS
4. Verify all features work
5. Test on Linux
6. Verify email integration
7. Test with different email providers
8. Document any platform issues

### Test 41: Performance testing

1. Sync with large mailbox (1000+ emails)
2. Verify sync completes reasonably
3. Check memory usage
4. Verify UI remains responsive
5. Test with frequent syncs
6. Verify no performance degradation
7. Test with multiple accounts

### Test 42: Security testing

1. Verify email content is encrypted
2. Check credential storage
3. Verify OAuth tokens are secure
4. Test with network monitoring
5. Verify HTTPS is used
6. Check for data leaks
7. Verify no plain text passwords

## Acceptance Criteria

- [ ] Email account can be configured via OAuth or IMAP/SMTP
- [ ] Email notifications can be enabled/disabled globally
- [ ] Email notifications can be enabled/disabled per account
- [ ] System monitors configured email accounts
- [ ] Polling frequency is configurable
- [ ] Manual sync option is available
- [ ] Real-time push notifications work (if supported)
- [ ] New emails from contacts generate notifications
- [ ] New emails from non-contacts generate notifications
- [ ] Contact matching works by email address
- [ ] Contact matching works by name (fallback)
- [ ] Unknown senders can be added as new contacts
- [ ] Notifications include sender name and email
- [ ] Notifications include email subject
- [ ] Notifications include email preview (first 100 chars)
- [ ] Notifications include timestamp
- [ ] Notifications link to related contact
- [ ] Notifications link to related lead/property (if applicable)
- [ ] Email threads are grouped into single notifications
- [ ] Multiple emails from same sender are batched
- [ ] VIP contacts have high-priority notifications
- [ ] VIP notifications override quiet hours
- [ ] Muted contacts don't generate notifications
- [ ] Keyword filtering works
- [ ] Folder-based filtering works
- [ ] Business hours filtering works
- [ ] Spam emails are filtered by default
- [ ] Notifications include attachment indicators
- [ ] Reply action opens compose with pre-filled fields
- [ ] Quick reply works for short responses
- [ ] Mark as read works from notification
- [ ] Archive action works from notification
- [ ] Delete action works from notification
- [ ] Snooze functionality works
- [ ] Create task from email works
- [ ] Add to contact notes works
- [ ] View full email opens complete message
- [ ] Desktop notifications are delivered
- [ ] In-app notifications are generated
- [ ] Notification badge shows accurate count
- [ ] Email-specific badge/count is shown
- [ ] Notification sound is distinct and configurable
- [ ] Notification preferences are respected
- [ ] Per-event-type configuration works
- [ ] Multiple email accounts are supported
- [ ] Account-specific filtering works
- [ ] Authentication failures are handled gracefully
- [ ] Re-authentication is easy to perform
- [ ] Network errors are handled with retries
- [ ] Rate limits are respected
- [ ] Large emails are handled properly
- [ ] Email content is encrypted
- [ ] Credentials are stored securely
- [ ] OAuth tokens are refreshed automatically
- [ ] Email statistics are available
- [ ] Conversation/thread view is supported
- [ ] Deduplication prevents duplicate notifications
- [ ] Offline emails are synced when online
- [ ] Privacy mode limits content preview
- [ ] Email account can be disconnected
- [ ] Works on Windows, macOS, and Linux
- [ ] Performance is acceptable with large mailboxes
- [ ] No memory leaks or performance degradation
- [ ] Keyboard navigation works
- [ ] Screen reader compatibility
- [ ] Translations are supported
- [ ] No security vulnerabilities
- [ ] HTTPS is used for all communication
- [ ] Privacy policy is clear about email handling
