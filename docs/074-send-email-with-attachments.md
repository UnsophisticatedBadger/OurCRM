# US-074: Send Email with Attachments

## User Story

**As an** agent  
**I want to** attach files (contracts, documents, photos) to emails  
**So that** I can send important documents to clients without switching applications

## Priority

**MVP:** Must Have

**Rationale:** Real estate agents frequently need to send documents like contracts, disclosures, inspection reports, and property photos via email. Attachment support is essential for the email feature to be useful for real estate work.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design attachment UI
- 1 hour: Implement file selection
- 1 hour: Add file validation (size, type)
- 1 hour: Display attached files
- 1 hour: Allow attachment removal
- 1 hour: Integrate with email sending
- 1 hour: Test attachment functionality
- 1 hour: Test with various file types
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-070 (Send Email to Contact), US-073 (Configure Email Settings)

**Blocks:** US-075 (Attach Contact Documents to Email)

## Description

Users should be able to attach one or more files to emails they send from OurCRM. The attachment UI should allow file selection from the computer, display attached files with their names and sizes, and allow removal of attachments before sending. File size limits should be enforced to prevent email delivery issues.

Common attachment use cases for real estate:
- Contracts and agreements (PDF)
- Property photos (JPG, PNG)
- Inspection reports (PDF)
- Disclosures (PDF)
- Market reports (PDF)

## BDD Scenarios

### Scenario 1: Add attachment to email

```
Given the email compose form is open
When I click "Attach File"
  And I select a file from my computer
Then the file should be attached to the email
  And it should appear in the attachments list
  And it should show the filename and file size
```

### Scenario 2: Add multiple attachments

```
Given the email compose form is open
When I click "Attach Files"
  And I select multiple files
Then all files should be attached
  And all should appear in the attachments list
  And each should show its filename and size
```

### Scenario 3: Remove attachment

```
Given I have attached files to an email
When I click the X or "Remove" next to an attachment
Then that file should be removed from the attachments
  And the email should no longer include it
```

### Scenario 4: File size validation

```
Given I am attaching a file
When I select a very large file (e.g., >25MB)
Then I should see a warning
  And the file should not be attached
  Or I should be warned that it may fail to send
```

### Scenario 5: File type validation

```
Given I am attaching a file
When I select an executable file (.exe, .bat)
Then I should see a warning
  And the file should not be attached
  Or I should be warned about security risks
```

### Scenario 6: Attachment progress indicator

```
Given I am attaching large files
When I select the files
Then a progress indicator should appear
  And show the upload progress
  And indicate when each file is ready
```

### Scenario 7: Send email with attachments

```
Given I have attached files to an email
When I click "Send"
Then the email should be sent with all attachments
  And I should see a success message
  And the attachments should be available to the recipient
```

### Scenario 8: Attachment from contact documents (optional)

```
Given I am sending an email to a contact
When I click "Attach from Documents"
Then I should see a list of documents associated with the contact
  And I can select one or more to attach
  And they should be added to the email
```

## Manual Testing Steps

### Test 1: Add single attachment

1. Open the email compose form
2. Click "Attach File"
3. Select a file
4. Verify it appears in the attachments list
5. Verify the filename and size are shown

### Test 2: Add multiple attachments

1. Open the email compose form
2. Click "Attach Files"
3. Select multiple files
4. Verify all appear in the list
5. Verify each shows its details

### Test 3: Remove attachment

1. Attach files to an email
2. Click remove on one
3. Verify it's removed
4. Verify it won't be sent
5. Remove all attachments
6. Verify the email has no attachments

### Test 4: Test file size limit

1. Try to attach a very large file
2. Verify the warning
3. Try to attach a file just under the limit
4. Verify it works

### Test 5: Test file type restrictions

1. Try to attach an executable file
2. Verify the warning
3. Try to attach a PDF
4. Verify it works
5. Try various file types (JPG, DOCX, XLSX)

### Test 6: Test sending with attachments

1. Attach files to an email
2. Enter subject and body
3. Click "Send"
4. Verify the success message
5. Check the recipient's inbox
6. Verify they received the attachments
7. Verify the attachments are not corrupted

### Test 7: Test large attachments

1. Attach large files (5-10MB)
2. Send the email
3. Verify it works
4. Check the recipient's inbox
5. Verify the files arrived

### Test 8: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] "Attach File" button is available in email compose
- [ ] Single files can be attached
- [ ] Multiple files can be attached
- [ ] Attached files show filename and size
- [ ] Attachments can be removed before sending
- [ ] File size limits are enforced
- [ ] File type restrictions are enforced
- [ ] Progress indicator shows for large files
- [ ] Email sends successfully with attachments
- [ ] Recipient receives the attachments
- [ ] Attachments are not corrupted
- [ ] Works on Windows, macOS, and Linux
- [ ] UI is intuitive and clear