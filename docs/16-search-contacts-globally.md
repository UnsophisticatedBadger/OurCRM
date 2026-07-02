# 16 - Search Contacts Globally

**Capability:** App Shell
**Milestone:** Secure Shell
**Status:** Not Done
**GitHub Issue:** #16

## User Story

As a real estate agent, I want to open a global search overlay from anywhere in the application and search my contacts, so that I can find someone quickly without navigating to the Contacts section first.

## Dependencies

- #52 — Search Contacts

## Notes

#58 establishes the global search infrastructure: the Ctrl+K overlay, keyboard navigation, and Escape-to-close behaviour. #59 extends it to search leads, properties, and transactions. Any future search story builds on top of this one.

## Acceptance Criteria

1. Pressing Ctrl+K from any section opens the global search overlay with the text input focused and ready to type
2. Typing in the search input queries contacts by name, email, and phone and shows matching results in real time as the user types
3. Arrow keys move the highlight through results; pressing Enter on a highlighted result opens that contact's detail view and closes the overlay
4. Pressing Escape or clicking outside the overlay closes it and returns the user to the view they were on
5. When no contacts match the query, a "No results found" message is displayed
6. The Ctrl+K shortcut and the overlay function correctly from every section of the application

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/shell.feature`.

```gherkin
@story_16
Scenario: User opens global search from the Leads section and sees the focused input
  Given the user is viewing the Leads section
  When the user presses Ctrl+K
  Then the global search overlay opens
  And the search text input is focused

@story_16
Scenario: User types a contact name and sees matching results
  Given a contact "Alice Smith" exists
  And the global search overlay is open
  When the user types "Alice"
  Then "Alice Smith" appears in the results

@story_16
Scenario: User navigates to a result with arrow keys and opens it with Enter
  Given the global search overlay shows results for "Alice"
  When the user presses the down arrow key to highlight "Alice Smith"
  And presses Enter
  Then Alice Smith's contact detail view opens
  And the overlay closes

@story_16
Scenario: User presses Escape and returns to the previous view
  Given the user opened the global search overlay from the Properties section
  When the user presses Escape
  Then the overlay closes
  And the Properties section is visible

@story_16
Scenario: User searches for a term with no matching contacts
  Given the global search overlay is open
  When the user types "zzznomatch"
  Then a "No results found" message is displayed
```

## Manual Tests

**Story:** [#58 — Search Contacts Globally](../docs/030-search-contacts-globally.md)

### User opens global search from different sections and sees the focused input
1. Navigate to the Leads section
2. Press Ctrl+K
3. Confirm the overlay opens and the search input is focused
4. Press Escape, navigate to Properties, and repeat
5. Confirm the overlay opens from every major section

### User searches for a contact and results appear in real time
1. Open global search (Ctrl+K)
2. Type a partial contact name (e.g., the first three letters)
3. Confirm matching contacts appear immediately as you type
4. Type additional characters and confirm the list narrows
5. Clear the input and confirm results clear

### User navigates results with the keyboard and opens a contact
1. Open global search and type a name with multiple matches
2. Press the down arrow to move the highlight through results
3. Press the up arrow to move back
4. Press Enter on a highlighted result
5. Confirm the contact's detail view opens and the overlay is gone

### Escape closes the overlay and restores the previous view
1. Navigate to the Transactions section
2. Open global search and type something
3. Press Escape
4. Confirm the overlay closes and the Transactions section is visible and unchanged

### No-results state
1. Open global search and type a string that matches no contacts
2. Confirm "No results found" is shown (not a blank screen)

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_global_search.py` |
| Manual tests | `tests/manual/shell/global_search.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
