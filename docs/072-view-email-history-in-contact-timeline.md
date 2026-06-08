# US-072: View Email History in Contact Timeline

## User Story

**As an** agent  
**I want to** see all emails sent to a contact in their timeline  
**So that** I have a complete communication history with each person

## Priority

**MVP:** Must Have

**Rationale:** Email history is essential for maintaining context with clients. Agents need to remember what was discussed, when, and what was promised. Without email history, agents lose track of important conversations and make mistakes.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design email history display
- 1 hour: Display emails in contact timeline
- 1 hour: Show email details (subject, date, preview)
- 1 hour: Add email filtering
- 1 hour: Implement email search
- 1 hour: Test email history display
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-070 (Send Email to Contact)

**Blocks:** US-073 (View Email Details)

## Description

All emails sent to a contact should be automatically logged in the contact's timeline. The timeline should display the emails chronologically with key information: subject, date sent, and a preview of the content. Users should be able to click on an email to see the full content and details.

The email history provides a complete communication record, making it easy to review past conversations and maintain context with each contact.

## BDD Scenarios

### Scenario 1: View email history

```
Given I have sent several emails to a contact
When I view the contact's details
Then the emails should appear in the timeline
  And each email should show:
    - Subject
    - Date sent
    - Preview of the content
    - Status (Sent/Failed)
```

### Scenario 2: Emails are in chronological order

```
Given I have sent multiple emails to a contact
When I view the email history
Then they should be in chronological order
  And I can choose newest first or oldest first
```

### Scenario 3: Click email to see full content

```
Given I am viewing the email history
When I click on an email
Then the full email should be displayed
  And I can see the complete subject, body, and metadata
  And any attachments are listed
```

### Scenario 4: Search email history

```
Given a contact has many emails
When I search for specific text in the emails
Then matching emails should be highlighted
  And I can quickly find what I'm looking for
```

### Scenario 5: Filter email history

```
Given a contact has many emails
When I filter by date range
Then only emails from that period are shown
  And I can narrow down the history
```

### Scenario 6: Email with attachments

```
Given I sent an email with an attachment
When I view the email history
Then the attachment should be indicated
  And I can download it from the history
```

### Scenario 7: Failed email attempts

```
Given an email failed to send
When I view the email history
Then it should be marked as "Failed"
  And I can see the error reason
  And I can retry sending it
```

### Scenario 8: Email history is searchable globally

```
Given I have many contacts with email history
When I use global search
Then I should be able to search across all email content
  And find emails by subject or content
```

## Manual Testing Steps

### Test 1: View email history

1. Send several emails to a contact
2. View the contact's details
3. Verify the emails appear in the timeline
4. Verify each shows subject, date, and preview
5. Verify they're marked as "Sent"

### Test 2: Test chronological order

1. Send emails on different days
2. View the timeline
3. Verify the order is correct
4. Try sorting options
5. Verify both newest and oldest first work

### Test 3: Test email details

1. Click on an email in the timeline
2. Verify the full content is shown
3. Verify all metadata is displayed
4. Check that attachments are listed

### Test 4: Test search

1. Have a contact with many emails
2. Use the search function
3. Search for specific text
4. Verify matching emails are highlighted
5. Verify the search is fast

### Test 5: Test date filtering

1. Have emails over different time periods
2. Filter by date range
3. Verify only matching emails are shown
4. Test various date ranges

### Test 6: Test attachments

1. Send an email with an attachment
2. View the email history
3. Verify the attachment is indicated
4. Download the attachment
5. Verify it works

### Test 7: Test failed emails

1. Try to send an email with invalid SMTP settings
2. Verify it fails
3. View the email history
4. Verify it's marked as "Failed"
5. See the error reason
6. Retry sending

### Test 8: Test global search

1. Have many contacts with emails
2. Use global search
3. Search for text that appears in an email subject or body
4. Verify the contact with that email appears in results

### Test 9: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Sent emails appear in contact's timeline
- [ ] Each email shows subject, date, and preview
- [ ] Emails are in chronological order
- [ ] Can sort by newest or oldest first
- [ ] Clicking an email shows full content
- [ ] Email search works within contact
- [ ] Date filtering works
- [ ] Attachments are indicated and downloadable
- [ ] Failed emails are marked and can be retried
- [ ] Email content is searchable globally
- [ ] History is comprehensive and accurate
- [ ] Works on Windows, macOS, and Linux
- [ ] UI is intuitive and easy to navigate