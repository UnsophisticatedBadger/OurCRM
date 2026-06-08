# US-021: View Contact List

## User Story

**As an** agent  
**I want to** view a list of all my contacts  
**So that** I can see everyone I work with at a glance

## Priority

**MVP:** Must Have

**Rationale:** After creating contacts, users need to see them. The contact list is the primary way users interact with their contact database and find specific people.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design list layout and columns
- 2 hours: Create list UI with table or grid view
- 1 hour: Implement data loading from database
- 1 hour: Add sorting by columns
- 1 hour: Add row selection
- 1 hour: Add double-click to open contact
- 1 hour: Implement empty state (no contacts yet)
- 2 hours: Test with various data volumes
- 1 hour: Test performance with large lists

## Dependencies

**Depends on:** US-020 (Create a New Contact)

**Blocks:** US-022 (View Contact Details), US-023 (Edit Contact), US-024 (Delete Contact)

## Description

The Contacts section should display a list of all contacts in a table or grid view. Each row represents one contact and shows key information like name, email, phone, and tags. Users should be able to sort by columns, select contacts, and double-click to view details.

The list should load quickly even with hundreds of contacts. When there are no contacts, an empty state should be displayed with a helpful message and a button to create the first contact.

## BDD Scenarios

### Scenario 1: View contact list with contacts

```
Given I have created several contacts
  And I am in the Contacts section
When the Contacts section loads
Then I should see a list of all my contacts
  And each contact should display:
    - Name (first and last)
    - Email
    - Phone
    - Tags (if any)
  And the contacts should be sorted by name by default
```

### Scenario 2: Empty state with no contacts

```
Given I have no contacts
  And I am in the Contacts section
When the Contacts section loads
Then I should see an empty state message
  And the message should say "No contacts yet"
  And there should be a button "Create Your First Contact"
```

### Scenario 3: Sort by column

```
Given I am viewing the contact list
  And I have multiple contacts
When I click on the "Name" column header
Then the contacts should be sorted by name alphabetically
  And the column header should show a sort indicator
```

### Scenario 4: Reverse sort order

```
Given the contacts are sorted by name ascending
When I click the "Name" column header again
Then the contacts should be sorted by name descending
  And the sort indicator should update
```

### Scenario 5: Select a contact

```
Given I am viewing the contact list
When I click on a contact row
Then the contact should be selected (highlighted)
  And I should be able to perform actions on it
```

### Scenario 6: Open contact details

```
Given I am viewing the contact list
When I double-click on a contact
Then the contact details should open
  And I should be able to view all information about the contact
```

### Scenario 7: List loads quickly

```
Given I have 500 contacts
When I open the Contacts section
Then the list should load in under 2 seconds
  And scrolling should be smooth
  And the UI should remain responsive
```

## Manual Testing Steps

### Test 1: View list with contacts

1. Create 5-10 contacts with various data
2. Navigate to the Contacts section
3. Verify all contacts are displayed
4. Verify the columns show the expected information
5. Verify the data is accurate
6. Check the visual layout is clean and readable

### Test 2: Test empty state

1. Delete all contacts (or start with a fresh database)
2. Navigate to the Contacts section
3. Verify the empty state message appears
4. Verify the "Create Your First Contact" button is visible
5. Click the button
6. Verify it opens the new contact form

### Test 3: Test sorting

1. Create contacts with various names (e.g., Smith, Johnson, Williams)
2. Navigate to the Contacts section
3. Click the "Name" column header
4. Verify contacts are sorted alphabetically
5. Click again
6. Verify reverse order
7. Test sorting by other columns (email, phone)

### Test 4: Test selection

1. Click on a contact row
2. Verify it's highlighted
3. Click on another contact
4. Verify only the new one is selected
5. Test keyboard navigation (arrow keys)
6. Verify selection works with keyboard

### Test 5: Test double-click to open

1. Double-click on a contact
2. Verify the contact details open
3. Close the details
4. Verify you return to the list
5. Verify the contact is still selected

### Test 6: Test with large dataset

1. Create 500+ contacts (use a script or import)
2. Open the Contacts section
3. Measure how long it takes to load
4. Verify it's under 2 seconds
5. Test scrolling performance
6. Verify the UI remains responsive
7. Document any performance issues

### Test 7: Test with small dataset

1. Create 1-2 contacts
2. Open the Contacts section
3. Verify it displays correctly
4. Verify it's not awkward with just 1-2 items
5. Test with 0 contacts (empty state)

### Test 8: Test on all platforms

1. Test contact list on Windows
2. Verify it displays correctly
3. Test on macOS
4. Verify it displays correctly
5. Test on Linux
6. Verify it displays correctly
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Contact list displays all contacts
- [ ] Each contact shows name, email, phone, and tags
- [ ] Contacts are sorted by name by default
- [ ] Users can sort by clicking column headers
- [ ] Users can reverse sort order
- [ ] Users can select contacts
- [ ] Double-click opens contact details
- [ ] Empty state is shown when no contacts exist
- [ ] List loads in under 2 seconds with 500 contacts
- [ ] Scrolling is smooth with large lists
- [ ] UI remains responsive with large lists
- [ ] Works on Windows, macOS, and Linux
- [ ] Visual design is clean and professional