# US-040: Create a New Property Listing

## User Story

**As an** agent  
**I want to** create a new property listing  
**So that** I can track properties I'm selling or have listed

## Priority

**MVP:** Must Have

**Rationale:** Properties are core to real estate. Agents need to track their listings, their details, status, and associated information. Without property management, the CRM is incomplete for real estate use.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design property creation form
- 2 hours: Create form UI with property fields
- 1 hour: Implement form validation
- 1 hour: Create property model
- 2 hours: Implement repository for saving properties
- 1 hour: Wire up form to repository
- 1 hour: Add success/error feedback
- 1 hour: Test property creation
- 1 hour: Test validation
- 1 hour: Test data persistence

## Dependencies

**Depends on:** US-015 (Create the First Window), US-016 (Navigate Between Sections), US-014 (Create Encrypted Database)

**Blocks:** US-041 (View Property List), US-042 (View Property Details), US-043 (Edit Property), US-044 (Mark Property Status)

## Description

A user should be able to create a new property listing with all relevant information including address, property type, bedrooms, bathrooms, square footage, listing price, status, and description. The property creation form should be accessible from the Properties section.

When the user clicks "New Property", a form appears. After filling out the form and clicking "Save", the property is saved to the database and the user returns to the property list. Properties can be linked to contacts (sellers, buyers) and can have photos and documents attached (future feature).

## BDD Scenarios

### Scenario 1: Open new property form

```
Given I am in the Properties section
When I click "New Property" button
Then a new property form should open
  And the form should have fields for:
    - Property Type (Single Family/Condo/Townhouse/Land/Multi-Family/Commercial)
    - Address
    - City
    - State
    - ZIP Code
    - Bedrooms
    - Bathrooms
    - Square Feet
    - Lot Size
    - Year Built
    - Listing Price
    - Status (Active/Pending/Sold/Withdrawn)
    - Description
    - MLS Number (optional)
```

### Scenario 2: Create property with all fields

```
Given the new property form is open
When I fill in all fields with valid data
  And I click "Save"
Then the property should be saved to the database
  And I should see a success message
  And I should return to the Properties list
  And the new property should appear in the list
```

### Scenario 3: Create property with minimal fields

```
Given the new property form is open
When I fill in only required fields (address, type, price)
  And I click "Save"
Then the property should be saved
  And optional fields should be empty
```

### Scenario 4: Validate required fields

```
Given the new property form is open
When I leave the address field empty
  And I click "Save"
Then I should see an error message
  And the property should not be saved
```

### Scenario 5: Validate listing price

```
Given the new property form is open
When I enter a negative listing price
  Or I enter text in the price field
  And I click "Save"
Then I should see a validation error
  And the property should not be saved
```

### Scenario 6: Property appears in list immediately

```
Given I have just saved a new property
When I view the Properties list
Then the new property should be visible
  And it should show the address and key information
```

### Scenario 7: Link property to contact

```
Given I am creating a property
When I select a contact as the seller
  Or I search for and select a contact
Then the property should be linked to that contact
  And I should be able to see the link
```

## Manual Testing Steps

### Test 1: Open the new property form

1. Navigate to the Properties section
2. Click "New Property" button
3. Verify the form opens
4. Verify all expected fields are present
5. Verify the form is clean and empty

### Test 2: Create a complete property

1. Open the new property form
2. Fill in all fields with valid data
3. Click "Save"
4. Verify the success message
5. Verify you return to the Properties list
6. Verify the new property is visible
7. Click on the property to verify all data was saved

### Test 3: Test required field validation

1. Open the new property form
2. Leave the address field empty
3. Fill in other fields
4. Click "Save"
5. Verify the error message
6. Enter an address
7. Verify you can save

### Test 4: Test price validation

1. Open the new property form
2. Enter a negative price
3. Click "Save"
4. Verify the validation error
5. Enter text in the price field
6. Verify the validation error
7. Enter a valid price
8. Verify you can save

### Test 5: Test property persistence

1. Create a property with all fields
2. Save the property
3. Close the application
4. Restart the application
5. Navigate to Properties
6. Verify the property is still there
7. Verify all data persisted

### Test 6: Test contact linking

1. Create a contact first
2. Create a new property
3. Link it to the contact as the seller
4. Save the property
5. Open the property details
6. Verify the contact is linked
7. Open the contact
8. Verify the property is linked from their side

### Test 7: Test on all platforms

1. Test property creation on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] "New Property" button is accessible from Properties section
- [ ] Form opens with all property fields
- [ ] Required fields are clearly marked
- [ ] Form validation works for all fields
- [ ] Price validation prevents negative or non-numeric values
- [ ] Property saves successfully with valid data
- [ ] Success message appears after save
- [ ] New property appears in the list immediately
- [ ] Properties can be linked to contacts
- [ ] Property data persists across restarts
- [ ] Data is encrypted in the database
- [ ] Works on Windows, macOS, and Linux
- [ ] Form is intuitive and easy to use