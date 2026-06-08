# US-089: Create a Note

## User Story

**As an** agent  
**I want to** create standalone notes  
**So that** I can capture information that's not tied to a specific contact, lead, or property

## Priority

**MVP:** Must Have

**Rationale:** Agents accumulate general information: market insights, personal reminders, procedures, ideas, and miscellaneous information that doesn't fit into specific records. Standalone notes provide a place for this information without forcing it into inappropriate categories.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design note creation form
- 2 hours: Create form UI with rich text editor
- 1 hour: Implement note categorization
- 1 hour: Add tagging support
- 1 hour: Implement search functionality
- 1 hour: Save notes to database
- 1 hour: Test note creation
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-015 (Create the First Window), US-014 (Create Encrypted Database)

**Blocks:** US-089a (View Notes List), US-089b (Search Notes)

## Description

Users should be able to create standalone notes for information that isn't tied to a specific contact, lead, or property. Notes can include rich text formatting, categories, tags, and optional links to related records.

Notes are searchable, categorized, and can be quickly accessed. They provide a flexible way to capture and organize information that doesn't fit into structured records.

## BDD Scenarios

### Scenario 1: Open note creation form

```
Given I am in the Notes section
When I click "New Note"
Then the note creation form should open
  And the form should have:
    - Title
    - Rich text content editor
    - Category (Personal/Work/Idea/Procedure/Other)
    - Tags
    - Optional link to contact/lead/property
```

### Scenario 2: Create a simple note

```
Given the note form is open
When I enter a title and content
  And I click "Save"
Then the note should be saved
  And appear in the notes list
```

### Scenario 3: Create a note with rich formatting

```
Given the note form is open
When I use the rich text editor to format the content
  (bold, italic, lists, headings, etc.)
Then the formatting should be preserved when saved
  And displayed when viewing the note
```

### Scenario 4: Add tags to a note

```
Given I am creating a note
When I add tags (e.g., "important", "follow-up", "market")
Then the tags should be saved with the note
  And I can find the note by searching for tags
```

### Scenario 5: Link note to a record

```
Given I am creating a note
When I link it to a contact, lead, or property
Then the note should be associated with that record
  And accessible from the record's details
```

### Scenario 6: Categorize notes

```
Given I am creating a note
When I select a category
Then the note is organized by that category
  And I can filter notes by category
```

### Scenario 7: Note appears in list immediately

```
Given I have saved a new note
When I view the notes list
Then the new note should be visible
  With title, category, and date
```

### Scenario 8: Notes persist across restarts

```
Given I have created notes
When I close the application
  And I restart the application
  And I open the notes section
Then all my notes should be there
```

## Manual Testing Steps

### Test 1: Create a basic note

1. Go to Notes section
2. Click "New Note"
3. Enter a title
4. Enter some content
5. Save the note
6. Verify it appears in the list
7. Open the note
8. Verify the content is correct

### Test 2: Test rich text formatting

1. Create a note
2. Use the rich text editor
3. Add bold, italic, lists, headings
4. Save the note
5. Reopen it
6. Verify formatting is preserved
7. Test various formatting options

### Test 3: Test tags

1. Create a note with tags
2. Save it
3. Search for a tag
4. Verify the note is found
5. Try multiple tags
6. Verify they all work

### Test 4: Test linking

1. Create a note
2. Link it to a contact
3. Save it
4. Open the contact
5. Verify the note appears in the contact's notes
6. Click on it to open the note

### Test 5: Test categories

1. Create notes in different categories
2. View the notes list
3. Filter by category
4. Verify the filter works
5. Test all categories

### Test 6: Test search

1. Create several notes
2. Use the search function
3. Search for keywords
4. Verify matching notes are found
5. Search by tags
6. Verify it works

### Test 7: Test persistence

1. Create several notes
2. Close the application
3. Restart the application
4. Open the notes section
5. Verify all notes are there

### Test 8: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] "New Note" button is accessible from Notes section
- [ ] Note creation form opens
- [ ] Can create simple text notes
- [ ] Rich text formatting is supported
- [ ] Tags can be added to notes
- [ ] Notes can be categorized
- [ ] Notes can be linked to records
- [ ] Notes appear in list immediately
- [ ] Notes persist across restarts
- [ ] Notes are searchable
- [ ] Can filter by category
- [ ] Works on Windows, macOS, and Linux
- [ ] UI is intuitive and easy to use
- [ ] Data is encrypted in the database
