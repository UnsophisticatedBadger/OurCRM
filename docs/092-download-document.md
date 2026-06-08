# US-092: Download Document

## User Story

**As an** agent  
**I want to** download a document to my computer  
**So that** I can open it, print it, email it, or share it with others

## Priority

**MVP:** Must Have

**Rationale:** Documents stored in the CRM often need to be downloaded for use outside the system: emailing to clients, printing for closings, sharing with title companies, or opening in external applications. Download functionality is essential for document usefulness.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design download UI
- 1 hour: Implement download functionality
- 1 hour: Add download progress for large files
- 1 hour: Handle file save dialog
- 1 hour: Test download with various file types
- 1 hour: Test download with large files
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-091 (View Contact Documents), US-090 (Upload Document to Contact)

**Blocks:** US-093 (Delete Document)

## Description

Users should be able to download any document associated with a contact to their computer. The download should trigger the system's standard file save dialog, allowing the user to choose the location and filename. Large files should show download progress.

The downloaded file should be identical to the original upload (not corrupted or modified) and should open correctly in the appropriate application.

## BDD Scenarios

### Scenario 1: Download a document

```
Given I am viewing a contact's documents
  And I have a document I want to download
When I click the "Download" button or icon
Then the system file save dialog should appear
  And I can choose where to save the file
  And the file should be saved to my computer
  And it should match the original file
```

### Scenario 2: Download large file with progress

```
Given I am downloading a large document (>10MB)
When the download is in progress
Then I should see a progress indicator
  And the download speed
  And the estimated time remaining
```

### Scenario 3: Download preserves original filename

```
Given I have a document named "Purchase_Agreement.pdf"
When I download it
Then the default filename should be "Purchase_Agreement.pdf"
  And I can change it if I want
  But the original name is suggested
```

### Test 4: Downloaded file is not corrupted

```
Given I have downloaded a document
When I open it in the appropriate application
Then the file should open correctly
  And the content should be intact
  And there should be no corruption
```

### Test 5: Download multiple files

```
Given I have selected multiple documents
When I choose "Download Selected"
Then I should be prompted to choose a folder
  And all files should be saved to that folder
  With their original filenames
```

### Test 6: Open document directly

```
Given I have a viewable document (PDF, image)
When I click "Open" instead of "Download"
Then the document should open in the default application
  Without needing to download first
```

### Test 7: Download from document details

```
Given I am viewing a document's details
When I click "Download"
Then the file save dialog should appear
  And the document should be downloaded
```

### Test 8: Permission errors

```
Given I try to download a document
  But I don't have permission to save to the chosen location
When I select the location
Then I should see a clear error message
  And I can choose a different location
```

## Manual Testing Steps

### Test 1: Download a document

1. View a contact's documents
2. Click the download button on a document
3. Verify the file save dialog appears
4. Choose a location
5. Save the file
6. Verify the file is saved
7. Open the file
8. Verify it's not corrupted

### Test 2: Test large file download

1. Upload a large file (>10MB)
2. Download it
3. Verify the progress indicator
4. Verify it completes successfully
5. Verify the file size matches
6. Open it
7. Verify it works

### Test 3: Test filename preservation

1. Upload a file with a specific name
2. Download it
3. Verify the default filename matches
4. Try changing the filename
5. Verify the new name is used

### Test 4: Test file integrity

1. Upload a PDF
2. Download it
3. Compare file sizes (should be identical)
4. Open the downloaded file
5. Verify it opens correctly
6. Test with various file types (PDF, JPG, DOCX)

### Test 5: Test multiple downloads

1. Select multiple documents
2. Choose "Download Selected"
3. Verify the folder selection dialog
4. Choose a folder
5. Verify all files are saved
6. Verify they have correct names

### Test 6: Test open directly

1. Click "Open" on a PDF document
2. Verify it opens in the default PDF viewer
3. Test with an image
4. Verify it opens in the default image viewer
5. Test with various viewable types

### Test 7: Test permission errors

1. Try to download to a read-only location
2. Verify the error message
3. Try to download to a location without permission
4. Verify the error
5. Choose a different location
6. Verify it works

### Test 8: Test on all platforms

1. Test download on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Documents can be downloaded from the documents list
- [ ] System file save dialog appears
- [ ] User can choose download location
- [ ] Original filename is suggested
- [ ] Downloaded file matches the original
- [ ] Large files show download progress
- [ ] Multiple files can be downloaded at once
- [ ] Viewable documents can be opened directly
- [ ] Permission errors are handled gracefully
- [ ] Downloads work with all supported file types
- [ ] Works on Windows, macOS, and Linux
- [ ] Download is fast and reliable
- [ ] No file corruption during download
