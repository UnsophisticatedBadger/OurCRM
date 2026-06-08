# US-089b: Search Notes

## User Story

**As an** agent  
**I want to** search through my notes by keyword  
**So that** I can quickly find specific information I've captured

## Priority

**MVP:** Must Have

**Rationale:** As notes accumulate, finding specific information becomes challenging. Search functionality allows agents to locate notes quickly by searching title, content, tags, or categories.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design search UI
- 1 hour: Implement full-text search
- 1 hour: Add search filters
- 1 hour: Display search results
- 1 hour: Highlight matches in results
- 1 hour: Test search functionality
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-089 (Create a Note), US-089a (View Notes List)

**Blocks:** None

## Description

Users should be able to search through their notes using keywords. The search should look across note titles, content, tags, and categories. Results should be ranked by relevance with the most relevant notes appearing first.

The search should be fast, support partial matches, and highlight the matching text in the results. Users should be able to search within a specific category or tag, or across all notes.

## BDD Scenarios

### Scenario 1: Basic note search

```
Given I have many notes
When I enter a search term
Then matching notes should be displayed
  Including notes where the term appears in:
    - Title
    - Content
    - Tags
    - Category
```

### Scenario 2: Search with multiple keywords

```
Given I am searching notes
When I enter multiple keywords
Then notes matching ALL keywords should be shown
  (Boolean AND search)
```

### Scenario 3: Search within category

```
Given I am searching notes
When I select a category filter
  And enter a search term
Then only notes in that category should be searched
  And matching notes should be shown
```

### Scenario 4: Search by tag

```
Given I have notes with various tags
When I search for a tag
Then all notes with that tag should be shown
  Even if the tag doesn't appear in the content
```

### Scenario 5: Highlight matching text

```
Given I have performed a search
When I view the results
Then the matching text should be highlighted
  In both title and content preview
  So I can see why each note matched
```

### Scenario 6: Search results are ranked

```
Given I have performed a search
When I view the results
Then the most relevant notes should appear first
  Based on:
    - Where the match occurs (title > content > tags)
    - How many times the term appears
    - Recency
```

### Scenario 7: No results found

```
Given I search for something that doesn't match
When the search completes
Then I should see "No notes found"
  And suggestions to try different keywords
```

### Scenario 8: Search is fast

```
Given I have 500 notes
When I search for a term
Then results should appear within 500ms
  And the UI should remain responsive
```

## Manual Testing Steps

### Test 1: Basic search

1. Create notes with various content
2. Enter a search term
3. Verify matching notes are shown
4. Test with terms in title
5. Test with terms in content
6. Test with terms in tags

### Test 2: Test multiple keywords

1. Enter multiple keywords
2. Verify only notes matching all are shown
3. Try different keyword combinations
4. Verify the AND logic works

### Test 3: Test category filter

1. Create notes in various categories
2. Select a category filter
3. Enter a search term
4. Verify only that category is searched
5. Verify the results are correct

### Test 4: Test tag search

1. Create notes with various tags
2. Search for a tag
3. Verify notes with that tag are shown
4. Test with multiple tags

### Test 5: Test highlighting

1. Perform a search
2. View the results
3. Verify matching text is highlighted
4. Check both title and content
5. Verify highlighting is clear

### Test 6: Test ranking

1. Create notes with varying relevance
2. Search for a term
3. Verify the order (most relevant first)
4. Check title matches rank higher
5. Check multiple matches rank higher

### Test 7: Test no results

1. Search for something that doesn't exist
2. Verify the "No notes found" message
3. Verify suggestions are helpful
4. Try a different search
5. Verify results appear

### Test 8: Test performance

1. Create many notes
2. Search and measure time
3. Verify it's fast
4. Test UI responsiveness

### Test 9: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Can search by keyword
- [ ] Searches across title, content, tags, category
- [ ] Multiple keywords work (AND logic)
- [ ] Can filter by category
- [ ] Can search by tag
- [ ] Matching text is highlighted
- [ ] Results are ranked by relevance
- [ ] No results state is clear
- [ ] Search is fast (under 500ms with 500 notes)
- [ ] UI is responsive during search
- [ ] Works on Windows, macOS, and Linux
- [ ] Search is intuitive and accurate
- [ ] Performance is good
