# 64 - Search Contacts

**Capability:** Contacts
**Milestone:** MVP
**Status:** Done
**GitHub Issue:** #64

## User Story

As a real estate agent, I want to search my contacts by any field shown in the contact list as I type, so that I can find someone in seconds instead of scrolling through the list.

## Dependencies

- #57 — View Contact List

## Acceptance Criteria

1. A search box in the Contacts section filters the list as the user types; results update with each keystroke
2. Search matches against every field shown in the contact list — first name, last name, street address, city, email, phone, and tags; matching is case-insensitive and supports partial strings
3. When no contacts match, "No contacts found" is shown with a prompt to clear the search
4. Clearing the search box (standard text editing — backspace/delete) restores the full contact list
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
Scenario: Searching by phone finds the correct contact
  Given a contact with phone "555-0100" exists
  When the user searches for "0100"
  Then that contact is shown in results

@story_64
Scenario: Searching by street address finds the correct contact
  Given a contact with street address "123 Oak St" exists
  When the user searches for "Oak"
  Then that contact is shown in results

@story_64
Scenario: Searching by city finds the correct contact
  Given a contact with city "Austin" exists
  When the user searches for "Austin"
  Then that contact is shown in results

@story_64
Scenario: Searching by tag finds the correct contact
  Given a contact tagged "vip" exists
  When the user searches for "vip"
  Then that contact is shown in results

@story_64
Scenario: No results shows a helpful message
  Given a contact "John Smith" exists
  When the user searches for "xyz123"
  Then a "No contacts found" message is shown

@story_64
Scenario: Clearing the search restores the full contact list
  Given contacts "John Smith" and "Jane Doe" exist and the user has searched for "John"
  When the user clears the search box
  Then all contacts are shown again
```

## Manual Tests

**Story:** [#64 — Search Contacts](64-search-contacts.md)
### User searches by name and sees filtered results
1. Create contacts with varied names
2. Type part of a name in the search box
3. Confirm the list updates with each keystroke to show only matching contacts
4. Confirm matching is case-insensitive (search "john" finds "John Smith")

### User searches by email and phone
1. Type part of a contact's email address — confirm that contact appears
2. Clear and type part of a phone number — confirm the correct contact appears

### User searches by street address, city, and tags
1. Type part of a contact's street address — confirm that contact appears
2. Clear and type a contact's city — confirm that contact appears
3. Clear and type one of a contact's tags — confirm that contact appears

### Partial match works
1. Create contacts "John Smith" and "Johnson"
2. Search for "John" — confirm both appear
3. Search for "Johns" — confirm only "Johnson" appears

### No results shows a clear message
1. Search for a string that matches no contacts
2. Confirm "No contacts found" appears with a way to clear the search

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

- [x] BDD scenarios pass end-to-end
- [x] Feature reachable from the running app
- [x] `ruff`, `mypy --strict` clean
- [x] Manual tests documented and verified
- [x] Wiki documentation written, or marked N/A with a reason
