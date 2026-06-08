# US-048: View Transaction List

## User Story

**As an** agent  
**I want to** view a list of all my transactions  
**So that** I can see all my active and closed deals

## Priority

**MVP:** Must Have

**Rationale:** Transactions represent the agent's active business. Seeing all transactions at a glance helps agents track what's in progress, what's closing soon, and what's been completed. This is critical for daily operations and business planning.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design list layout and columns
- 2 hours: Create list UI with transaction-specific columns
- 1 hour: Implement data loading
- 1 hour: Add sorting by columns
- 1 hour: Add status indicators
- 1 hour: Implement empty state
- 1 hour: Add filtering by status
- 1 hour: Test with various data volumes
- 1 hour: Test performance
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-047 (Create a New Transaction)

**Blocks:** US-049 (View Transaction Details), US-050 (Track Transaction Status), US-051 (Record Closing Date)

## Description

The Transactions section should display a list of all transactions in a table view. Each row represents one transaction and shows key information including property address, buyer/seller names, transaction type, status, contract date, and closing date. The status should be color-coded for quick visual identification.

The list should support sorting by columns, filtering by status, and should load quickly even with hundreds of transactions. When there are no transactions, an empty state should be displayed.

## BDD Scenarios

### Scenario 1: View transaction list with transactions

```
Given I have created several transactions
  And I am in the Transactions section
When the Transactions section loads
Then I should see a list of all my transactions
  And each transaction should display:
    - Property address
    - Buyer name
    - Seller name
    - Transaction type (Sale/Lease)
    - Status (color-coded)
    - Contract date
    - Closing date
    - Sale price
```

### Scenario 2: Status is color-coded

```
Given I am viewing the transaction list
  And I have transactions with different statuses
When I look at the status column
Then Under Contract should be shown in yellow
  And Pending should be shown in orange
  And Closed should be shown in green
  And Cancelled should be shown in gray
```

### Scenario 3: Empty state with no transactions

```
Given I have no transactions
  And I am in the Transactions section
When the Transactions section loads
Then I should see an empty state message
  And the message should say "No transactions yet"
  And there should be a button "Create Your First Transaction"
```

### Scenario 4: Sort by closing date

```
Given I am viewing the transaction list
When I click on the "Closing Date" column header
Then the transactions should be sorted by closing date
  And the earliest closing dates should appear first
```

### Scenario 5: Filter by status

```
Given I am viewing the transaction list
When I filter by "Under Contract Only"
Then only transactions with that status should be displayed
  And the filter should be clearly indicated
```

### Scenario 6: Sort by sale price

```
Given I am viewing the transaction list
When I click on the "Sale Price" column header
Then the transactions should be sorted by price
  And the most expensive should appear first
```

### Scenario 7: Highlight upcoming closings

```
Given I have transactions closing in the next 30 days
When I view the transaction list
Then those transactions should be highlighted
  And I should be able to see them at a glance
```

### Scenario 8: List loads quickly

```
Given I have 150 transactions
When I open the Transactions section
Then the list should load in under 2 seconds
  And scrolling should be smooth
```

## Manual Testing Steps

### Test 1: View list with transactions

1. Create 5-10 transactions with various data
2. Navigate to the Transactions section
3. Verify all transactions are displayed
4. Verify the columns show the expected information
5. Verify the data is accurate
6. Check the visual layout is clean and readable

### Test 2: Test status colors

1. Create transactions with all four statuses
2. Navigate to the Transactions section
3. Verify Under Contract is yellow
4. Verify Pending is orange
5. Verify Closed is green
6. Verify Cancelled is gray
7. Verify colors are clearly distinguishable

### Test 3: Test empty state

1. Delete all transactions (or start with a fresh database)
2. Navigate to the Transactions section
3. Verify the empty state message appears
4. Verify the "Create Your First Transaction" button is visible
5. Click the button
6. Verify it opens the new transaction form

### Test 4: Test sorting

1. Create transactions with various dates and prices
2. Click on each column header
3. Verify sorting works for each column
4. Click again to reverse order
5. Verify the sort indicator updates

### Test 5: Test status filtering

1. Create transactions with different statuses
2. Filter by "Under Contract Only"
3. Verify only matching transactions are shown
4. Clear the filter
5. Verify all transactions are shown again

### Test 6: Test upcoming closings highlight

1. Create transactions with various closing dates
2. Some in the next 30 days, some further out
3. View the transaction list
4. Verify upcoming closings are highlighted
5. Verify they're easy to identify

### Test 7: Test with large dataset

1. Create 150+ transactions
2. Open the Transactions section
3. Measure load time
4. Verify it's under 2 seconds
5. Test scrolling performance
6. Verify UI remains responsive

### Test 8: Test on all platforms

1. Test transaction list on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Transaction list displays all transactions
- [ ] Each transaction shows address, buyer, seller, type, status, dates, price
- [ ] Status is color-coded (Under Contract=yellow, Pending=orange, Closed=green, Cancelled=gray)
- [ ] Transactions are sorted by status or date by default
- [ ] Users can sort by clicking column headers
- [ ] Users can filter by status
- [ ] Upcoming closings are highlighted
- [ ] Empty state is shown when no transactions exist
- [ ] List loads in under 2 seconds with 150 transactions
- [ ] Scrolling is smooth with large lists
- [ ] UI remains responsive
- [ ] Works on Windows, macOS, and Linux
- [ ] Visual design is clean and professional
- [ ] Status colors are consistent and readable