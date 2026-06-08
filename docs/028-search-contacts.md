# US-028: Search Contacts

## User Story

**As an** agent  
**I want to** search for contacts by name, email, or phone  
**So that** I can quickly find specific people

## Priority

**MVP:** Must Have

**Rationale:** With hundreds of contacts, scrolling through the list is inefficient. Search allows agents to find someone in seconds by typing a name, email, or phone number. This is one of the most frequently used features in any CRM.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design search UI (search box location and behavior)
- 2 hours: Implement multi-field search
- 1 hour: Add inline results (as you type)
- 1 hour: Implement case-insensitive search
- 1 hour: Add partial match support
- 1 hour: Implement keyboard shortcut (Ctrl+F or /)
- 1 hour: Highlight matching text in results
- 1 hour: Test search with various queries
- 1 hour: Test performance
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-021 (View Contact List), US-020 (Create a New Contact)

**Blocks:** US-029 (Search Across All Fields)

## Description

Users should be able to search contacts by typing in a search box. The search should look across multiple fields (name, email, phone, notes, tags) and return results as the user types (inline search). Results should be ranked by relevance, with exact matches appearing first.

The search should be fast (results appear within 300ms) and should work with partial matches (typing "Joh" should find "John Smith"). The search box should be easily accessible and should support keyboard shortcuts.

## BDD Scenarios

### Scenario 1: Search by name

```
Given I am in the Contacts section
  And I have contacts in the database
When I type "John" in the search box
Then I should see all contacts with "John" in their name
  And results should appear as I type (inline search)
  And matching text should be highlighted
```

### Scenario 2: Search by email

```
Given I am in the Contacts section
When I type an email address or part of it
Then I should see all contacts with matching email
  And the search should be case-insensitive
```

### Scenario 3: Search by phone

```
Given I am in the Contacts section
When I type a phone number or part of it
Then I should see all contacts with matching phone number
  And the search should work with formatted or unformatted numbers
```

### Scenario 4: Search is case-insensitive

```
Given I have a contact named "John Smith"
When I search for "john" (lowercase)
  Or "JOHN" (uppercase)
  Or "JoHn" (mixed case)
Then I should find the contact regardless of case
```

### Scenario 5: Partial match

```
Given I have a contact named "Johnson"
When I search for "John"
Then I should find "Johnson" (partial match)
  And the contact should appear in results
```

### Scenario 6: No results found

```
Given I am in the Contacts section
When I search for something that doesn't match any contact
Then I should see an empty state message
  And the message should say "No contacts found"
  And it should suggest clearing the search
```

### Scenario 7: Clear search

```
Given I have typed a search query
When I clear the search box
  Or I press Escape
Then all contacts should be displayed again
  And the search results should disappear
```

### Scenario 8: Search performance

```
Given I have 500 contacts
When I type in the search box
Then results should appear within 300ms
  And the UI should remain responsive
  And typing should not lag
```

### Scenario 9: Keyboard shortcut for search

```
Given I am in the Contacts section
When I press Ctrl+F (or Cmd+F on macOS)
  Or I press the forward slash key
Then the search box should be focused
  And I can start typing immediately
```

## Manual Testing Steps

### Test 1: Basic search by name

1. Create 10 contacts with various names
2. Navigate to the Contacts section
3. Type "John" in the search box
4. Verify only contacts with "John" in the name are shown
5. Verify results appear as you type
6. Clear the search
7. Verify all contacts are shown again

### Test 2: Search by email

1. Create contacts with various email addresses
2. Type part of an email in the search
3. Verify the contact is found
4. Try different parts of the email (username, domain)
5. Verify both work

### Test 3: Search by phone

1. Create contacts with various phone numbers
2. Type part of a phone number
3. Verify the contact is found
4. Try with and without formatting
5. Verify both work

### Test 4: Test case insensitivity

1. Create a contact named "John Smith"
2. Search for "john" - verify it's found
3. Search for "JOHN" - verify it's found
4. Search for "JoHn" - verify it's found
5. Verify all work the same

### Test 5: Test partial matching

1. Create contacts: "John Smith", "Johnson", "Mary Johnson"
2. Search for "John" - verify all three are found
3. Search for "Johns" - verify "Johnson" and "Mary Johnson" are found
4. Search for "Smith" - verify only "John Smith" is found

### Test 6: Test no results

1. Search for "xyz123" (something that doesn't exist)
2. Verify the empty state message appears
3. Verify it's clear what happened
4. Clear the search
5. Verify contacts are shown again

### Test 7: Test search performance

1. Create 500+ contacts (use a script or import)
2. Navigate to the Contacts section
3. Type in the search box
4. Measure response time
5. Verify it's under 300ms
6. Test scrolling and UI responsiveness

### Test 8: Test keyboard shortcuts

1. Navigate to the Contacts section
2. Press Ctrl+F (or Cmd+F on macOS)
3. Verify the search box is focused
4. Type a search query
5. Verify it works
6. Test with the / key
7. Verify it also works

### Test 9: Test on all platforms

1. Test search on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Search box is visible and accessible
- [ ] Search works across name, email, phone fields
- [ ] Results appear as user types (inline)
- [ ] Search is case-insensitive
- [ ] Partial matches are supported
- [ ] Matching text is highlighted in results
- [ ] No results state is clear and helpful
- [ ] Search can be cleared easily
- [ ] Search is fast (under 300ms with 500 contacts)
- [ ] Keyboard shortcuts work (Ctrl+F, /)
- [ ] UI remains responsive during search
- [ ] Works on Windows, macOS, and Linux
- [ ] Search box is clearly visible and intuitive