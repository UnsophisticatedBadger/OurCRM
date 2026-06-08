# US-023: Edit a Contact

## User Story

**As an** agent  
**I want to** edit a contact's information  
**So that** I can keep their information up to date

## Priority

**MVP:** Must Have

**Rationale:** Contact information changes frequently. Users need to be able to update phone numbers, addresses, notes, and other details without deleting and recreating the contact.

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

**Depends on:** US-022 (View Contact Details), US-020 (Create a New Contact)

**Blocks:** None

## Description

Users should be able to edit any contact's information. The edit form should be similar to the create form but pre-populated with the contact's current data. After making changes and clicking "Save", the contact is updated in the database.

The edit can be accessed from the contact details view by clicking the "Edit" button. The form should validate the data the same way as the create form. Users should be able to cancel without saving changes.

## BDD Scenarios

### Scenario 1: Open edit form

```
Given I am viewing a contact's details
When I click the "Edit" button
Then the edit form should open
  And all fields should be pre-populated with the contact's current data
  And the form title should indicate I'm editing (not creating)
```

### Scenario 2: Edit and save contact

```
Given the edit form is open
  And all fields are pre-populated
When I change some information
  And I click "Save"
Then the contact should be updated in the database
  And I should see a success message
  And I should return to the contact details
  And the updated information should be displayed
```

### Scenario 3: Edit with validation errors

```
Given the edit form is open
When I change a field to an invalid value
  And I click "Save"
Then I should see validation errors
  And the contact should not be saved
  And the form should remain open
```

### Scenario 4: Cancel edit

```
Given the edit form is open
  And I have made changes
When I click "Cancel"
Then the form should close
  And no changes should be saved
  And I should return to the contact details
  And the original data should still be there
```

### Scenario 5: Edit persists across restarts

```
Given I have edited and saved a contact
When I close the application
  And I restart the application
  And I open the contact
Then the updated information should be displayed
```

### Scenario 6: Edit from contact list

```
Given I am viewing the contact list
  And I have selected a contact
When I right-click and select "Edit"
  Or I press Ctrl+E
Then the edit form should open
  And the form should be pre-populated
```

## Manual Testing Steps

### Test 1: Open edit form

1. Create a contact with all fields filled
2. Open the contact's details
3. Click "Edit"
4. Verify the edit form opens
5. Verify all fields are pre-populated with the correct data
6. Verify the form title says "Edit Contact" (not "New Contact")

### Test 2: Edit and save

1. Open a contact's edit form
2. Change the phone number
3. Change the address
4. Add a note
5. Click "Save"
6. Verify the success message
7. Verify you return to the details
8. Verify the changes are displayed

### Test 3: Test validation

1. Open the edit form
2. Clear the name field
3. Enter an invalid email
4. Click "Save"
5. Verify validation errors appear
6. Fix the errors
7. Verify you can now save

### Test 4: Test cancel

1. Open the edit form
2. Make several changes
3. Click "Cancel"
4. Verify the form closes
5. Verify no changes were saved
6. Check that the original data is still there

### Test 5: Test persistence

1. Edit a contact
2. Save the changes
3. Close the application
4. Restart the application
5. Open the contact
6. Verify the changes persisted

### Test 6: Test edit from list

1. Select a contact in the list
2. Right-click and select "Edit"
3. Verify the edit form opens
4. Test keyboard shortcut (Ctrl+E)
5. Verify it also opens the edit form

### Test 7: Test on all platforms

1. Test edit on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Edit form opens from contact details
- [ ] Form is pre-populated with current data
- [ ] All fields can be edited
- [ ] Validation works the same as create
- [ ] Save updates the contact in the database
- [ ] Success message appears after save
- [ ] Cancel discards changes
- [ ] Changes persist across restarts
- [ ] Can be accessed from contact list (right-click or shortcut)
- [ ] Keyboard shortcut works (Ctrl+E / Cmd+E)
- [ ] Works on Windows, macOS, and Linux
- [ ] Updated data appears in contact list immediately