# US-043 — Search Across All Sections

**Capability:** App Shell
**Status:** Not Done

## User Story

As a real estate agent, I want the global search to find contacts, leads, properties, and transactions all at once, so that I can locate any record without knowing which section it lives in.

## Dependencies

- US-030 — Search Contacts Globally

## Acceptance Criteria

1. The global search queries contacts, leads, properties, and transactions simultaneously when the user types
2. Results are grouped under section headers: Contacts, Leads, Properties, Transactions
3. Section headers that have no results are not shown
4. Each result row shows enough to identify the record: contact and lead rows show the person's name; property and transaction rows show the property address
5. Clicking (or pressing Enter on) a result opens that record's detail view, navigating to the correct section, and closes the overlay
6. When no records across any section match the query, a "No results found" message is displayed

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/shell.feature`.

```gherkin
@us061
Scenario: User types a term matching records in multiple sections and sees grouped results
  Given a contact "Alice Smith", a lead "Bob Jones", and a property "Alice Lane" exist
  When the user opens global search and types "Alice"
  Then a "Contacts" section header appears with "Alice Smith"
  And a "Properties" section header appears with "Alice Lane"
  And no "Leads" or "Transactions" section header is shown

@us061
Scenario: User clicks a lead result and is taken to that lead
  Given a lead "Bob Jones" exists
  And the global search shows "Bob Jones" under the Leads section
  When the user clicks "Bob Jones"
  Then Bob Jones's lead detail view opens
  And the overlay closes

@us061
Scenario: User clicks a property result and is taken to that property
  Given a property "123 Oak St" exists
  And the global search shows it under the Properties section
  When the user clicks "123 Oak St"
  Then the property detail view for "123 Oak St" opens
  And the overlay closes

@us061
Scenario: User types a term matching only contacts and only the Contacts section is shown
  Given a contact named "Zelda" exists and no leads, properties, or transactions match "Zelda"
  When the user types "Zelda" in global search
  Then only the "Contacts" section header is shown

@us061
Scenario: User types a term matching no records across any section
  Given the global search overlay is open
  When the user types "zzznomatch"
  Then a "No results found" message is displayed
  And no section headers are shown
```

## Manual Tests

**Story:** [US-031 — Search Across All Sections](../docs/035-search-across-all-sections.md)

### Results are grouped by section and only non-empty sections appear
1. Create at least one contact, one lead, one property, and one transaction that all share a keyword (e.g., "Smith")
2. Open global search and type "Smith"
3. Confirm Contacts, Leads, Properties, and Transactions section headers all appear
4. Confirm each header only lists its own matching records
5. Search for a term that matches only contacts and confirm the other section headers are absent

### Clicking a result navigates to the correct record and section
1. Search for a term and click a contact result
2. Confirm the contact detail view opens
3. Go back and search again; click a lead result
4. Confirm the lead detail view opens
5. Repeat for a property and a transaction

### Each result row is identifiable
1. Confirm contact rows show the contact's full name
2. Confirm lead rows show the lead's name
3. Confirm property rows show the property address
4. Confirm transaction rows show the property address and status

### No-results state when nothing matches across any section
1. Type a string that does not match any contact, lead, property, or transaction
2. Confirm "No results found" is shown with no section headers

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_cross_section_search.py` |
| Manual tests | `tests/manual/shell/cross_section_search.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
