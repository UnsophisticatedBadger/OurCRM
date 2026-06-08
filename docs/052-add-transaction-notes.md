# US-052: Add Transaction Notes

## User Story

**As an** agent  
**I want to** add notes to a transaction  
**So that** I can track important details, communications, and issues throughout the closing process

## Priority

**MVP:** Must Have

**Rationale:** Transactions involve many parties, deadlines, and moving pieces. Notes are essential for tracking conversations with buyers, sellers, lenders, title companies, and other stakeholders. Without notes, agents lose critical context and make mistakes.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design notes UI
- 1 hour: Create note input and display
- 1 hour: Implement add note functionality
- 1 hour: Add timestamps to notes
- 1 hour: Implement note history
- 1 hour: Add note categories (optional)
- 1 hour: Test note creation and display
- 1 hour: Test persistence
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-049 (View Transaction Details), US-047 (Create a New Transaction)

**Blocks:** None

## Description

Users should be able to add free-form text notes to any transaction. Notes are displayed in chronological order (newest first or oldest first) with timestamps showing when each note was added. Notes are searchable and can be edited or deleted if needed.

Notes are where agents capture the "story" of a transaction - "Buyer requested repair credits", "Seller agreed to closing date of March 15", "Title company found issue with survey", etc. This context is invaluable for managing complex deals.

## BDD Scenarios

### Scenario 1: Add a note to a transaction

```
Given I am viewing a transaction's details
When I click "Add Note"
Then a note input field should appear
  And I can type my note
  And I can click "Save" to add the note
```

### Scenario 2: Note appears in transaction details

```
Given I have added a note to a transaction
When I view the transaction's details
Then the note should be displayed
  And it should show the note text
  And it should show when the note was added (timestamp)
```

### Scenario 3: Add multiple notes

```
Given I have added several notes to a transaction
When I view the transaction's details
Then all notes should be displayed
  And they should be ordered chronologically
  And each note should have its own timestamp
```

### Scenario 4: Notes persist across restarts

```
Given I have added notes to a transaction
When I close the application
  And I restart the application
  And I open the transaction
Then all the notes should still be there
```

### Scenario 5: Empty note is rejected

```
Given I am adding a note to a transaction
When I leave the note text empty
  And I click "Save"
Then I should see an error message
  And the note should not be saved
```

### Scenario 6: Note is searchable

```
Given I have added notes with various text
When I search for text that appears in a note
Then transactions with matching notes should appear in search results
```

### Scenario 7: Long notes are handled properly

```
Given I am adding a note
When I type a very long note (1000+ characters)
Then the note should be saved
  And it should display properly in the details view
  And it should wrap or scroll as needed
```

### Scenario 8: Notes show author (optional)

```
Given I have added notes to a transaction
When I view the notes
Then each note should show who added it (if multi-user)
  Or "Me" for single-user systems
```

## Manual Testing Steps

### Test 1: Add a note

1. Open a transaction's details
2. Click "Add Note"
3. Type a note (e.g., "Buyer requested closing date of March 15")
4. Click "Save"
5. Verify the note appears in the transaction details
6. Verify the timestamp is correct

### Test 2: Add multiple notes

1. Open a transaction's details
2. Add 3 different notes at different times
3. Verify all 3 notes are displayed
4. Verify the order is correct (newest first or oldest first)
5. Verify each has its own timestamp

### Test 3: Test empty note

1. Open a transaction's details
2. Click "Add Note"
3. Leave the note empty
4. Click "Save"
5. Verify the error message
6. Verify no empty note is saved

### Test 4: Test note persistence

1. Add several notes to a transaction
2. Close the application
3. Restart the application
4. Open the transaction
5. Verify all notes are still there
6. Verify timestamps are correct

### Test 5: Test long notes

1. Add a note with 1000+ characters
2. Verify it saves
3. View it in the transaction details
4. Verify it displays properly
5. Check that it wraps or scrolls as needed

### Test 6: Test note search

1. Add notes with specific keywords to different transactions
2. Use the search function
3. Search for a keyword that appears in a note
4. Verify the transaction with that note appears in results
5. Verify the note text is searchable

### Test 7: Test on all platforms

1. Test notes on Windows
2. Verify they work
3. Test on macOS
4. Verify they work
5. Test on Linux
6. Verify they work
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] "Add Note" button is accessible from transaction details
- [ ] Note input field appears when clicked
- [ ] Notes can be saved with text
- [ ] Empty notes are rejected
- [ ] Notes display in transaction details
- [ ] Notes show timestamps
- [ ] Notes are ordered chronologically
- [ ] Notes persist across restarts
- [ ] Notes are searchable
- [ ] Long notes are handled properly
- [ ] Notes are associated with the correct transaction
- [ ] Notes are encrypted in the database
- [ ] Works on Windows, macOS, and Linux
- [ ] Notes are clearly displayed and readable