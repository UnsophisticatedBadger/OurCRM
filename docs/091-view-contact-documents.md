# US-091: View Contact Documents

## User Story

**As an** agent  
**I want to** view all documents associated with a contact  
**So that** I can quickly find and access client-related files

## Priority

**MVP:** Must Have

**Rationale:** After uploading documents, agents need to see them organized and easily accessible. The documents view is the primary way agents retrieve contracts, photos, and other files for their contacts.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design documents list view
- 1 hour: Display documents in contact details
- 1 hour: Add filtering by category
- 1 hour: Add sorting options
- 1 hour: Add document search
- 1 hour: Test documents view
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-090 (Upload Document to Contact)

**Blocks:** US-092 (Download Document), US-093 (Delete Document)

## Description

Users should be able to view all documents associated with a contact in a clear, organized list. Each document should show its filename, file type icon, file size, upload date, category, and description. The view should support filtering by category, sorting by various criteria, and searching by filename.

The documents list should be easily accessible from the contact's details page and should make it quick to find specific documents among potentially dozens of files.

## BDD Scenarios

### Scenario 1: View documents list

```
Given a contact has several documents
When I view the contact's details
Then I should see a documents section
  And all documents should be listed
  And each should show:
    - Filename
    - File type icon
    - File size
    - Upload date
    - Category
    - Description (if provided)
```

### Scenario 2: Filter by category

```
Given a contact has documents in various categories
When I filter by "Contracts"
Then only contract documents should be shown
  And the filter should be clearly indicated
```

### Scenario 3: Sort documents

```
Given a contact has multiple documents
When I sort by:
  - Filename
  - Upload date
  - File size
  - Category
Then the documents should be sorted accordingly
```

### Scenario 4: Search documents

```
Given a contact has many documents
When I search for a filename or keyword
Then matching documents should be shown
  And the search should be fast
```

### Scenario 5: Empty state for no documents

```
Given a contact has no documents
When I view the contact's details
Then I should see a message like "No documents yet"
  And a button to "Upload First Document"
```

### Scenario 6: Document count by category

```
Given a contact has documents in various categories
When I view the documents section
Then I should see counts by category:
  - Contracts (3)
  - Disclosures (5)
  - Photos (12)
  - Other (2)
```

### Scenario 7: Click document to open or download

```
Given I am viewing the documents list
When I click on a document
Then I should be able to:
  - Open it (if it's a viewable type)
  - Download it to my computer
  - See full details
```

### Scenario 8: Total storage used

```
Given a contact has multiple documents
When I view the documents section
Then I should see the total storage used
  E.g., "Total: 45.2 MB across 8 documents"
```

## Manual Testing Steps

### Test 1: View documents list

1. Upload several documents to a contact
2. View the contact's details
3. Verify the documents section is visible
4. Verify all documents are listed
5. Verify all metadata is shown

### Test 2: Test filtering

1. Have documents in various categories
2. Filter by "Contracts"
3. Verify only contracts are shown
4. Filter by "Photos"
5. Verify only photos are shown
6. Clear the filter
7. Verify all are shown again

### Test 3: Test sorting

1. Have multiple documents
2. Sort by filename
3. Verify alphabetical order
4. Sort by upload date
5. Verify chronological order
6. Sort by file size
7. Verify size order

### Test 4: Test search

1. Have many documents
2. Search for a specific filename
3. Verify matching documents are shown
4. Search for partial filename
5. Verify it works
6. Clear the search
7. Verify all are shown again

### Test 5: Test empty state

1. Create a contact with no documents
2. View the contact's details
3. Verify the "No documents yet" message
4. Verify the "Upload First Document" button
5. Click the button
6. Verify it opens the upload dialog

### Test 6: Test category counts

1. Have documents in various categories
2. View the documents section
3. Verify the counts are accurate
4. Verify they're displayed clearly

### Test 7: Test document actions

1. View documents list
2. Click on a document
3. Verify you can open or download it
4. Verify the file is not corrupted
5. Test with various file types

### Test 8: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Documents list is visible in contact details
- [ ] Each document shows all metadata
- [ ] Can filter by category
- [ ] Can sort by various criteria
- [ ] Can search by filename
- [ ] Empty state is shown when no documents
- [ ] Category counts are displayed
- [ ] Documents can be opened or downloaded
- [ ] Total storage is shown
- [ ] Documents are listed chronologically by default
- [ ] Performance is good even with many documents
- [ ] Works on Windows, macOS, and Linux
- [ ] UI is intuitive and well-organized
