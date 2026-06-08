# US-132: Save Search Criteria

## User Story

**As an** agent  
**I want to** save my search criteria for quick access later  
**So that** I don't have to re-enter the same search filters repeatedly

## Priority

**MVP:** Should Have

**Rationale:** Agents frequently search for the same criteria (e.g., "Hot leads from Zillow", "Contacts tagged as investor"). Saved searches allow one-click access to frequently used filters, improving productivity and workflow efficiency.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design saved search UI
- 2 hours: Implement save search functionality
- 1 hour: Implement load saved search
- 1 hour: Add saved search management (edit/delete)
- 1 hour: Test saved search functionality
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-028 (Search Contacts), US-087 (Search Leads)

**Blocks:** None

## Description

Users should be able to save search criteria (filters, tags, categories, status, etc.) with a custom name. Saved searches should be accessible from a "Saved Searches" menu or section. Users can run a saved search with one click, edit saved searches, and delete them when no longer needed.

Saved searches should work across contacts, leads, and properties.

## BDD Scenarios

### Scenario 1: Save a search

Given I have entered search criteria When I click "Save Search" And I enter a name for the search And I click "Save" Then the search criteria should be saved And it should be accessible from Saved Searches


### Scenario 2: Run a saved search

Given I have saved searches When I click on a saved search Then the search criteria should be applied And the results should be displayed


### Scenario 3: Edit a saved search

Given I have a saved search When I edit the saved search And I change the name or criteria And I save the changes Then the saved search should be updated


### Scenario 4: Delete a saved search

Given I have a saved search When I delete the saved search And I confirm the deletion Then the saved search should be removed And it should no longer appear in the list


### Scenario 5: Saved search includes all filters

Given I have applied multiple filters (tags, status, category, date range, etc.) When I save the search Then all filters should be saved And when I run it, all filters should be applied


### Scenario 6: Saved searches are organized by section

Given I have saved searches for contacts, leads, and properties When I view saved searches Then they should be organized by section:

Contact Searches
Lead Searches
Property Searches

### Scenario 7: Quick access to saved searches

Given I have saved searches When I open the search interface Then I should see my saved searches And I can click one to run it immediately


## Manual Testing Steps

### Test 1: Save a search

1. Go to Contacts
2. Apply several filters (tags, status, etc.)
3. Click "Save Search"
4. Enter a name
5. Save
6. Verify it appears in Saved Searches

### Test 2: Run a saved search

1. Go to Saved Searches
2. Click on a saved search
3. Verify the filters are applied
4. Verify the results are correct

### Test 3: Edit a saved search

1. Find a saved search
2. Edit the name or criteria
3. Save the changes
4. Run the search
5. Verify the changes are applied

### Test 4: Delete a saved search

1. Find a saved search
2. Delete it
3. Confirm the deletion
4. Verify it's removed from the list
5. Verify it can't be run

### Test 5: Test all filters are saved

1. Apply many different filters
2. Save the search
3. Run the search
4. Verify all filters are applied
5. Verify nothing is missing

### Test 6: Test organization by section

1. Save searches in different sections
2. View Saved Searches
3. Verify they're organized by section
4. Verify it's easy to find the right one

### Test 7: Test quick access

1. Open the search interface
2. Verify saved searches are visible
3. Click one
4. Verify it runs immediately

### Test 8: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Can save search criteria with a custom name
- [ ] Saved searches are accessible from a menu/section
- [ ] Can run a saved search with one click
- [ ] Can edit saved searches
- [ ] Can delete saved searches
- [ ] All filters are saved (tags, status, category, etc.)
- [ ] Saved searches are organized by section
- [ ] Quick access to saved searches from search interface
- [ ] Saved searches persist across restarts
- [ ] Works on Windows, macOS, and Linux
- [ ] UI is intuitive and clear
- [ ] Search names are unique