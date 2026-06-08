# US-070: Send Email to Contact

## User Story

**As an** agent  
**I want to** send an email to a contact from within OurCRM  
**So that** I can communicate with clients without switching to my email application

## Priority

**MVP:** Must Have

**Rationale:** Email is a primary communication method for real estate agents. Being able to send emails from within the CRM saves time and keeps all communication in one place. This is a core feature that agents use daily.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design email composition UI
- 2 hours: Create compose email form
- 1 hour: Implement SMTP configuration
- 1 hour: Add recipient field (pre-filled from contact)
- 1 hour: Add subject and body fields
- 1 hour: Implement send functionality
- 1 hour: Add success/error feedback
- 1 hour: Test email sending
- 1 hour: Test with various email providers
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-022 (View Contact Details), US-017 (Open Settings Window)

**Blocks:** US-071 (Use Email Templates), US-072 (Email Logging in Contact Timeline)

## Description

Users should be able to send emails to contacts directly from within OurCRM. The email composition form should be accessible from the contact details page. The form should have fields for recipient (pre-filled from the contact), subject, body, and optional attachments.

The email should be sent using the configured SMTP settings (configured separately in email settings). After sending, the email should be logged in the contact's timeline for future reference.

## BDD Scenarios

### Scenario 1: Open email compose form

```
Given I am viewing a contact's details
When I click "Send Email" or the email icon
Then the email compose form should open
  And the recipient should be pre-filled with the contact's email
  And I can enter the subject and body
```

### Scenario 2: Send email successfully

```
Given the email compose form is open
  And SMTP is configured
When I enter a subject and body
  And I click "Send"
Then the email should be sent via SMTP
  And I should see a success message
  And the form should close
  And the email should be logged in the contact's timeline
```

### Scenario 3: Email not configured

```
Given SMTP is not configured
When I try to send an email
Then I should see a message that email is not configured
  And a link to configure it in Settings
```

### Scenario 4: Invalid recipient

```
Given I am composing an email
When I try to send without a recipient
  Or with an invalid email address
Then I should see a validation error
  And the email should not be sent
```

### Scenario 5: Send email with attachment

```
Given the email compose form is open
When I click "Attach File"
  And I select a file
Then the file should be attached to the email
  And I can remove it before sending
```

### Scenario 6: HTML email support

```
Given I am composing an email
When I toggle to HTML mode
Then I can format the email with HTML
  And the recipient will receive formatted HTML
```

### Scenario 7: Email send failure

```
Given the email compose form is open
When I try to send but SMTP fails
Then I should see an error message
  And the email should be saved as a draft
  And I can retry sending
```

### Scenario 8: Email is logged in timeline

```
Given I sent an email to a contact
When I view the contact's details
Then the email should appear in the timeline
  And it should show the subject, date, and a preview
  And it should be marked as "Sent"
```

## Manual Testing Steps

### Test 1: Open email compose form

1. Configure SMTP settings
2. Open a contact's details
3. Click "Send Email"
4. Verify the form opens
5. Verify the recipient is pre-filled
6. Verify subject and body fields are empty

### Test 2: Send email

1. Open the email compose form
2. Enter a subject
3. Enter a body
4. Click "Send"
5. Verify the success message
6. Verify the form closes
7. Check the recipient's inbox
8. Verify the email was received

### Test 3: Test without configuration

1. Don't configure SMTP (or use invalid settings)
2. Try to send an email
3. Verify the error message
4. Verify the link to Settings

### Test 4: Test validation

1. Open the email form
2. Clear the recipient field
3. Click "Send"
4. Verify the validation error
5. Enter an invalid email
6. Verify the error

### Test 5: Test attachments

1. Open the email form
2. Click "Attach File"
3. Select a file
4. Verify it's attached
5. Remove the attachment
6. Verify it's removed

### Test 6: Test HTML emails

1. Open the email form
2. Toggle to HTML mode
3. Add HTML formatting
4. Send the email
5. Verify the recipient receives formatted HTML

### Test 7: Test send failure

1. Configure SMTP with invalid settings
2. Try to send an email
3. Verify the error message
4. Verify the draft is saved
5. Fix the settings and retry

### Test 8: Test timeline logging

1. Send an email to a contact
2. View the contact's details
3. Verify the email appears in the timeline
4. Verify it shows the subject and date
5. Click on it to see the full content

### Test 9: Test with different email providers

1. Test with Gmail SMTP
2. Verify it works
3. Test with Outlook SMTP
4. Verify it works
5. Test with other providers

### Test 10: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] "Send Email" button is accessible from contact details
- [ ] Email compose form opens with recipient pre-filled
- [ ] Subject and body fields are available
- [ ] Email sends successfully via SMTP
- [ ] Success message appears after sending
- [ ] Email is logged in contact's timeline
- [ ] Error handling for SMTP failures
- [ ] Validation for invalid recipients
- [ ] Attachment support works
- [ ] HTML email support works
- [ ] Email configuration is clear if not set up
- [ ] Works with various SMTP providers
- [ ] Works on Windows, macOS, and Linux
- [ ] Form is intuitive and easy to use