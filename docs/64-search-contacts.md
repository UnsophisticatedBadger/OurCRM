# 64 - Search Contacts

**Capability:** Contacts
**Milestone:** MVP
**Status:** Not Done
**GitHub Issue:** #64

## User Story

As a real estate agent, I want to search my contacts by name, email, or phone as I type, so that I can find someone in seconds instead of scrolling through the list.

## Dependencies

- #44 — View Contact List

## Acceptance Criteria

1. A search box in the Contacts section filters the list as the user types; results update with each keystroke
2. Search matches against name, email, and phone; matching is case-insensitive and supports partial strings
3. When no contacts match, "No contacts found" is shown with a prompt to clear the search
4. Clearing the search box (or pressing Escape) restores the full contact list
5. Ctrl+F / Cmd+F focuses the search box from anywhere in the Contacts section

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/contacts.feature`.

```gherkin
@story_64
Scenario: Typing in the search box filters the contact list
  Given contacts "John Smith" and "Jane Doe" exist
  When the user types "John" in the search box
  Then only "John Smith" is shown

@story_64
Scenario: Search is case-insensitive
  Given a contact "John Smith" exists
  When the user searches for "john"
  Then "John Smith" appears in results

@story_64
Scenario: Search supports partial matches
  Given a contact "Johnson" exists
  When the user searches for "John"
  Then "Johnson" appears in results

@story_64
Scenario: Searching by email finds the correct contact
  Given a contact with email "jane@example.com" exists
  When the user searches for "jane@example"
  Then that contact is shown in results

@story_64
Scenario: No results shows a helpful message
  When the user searches for "xyz123"
  Then "No contacts found" is shown

@story_64
Scenario: Clearing the search restores the full contact list
  Given the user has searched for "John"
  When the user clears the search box
  Then all contacts are shown again
```

## Manual Tests

**Story:** [#52 — Search Contacts](../docs/020-search-contacts.md)

### User searches by name and sees filtered results
1. Create contacts with varied names
2. Type part of a name in the search box
3. Confirm the list updates with each keystroke to show only matching contacts
4. Confirm matching is case-insensitive (search "john" finds "John Smith")

### User searches by email and phone
1. Type part of a contact's email address — confirm that contact appears
2. Clear and type part of a phone number — confirm the correct contact appears

### Partial match works
1. Create contacts "John Smith" and "Johnson"
2. Search for "John" — confirm both appear
3. Search for "Johns" — confirm only "Johnson" appears

### No results shows a clear message
1. Search for a string that matches no contacts
2. Confirm "No contacts found" appears with a way to clear the search

### Escape clears the search
1. Type a search query
2. Press Escape
3. Confirm the search box empties and all contacts reappear

### Ctrl+F focuses the search box
1. Navigate to the Contacts section
2. Press Ctrl+F (Cmd+F on macOS)
3. Confirm the search box is focused and ready to accept input

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/contacts.feature` |
| BDD step defs | `tests/bdd/test_contacts.py` |
| Unit tests | `tests/unit/contacts/test_contact_search.py` |
| Manual tests | `tests/manual/contacts/search_contacts.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
