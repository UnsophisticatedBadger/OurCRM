# US-025: Add Notes to a Contact

## User Story

**As an** agent  
**I want to** add notes to a contact  
**So that** I can remember important details about them

## Priority

**MVP:** Must Have

**Rationale:** Notes are where agents store the context that makes a CRM valuable - reminders, preferences, conversation details, and other information that doesn't fit into structured fields. Without notes, the CRM is just a digital address book.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design notes UI
- 2 hours: Create note input and display
- 1 hour: Implement add note functionality
- 1 hour: Add timestamps to notes
- 1 hour: Implement note history
- 1 hour: Allow editing/deleting notes (optional)
- 1 hour: Test note creation and display
- 1 hour: Test persistence
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-022 (View Contact Details)

**Blocks:** None

## Description

Users should be able to add free-form text notes to any contact. Notes are displayed in chronological order (newest first or oldest first) with timestamps showing when each note was added. Notes should be searchable and can be edited or deleted if needed.

Notes are where agents capture the "why" behind their relationships - "Prefers email over phone", "Looking to buy in 6 months", "Spouse is also a realtor", etc. This contextual information is what makes a CRM valuable.

## BDD Scenarios

### Scenario 1: Add a note to a contact

```
Given I am viewing a contact's details
When I click "Add Note"
Then a note input field should appear
  And I can type my note
  And I can click "Save" to add the note
```

### Scenario 2: Note appears in contact details

```
Given I have added a note to a contact
When I view the contact's details
Then the note should be displayed
  And it should show the note text
  And it should show when the note was added (timestamp)
  And it should show in chronological order
```

### Scenario 3: Add multiple notes

```
Given I have added several notes to a contact
When I view the contact's details
Then all notes should be displayed
  And they should be ordered (newest first or oldest first)
  And each note should have its own timestamp
```

### Scenario 4: Notes persist across restarts

```
Given I have added notes to a contact
When I close the application
  And I restart the application
  And I open the contact
Then all the notes should still be there
```

### Scenario 5: Empty note is rejected

```
Given I am adding a note to a contact
When I leave the note text empty
  And I click "Save"
Then I should see an error message
  And the note should not be saved
```

### Scenario 6: Note is searchable

```
Given I have added notes with various text
When I search for text that appears in a note
Then contacts with matching notes should appear in search results
```

### Scenario 7: Long notes are handled properly

```
Given I am adding a note
When I type a very long note (1000+ characters)
Then the note should be saved
  And it should display properly in the details view
  And it should wrap or scroll as needed
```

## Manual Testing Steps

### Test 1: Add a note

1. Open a contact's details
2. Click "Add Note"
3. Type a note (e.g., "Prefers email communication")
4. Click "Save"
5. Verify the note appears in the contact details
6. Verify the timestamp is correct

### Test 2: Add multiple notes

1. Open a contact's details
2. Add 3 different notes at different times
3. Verify all 3 notes are displayed
4. Verify the order is correct (newest first or oldest first)
5. Verify each has its own timestamp

### Test 3: Test empty note

1. Open a contact's details
2. Click "Add Note"
3. Leave the note empty
4. Click "Save"
5. Verify the error message
6. Verify no empty note is saved

### Test 4: Test note persistence

1. Add several notes to a contact
2. Close the application
3. Restart the application
4. Open the contact
5. Verify all notes are still there
6. Verify timestamps are correct

### Test 5: Test long notes

1. Add a note with 1000+ characters
2. Verify it saves
3. View it in the contact details
4. Verify it displays properly
5. Check that it wraps or scrolls as needed

### Test 6: Test note search

1. Add notes with specific keywords to different contacts
2. Use the search function
3. Search for a keyword that appears in a note
4. Verify the contact with that note appears in results
5. Verify the note text is searchable

### Test 7: Test note editing (if implemented)

1. Add a note
2. Edit the note
3. Save the changes
4. Verify the updated text is displayed
5. Verify the timestamp updates or shows "edited"

### Test 8: Test note deletion (if implemented)

1. Add a note
2. Delete the note
3. Verify it's removed
4. Verify it can be deleted without deleting the contact

### Test 9: Test on all platforms

1. Test notes on Windows
2. Verify they work
3. Test on macOS
4. Verify they work
5. Test on Linux
6. Verify they work
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] "Add Note" button is accessible from contact details
- [ ] Note input field appears when clicked
- [ ] Notes can be saved with text
- [ ] Empty notes are rejected
- [ ] Notes display in contact details
- [ ] Notes show timestamps
- [ ] Notes are ordered chronologically
- [ ] Notes persist across restarts
- [ ] Notes are searchable
- [ ] Long notes are handled properly
- [ ] Notes are associated with the correct contact
- [ ] Notes are encrypted in the database
- [ ] Works on Windows, macOS, and Linux
- [ ] Notes are clearly displayed and readable