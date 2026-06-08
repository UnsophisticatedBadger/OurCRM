# US-155: Search Operators (AND, OR, NOT)

## User Story

**As an** agent  
**I want to** use search operators to refine my searches  
**So that** I can find exactly what I'm looking for with precise criteria

## Priority

**Future:** Post-MVP

**Rationale:** Power users need advanced search capabilities. Search operators (AND, OR, NOT, quotes, etc.) enable precise queries that simple search can't handle.

## Estimated Effort

**Size:** Medium (M) - 3-5 days

**Breakdown:**
- 2 hours: Design search operator syntax
- 3 hours: Implement operator parsing
- 2 hours: Add operator help/tooltips
- 2 hours: Test operator combinations
- 2 hours: Test search quality
- 2 hours: Test on all platforms

## Dependencies

**Depends on:** US-028 (Search Contacts), US-154 (Fuzzy Search / Typo Tolerance)

**Blocks:** None

## Description

Search should support operators:
- **AND**: Both terms must match ("John AND Smith")
- **OR**: Either term matches ("John OR Jane")
- **NOT**: Exclude terms ("John NOT Smith")
- **Quotes**: Exact phrase ("\"John Smith\"")
- **Parentheses**: Grouping ("(John OR Jane) AND Smith")

Operators should be documented and easy to discover.

## BDD Scenarios

### Scenario 1: Search with AND operator

Given I am searching When I type "John AND Smith" Then only contacts with both terms should be shown


### Scenario 2: Search with OR operator

Given I am searching When I type "John OR Jane" Then contacts with either term should be shown


### Scenario 3: Search with NOT operator

Given I am searching When I type "John NOT Smith" Then contacts with John but not Smith should be shown


### Scenario 4: Search with exact phrase

Given I am searching When I type ""John Smith"" Then only exact phrase matches should be shown


### Scenario 5: Search with grouping

Given I am searching When I type "(John OR Jane) AND Smith" Then the grouping should be respected


### Scenario 6: Operator help available

Given I am in the search interface When I look for help Then search operators should be documented With examples


### Scenario 7: Case insensitive operators

Given I am searching When I type "john AND smith" (lowercase) Then it should work the same as uppercase


### Scenario 8: Combine with filters

Given I have applied filters When I use search operators Then both filters and operators should apply


## Manual Testing Steps

### Test 1: Test AND operator

1. Search "John AND Smith"
2. Verify both required

### Test 2: Test OR operator

1. Search "John OR Jane"
2. Verify either matches

### Test 3: Test NOT operator

1. Search "John NOT Smith"
2. Verify exclusion works

### Test 4: Test exact phrase

1. Search "\"John Smith\""
2. Verify exact match only

### Test 5: Test grouping

1. Search with parentheses
2. Verify grouping respected

### Test 6: Test help

1. Look for operator help
2. Verify documentation exists

### Test 7: Test case insensitivity

1. Use lowercase operators
2. Verify they work

### Test 8: Test on all platforms

1. Test Windows, macOS, Linux
2. Verify all work

## Acceptance Criteria

- [ ] AND operator works
- [ ] OR operator works
- [ ] NOT operator works
- [ ] Exact phrase (quotes) works
- [ ] Grouping (parentheses) works
- [ ] Operators are case-insensitive
- [ ] Operator help is available
- [ ] Can combine with filters
- [ ] Complex queries work
- [ ] Works on Windows, macOS, and Linux
- [ ] Search performance remains good