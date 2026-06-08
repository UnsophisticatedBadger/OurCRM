# US-061: Search Across All Sections

## User Story

**As an** agent  
**I want to** search for contacts, leads, properties, and transactions from one place  
**So that** I can find anything in the system without knowing which section it's in

## Priority

**MVP:** Must Have

**Rationale:** Global search across all sections is a major productivity feature. Instead of searching each section separately, agents can find anything from one search interface. This is especially useful when you remember a detail but not which section it belongs to.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design multi-section search UI
- 2 hours: Extend global search to all sections
- 1 hour: Group results by section
- 1 hour: Add section indicators to results
- 1 hour: Implement navigation to result
- 1 hour: Add result type icons
- 1 hour: Test search across sections
- 1 hour: Test performance
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-060 (Search Contacts Globally), US-028 (Search Contacts)

**Blocks:** US-062 (Quick Actions Menu), US-063 (Recent Searches)

## Description

The global search (Ctrl+K / Cmd+K) should search across all sections: contacts, leads, properties, and transactions. Results should be grouped by section type and clearly labeled. Each result should show enough information to identify it (name, address, etc.) and clicking it should open the relevant section.

The search should be fast and should work across all data fields (name, email, phone, address, notes, tags, etc.) in all sections. Results should be ranked by relevance.

## BDD Scenarios

### Scenario 1: Search across all sections

```
Given I have contacts, leads, properties, and transactions
When I open global search (Ctrl+K)
  And I type a search query
Then I should see results grouped by section:
  - Contacts (with count)
  - Leads (with count)
  - Properties (with count)
  - Transactions (with count)
```

### Scenario 2: Results show section type

```
Given I am viewing global search results
When I look at each result
Then I should see what type it is:
  - Contact icon + name
  - Lead icon + name
  - Property icon + address
  - Transaction icon + address
  And the section should be clearly labeled
```

### Scenario 3: Click result to open

```
Given I am viewing global search results
When I click on a contact result
Then the Contacts section should open
  And the specific contact should be selected
  And its details should be visible
```

### Scenario 4: Click property result

```
Given I am viewing global search results
When I click on a property result
Then the Properties section should open
  And the specific property should be selected
  And its details should be visible
```

### Scenario 5: Search shows result counts

```
Given I have results from multiple sections
When I view the search results
Then I should see:
  - Contacts (5 results)
  - Leads (3 results)
  - Properties (2 results)
  - Transactions (1 result)
  And the counts should be accurate
```

### Scenario 6: Empty sections are hidden

```
Given I search for something that only matches contacts
When I view the results
Then only the Contacts section is shown
  And empty sections (Leads, Properties, Transactions) are not shown
```

### Scenario 7: No results found

```
Given I search for something that doesn't match anything
When I view the results
Then I should see "No results found"
  And it should be clear nothing matched
```

### Scenario 8: Search is fast

```
Given I have 500 contacts, 200 leads, 100 properties, 50 transactions
When I type in the global search
Then results should appear within 500ms
  And the UI should remain responsive
```

## Manual Testing Steps

### Test 1: Search across all sections

1. Create contacts, leads, properties, and transactions
2. Open global search (Ctrl+K)
3. Type a common term that appears in multiple sections
4. Verify results are grouped by section
5. Verify each section shows its results

### Test 2: Test result type indicators

1. Search for a term
2. Verify each result shows its type
3. Check that icons are clear
4. Verify section labels are visible

### Test 3: Test navigation

1. Search and find a contact
2. Click on it
3. Verify it opens the contact
4. Go back and search for a property
5. Click on it
6. Verify it opens the property
7. Test with leads and transactions

### Test 4: Test result counts

1. Search for a term
2. Verify the counts for each section are correct
3. Manually count to verify accuracy

### Test 5: Test empty sections

1. Search for a term that only matches contacts
2. Verify only Contacts section is shown
3. Verify other sections are not shown

### Test 6: Test no results

1. Search for something that doesn't exist
2. Verify the "No results found" message
3. Verify it's clear

### Test 7: Test performance

1. Create large datasets
2. Search and measure time
3. Verify it's under 500ms
4. Test UI responsiveness

### Test 8: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Global search searches all sections
- [ ] Results are grouped by section type
- [ ] Each result shows its type clearly
- [ ] Result counts are shown for each section
- [ ] Clicking a result opens the relevant section
- [ ] Empty sections are not shown
- [ ] No results state is clear
- [ ] Search is fast (under 500ms with large datasets)
- [ ] Works on Windows, macOS, and Linux
- [ ] Search is comprehensive but not overwhelming
- [ ] Results are relevant and accurate
- [ ] Navigation is smooth and intuitive