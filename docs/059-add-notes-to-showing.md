# US-059: Add Notes to a Showing

## User Story

**As an** agent  
**I want to** add notes to a showing (before, during, or after)  
**So that** I can capture important details about the buyer's reaction and feedback

## Priority

**MVP:** Must Have

**Rationale:** Showing notes are critical for remembering buyer reactions, concerns, and interests. Without notes, agents forget what was said at showings and lose valuable context for follow-ups. Notes help agents personalize their approach and make better recommendations.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design notes UI
- 1 hour: Create note input and display
- 1 hour: Implement add note functionality
- 1 hour: Add timestamps to notes
- 1 hour: Allow notes before, during, and after showing
- 1 hour: Test note creation and display
- 1 hour: Test persistence
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-056 (Schedule a Showing), US-058 (Mark Showing as Completed)

**Blocks:** None

## Description

Users should be able to add free-form text notes to any showing. Notes can be added before the showing (preparation notes), during the showing (quick notes), or after the showing (feedback notes). All notes are timestamped and displayed in chronological order.

Notes for showings are particularly important because they capture the buyer's real-time reactions and feedback. This context is invaluable for follow-up conversations and helping buyers find the right property.

## BDD Scenarios

### Scenario 1: Add a note to a showing

```
Given I am viewing a showing's details
When I click "Add Note"
Then a note input field should appear
  And I can type my note
  And I can click "Save" to add the note
```

### Scenario 2: Note appears in showing details

```
Given I have added a note to a showing
When I view the showing's details
Then the note should be displayed
  And it should show the note text
  And it should show when the note was added (timestamp)
```

### Scenario 3: Add notes before showing

```
Given I have a showing scheduled
When I add a note like "Bring pre-approval letter and property disclosures"
Then the note should be saved
  And it should be visible when I view the showing
```

### Scenario 4: Add notes during showing

```
Given I am at a showing
When I quickly add a note about the buyer's reaction
Then the note should be saved with a timestamp
  And I can review it later
```

### Scenario 5: Add notes after showing

```
Given I have completed a showing
When I add detailed notes about the buyer's feedback
Then the note should be saved
  And it should be associated with the completed showing
```

### Scenario 6: Multiple notes per showing

```
Given I have added several notes to a showing
When I view the showing's details
Then all notes should be displayed
  And they should be ordered chronologically
  And each note should have its own timestamp
```

### Scenario 7: Notes persist across restarts

```
Given I have added notes to a showing
When I close the application
  And I restart the application
  And I open the showing
Then all the notes should still be there
```

### Scenario 8: Notes are searchable

```
Given I have added notes with various text
When I search for text that appears in a note
Then showings with matching notes should appear in search results
```

## Manual Testing Steps

### Test 1: Add a note

1. Open a showing's details
2. Click "Add Note"
3. Type a note (e.g., "Buyer loved the kitchen but concerned about backyard size")
4. Click "Save"
5. Verify the note appears in the showing details
6. Verify the timestamp is correct

### Test 2: Add notes before showing

1. Schedule a showing
2. Add a preparation note
3. Verify the note is saved
4. View the showing later
5. Verify the note is still there

### Test 3: Add notes during showing

1. At a showing, quickly add a note
2. Verify it saves quickly
3. Verify the timestamp is accurate
4. Add another note during the same showing
5. Verify both are saved

### Test 4: Add notes after showing

1. Complete a showing
2. Add detailed feedback notes
3. Verify they save
4. View the completed showing
5. Verify the notes are associated

### Test 5: Test multiple notes

1. Add 3-4 notes to a showing at different times
2. View the showing details
3. Verify all notes are displayed
4. Verify the order is correct
5. Verify each has its own timestamp

### Test 6: Test note persistence

1. Add several notes to a showing
2. Close the application
3. Restart the application
4. Open the showing
5. Verify all notes are still there
6. Verify timestamps are correct

### Test 7: Test note search

1. Add notes with specific keywords to different showings
2. Use the search function
3. Search for a keyword that appears in a note
4. Verify the showing with that note appears in results

### Test 8: Test on all platforms

1. Test notes on Windows
2. Verify they work
3. Test on macOS
4. Verify they work
5. Test on Linux
6. Verify they work
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] "Add Note" button is accessible from showing details
- [ ] Note input field appears when clicked
- [ ] Notes can be saved with text
- [ ] Notes can be added before, during, and after showings
- [ ] Empty notes are rejected
- [ ] Notes display in showing details
- [ ] Notes show timestamps
- [ ] Notes are ordered chronologically
- [ ] Notes persist across restarts
- [ ] Notes are searchable
- [ ] Notes are associated with the correct showing
- [ ] Notes are encrypted in the database
- [ ] Works on Windows, macOS, and Linux
- [ ] Notes are clearly displayed and readable