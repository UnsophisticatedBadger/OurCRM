# US-163: Commission Report

## User Story

**As an** agent  
**I want to** see a report of my commission earnings  
**So that** I can track my income and plan my finances

## Priority

**Future:** Post-MVP

**Rationale:** Commission tracking is essential for business planning. Agents need to know their earnings by period, source, and property type for tax planning and goal setting.

## Estimated Effort

**Size:** Medium (M) - 3-5 days

**Breakdown:**
- 2 hours: Design commission report UI
- 3 hours: Implement commission calculations
- 2 hours: Add date range filtering
- 2 hours: Add visualizations
- 2 hours: Test report accuracy
- 2 hours: Test on all platforms

## Dependencies

**Depends on:** US-046 (Mark Property as Sold), US-047 (Create a New Transaction)

**Blocks:** None

## Description

The commission report should show:
- Total commission earned in period
- Commission by property type
- Commission by source
- Average commission per transaction
- Commission trends over time

Data should be filterable and exportable.

## BDD Scenarios

### Scenario 1: View commission report

Given I have closed transactions When I open the commission report Then I should see total commission earned


### Scenario 2: Filter by date range

Given I am viewing the report When I select a date range Then only commissions in that range should be counted


### Scenario 3: Commission by property type

Given I have sold various property types When I view the report Then I should see commission by type


### Scenario 4: Commission by source

Given I have leads from various sources When I view the report Then I should see commission by source


### Scenario 5: Average commission

Given I have multiple transactions When I view the report Then I should see average commission per transaction


### Scenario 6: Commission trends

Given I have historical data When I view the report Then I should see commission trends over time


### Scenario 7: Export report

Given I am viewing the report When I click "Export" Then I can export to PDF or CSV


### Scenario 8: Pending vs earned commission

Given I have pending and closed transactions When I view the report Then I should see both pending and earned


## Manual Testing Steps

### Test 1: View commission report

1. Open report
2. Verify total shown
3. Verify accuracy

### Test 2: Test date filter

1. Set date range
2. Verify totals adjust

### Test 3: Test by property type

1. View type breakdown
2. Verify accurate

### Test 4: Test by source

1. View source breakdown
2. Verify accurate

### Test 5: Test average

1. View average commission
2. Verify calculation

### Test 6: Test trends

1. View trend chart
2. Verify accurate

### Test 7: Test export

1. Export report
2. Verify file created

### Test 8: Test on all platforms

1. Test Windows, macOS, Linux
2. Verify all work

## Acceptance Criteria

- [ ] Commission report accessible
- [ ] Total commission shown
- [ ] Filter by date range
- [ ] Commission by property type
- [ ] Commission by source
- [ ] Average commission calculated
- [ ] Commission trends shown
- [ ] Pending vs earned distinguished
- [ ] Can export report
- [ ] Visual charts included
- [ ] Works on Windows, macOS, and Linux