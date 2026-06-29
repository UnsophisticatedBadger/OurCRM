# 19 - Recent Searches And Quick Access

**Capability:** App Shell
**Milestone:** v0.2.0 — Secure Shell
**Status:** Not Done
**GitHub Issue:** #19

## User Story

As a real estate agent, I want to see my recent search terms and recently viewed records when I open global search with an empty query, so that I can quickly return to what I was just working on.

## Dependencies

- #58 — Search Contacts Globally
- #59 — Search Across All Sections

## Acceptance Criteria

1. Opening the global search overlay with an empty query shows recent search terms, most recent first, capped at the last 10
2. Each completed search adds that search term to the recent searches list
3. Clicking a recent search term populates the search input with that term and runs the search immediately
4. A "Clear recent searches" action removes all stored search terms from the list
5. Below recent search terms, the overlay shows the last 10 recently viewed records (contacts, leads, properties, transactions) in reverse view order
6. Clicking a recently viewed record opens that record's detail view and closes the overlay

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/shell.feature`.

```gherkin
@story_19
Scenario: Recent search terms appear when the overlay opens with an empty query
  Given the user previously searched for "Alice" and then "Bob"
  When the user opens global search with an empty query
  Then "Bob" appears first in the recent searches list
  And "Alice" appears below it

@story_19
Scenario: Clicking a recent search term runs that search
  Given the global search overlay is open and shows "Alice" in recent searches
  When the user clicks "Alice"
  Then the search input is populated with "Alice"
  And results for "Alice" are shown

@story_19
Scenario: Clearing recent searches removes all terms
  Given the global search overlay shows recent search terms
  When the user clicks "Clear recent searches"
  Then the recent searches list is empty

@story_19
Scenario: Recently viewed records appear below recent searches
  Given the user has viewed contact "Alice Smith" and property "123 Oak St" in that order
  When the user opens global search with an empty query
  Then "123 Oak St" appears first in recently viewed records
  And "Alice Smith" appears below it

@story_19
Scenario: Clicking a recently viewed record opens it
  Given the global search overlay shows "Alice Smith" in recently viewed records
  When the user clicks "Alice Smith"
  Then Alice Smith's contact detail view opens
  And the overlay closes

@story_19
Scenario: Recent list is capped at 10 entries
  Given the user has performed 12 different searches
  When the user opens global search with an empty query
  Then only the 10 most recent search terms are shown
```

## Manual Tests

**Story:** [#61 — Recent Searches and Quick Access](../docs/033-recent-searches-and-quick-access.md)

### Recent search terms appear in reverse chronological order
1. Perform three searches: "Alice", "Bob", then "Carol"
2. Open global search with an empty query
3. Confirm "Carol" is listed first, then "Bob", then "Alice"

### Clicking a recent term re-runs the search
1. Open global search (empty query) and click "Carol" from recent searches
2. Confirm the search input fills with "Carol" and results appear immediately

### Clearing recent searches removes all terms
1. Ensure at least one recent search is listed
2. Click "Clear recent searches"
3. Confirm the list is empty and no search terms remain

### Recently viewed records appear below recent searches
1. Open a contact, then a property, then a lead (in that order)
2. Open global search with an empty query
3. Confirm the lead (most recently viewed) appears first, then property, then contact

### Clicking a recently viewed record opens it
1. From the recently viewed list, click any record
2. Confirm the correct detail view opens and the overlay closes

### Recent searches are capped at 10
1. Perform 12 distinct searches
2. Open global search with an empty query
3. Confirm only 10 entries are shown (the most recent 10)

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_recent_searches.py` |
| Manual tests | `tests/manual/shell/recent_searches.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
