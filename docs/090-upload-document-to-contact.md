# US-090: Upload Document to Contact

## User Story

**As an** agent  
**I want to** upload documents (PDFs, contracts, photos) to a contact  
**So that** I can keep all client-related files organized in one place

## Priority

**MVP:** Must Have

**Rationale:** Real estate agents handle many documents: contracts, disclosures, pre-approval letters, inspection reports. Keeping these organized by contact is essential for client management and legal compliance.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design document upload UI
- 2 hours: Implement file selection and upload
- 1 hour: Store document in database (encrypted BLOB)
- 1 hour: Display document metadata
- 1 hour: Add document categories/tags
- 1 hour: Test upload and storage
- 1 hour: Test with various file types
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-022 (View Contact Details), US-014 (Create Encrypted Database)

**Blocks:** US-091 (View Contact Documents), US-092 (Delete Document), US-093 (Download Document)

## Description

Users should be able to upload documents to any contact. Documents are stored encrypted in the database (MVP) and can be PDFs, images, Word documents, or other common file types. Each document should have metadata: filename, file type, file size, upload date, optional category, and optional description.

The upload should support single or multiple files and should show progress for large files. Documents should be associated with the specific contact and accessible from the contact's details page.

## BDD Scenarios

### Scenario 1: Upload a document to a contact

```
Given I am viewing a contact's details
When I click "Upload Document"
  And I select a file from my computer
Then the document should be uploaded
  And stored encrypted in the database
  And appear in the contact's documents list
  And show filename, type, size, and upload date
```

### Scenario 2: Upload multiple documents

```
Given I am viewing a contact's details
When I click "Upload Documents"
  And I select multiple files
Then all documents should be uploaded
  And all should appear in the documents list
```

### Scenario 3: Add document metadata

```
Given I am uploading a document
When I enter:
  - Category (Contract/Disclosure/Photo/Other)
  - Description (optional)
  And I click "Upload"
Then the document should be saved with the metadata
```

### Scenario 4: File size validation

```
Given I am uploading a document
When I select a very large file (e.g., >50MB)
Then I should see a warning
  And the file should not be uploaded
  Or I should be warned about storage limits
```

### Scenario 5: File type validation

```
Given I am uploading a document
When I select an unsupported file type
  Or a potentially dangerous file (.exe, .bat)
Then I should see a warning
  And the file should not be uploaded
```

### Scenario 6: Upload progress

```
Given I am uploading large documents
When the upload is in progress
Then I should see a progress indicator
  And the upload speed
  And the estimated time remaining
```

### Scenario 7: Document appears in contact's documents

```
Given I have uploaded documents to a contact
When I view the contact's details
Then the documents should be listed
  And each should show:
    - Filename
    - File type icon
    - File size
    - Upload date
    - Category
    - Description
```

### Scenario 8: Documents persist across restarts

```
Given I have uploaded documents to a contact
When I close the application
  And I restart the application
  And I open the contact
Then all documents should still be there
```

## Manual Testing Steps

### Test 1: Upload single document

1. Open a contact's details
2. Click "Upload Document"
3. Select a file
4. Verify the upload progress
5. Verify the document appears in the list
6. Verify all metadata is correct

### Test 2: Upload multiple documents

1. Open a contact's details
2. Click "Upload Documents"
3. Select multiple files
4. Verify all upload
5. Verify all appear in the list

### Test 3: Test with metadata

1. Upload a document
2. Add category and description
3. Verify the metadata is saved
4. View the document in the list
5. Verify the metadata is shown

### Test 4: Test file size limit

1. Try to upload a very large file
2. Verify the warning
3. Try with a file just under the limit
4. Verify it works

### Test 5: Test file type restrictions

1. Try to upload an executable
2. Verify the warning
3. Try to upload a PDF
4. Verify it works
5. Try various file types

### Test 6: Test upload progress

1. Upload large files
2. Verify the progress indicator
3. Verify it's accurate
4. Test with very large files

### Test 7: Test persistence

1. Upload several documents
2. Close the application
3. Restart the application
4. Open the contact
5. Verify all documents are there

### Test 8: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] "Upload Document" button is accessible from contact details
- [ ] Single files can be uploaded
- [ ] Multiple files can be uploaded
- [ ] Documents are stored encrypted in the database
- [ ] File metadata is captured and displayed
- [ ] File size limits are enforced
- [ ] File type restrictions are enforced
- [ ] Upload progress is shown
- [ ] Documents are associated with the correct contact
- [ ] Documents persist across restarts
- [ ] Documents can be categorized
- [ ] Documents can have descriptions
- [ ] Works on Windows, macOS, and Linux
- [ ] UI is intuitive and provides feedback
