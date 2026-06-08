# US-029: Search Across All Fields

## User Story

**As an** agent  
**I want to** search across all contact fields including notes and tags  
**So that** I can find contacts even when I don't remember their exact name

## Priority

**MVP:** Must Have

**Rationale:** Agents often remember details about a contact from notes ("met at conference") or tags ("investor") rather than their name. Comprehensive search across all fields makes the CRM truly useful for finding information.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Extend search to include notes and tags
- 1 hour: Implement relevance ranking
- 1 hour: Add search result highlighting
- 1 hour: Test search across all fields
- 1 hour: Test performance with full-text search
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-028 (Search Contacts), US-025 (Add Notes), US-026 (Tag Contacts)

**Blocks:** None

## Description

The search functionality should extend beyond basic fields (name, email, phone) to include all contact data: notes, tags, addresses, and any other relevant information. This makes the search truly comprehensive and useful for finding contacts based on any information the user remembers.

Search results should be ranked by relevance, with name matches appearing before notes matches. The search should be fast even with hundreds of contacts and thousands of notes.

## BDD Scenarios

### Scenario 1: Search in notes

```
Given I have a contact with a note containing "conference"
When I search for "conference"
Then the contact should appear in search results
  Even if "conference" is not in the name, email, or phone
```

### Scenario 2: Search by tag

```
Given I have contacts tagged as "investor"
When I search for "investor"
Then all contacts with that tag should appear in results
```

### Scenario 3: Search in address

```
Given I have a contact with address "123 Main St, Houston"
When I search for "Houston" or "Main St"
Then the contact should appear in results
```

### Scenario 4: Relevance ranking

```
Given I search for "John"
  And I have "John Smith" (name match)
  And I have "Jane Doe" with a note mentioning "John"
Then "John Smith" should appear first
  And "Jane Doe" should appear second
  And the ranking should be clear
```

### Scenario 5: Search highlights matches

```
Given I search for "investor"
When results are displayed
Then matching text should be highlighted
  And it should be clear why each result matched
```

### Scenario 6: Search across multiple fields simultaneously

```
Given I have a contact with:
  - Name: "John Smith"
  - Email: "john@example.com"
  - Note: "Looking for investment properties"
When I search for "investment"
Then the contact should appear
  And the note should be highlighted
```

### Scenario 7: Empty search shows all

```
Given I am in the Contacts section
When the search box is empty
Then all contacts should be displayed
```

## Manual Testing Steps

### Test 1: Search in notes

1. Create a contact with a note: "Met at real estate conference in 2024"
2. Navigate to the Contacts section
3. Search for "conference"
4. Verify the contact appears in results
5. Verify the note text is highlighted

### Test 2: Search by tag

1. Create contacts with various tags
2. Search for a tag name
3. Verify contacts with that tag appear
4. Verify the tag is highlighted

### Test 3: Search in address

1. Create contacts with various addresses
2. Search for part of an address
3. Verify contacts are found
4. Test with city, street, ZIP code

### Test 4: Test relevance ranking

1. Create "John Smith" (name match for "John")
2. Create "Jane Doe" with note "Met John at conference"
3. Create "Bob Johnson" with email "john@example.com"
4. Search for "John"
5. Verify "John Smith" appears first
6. Verify "Bob Johnson" appears second (email match)
7. Verify "Jane Doe" appears third (note match)

### Test 5: Test highlighting

1. Search for a term
2. Verify matching text is highlighted in results
3. Check name, email, notes, tags
4. Verify highlighting is clear and visible

### Test 6: Test complex search

1. Create contacts with various data
2. Search for terms that appear in multiple fields
3. Verify all relevant contacts are found
4. Test with addresses, notes, tags, emails

### Test 7: Test performance

1. Create 500 contacts with extensive notes
2. Search for a term
3. Verify results appear quickly (under 300ms)
4. Verify the UI remains responsive

### Test 8: Test on all platforms

1. Test comprehensive search on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Search includes notes field
- [ ] Search includes tags
- [ ] Search includes address fields
- [ ] Results are ranked by relevance
- [ ] Name matches rank higher than note matches
- [ ] Matching text is highlighted
- [ ] Search works across multiple fields simultaneously
- [ ] Empty search shows all contacts
- [ ] Search is fast (under 300ms with 500 contacts)
- [ ] UI remains responsive
- [ ] Works on Windows, macOS, and Linux
- [ ] Clear indication of why each result matched
- [ ] Search is comprehensive but not overwhelming