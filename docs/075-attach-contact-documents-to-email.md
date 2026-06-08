# US-075: Attach Contact Documents to Email

## User Story

**As an** agent  
**I want to** quickly attach documents that are already associated with a contact  
**So that** I don't have to search my computer for files I've already organized

## Priority

**MVP:** Should Have (could be deferred to post-MVP)

**Rationale:** This is a quality-of-life feature that improves workflow efficiency. Instead of searching the file system for documents, agents can select from documents already linked to the contact. While helpful, this can be deferred to v0.2 if needed for MVP timeline.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design document selection UI
- 1 hour: List contact's documents
- 1 hour: Allow multi-select of documents
- 1 hour: Add selected documents to email
- 1 hour: Test document selection
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-074 (Send Email with Attachments), US-076 (Attach Document to Contact - or similar)

**Blocks:** None

## Description

When composing an email to a contact, users should be able to quickly attach documents that are already associated with that contact. Instead of browsing the file system, they can select from a list of documents linked to the contact (contracts, photos, disclosures, etc.).

This feature requires that documents can be associated with contacts (which should be implemented as part of the document management features).

## BDD Scenarios

### Scenario 1: See contact's documents in email compose

```
Given a contact has several documents attached
  And I am composing an email to that contact
When I click "Attach from Contact's Documents"
Then I should see a list of the contact's documents
  And each document should show:
    - Filename
    - File type
    - File size
    - Date added
```

### Scenario 2: Select and attach documents

```
Given I am viewing the contact's documents
When I select one or more documents
  And I click "Attach Selected"
Then the documents should be added to the email attachments
  And the selection dialog should close
```

### Scenario 3: Search contact's documents

```
Given a contact has many documents
When I am selecting documents to attach
Then I should be able to search by filename
  And filter by file type
  To quickly find what I need
```

### Scenario 4: Preview document before attaching

```
Given I am viewing the contact's documents
When I click on a document
Then I should be able to preview it (if possible)
  And then decide whether to attach it
```

### Scenario 5: Contact has no documents

```
Given a contact has no documents
When I click "Attach from Contact's Documents"
Then I should see a message that no documents are available
  And an option to browse the file system instead
```

### Scenario 6: Mix contact documents and new files

```
Given I have attached some of the contact's documents
When I want to add more attachments
Then I can add files from the file system
  And the contact's documents and new files are all in the attachments list
```

### Scenario 7: Recent documents shown first

```
Given a contact has many documents
When I am selecting documents to attach
Then recently added documents should appear first
  Or I can sort by various criteria
```

## Manual Testing Steps

### Test 1: View contact's documents

1. Attach several documents to a contact
2. Open email compose for that contact
3. Click "Attach from Contact's Documents"
4. Verify the documents are listed
5. Verify all details are shown

### Test 2: Select and attach

1. View the contact's documents
2. Select one document
3. Click "Attach Selected"
4. Verify it's added to the email
5. Repeat with multiple documents
6. Verify all are attached

### Test 3: Test search

1. Have many documents for a contact
2. Open the document selection
3. Search for a specific filename
4. Verify the search works
5. Test with partial filenames

### Test 4: Test filter

1. Have various file types
2. Open the document selection
3. Filter by file type (e.g., PDFs only)
4. Verify the filter works

### Test 5: Test preview

1. Open the document selection
2. Click on a document
3. Verify the preview appears
4. Close the preview
5. Test with various file types

### Test 6: Test no documents

1. Create a contact with no documents
2. Open email compose
3. Click "Attach from Contact's Documents"
4. Verify the "no documents" message
5. Verify the option to browse file system

### Test 7: Test mix of sources

1. Attach some contact documents
2. Then add files from file system
3. Verify all are in the attachments list
4. Verify they're all distinguishable

### Test 8: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] "Attach from Contact's Documents" option is available
- [ ] Contact's documents are listed
- [ ] Each document shows filename, type, size, and date
- [ ] Documents can be selected (single or multiple)
- [ ] Selected documents are attached to the email
- [ ] Search by filename works
- [ ] Filter by file type works
- [ ] Document preview is available
- [ ] Empty state is clear when no documents exist
- [ ] Can mix contact documents and new files
- [ ] Works on Windows, macOS, and Linux
- [ ] UI is intuitive and efficient
- [ ] Saves time compared to file system browsing