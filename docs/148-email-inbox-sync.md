# US-148: Email Inbox Sync

## User Story

**As an** agent  
**I want to** sync my email inbox with OurCRM  
**So that** I can see all email conversations with contacts in one place

## Priority

**Future:** Post-MVP

**Rationale:** Email inbox sync provides a complete communication history with each contact. Instead of just sent emails, agents can see received emails too, providing full context for every relationship.

## Estimated Effort

**Size:** Large (L) - 5-8 days

**Breakdown:**
- 3 hours: Design inbox sync architecture
- 4 hours: Implement email fetching (IMAP or API)
- 3 hours: Match emails to contacts
- 3 hours: Display emails in contact timeline
- 3 hours: Handle attachments
- 3 hours: Test sync functionality
- 3 hours: Test on all platforms

## Dependencies

**Depends on:** US-146 (Gmail OAuth Integration) or US-147 (Outlook OAuth Integration)

**Blocks:** None

## Description

Users should be able to sync their email inbox so that:
1. Received emails from contacts appear in contact timeline
2. Sent emails are already logged (existing feature)
3. Email threads are grouped together
4. Attachments are downloadable

This requires OAuth connection with read permissions on email.

## BDD Scenarios

### Scenario 1: Enable inbox sync

Given I have connected Gmail or Outlook via OAuth When I enable inbox sync Then emails should start syncing And I should see a sync status


### Scenario 2: Received emails appear in contact timeline

Given inbox sync is enabled When I receive an email from a contact Then it should appear in their timeline And I can read the full email


### Scenario 3: Emails are matched to contacts

Given I receive an email When it's synced Then it should be matched to the correct contact Based on email address


### Scenario 4: Email threads are grouped

Given I have multiple emails in a conversation When I view the timeline Then they should be grouped as a thread And I can expand/collapse


### Scenario 5: Attachments are accessible

Given an email has attachments When I view it in the timeline Then I should be able to download them And preview if possible


### Scenario 6: Sync is bidirectional

Given inbox sync is enabled When I send an email from OurCRM Then it should appear in both sent folder and timeline


### Scenario 7: Can disable inbox sync

Given inbox sync is enabled When I disable it Then new emails should not sync And existing synced emails remain


### Scenario 8: Sync happens automatically

Given inbox sync is enabled When new emails arrive Then they should sync automatically Without manual intervention


## Manual Testing Steps

### Test 1: Enable inbox sync

1. Connect email via OAuth
2. Enable inbox sync
3. Verify sync starts
4. Verify status is shown

### Test 2: Test received emails

1. Send email to your connected account from a contact
2. Wait for sync
3. View contact timeline
4. Verify email appears

### Test 3: Test contact matching

1. Send from email that matches a contact
2. Verify it's matched correctly
3. Test with email not in contacts
4. Verify behavior

### Test 4: Test thread grouping

1. Have email conversation
2. View timeline
3. Verify threads are grouped

### Test 5: Test attachments

1. Receive email with attachment
2. Verify attachment is shown
3. Download it
4. Verify it works

### Test 6: Test disable sync

1. Disable inbox sync
2. Send new email
3. Verify it doesn't sync

### Test 7: Test automatic sync

1. Leave app running
2. Receive email
3. Verify it syncs automatically

### Test 8: Test on all platforms

1. Test Windows, macOS, Linux
2. Verify all work

## Acceptance Criteria

- [ ] Inbox sync can be enabled/disabled
- [ ] Received emails appear in contact timeline
- [ ] Emails are matched to correct contacts
- [ ] Email threads are grouped
- [ ] Attachments are downloadable
- [ ] Sync happens automatically
- [ ] Works with Gmail and Outlook
- [ ] Existing sent emails still logged
- [ ] Sync status is visible
- [ ] Can disable sync at any time
- [ ] Works on Windows, macOS, and Linux