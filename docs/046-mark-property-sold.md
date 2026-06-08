# US-046: Mark Property as Sold

## User Story

**As an** agent  
**I want to** mark a property as sold and record the sale details  
**So that** I can track successful sales and calculate commission

## Priority

**MVP:** Must Have

**Rationale:** Marking a property as sold is a critical milestone. It represents a successful transaction and needs to track sale price, closing date, and other important details for commission calculation and business analysis.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design "Mark as Sold" dialog
- 1 hour: Implement sale details form (sale price, closing date, buyer)
- 1 hour: Link to buyer contact
- 1 hour: Calculate commission (optional)
- 1 hour: Update property status to Sold
- 1 hour: Add sale celebration message
- 1 hour: Test sold flow
- 1 hour: Test sale details persistence
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-044 (Mark Property Status), US-042 (View Property Details)

**Blocks:** None

## Description

Users should be able to mark a property as sold when a transaction closes. The system should prompt for sale details including sale price, closing date, buyer (linked to a contact), and optionally commission information. Once marked as sold, the property moves to the "Sold" status and the sale details are recorded.

This is a significant business event that should be celebrated and tracked. The sale information can be used for commission calculation, business reporting, and historical analysis.

## BDD Scenarios

### Scenario 1: Mark property as sold

```
Given I am viewing a property that has closed
When I click "Mark as Sold"
Then a sale details dialog should appear
  And I should enter:
    - Sale price
    - Closing date
    - Buyer (select from contacts or create new)
    - Commission percentage (optional)
    - Notes (optional)
```

### Scenario 2: Property moves to Sold status

```
Given I have entered sale details
When I confirm the sale
Then the property status should change to "Sold"
  And the sale details should be saved
  And the property should appear in the Sold filter
```

### Scenario 3: Link buyer to property

```
Given I am marking a property as sold
When I select a buyer from my contacts
Then the buyer should be linked to the property
  And the link should be visible in property details
```

### Scenario 4: Commission is calculated

```
Given I enter a sale price and commission percentage
When I save the sale
Then the commission amount should be calculated and displayed
  And it should be saved with the sale record
```

### Scenario 5: Sale celebration

```
Given I have just marked a property as sold
When the sale is saved
Then I should see a congratulatory message
  And the message should celebrate the successful sale
```

### Scenario 6: Sale details are editable

```
Given I have marked a property as sold
When I need to correct or update the sale details
Then I should be able to edit the sale information
  And the changes should be saved
```

### Scenario 7: Cannot accidentally unmark as sold

```
Given a property has been marked as sold
When I try to change its status
Then the system should warn that this is a sold property
  And ask for confirmation
```

### Scenario 8: Sale history is tracked

```
Given I have marked properties as sold over time
When I view my sales history
Then I should see all closed sales
  And their details (price, date, commission)
```

## Manual Testing Steps

### Test 1: Mark property as sold

1. Open a property's details
2. Click "Mark as Sold"
3. Verify the sale details dialog appears
4. Enter sale price
5. Enter closing date
6. Select or add a buyer
7. Optionally enter commission
8. Click "Save" or "Confirm"

### Test 2: Test status change

1. Mark a property as sold
2. Verify the status changes to "Sold"
3. View the property list
4. Verify it appears under "Sold" filter
5. Verify the visual indicator changed

### Test 3: Test buyer linking

1. Create a contact (buyer)
2. Mark a property as sold
3. Select the buyer from contacts
4. Save the sale
5. Open the property details
6. Verify the buyer is linked
7. Open the contact
8. Verify the property is linked from their side

### Test 4: Test commission calculation

1. Mark a property as sold
2. Enter sale price: $500,000
3. Enter commission: 3%
4. Save the sale
5. Verify the commission is calculated: $15,000
6. Verify it's displayed and saved

### Test 5: Test sale celebration

1. Mark a property as sold
2. Verify the congratulatory message appears
3. Verify it's encouraging and celebratory
4. Check that it doesn't feel spammy

### Test 6: Test editing sale details

1. Mark a property as sold
2. Open the sale details
3. Edit the sale price
4. Save the changes
5. Verify the updates are saved

### Test 7: Test accidental unmark protection

1. Mark a property as sold
2. Try to change its status
3. Verify a warning appears
4. Confirm the warning is clear

### Test 8: Test sale history

1. Mark several properties as sold over time
2. View the sales history
3. Verify all sales are shown
4. Verify sale details are accurate
5. Test sorting and filtering

### Test 9: Test on all platforms

1. Test mark as sold on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] "Mark as Sold" action is available for properties
- [ ] Sale details dialog appears with required fields
- [ ] Sale price can be entered
- [ ] Closing date can be selected
- [ ] Buyer can be linked from contacts
- [ ] Commission can be calculated and saved
- [ ] Property status changes to "Sold"
- [ ] Sale details are saved with the property
- [ ] Success message celebrates the sale
- [ ] Sale details can be edited later
- [ ] Cannot accidentally unmark without warning
- [ ] Sale history is tracked
- [ ] Works on Windows, macOS, and Linux
- [ ] Sale information is accurate and complete