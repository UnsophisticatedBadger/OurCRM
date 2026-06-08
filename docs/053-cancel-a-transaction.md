# US-053: Cancel a Transaction

## User Story

**As an** agent  
**I want to** cancel a transaction  
**So that** I can mark deals that fell through and track the reason

## Priority

**MVP:** Must Have

**Rationale:** Not all transactions close successfully. Deals fall through for many reasons: financing issues, inspection problems, appraisal gaps, buyer remorse, etc. Tracking cancelled transactions and the reasons helps agents learn from failures and maintain accurate business metrics.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design cancellation UI
- 1 hour: Implement cancellation reason selection
- 1 hour: Add optional notes field for details
- 1 hour: Update transaction status to Cancelled
- 1 hour: Track cancellation date and reason
- 1 hour: Add confirmation dialog
- 1 hour: Test cancellation flow
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-050 (Track Transaction Status), US-049 (View Transaction Details)

**Blocks:** None

## Description

Users should be able to cancel a transaction when a deal falls through. The cancellation should require confirmation and should capture the reason for cancellation (financing, inspection, appraisal, buyer remorse, seller issue, other). Optional notes can be added for additional context.

When a transaction is cancelled:
- Status changes to "Cancelled"
- Cancellation date is recorded
- Reason is saved
- The transaction is preserved for historical analysis
- Commission is not earned

## BDD Scenarios

### Scenario 1: Cancel a transaction

```
Given I am viewing a transaction's details
  And the transaction is "Under Contract" or "Pending"
When I click "Cancel Transaction"
Then a cancellation dialog should appear
  And I should select a reason for cancellation
  And I can add optional notes
```

### Scenario 2: Transaction status changes to Cancelled

```
Given I have confirmed a cancellation with a reason
When the cancellation is saved
Then the transaction status should change to "Cancelled"
  And the cancellation date should be recorded
  And the reason should be saved
```

### Scenario 3: Cancellation requires confirmation

```
Given I am cancelling a transaction
When I select "Cancel Transaction"
Then a confirmation dialog should appear
  And I must confirm before the cancellation is processed
  And the dialog should warn that this action cannot be undone
```

### Scenario 4: Cancellation reason is required

```
Given I am cancelling a transaction
When I try to save without selecting a reason
Then I should see a validation error
  And the cancellation should not be processed
```

### Scenario 5: Cancellation is logged

```
Given I have cancelled a transaction
When I view the transaction's history
Then I should see:
  - Cancellation date
  - Reason
  - Optional notes
  - Who cancelled it
```

### Scenario 6: Cancelled transactions are filtered

```
Given I have cancelled transactions
When I filter by "Cancelled Only"
Then only cancelled transactions should be displayed
  And they should be visually distinct from active transactions
```

### Scenario 7: Cannot cancel a Closed transaction

```
Given a transaction is already "Closed"
When I try to cancel it
Then the system should prevent the cancellation
  And explain that closed transactions cannot be cancelled
```

### Scenario 8: Cancellation analytics (optional)

```
Given I have cancelled multiple transactions
When I view cancellation analytics
Then I should see:
  - Cancellation rate
  - Most common reasons
  - Trends over time
```

## Manual Testing Steps

### Test 1: Cancel a transaction

1. Open a transaction's details
2. Click "Cancel Transaction"
3. Verify the cancellation dialog appears
4. Select a reason (e.g., "Financing")
5. Add optional notes
6. Confirm the cancellation
7. Verify the status changes to "Cancelled"
8. Verify the cancellation date and reason are saved

### Test 2: Test confirmation

1. Open a transaction
2. Click "Cancel Transaction"
3. Verify a confirmation dialog appears
4. Verify the warning about the action
5. Test canceling the cancellation
6. Verify the transaction is not cancelled

### Test 3: Test reason validation

1. Open a transaction
2. Click "Cancel Transaction"
3. Try to save without selecting a reason
4. Verify the validation error
5. Select a reason
6. Verify you can now save

### Test 4: Test cancellation history

1. Cancel a transaction
2. Open the transaction's history
3. Verify the cancellation is logged
4. Verify the date, reason, and notes are shown

### Test 5: Test cancelled filter

1. Create transactions in various statuses
2. Cancel a few of them
3. Filter by "Cancelled Only"
4. Verify only cancelled transactions are shown
5. Verify they're visually distinct

### Test 6: Test cancel closed transaction

1. Try to cancel a transaction that's already Closed
2. Verify the system prevents it
3. Verify the explanation is clear

### Test 7: Test on all platforms

1. Test cancellation on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] "Cancel Transaction" action is available for active transactions
- [ ] Cancellation dialog appears with reason selection
- [ ] Cancellation reason is required
- [ ] Optional notes can be added
- [ ] Confirmation dialog prevents accidental cancellation
- [ ] Transaction status changes to "Cancelled"
- [ ] Cancellation date is recorded
- [ ] Reason is saved with the transaction
- [ ] Cancellation is logged in history
- [ ] Cancelled transactions are visually distinct
- [ ] Cannot cancel a Closed transaction
- [ ] Works on Windows, macOS, and Linux
- [ ] Cancellation tracking is accurate