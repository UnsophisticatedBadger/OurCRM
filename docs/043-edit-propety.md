# US-043: Edit a Property

## User Story

**As an** agent  
**I want to** edit a property's information  
**So that** I can keep listings up to date with price changes, status updates, and new information

## Priority

**MVP:** Must Have

**Rationale:** Property information changes frequently - price reductions, status changes (Active to Pending to Sold), new photos, updated descriptions. Agents need to be able to update properties without deleting and recreating them.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Create edit form (similar to create form)
- 1 hour: Pre-populate form with existing data
- 1 hour: Implement update logic
- 1 hour: Add validation
- 1 hour: Test edit functionality
- 1 hour: Test data persistence
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-042 (View Property Details), US-040 (Create a New Property Listing)

**Blocks:** None

## Description

Users should be able to edit any property's information. The edit form should be similar to the create form but pre-populated with the property's current data. After making changes and clicking "Save", the property is updated in the database.

The edit can be accessed from the property details view by clicking the "Edit" button. The form should validate the data the same way as the create form. Users should be able to cancel without saving changes.

## BDD Scenarios

### Scenario 1: Open edit form

```
Given I am viewing a property's details
When I click the "Edit" button
Then the edit form should open
  And all fields should be pre-populated with the property's current data
  And the form title should indicate I'm editing (not creating)
```

### Scenario 2: Edit and save property

```
Given the edit form is open
  And all fields are pre-populated
When I change some information
  And I click "Save"
Then the property should be updated in the database
  And I should see a success message
  And I should return to the property details
  And the updated information should be displayed
```

### Scenario 3: Edit price reduction

```
Given I am editing a property
When I change the listing price to a lower amount
  And I save the changes
Then the new price should be saved
  And the change should be reflected everywhere
```

### Scenario 4: Edit with validation errors

```
Given the edit form is open
When I change a field to an invalid value
  And I click "Save"
Then I should see validation errors
  And the property should not be saved
  And the form should remain open
```

### Scenario 5: Cancel edit

```
Given the edit form is open
  And I have made changes
When I click "Cancel"
Then the form should close
  And no changes should be saved
  And I should return to the property details
  And the original data should still be there
```

### Scenario 6: Edit persists across restarts

```
Given I have edited and saved a property
When I close the application
  And I restart the application
  And I open the property
Then the updated information should be displayed
```

### Scenario 7: Edit from property list

```
Given I am viewing the property list
  And I have selected a property
When I right-click and select "Edit"
  Or I press Ctrl+E
Then the edit form should open
  And the form should be pre-populated
```

## Manual Testing Steps

### Test 1: Open edit form

1. Create a property with all fields filled
2. Open the property's details
3. Click "Edit"
4. Verify the edit form opens
5. Verify all fields are pre-populated with the correct data
6. Verify the form title says "Edit Property" (not "New Property")

### Test 2: Edit and save

1. Open a property's edit form
2. Change the price
3. Change the status from Active to Pending
4. Update the description
5. Click "Save"
6. Verify the success message
7. Verify you return to the details
8. Verify the changes are displayed

### Test 3: Test price reduction

1. Open a property with price $500,000
2. Edit and change price to $475,000
3. Save the changes
4. Verify the new price is saved
5. Check the property list
6. Verify the list shows the new price

### Test 4: Test validation

1. Open the edit form
2. Clear the address field
3. Enter a negative price
4. Click "Save"
5. Verify validation errors appear
6. Fix the errors
7. Verify you can now save

### Test 5: Test cancel

1. Open the edit form
2. Make several changes
3. Click "Cancel"
4. Verify the form closes
5. Verify no changes were saved
6. Check that the original data is still there

### Test 6: Test persistence

1. Edit a property
2. Save the changes
3. Close the application
4. Restart the application
5. Open the property
6. Verify the changes persisted

### Test 7: Test edit from list

1. Select a property in the list
2. Right-click and select "Edit"
3. Verify the edit form opens
4. Test keyboard shortcut (Ctrl+E)
5. Verify it also opens the edit form

### Test 8: Test on all platforms

1. Test edit on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Edit form opens from property details
- [ ] Form is pre-populated with current data
- [ ] All fields can be edited
- [ ] Validation works the same as create
- [ ] Save updates the property in the database
- [ ] Success message appears after save
- [ ] Cancel discards changes
- [ ] Changes persist across restarts
- [ ] Can be accessed from property list (right-click or shortcut)
- [ ] Keyboard shortcut works (Ctrl+E / Cmd+E)
- [ ] Works on Windows, macOS, and Linux
- [ ] Updated data appears in property list immediately