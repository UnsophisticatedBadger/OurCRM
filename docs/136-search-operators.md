# US-136 — Search Operators

**Capability:** shell
**Status:** Not Done
**Priority:** Post-MVP

## User Story
As an agent, I want to use AND, OR, NOT, and phrase operators in search, so that I can construct precise queries when simple keyword search isn't specific enough.

## Dependencies
- US-024 — Search Contacts
- US-030 — Search Contacts Globally

## Acceptance Criteria
1. Search supports the AND operator: `John AND Smith` returns records containing both terms
2. Search supports the OR operator: `John OR Jane` returns records containing either term
3. Search supports the NOT operator: `John NOT Smith` returns records containing "John" but not "Smith"
4. Search supports exact phrases in double quotes: `"John Smith"` returns only records containing that exact phrase
5. Search supports parentheses for grouping: `(John OR Jane) AND Smith` applies the grouping correctly
6. Operators are case-insensitive: `and`, `AND`, and `And` all behave the same
7. A "Search tips" link near the search field opens inline documentation listing all supported operators with examples
8. Operator queries can be combined with existing list filters (e.g., status filter + AND query)

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/shell.feature`.

```gherkin
@us155
Scenario: AND operator returns only records matching both terms
  Given contacts "John Smith" and "John Adams" exist
  When the user searches for "John AND Smith"
  Then only "John Smith" is returned

@us155
Scenario: OR operator returns records matching either term
  Given contacts "John Smith" and "Jane Adams" exist
  When the user searches for "John OR Jane"
  Then both contacts are returned

@us155
Scenario: NOT operator excludes matching records
  Given contacts "John Smith" and "John Adams" exist
  When the user searches for "John NOT Smith"
  Then "John Adams" is returned and "John Smith" is not

@us155
Scenario: Quoted phrase matches exact phrase only
  Given a contact "John Smith" and a note containing "John Q Smith" exist
  When the user searches for "\"John Smith\""
  Then only the exact phrase "John Smith" is matched

@us155
Scenario: Operators are case-insensitive
  Given contacts "John Smith" and "John Adams" exist
  When the user searches for "john and smith"
  Then only "John Smith" is returned

@us155
Scenario: Search tips link opens operator documentation
  Given the user is in the search field
  When the user clicks "Search tips"
  Then inline documentation shows all supported operators with examples
```

## Manual Tests
**Story:** [US-136 — Search Operators](../docs/129-search-operators.md)

### AND operator returns only records matching both terms
1. Search for "John AND Smith"
2. Verify only records containing both "John" and "Smith" appear

### OR operator returns records matching either term
1. Search for "John OR Jane"
2. Verify records containing "John" or "Jane" (or both) appear

### NOT operator excludes matching records
1. Search for "John NOT Smith"
2. Verify "John Adams" appears but "John Smith" does not

### Exact phrase matching with double quotes
1. Search for `"John Smith"` (with quotes)
2. Verify only records with the exact phrase are returned

### Operator documentation is accessible
1. Click "Search tips" near the search field
2. Verify documentation lists AND, OR, NOT, quotes, and parentheses with examples

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_search_operators.py` |
| Manual tests | `tests/manual/shell/search-operators.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
