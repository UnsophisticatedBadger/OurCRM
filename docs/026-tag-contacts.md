# US-026: Tag Contacts

## User Story

**As an** agent  
**I want to** add tags to contacts  
**So that** I can organize and categorize them

## Priority

**MVP:** Must Have

**Rationale:** Tags provide flexible categorization beyond rigid fields. Agents can use tags for "buyer", "seller", "past-client", "investor", "referral-source", or any custom categorization. Tags enable filtering and segmentation.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design tags UI
- 2 hours: Create tag input and display
- 1 hour: Implement add tag functionality
- 1 hour: Implement remove tag functionality
- 1 hour: Create tag management (predefined vs custom)
- 1 hour: Implement tag-based filtering
- 1 hour: Display tags as colored badges
- 1 hour: Test tag operations
- 1 hour: Test filtering by tags
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-022 (View Contact Details), US-020 (Create a New Contact)

**Blocks:** US-027 (Filter Contacts by Tags), US-028 (Search Contacts)

## Description

Users should be able to add tags to contacts for flexible categorization. Tags are short labels (like "buyer", "seller", "investor", "past-client") that help organize contacts beyond the structured fields. Tags should be displayed as colored badges on the contact and should be filterable.

Tags can be predefined (common categories) or custom (user-created). When viewing a contact, users should see all tags and be able to add or remove tags. The contact list should support filtering by tags.

## BDD Scenarios

### Scenario 1: Add a tag to a contact

```
Given I am viewing a contact's details
When I click "Add Tag"
  And I type a tag name
  And I press Enter or click "Add"
Then the tag should be added to the contact
  And it should appear as a colored badge
```

### Scenario 2: Add multiple tags

```
Given I am viewing a contact's details
When I add several tags (e.g., "buyer", "investor", "referral")
Then all tags should be displayed
  And each should have its own color
  And they should be clearly visible
```

### Scenario 3: Remove a tag

```
Given a contact has several tags
When I click the X on a tag
  Or I right-click and select "Remove"
Then the tag should be removed from the contact
  And it should no longer be displayed
```

### Scenario 4: Tags persist across restarts

```
Given I have added tags to contacts
When I close the application
  And I restart the application
  And I open the contact
Then all tags should still be there
```

### Scenario 5: Filter contacts by tag

```
Given I have contacts with various tags
  And I am in the Contacts section
When I click on a tag in the filter panel
  Or I select a tag from a dropdown
Then only contacts with that tag should be displayed
```

### Scenario 6: Clear tag filter

```
Given I have filtered contacts by a tag
When I click "Clear Filter" or "All Contacts"
Then all contacts should be displayed again
```

### Scenario 7: Predefined tags are available

```
Given I am adding a tag to a contact
When I start typing
Then I should see suggestions for common tags
  And I can select a suggestion or create a custom tag
```

### Scenario 8: Duplicate tags are prevented

```
Given a contact already has the tag "buyer"
When I try to add the tag "buyer" again
Then I should see a message that the tag already exists
  And the tag should not be duplicated
```

## Manual Testing Steps

### Test 1: Add tags to a contact

1. Open a contact's details
2. Click "Add Tag"
3. Type "buyer" and press Enter
4. Verify the tag appears as a colored badge
5. Add another tag "investor"
6. Verify both tags are displayed

### Test 2: Test multiple tags

1. Add 4-5 different tags to a contact
2. Verify all tags are displayed
3. Check that each has a different color (or consistent color scheme)
4. Verify the layout looks good with multiple tags

### Test 3: Remove tags

1. Add several tags to a contact
2. Click the X on one tag
3. Verify it's removed
4. Try right-click and "Remove"
5. Verify that also works

### Test 4: Test tag persistence

1. Add tags to several contacts
2. Close the application
3. Restart the application
4. Open the contacts
5. Verify all tags are still there

### Test 5: Test tag filtering

1. Create contacts with different tags
2. Go to the Contacts section
3. Filter by a specific tag
4. Verify only contacts with that tag are shown
5. Clear the filter
6. Verify all contacts are shown again

### Test 6: Test predefined tags

1. Start adding a tag
2. Verify suggestions appear for common tags
3. Select a suggestion
4. Verify it's added
5. Create a custom tag
6. Verify it works

### Test 7: Test duplicate prevention

1. Add "buyer" tag to a contact
2. Try to add "buyer" again
3. Verify the duplicate is prevented
4. Verify clear message about duplicate

### Test 8: Test on all platforms

1. Test tags on Windows
2. Verify they work
3. Test on macOS
4. Verify they work
5. Test on Linux
6. Verify they work
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] "Add Tag" button is accessible from contact details
- [ ] Tags can be added with text input
- [ ] Tags display as colored badges
- [ ] Multiple tags can be added to one contact
- [ ] Tags can be removed
- [ ] Tags persist across restarts
- [ ] Contacts can be filtered by tag
- [ ] Tag filter can be cleared
- [ ] Predefined tag suggestions are available
- [ ] Duplicate tags are prevented
- [ ] Tags are searchable
- [ ] Works on Windows, macOS, and Linux
- [ ] Tag colors are consistent and readable
- [ ] Tags are clearly visible on contact list and details