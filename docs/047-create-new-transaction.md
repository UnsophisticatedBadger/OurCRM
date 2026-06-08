# US-047: Create a New Transaction

## User Story

**As an** agent  
**I want to** create a new transaction  
**So that** I can track a deal from contract to closing

## Priority

**MVP:** Must Have

**Rationale:** Transactions represent active deals in progress. Agents need to track all the details of a transaction including parties involved, dates, amounts, and status. This is the operational core of an agent's business.

## Estimated Effort

**Size:** Medium (M) - 3 days

**Breakdown:**
- 1 hour: Design transaction creation form
- 2 hours: Create form UI with transaction fields
- 1 hour: Implement form validation
- 1 hour: Create transaction model
- 2 hours: Implement repository for saving transactions
- 1 hour: Link to property and contacts
- 1 hour: Wire up form to repository
- 1 hour: Add success/error feedback
- 1 hour: Test transaction creation
- 1 hour: Test validation
- 1 hour: Test data persistence

## Dependencies

**Depends on:** US-015 (Create the First Window), US-016 (Navigate Between Sections), US-014 (Create Encrypted Database)

**Blocks:** US-048 (View Transaction List), US-049 (View Transaction Details), US-050 (Track Transaction Status), US-051 (Record Closing Date)

## Description

A user should be able to create a new transaction to track a real estate deal. Transactions include the property involved, all parties (buyer, seller, agent), transaction type (sale, lease), contract date, closing date, sale price, and commission details.

The transaction creation form should allow linking to existing properties and contacts, or creating new ones if needed. After saving, the transaction appears in the Transactions section and can be tracked through to closing.

## BDD Scenarios

### Scenario 1: Open new transaction form

```
Given I am in the Transactions section
When I click "New Transaction" button
Then a new transaction form should open
  And the form should have fields for:
    - Transaction Type (Sale/Lease)
    - Property (link to existing or create new)
    - Buyer (link to contact)
    - Seller (link to contact)
    - Contract Date
    - Closing Date
    - Sale Price
    - Commission Percentage
    - Status (Under Contract/Pending/Closed/Cancelled)
    - Notes
```

### Scenario 2: Create transaction with all fields

```
Given the new transaction form is open
When I fill in all fields with valid data
  And I link to existing property and contacts
  And I click "Save"
Then the transaction should be saved
  And all relationships should be established
  And I should see a success message
  And the transaction should appear in the list
```

### Scenario 3: Link to existing property

```
Given I am creating a transaction
When I search for and select an existing property
Then the property should be linked to the transaction
  And the property details should be auto-populated (address, etc.)
```

### Scenario 4: Link buyer and seller

```
Given I am creating a transaction
When I select a buyer from my contacts
  And I select a seller from my contacts
Then both should be linked to the transaction
  And their information should be associated
```

### Scenario 5: Create new contact during transaction

```
Given I am creating a transaction
  And the buyer or seller doesn't exist as a contact
When I click "Create New Contact"
Then I can create the contact without leaving the transaction form
  And the new contact should be linked to the transaction
```

### Scenario 6: Validate required fields

```
Given the new transaction form is open
When I leave required fields empty
  And I click "Save"
Then I should see validation errors
  And the transaction should not be saved
```

### Scenario 7: Validate dates

```
Given I am creating a transaction
When I enter a closing date before the contract date
  And I click "Save"
Then I should see a validation error
  And the error should say "Closing date must be after contract date"
```

### Scenario 8: Calculate commission

```
Given I enter a sale price and commission percentage
When I save the transaction
Then the commission amount should be calculated
  And displayed (e.g., "$500,000 × 3% = $15,000")
```

## Manual Testing Steps

### Test 1: Open the new transaction form

1. Navigate to the Transactions section
2. Click "New Transaction" button
3. Verify the form opens
4. Verify all expected fields are present
5. Verify the form is clean and empty

### Test 2: Create a complete transaction

1. Create a property first
2. Create buyer and seller contacts
3. Open the new transaction form
4. Fill in all fields
5. Link to the property
6. Link to the buyer and seller
7. Click "Save"
8. Verify the success message
9. Verify the transaction appears in the list

### Test 3: Test property linking

1. Open a new transaction form
2. Search for an existing property
3. Select it
4. Verify the property is linked
5. Verify the property details are auto-populated

### Test 4: Test contact linking

1. Open a new transaction form
2. Select a buyer from contacts
3. Select a seller from contacts
4. Verify both are linked
5. Save the transaction
6. Verify the links persist

### Test 5: Test creating new contact

1. Open a new transaction form
2. Click "Create New Contact" for buyer
3. Fill in the contact details
4. Save the contact
5. Verify it auto-links to the transaction
6. Save the transaction
7. Verify everything is connected

### Test 6: Test validation

1. Open a new transaction form
2. Leave required fields empty
3. Click "Save"
4. Verify validation errors
5. Enter closing date before contract date
6. Verify the date validation error

### Test 7: Test commission calculation

1. Create a transaction
2. Enter sale price: $500,000
3. Enter commission: 3%
4. Save the transaction
5. Verify commission is calculated: $15,000
6. Verify it's displayed correctly

### Test 8: Test transaction persistence

1. Create a transaction with all fields
2. Save the transaction
3. Close the application
4. Restart the application
5. Navigate to Transactions
6. Verify the transaction is still there
7. Verify all links and data persisted

### Test 9: Test on all platforms

1. Test transaction creation on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] "New Transaction" button is accessible from Transactions section
- [ ] Form opens with all transaction fields
- [ ] Can link to existing property
- [ ] Can link to existing contacts (buyer/seller)
- [ ] Can create new contacts during transaction creation
- [ ] Required fields are validated
- [ ] Date validation prevents illogical dates
- [ ] Commission is calculated and displayed
- [ ] Transaction saves successfully with valid data
- [ ] Success message appears after save
- [ ] Transaction appears in the list immediately
- [ ] All relationships are established
- [ ] Data persists across restarts
- [ ] Data is encrypted in the database
- [ ] Works on Windows, macOS, and Linux
- [ ] Form is intuitive and easy to use