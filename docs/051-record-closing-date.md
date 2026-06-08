# US-051: Record Closing Date

## User Story

**As an** agent  
**I want to** record the actual closing date for a transaction  
**So that** I can track when deals actually close and calculate commission timing

## Priority

**MVP:** Must Have

**Rationale:** The closing date is a critical milestone in a real estate transaction. It represents when the deal actually closes, when commission is earned, and when the transaction is complete. Recording the actual closing date (which may differ from the estimated date) is essential for accurate business tracking.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design closing date recording UI
- 1 hour: Implement closing date field in transaction
- 1 hour: Add validation (must be after contract date)
- 1 hour: Calculate days to closing
- 1 hour: Update transaction status to Closed
- 1 hour: Calculate commission earned
- 1 hour: Test closing date recording
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-050 (Track Transaction Status), US-049 (View Transaction Details)

**Blocks:** US-052 (Mark Transaction as Closed), US-054 (View Closed Transactions)

## Description

Users should be able to record the actual closing date for a transaction. This may differ from the estimated closing date originally entered. When the closing date is recorded, the transaction is marked as Closed, and commission is calculated as earned.

The closing date should be validated to ensure it's after the contract date. The system should calculate how many days the transaction took from contract to closing, which is useful for business analysis and forecasting.

## BDD Scenarios

### Scenario 1: Record closing date

```
Given I am viewing a transaction's details
  And the transaction is "Under Contract" or "Pending"
When I click "Record Closing Date"
Then a date picker should appear
  And I can select the actual closing date
```

### Scenario 2: Closing date must be after contract date

```
Given I am recording a closing date
When I try to select a date before the contract date
Then I should see a validation error
  And the error should say "Closing date must be after contract date"
```

### Scenario 3: Transaction marked as Closed

```
Given I have recorded a closing date
When I save the closing date
Then the transaction status should change to "Closed"
  And the closing date should be saved
  And the transaction should be marked as complete
```

### Scenario 4: Commission is calculated

```
Given I have recorded a closing date
  And the transaction has a sale price and commission percentage
When the transaction is marked as Closed
Then the commission should be calculated as earned
  And the amount should be displayed
```

### Scenario 5: Days to closing are calculated

```
Given a transaction has a contract date and closing date
When I view the transaction details
Then I should see "Days from contract to closing: X"
  And it should be calculated automatically
```

### Scenario 6: Closing date is required for Closed status

```
Given I am trying to mark a transaction as Closed
When I don't provide a closing date
Then the system should prompt for the closing date
  And prevent closing without it
```

### Scenario 7: Closing date persists across restarts

```
Given I have recorded a closing date
When I close the application
  And I restart the application
  And I open the transaction
Then the closing date should be saved
  And the status should still be Closed
```

### Scenario 8: Upcoming closing reminders

```
Given I have transactions with closing dates in the next 7 days
When I view the transaction list
Then those transactions should be highlighted
  And I should see a reminder
```

## Manual Testing Steps

### Test 1: Record closing date

1. Open a transaction's details
2. Click "Record Closing Date"
3. Verify the date picker appears
4. Select today's date (or a future date)
5. Save the closing date
6. Verify the status changes to "Closed"
7. Verify the closing date is saved

### Test 2: Test date validation

1. Open a transaction
2. Click "Record Closing Date"
3. Try to select a date before the contract date
4. Verify the validation error
5. Select a valid date
6. Verify you can save

### Test 3: Test automatic status change

1. Open a transaction in "Under Contract" status
2. Record the closing date
3. Verify the status automatically changes to "Closed"
4. Verify the change is reflected in the list

### Test 4: Test commission calculation

1. Create a transaction with $500,000 sale price and 3% commission
2. Record the closing date
3. Verify the commission is calculated: $15,000
4. Verify it's marked as earned

### Test 5: Test days to closing

1. Create a transaction with contract date 2024-01-01
2. Record closing date 2024-02-01
3. Verify it shows "31 days from contract to closing"
4. Check the calculation is correct

### Test 6: Test closing date requirement

1. Try to mark a transaction as Closed without a closing date
2. Verify the system prompts for the closing date
3. Verify you cannot close without it

### Test 7: Test persistence

1. Record a closing date
2. Close the application
3. Restart the application
4. Open the transaction
5. Verify the closing date and Closed status persisted

### Test 8: Test on all platforms

1. Test closing date on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] "Record Closing Date" action is available for transactions
- [ ] Date picker allows selecting the closing date
- [ ] Closing date must be after contract date
- [ ] Transaction status changes to Closed when closing date is recorded
- [ ] Commission is calculated as earned
- [ ] Days from contract to closing are calculated
- [ ] Closing date is required for Closed status
- [ ] Closing date persists across restarts
- [ ] Upcoming closings are highlighted
- [ ] Works on Windows, macOS, and Linux
- [ ] Date validation prevents invalid dates
- [ ] Closing date is accurate and reliable