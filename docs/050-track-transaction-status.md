# US-050: Track Transaction Status

## User Story

**As an** agent  
**I want to** change a transaction's status (Under Contract, Pending, Closed, Cancelled)  
**So that** I can track where each transaction is in the closing process

## Priority

**MVP:** Must Have

**Rationale:** Transaction status is critical for tracking deals in progress. Transactions move through statuses from Under Contract to Pending to Closed (or Cancelled). Without status tracking, agents can't manage their pipeline effectively or know which deals need attention.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design status selection UI
- 1 hour: Implement status change in transaction details
- 1 hour: Add visual indicators for current status
- 1 hour: Implement quick status change from list
- 1 hour: Add status change history
- 1 hour: Test status changes
- 1 hour: Test that status updates reflect in list
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-047 (Create a New Transaction), US-048 (View Transaction List)

**Blocks:** US-051 (Record Closing Date), US-053 (Cancel Transaction)

## Description

Users should be able to change a transaction's status at any time. The status options are Under Contract (initial state after contract signing), Pending (moving toward closing), Closed (transaction complete), and Cancelled (deal fell through). The status should be clearly visible in the transaction list and details, and should be color-coded for quick identification.

Changing a status should be quick and easy, with the option to change it from either the transaction details or directly from the transaction list. The system should track when the status was last changed.

## BDD Scenarios

### Scenario 1: Set status when creating transaction

```
Given I am creating a new transaction
When I select a status from the status dropdown
  And I save the transaction
Then the transaction should be saved with the selected status
```

### Scenario 2: Change status from transaction details

```
Given I am viewing a transaction's details
  And the current status is "Under Contract"
When I click on the status field
  And I select "Pending"
  And I save the change
Then the transaction's status should be updated to "Pending"
  And the visual indicator should change
```

### Scenario 3: Change status from transaction list

```
Given I am viewing the transaction list
  And I have selected a transaction
When I right-click and select "Change Status"
  Or I use a quick action button
Then I should be able to change the status
  And the change should be reflected immediately in the list
```

### Scenario 4: Status is color-coded

```
Given I am viewing transactions with different statuses
When I look at the status indicators
Then Under Contract should be shown in yellow
  And Pending should be shown in orange
  And Closed should be shown in green
  And Cancelled should be shown in gray
```

### Scenario 5: Status persists across restarts

```
Given I have changed a transaction's status
When I close the application
  And I restart the application
  And I open the transaction
Then the status should be the updated value
```

### Scenario 6: Status change is logged

```
Given I have changed a transaction's status multiple times
When I view the transaction's history (if implemented)
Then I should see when the status was changed
  And what it was changed from and to
```

### Scenario 7: Mark as Closed requires confirmation

```
Given I am changing a transaction's status to "Closed"
When I select "Closed"
Then a confirmation dialog should appear
  And I should be asked to confirm the transaction has closed
  And optionally enter the actual closing date
```

### Scenario 8: Cancelled status is distinct

```
Given a transaction is marked as Cancelled
When I view it in the list
Then it should be visually distinct from active transactions
  And it should be clear the deal fell through
```

## Manual Testing Steps

### Test 1: Set status when creating

1. Create a new transaction
2. Select "Under Contract" from the status dropdown
3. Save the transaction
4. Verify the status is saved
5. Open the transaction details
6. Verify the status is "Under Contract"

### Test 2: Change status from details

1. Open a transaction's details
2. Current status is "Under Contract"
3. Click on the status field
4. Select "Pending"
5. Save the change
6. Verify the status updated
7. Verify the visual indicator changed

### Test 3: Change status from list

1. View the transaction list
2. Right-click on a transaction
3. Select "Change Status"
4. Choose "Closed"
5. Verify the status changed
6. Verify it reflected in the list immediately

### Test 4: Test color coding

1. Create transactions with all four statuses
2. View the transaction list
3. Verify Under Contract is yellow
4. Verify Pending is orange
5. Verify Closed is green
6. Verify Cancelled is gray
7. Verify colors are clearly distinguishable

### Test 5: Test status persistence

1. Change a transaction's status to "Pending"
2. Close the application
3. Restart the application
4. Open the transaction
5. Verify the status is still "Pending"

### Test 6: Test Closed confirmation

1. Open a transaction
2. Change status to "Closed"
3. Verify a confirmation dialog appears
4. Enter the actual closing date (if prompted)
5. Confirm
6. Verify the transaction is now marked as Closed

### Test 7: Test Cancelled distinction

1. Mark a transaction as Cancelled
2. View the transaction list
3. Verify it's visually distinct
4. Verify it's clear the deal is no longer active

### Test 8: Test on all platforms

1. Test status changes on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Status can be set when creating a transaction
- [ ] Status can be changed from transaction details
- [ ] Status can be changed from transaction list
- [ ] Status is color-coded (Under Contract=yellow, Pending=orange, Closed=green, Cancelled=gray)
- [ ] Status changes are saved immediately
- [ ] Status persists across restarts
- [ ] Visual indicators are clear and consistent
- [ ] Marking as Closed requires confirmation
- [ ] Cancelled transactions are visually distinct
- [ ] All four statuses are available
- [ ] Works on Windows, macOS, and Linux
- [ ] Status is clearly visible in list and details
- [ ] No accidental status changes