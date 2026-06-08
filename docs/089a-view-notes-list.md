# US-089a: View Notes List

## User Story

**As an** agent  
**I want to** view a list of all my notes  
**So that** I can quickly find and access the information I've captured

## Priority

**MVP:** Must Have

**Rationale:** After creating notes, agents need to browse and access them efficiently. A well-organized notes list makes it easy to find information quickly and maintain context.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design notes list layout
- 2 hours: Create list UI with note cards/rows
- 1 hour: Implement filtering by category
- 1 hour: Add sorting options
- 1 hour: Add tag-based filtering
- 1 hour: Implement search
- 1 hour: Show note previews
- 1 hour: Test notes list
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-089 (Create a Note)

**Blocks:** US-089b (Search Notes), US-089c (Edit Note)

## Description

Users should be able to view all their notes in a clear, organized list. The list should show key information for each note: title, category, tags, creation date, and a preview of the content. The view should support filtering, sorting, and searching to help agents find specific notes quickly.

The notes list should be the primary way agents browse and access their notes, making it easy to find information when needed.

## BDD Scenarios

### Scenario 1: View notes list

```
Given I have created several notes
When I view the Notes section
Then I should see a list of all my notes
  And each note should display:
    - Title
    - Category
    - Tags
    - Creation date
    - Content preview
    - Linked records (if any)
```

### Scenario 2: Filter by category

```
Given I have notes in various categories
When I filter by "Work"
Then only work notes should be shown
  And the filter should be clearly indicated
```

### Scenario 3: Filter by tags

```
Given I have notes with various tags
When I filter by a specific tag
Then only notes with that tag should be shown
```

### Scenario 4: Sort notes

```
Given I have multiple notes
When I sort by:
  - Title
  - Creation date
  - Last modified
  - Category
Then the notes should be sorted accordingly
```

### Scenario 5: Search notes

```
Given I have many notes
When I search for keywords
Then matching notes should be shown
  Including matches in title, content, and tags
```

### Scenario 6: Note preview shows content

```
Given I am viewing the notes list
When I look at a note
Then I should see a preview of the content
  (first few lines or summary)
  So I can identify it without opening
```

### Scenario 7: Linked records are shown

```
Given a note is linked to a contact
When I view the note in the list
Then I should see the linked contact
  And I can click to open the contact
```

### Scenario 8: Empty state for no notes

```
Given I have no notes
When I view the Notes section
Then I should see an empty state message
  And a button to "Create Your First Note"
```

## Manual Testing Steps

### Test 1: View list with notes

1. Create several notes with various data
2. Navigate to the Notes section
3. Verify all notes are displayed
4. Verify the columns show the expected information
5. Verify the data is accurate

### Test 2: Test category filtering

1. Create notes in various categories
2. Filter by "Work"
3. Verify only work notes are shown
4. Clear the filter
5. Verify all notes are shown again

### Test 3: Test tag filtering

1. Create notes with various tags
2. Filter by a specific tag
3. Verify only matching notes are shown
4. Test with multiple tags
5. Verify it works

### Test 4: Test sorting

1. Create notes with various dates and titles
2. Click on each column header
3. Verify sorting works
4. Click again to reverse order
5. Verify the sort indicator updates

### Test 5: Test search

1. Have many notes
2. Use the search function
3. Search for keywords
4. Verify matching notes are shown
5. Test with partial words
6. Verify it works

### Test 6: Test content preview

1. Create notes with long content
2. View the list
3. Verify previews are shown
4. Verify they're not too long
5. Verify they're informative

### Test 7: Test linked records

1. Create notes linked to contacts
2. View the list
3. Verify the linked contacts are shown
4. Click on a linked contact
5. Verify it opens the contact

### Test 8: Test empty state

1. Delete all notes
2. View the Notes section
3. Verify the empty state message
4. Verify the "Create First Note" button

### Test 9: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Notes list displays all notes
- [ ] Each note shows title, category, tags, date, preview
- [ ] Can filter by category
- [ ] Can filter by tags
- [ ] Can sort by various criteria
- [ ] Can search across notes
- [ ] Content previews are shown
- [ ] Linked records are displayed
- [ ] Empty state is shown when no notes
- [ ] List loads quickly even with many notes
- [ ] Scrolling is smooth
- [ ] Works on Windows, macOS, and Linux
- [ ] UI is intuitive and well-organized
- [ ] Performance is good
