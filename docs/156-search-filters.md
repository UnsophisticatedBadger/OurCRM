# US-156: Search Filters (Date Ranges, Custom Criteria)

## User Story

**As an** agent  
**I want to** filter searches by date ranges and custom criteria  
**So that** I can find exactly the records I need based on specific parameters

## Priority

**Future:** Post-MVP

**Rationale:** Advanced filtering enables precise data retrieval. Date ranges, custom fields, and multi-criteria filters help agents find exactly what they need for reporting, follow-ups, and analysis.

## Estimated Effort

**Size:** Medium (M) - 3-5 days

**Breakdown:**
- 2 hours: Design advanced filter UI
- 3 hours: Implement date range filters
- 2 hours: Add custom field filters
- 2 hours: Add multi-criteria support
- 2 hours: Test filter combinations
- 2 hours: Test on all platforms

## Dependencies

**Depends on:** US-028 (Search Contacts), US-155 (Search Operators)

**Blocks:** None

## Description

Advanced search filters should include:
- **Date ranges**: Created date, modified date, last contact
- **Custom fields**: Any custom field added to records
- **Numeric ranges**: Budget, price, value
- **Multi-select**: Multiple tags, categories, statuses
- **Conditional logic**: Greater than, less than, equals, contains

Filters should be combinable and savable for reuse.

## BDD Scenarios

### Scenario 1: Filter by date range

Given I am searching contacts When I set date range "Created: Jan 1 to Jan 31" Then only contacts created in that range should be shown


### Scenario 2: Filter by numeric range

Given I am searching leads When I set budget range "$300K to $500K" Then only leads in that budget should be shown


### Scenario 3: Filter by custom field

Given I have custom fields When I filter by a custom field value Then only matching records should be shown


### Scenario 4: Multiple filter criteria

Given I am searching When I apply multiple filters Then all criteria should be applied (AND logic by default)


### Scenario 5: Save filter combination

Given I have configured multiple filters When I save the search Then all filters should be saved And reusable later


### Scenario 6: Clear all filters

Given I have applied filters When I click "Clear All Filters" Then all filters should be removed And all records shown


### Scenario 7: Filter by relative date

Given I am searching When I select "Last 30 days" Then records from last 30 days should be shown Without specific dates


### Scenario 8: Filter by last activity

Given I am searching When I filter by "Last contacted: Before 6 months ago" Then inactive contacts should be shown


## Manual Testing Steps

### Test 1: Test date range filter

1. Set date range
2. Search
3. Verify results match

### Test 2: Test numeric range

1. Set numeric range
2. Search
3. Verify results match

### Test 3: Test custom field

1. Filter by custom field
2. Verify works

### Test 4: Test multiple filters

1. Apply several filters
2. Verify all applied

### Test 5: Test save filters

1. Configure filters
2. Save search
3. Reload
4. Verify filters restored

### Test 6: Test clear all

1. Apply filters
2. Clear all
3. Verify all records shown

### Test 7: Test relative dates

1. Select "Last 30 days"
2. Verify correct range

### Test 8: Test on all platforms

1. Test Windows, macOS, Linux
2. Verify all work

## Acceptance Criteria

- [ ] Date range filters work
- [ ] Numeric range filters work
- [ ] Custom field filters work
- [ ] Multiple filters can be combined
- [ ] Filters can be saved
- [ ] Can clear all filters
- [ ] Relative date options available
- [ ] Last activity filtering works
- [ ] Filter logic is clear
- [ ] Works on Windows, macOS, and Linux
- [ ] Filter performance is good