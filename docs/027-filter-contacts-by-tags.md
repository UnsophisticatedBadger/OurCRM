# US-027: Filter Contacts by Tags

## User Story

**As an** agent  
**I want to** filter the contact list by tags  
**So that** I can quickly find specific groups of contacts

## Priority

**MVP:** Must Have

**Rationale:** As agents accumulate hundreds of contacts, finding specific groups becomes difficult. Tag-based filtering allows quick access to "all buyers", "all investors", "all past clients", etc., without scrolling through the entire list.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design filter UI (sidebar, dropdown, or panel)
- 2 hours: Implement tag filter logic
- 1 hour: Add "All Contacts" option to show everything
- 1 hour: Add tag count (show how many contacts have each tag)
- 1 hour: Implement multiple tag filtering (optional)
- 1 hour: Test filter functionality
- 1 hour: Test performance with many tags
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-026 (Tag Contacts), US-021 (View Contact List)

**Blocks:** None

## Description

Users should be able to filter the contact list by one or more tags. The filter UI should be easily accessible from the Contacts section and should show all available tags with the count of contacts for each tag. When a filter is applied, only contacts with the selected tag(s) are displayed.

The filter should be easy to clear and should update the contact count in real-time. Optionally, users could filter by multiple tags (show contacts that have all selected tags or any selected tag).

## BDD Scenarios

### Scenario 1: View available tags for filtering

```
Given I am in the Contacts section
  And I have contacts with various tags
When I look at the filter panel
Then I should see all unique tags
  And each tag should show the count of contacts with that tag
  And there should be an "All Contacts" option
```

### Scenario 2: Filter by single tag

```
Given I am in the Contacts section
  And I can see the filter panel with tags
When I click on a tag (e.g., "buyer")
Then the contact list should update to show only contacts with the "buyer" tag
  And the tag should be visually selected in the filter panel
```

### Scenario 3: Clear filter

```
Given I have filtered contacts by a tag
When I click "All Contacts" or "Clear Filter"
Then all contacts should be displayed again
  And no tag should be selected in the filter panel
```

### Scenario 4: Filter shows count

```
Given I have contacts with various tags
When I view the filter panel
Then each tag should show the number of contacts with that tag
  And "All Contacts" should show the total number of contacts
```

### Scenario 5: Empty filter result

```
Given I filter by a tag that has no contacts
When the filter is applied
Then I should see an empty state message
  And the message should say "No contacts with this tag"
```

### Scenario 6: Filter persists when navigating

```
Given I have filtered contacts by a tag
When I navigate to another section and back to Contacts
Then the filter should still be applied
  And the filtered results should still be shown
```

### Scenario 7: Filter with no tags

```
Given I have contacts but none have tags
When I view the Contacts section
Then the filter panel should show "All Contacts"
  And there should be no other tag options
  Or it should indicate "No tags available"
```

## Manual Testing Steps

### Test 1: View tag filter panel

1. Create contacts with various tags (buyer, seller, investor, etc.)
2. Navigate to the Contacts section
3. Verify the filter panel is visible
4. Verify all unique tags are listed
5. Verify each tag shows a count
6. Verify "All Contacts" is at the top

### Test 2: Filter by tag

1. Click on the "buyer" tag in the filter panel
2. Verify only contacts with the "buyer" tag are shown
3. Verify the tag is visually selected
4. Click on "seller"
5. Verify only contacts with "seller" tag are shown

### Test 3: Clear filter

1. Apply a tag filter
2. Click "All Contacts"
3. Verify all contacts are shown again
4. Verify no tag is selected
5. Test with a "Clear Filter" button if available

### Test 4: Verify tag counts

1. Create 3 contacts with "buyer" tag
2. Create 2 contacts with "seller" tag
3. Create 1 contact with "investor" tag
4. View the filter panel
5. Verify counts are correct (buyer: 3, seller: 2, investor: 1)
6. Verify "All Contacts" shows 6

### Test 5: Test empty filter result

1. Create a tag "test" but don't assign it to any contact
2. Or delete all contacts with a specific tag
3. Filter by that tag
4. Verify the empty state message appears
5. Verify it's clear what happened

### Test 6: Test filter persistence

1. Apply a filter
2. Navigate to Leads
3. Navigate back to Contacts
4. Verify the filter is still applied
5. Verify the same contacts are shown

### Test 7: Test with no tags

1. Create contacts without any tags
2. View the Contacts section
3. Verify the filter panel handles this gracefully
4. Verify "All Contacts" works
5. Verify no tags are shown (or appropriate message)

### Test 8: Test on all platforms

1. Test filtering on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Filter panel is visible in Contacts section
- [ ] All unique tags are listed
- [ ] Each tag shows count of contacts
- [ ] "All Contacts" option is available
- [ ] Clicking a tag filters the list
- [ ] Filtered tag is visually selected
- [ ] Filter can be cleared
- [ ] Empty state shown when no matches
- [ ] Filter persists when navigating away and back
- [ ] Tag counts update when contacts are added/removed/tags changed
- [ ] Works on Windows, macOS, and Linux
- [ ] Filter UI is intuitive and easy to use
- [ ] Performance is good even with many tags and contacts