# US-020: Create a New Contact

## User Story

**As an** agent  
**I want to** create a new contact  
**So that** I can track people I work with

## Priority

**MVP:** Must Have

**Rationale:** Contacts are the foundation of a CRM. Without the ability to create and store contacts, the application has no value. This is the first end-to-end user feature.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design contact creation form
- 2 hours: Create form UI with all fields
- 1 hour: Implement form validation
- 1 hour: Create contact model
- 2 hours: Implement repository for saving contacts
- 1 hour: Wire up form to repository
- 1 hour: Add success/error feedback
- 1 hour: Test contact creation
- 1 hour: Test validation
- 1 hour: Test data persistence

## Dependencies

**Depends on:** US-015 (Create the First Window), US-016 (Navigate Between Sections), US-014 (Create Encrypted Database)

**Blocks:** US-021 (View Contact List), US-022 (View Contact Details), US-023 (Edit Contact), US-024 (Delete Contact)

## Description

A user should be able to create a new contact with basic information including name, email, phone, address, and notes. The contact creation should be done through a form that's accessible from the Contacts section.

When the user clicks "New Contact" or similar button, a form appears. After filling out the form and clicking "Save", the contact is saved to the encrypted database and the user returns to the contact list where the new contact is visible. If there are validation errors, they should be clearly displayed.

## BDD Scenarios

### Scenario 1: Open new contact form

```
Given I am in the Contacts section
When I click "New Contact" button
Then a new contact form should open
  And the form should have fields for:
    - First Name
    - Last Name
    - Email
    - Phone
    - Address
    - City
    - State
    - ZIP Code
    - Notes
```

### Scenario 2: Create contact with all fields

```
Given the new contact form is open
When I fill in all fields with valid data
  And I click "Save"
Then the contact should be saved to the database
  And I should see a success message
  And I should return to the Contacts list
  And the new contact should appear in the list
```

### Scenario 3: Create contact with only required fields

```
Given the new contact form is open
When I fill in only the required fields (name)
  And I click "Save"
Then the contact should be saved
  And optional fields should be empty
  And the contact should appear in the list
```

### Scenario 4: Validate required fields

```
Given the new contact form is open
When I leave the name field empty
  And I click "Save"
Then I should see an error message
  And the error should say "Name is required"
  And the contact should not be saved
```

### Scenario 5: Validate email format

```
Given the new contact form is open
When I enter an invalid email format
  And I click "Save"
Then I should see an error message
  And the error should say "Please enter a valid email address"
```

### Scenario 6: Validate phone format

```
Given the new contact form is open
When I enter an invalid phone number
  And I click "Save"
Then I should see an error message
  And the error should indicate the phone format is invalid
```

### Scenario 7: Cancel contact creation

```
Given the new contact form is open
  And I have entered some data
When I click "Cancel"
Then the form should close
  And no data should be saved
  And I should return to the Contacts list
```

### Scenario 8: Contact appears in list immediately

```
Given I have just saved a new contact
When I view the Contacts list
Then the new contact should be visible at the top or in the appropriate position
  And the contact should show the name and basic information
```

## Manual Testing Steps

### Test 1: Open the new contact form

1. Navigate to the Contacts section
2. Click "New Contact" button
3. Verify the form opens
4. Verify all expected fields are present
5. Verify the form is clean and empty

### Test 2: Create a complete contact

1. Open the new contact form
2. Fill in all fields with valid data
3. Click "Save"
4. Verify the success message appears
5. Verify you return to the Contacts list
6. Verify the new contact is visible in the list
7. Click on the contact to verify all data was saved

### Test 3: Test required field validation

1. Open the new contact form
2. Leave the name field empty
3. Fill in other fields
4. Click "Save"
5. Verify the error message appears
6. Verify the form does not close
7. Enter a name
8. Verify you can now save

### Test 4: Test email validation

1. Open the new contact form
2. Enter an invalid email (e.g., "notanemail")
3. Click "Save"
4. Verify the email validation error appears
5. Enter a valid email
6. Verify the error disappears
7. Save the contact

### Test 5: Test phone validation

1. Open the new contact form
2. Enter an invalid phone number
3. Click "Save"
4. Verify the phone validation error appears
5. Enter a valid phone number
6. Verify the error disappears

### Test 6: Test cancel functionality

1. Open the new contact form
2. Fill in some fields
3. Click "Cancel"
4. Verify the form closes
5. Verify no contact was created
6. Check the Contacts list

### Test 7: Test data persistence

1. Create a contact with all fields filled
2. Save the contact
3. Close the application
4. Restart the application
5. Navigate to Contacts
6. Verify the contact is still there
7. Click on it to verify all data persisted

### Test 8: Test on all platforms

1. Test contact creation on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] "New Contact" button is accessible from Contacts section
- [ ] Form opens with all expected fields
- [ ] Required fields are clearly marked
- [ ] Form validation works for all fields
- [ ] Email format is validated
- [ ] Phone format is validated
- [ ] Contact saves successfully with valid data
- [ ] Success message appears after save
- [ ] New contact appears in the list immediately
- [ ] Cancel button discards changes
- [ ] Contact data persists across restarts
- [ ] Data is encrypted in the database
- [ ] Works on Windows, macOS, and Linux
- [ ] Form is intuitive and easy to use