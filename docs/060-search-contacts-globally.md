# US-060: Search Contacts Globally

## User Story

**As an** agent  
**I want to** search for contacts from anywhere in the application  
**So that** I can quickly find someone without navigating to the Contacts section first

## Priority

**MVP:** Must Have

**Rationale:** Global search is a productivity multiplier. Instead of clicking through sections to find a contact, agents can press a keyboard shortcut and search from anywhere. This is standard in modern applications and significantly improves workflow efficiency.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design global search UI (command palette style)
- 2 hours: Implement global search activation (Ctrl+K or Cmd+K)
- 2 hours: Create search interface with results
- 1 hour: Implement search across contacts
- 1 hour: Add keyboard navigation
- 1 hour: Add recent searches or quick actions
- 1 hour: Test global search performance
- 1 hour: Test keyboard shortcuts
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-028 (Search Contacts), US-015 (Create the First Window)

**Blocks:** US-061 (Search Across All Sections), US-062 (Quick Actions Menu)

## Description

Users should be able to open a global search interface from anywhere in the application using a keyboard shortcut (Ctrl+K or Cmd+K). The search interface should be a command-palette style overlay that allows quick searching across contacts. Results should appear as the user types and should be navigable with keyboard arrows.

The global search should be fast, intuitive, and should not disrupt the current workflow. Pressing Escape should close the search and return to the previous view.

## BDD Scenarios

### Scenario 1: Open global search

```
Given I am anywhere in the application
When I press Ctrl+K (or Cmd+K on macOS)
Then the global search interface should open
  And it should be focused on the search input
  And I can start typing immediately
```

### Scenario 2: Search for a contact

```
Given the global search is open
When I type a contact name
Then matching contacts should appear in the results
  And results should update as I type
```

### Scenario 3: Navigate results with keyboard

```
Given the global search is open
  And I see search results
When I press the down arrow key
Then the next result should be highlighted
When I press the up arrow key
Then the previous result should be highlighted
When I press Enter
Then the selected contact should open
```

### Scenario 4: Close global search

```
Given the global search is open
When I press Escape
  Or I click outside the search
Then the search should close
  And I should return to my previous view
```

### Scenario 5: Show no results state

```
Given the global search is open
When I search for something that doesn't match
Then I should see a "No results found" message
  And it should suggest clearing the search
```

### Scenario 6: Search is fast

```
Given the global search is open
When I type in the search box
Then results should appear within 300ms
  And the UI should remain responsive
```

### Scenario 7: Global search works from any section

```
Given I am in the Leads section
When I press Ctrl+K
Then the global search should open
  And I can search for contacts
Given I am in the Properties section
When I press Ctrl+K
Then the global search should open
  And I can search for contacts
```

### Scenario 8: Clear search

```
Given the global search is open
  And I have typed a search query
When I clear the search box
Then all contacts should be shown (or no results)
  And I can start a new search
```

## Manual Testing Steps

### Test 1: Open global search

1. Open OurCRM
2. From the main window, press Ctrl+K (or Cmd+K on macOS)
3. Verify the global search interface opens
4. Verify the search input is focused
5. Verify you can start typing immediately

### Test 2: Search for a contact

1. Open global search
2. Type a contact name
3. Verify matching contacts appear
4. Verify results update as you type
5. Test with partial names

### Test 3: Test keyboard navigation

1. Open global search
2. Type to get results
3. Press down arrow to navigate
4. Verify the highlight moves
5. Press up arrow
6. Verify it moves back
7. Press Enter on a result
8. Verify the contact opens

### Test 4: Test close

1. Open global search
2. Press Escape
3. Verify the search closes
4. Verify you return to your previous view
5. Test clicking outside the search
6. Verify it also closes

### Test 5: Test no results

1. Open global search
2. Type something that doesn't match
3. Verify the "No results found" message
4. Clear the search
5. Verify you can search again

### Test 6: Test from different sections

1. Navigate to Leads
2. Open global search
3. Verify it works
4. Navigate to Properties
5. Open global search
6. Verify it works
7. Test from all major sections

### Test 7: Test performance

1. Open global search
2. Type a search query
3. Measure response time
4. Verify it's under 300ms
5. Test with many contacts

### Test 8: Test on all platforms

1. Test global search on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Global search opens with Ctrl+K (or Cmd+K)
- [ ] Search input is focused when opened
- [ ] Search works across all contacts
- [ ] Results appear as user types
- [ ] Results are navigable with arrow keys
- [ ] Enter opens the selected contact
- [ ] Escape closes the search
- [ ] Clicking outside closes the search
- [ ] No results state is clear
- [ ] Search is fast (under 300ms)
- [ ] Works from any section
- [ ] Works on Windows, macOS, and Linux
- [ ] Search interface is intuitive and non-intrusive