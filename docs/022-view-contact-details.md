# US-022: View Contact Details

## User Story

**As an** agent  
**I want to** view detailed information about a specific contact  
**So that** I can see everything I know about that person

## Priority

**MVP:** Must Have

**Rationale:** Users need to see complete information about a contact, not just the summary shown in the list. The details view is where users spend time reviewing and managing individual contacts.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design details view layout
- 2 hours: Create details UI with all contact fields
- 1 hour: Add edit and delete buttons
- 1 hour: Show related information (notes, activities, transactions)
- 1 hour: Add navigation between contacts (previous/next)
- 1 hour: Implement back button to return to list
- 1 hour: Test with various contact data
- 1 hour: Test navigation flow
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-021 (View Contact List)

**Blocks:** US-023 (Edit Contact), US-024 (Delete Contact), US-025 (Add Notes to Contact)

## Description

When a user double-clicks a contact or clicks a "View" button, the contact details view should open. This view shows all information about the contact organized in a clear, readable layout. It should include the contact's basic information, notes, tags, and any related activities or transactions.

The details view should have buttons for common actions (Edit, Delete, Add Note) and should allow navigation between contacts (Previous/Next buttons). Users should be able to return to the contact list easily.

## BDD Scenarios

### Scenario 1: Open contact details

```
Given I am viewing the contact list
  And I have selected a contact
When I double-click the contact
  Or I click the "View Details" button
Then the contact details view should open
  And I should see all the contact's information
  And the data should match what I entered
```

### Scenario 2: Contact details layout

```
Given the contact details view is open
When I examine the layout
Then I should see:
  - Contact name (as a heading)
  - Email address
  - Phone number
  - Address
  - Tags
  - Notes
  - Edit button
  - Delete button
  - Add Note button
  - Previous/Next navigation buttons
  - Back to list button
```

### Scenario 3: Navigate to next contact

```
Given I am viewing a contact's details
  And there are other contacts in the list
When I click the "Next" button
Then the next contact's details should be displayed
  And the data should update accordingly
```

### Scenario 4: Navigate to previous contact

```
Given I am viewing a contact's details
  And there are other contacts in the list
When I click the "Previous" button
Then the previous contact's details should be displayed
  And the data should update accordingly
```

### Scenario 5: Return to contact list

```
Given I am viewing a contact's details
When I click the "Back to List" button
  Or I press the Escape key
Then I should return to the contact list
  And the contact I was viewing should still be selected
```

### Scenario 6: View contact with all fields filled

```
Given I have created a contact with all fields filled
When I open the contact's details
Then all fields should be displayed with the correct data
  And the layout should be clean and organized
  And no fields should be missing or cut off
```

### Scenario 7: View contact with minimal data

```
Given I have created a contact with only required fields
When I open the contact's details
Then the filled fields should be displayed
  And empty fields should be hidden or shown as "Not provided"
```

## Manual Testing Steps

### Test 1: Open contact details

1. Create a contact with all fields filled
2. Navigate to the Contacts section
3. Double-click the contact
4. Verify the details view opens
5. Verify all data is displayed correctly
6. Check that the layout is clean and readable

### Test 2: Test details layout

1. Open a contact's details
2. Verify all sections are present
3. Check that data is organized logically
4. Verify Edit, Delete, and Add Note buttons are visible
5. Verify Previous/Next buttons are present
6. Verify Back button is present

### Test 3: Test navigation between contacts

1. Create 3 contacts
2. Open the first contact's details
3. Click "Next"
4. Verify the second contact is displayed
5. Click "Next" again
6. Verify the third contact is displayed
7. Click "Previous"
8. Verify the second contact is displayed again

### Test 4: Test back to list

1. Open a contact's details
2. Click "Back to List"
3. Verify you return to the contact list
4. Verify the contact you were viewing is still selected
5. Test with Escape key
6. Verify it also returns to the list

### Test 5: Test with minimal data

1. Create a contact with only a name
2. Open the details
3. Verify the name is displayed
4. Verify empty fields are handled gracefully
5. Check that the layout doesn't break

### Test 6: Test with all data

1. Create a contact with all fields filled including long notes
2. Open the details
3. Verify all data is visible
4. Check that long notes wrap properly
5. Verify the layout is still clean

### Test 7: Test action buttons

1. Open a contact's details
2. Click "Edit"
3. Verify the edit form opens
4. Cancel and return to details
5. Click "Add Note"
6. Verify the note input appears
7. Click "Delete"
8. Verify the delete confirmation appears

### Test 8: Test on all platforms

1. Test details view on Windows
2. Verify it displays correctly
3. Test on macOS
4. Verify it displays correctly
5. Test on Linux
6. Verify it displays correctly
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Contact details open from the list
- [ ] All contact information is displayed
- [ ] Layout is clean and organized
- [ ] Edit, Delete, and Add Note buttons are present
- [ ] Previous/Next navigation works
- [ ] Back to list button works
- [ ] Escape key returns to list
- [ ] Empty fields are handled gracefully
- [ ] Long text wraps properly
- [ ] Contact remains selected when returning to list
- [ ] Works on Windows, macOS, and Linux
- [ ] Visual design is professional and readable