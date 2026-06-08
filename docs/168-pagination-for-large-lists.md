# US-168: Pagination for Large Lists

## User Story

**As a** user  
**I want to** see large lists in pages  
**So that** the application remains responsive with thousands of records

## Priority

**Future:** Post-MVP

**Rationale:** Loading thousands of records at once slows the UI. Pagination loads data in chunks, keeping the interface responsive regardless of total data volume.

## Estimated Effort

**Size:** Medium (M) - 3-5 days

**Breakdown:**
- 2 hours: Design pagination UI
- 3 hours: Implement pagination logic
- 3 hours: Add database LIMIT/OFFSET
- 2 hours: Test with large datasets
- 2 hours: Test on all platforms

## Dependencies

**Depends on:** US-021 (View Contact List), US-031 (View Lead List)

**Blocks:** None

## Description

Lists should be paginated:
- Default 50 or 100 records per page
- Navigate between pages
- Show total count
- Jump to specific page
- Maintain filters/sorts across pages

## BDD Scenarios

### Scenario 1: Lists are paginated

Given I have 500 contacts When I view the contact list Then I should see 50 or 100 per page With navigation controls


### Scenario 2: Navigate between pages

Given I am viewing page 1 When I click "Next" Then page 2 should be displayed


### Scenario 3: Jump to specific page

Given I have many pages When I enter page number 10 Then page 10 should be displayed


### Scenario 4: Total count shown

Given I am viewing a paginated list When I look at the controls Then I should see "Showing 1-50 of 500"


### Scenario 5: Filters persist across pages

Given I have applied filters When I change pages Then filters should remain applied


### Scenario 6: Sort persists across pages

Given I have sorted the list When I change pages Then sort should remain applied


### Scenario 7: Page size configurable

Given I am viewing a list When I change page size Then I can choose 25, 50, 100, 200


### Scenario 8: Performance with pagination

Given I have 10,000 records When I view the list Then each page should load in under 1 second


## Manual Testing Steps

### Test 1: Test pagination

1. View list with many records
2. Verify paginated
3. Verify controls present

### Test 2: Test navigate pages

1. Click Next
2. Click Previous
3. Verify navigation works

### Test 3: Test jump to page

1. Enter page number
2. Verify jumps to that page

### Test 4: Test total count

1. View list
2. Verify count shown
3. Verify accurate

### Test 5: Test filters persist

1. Apply filters
2. Change pages
3. Verify filters remain

### Test 6: Test sort persists

1. Sort list
2. Change pages
3. Verify sort remains

### Test 7: Test page size

1. Change page size
2. Verify changes

### Test 8: Test on all platforms

1. Test Windows, macOS, Linux
2. Verify all work

## Acceptance Criteria

- [ ] Lists are paginated
- [ ] Default 50-100 records per page
- [ ] Can navigate between pages
- [ ] Can jump to specific page
- [ ] Total count shown
- [ ] Filters persist across pages
- [ ] Sort persists across pages
- [ ] Page size configurable
- [ ] Performance good (under 1 second per page)
- [ ] Works on Windows, macOS, and Linux
