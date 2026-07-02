# 57 - View Contact List

**Capability:** Contacts
**Milestone:** MVP
**Status:** Not Done
**GitHub Issue:** #57

## User Story

As a real estate agent, I want to see all my contacts in a sortable list, so that I can find anyone I work with at a glance.

## Dependencies

- #43 — Create a New Contact

## Acceptance Criteria

1. The Contacts section displays a table of all contacts with name, email, phone, and tags columns; sorted by name by default
2. Clicking a column header sorts by that column; clicking the same header again reverses the order
3. Double-clicking a contact row opens its details view
4. When no contacts exist, an empty state message "No contacts yet" is shown with a "Create Your First Contact" button
5. Sort column, sort direction, and scroll position are preserved when the user navigates away and returns

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/contacts.feature`.

```gherkin
@story_57
Scenario: User with contacts sees them listed in the Contacts section
  Given the user has created contacts "Alice Brown" and "Bob Carter"
  When the user opens the Contacts section
  Then the list shows "Alice Brown" and "Bob Carter"
  And the list is sorted by name by default

@story_57
Scenario: User with no contacts sees an empty state
  Given the user has no contacts
  When the user opens the Contacts section
  Then "No contacts yet" is shown
  And a "Create Your First Contact" button is visible

@story_57
Scenario: User sorts the contact list by clicking a column header
  Given the user is viewing a contact list with multiple contacts
  When the user clicks the "Name" column header
  Then the contacts are sorted alphabetically by name ascending
  When the user clicks the "Name" column header again
  Then the contacts are sorted by name descending

@story_57
Scenario: User double-clicks a contact and sees its details
  Given the user is viewing the contact list
  When the user double-clicks "Alice Brown"
  Then the contact details view opens for "Alice Brown"

@story_57
Scenario: Sort order is preserved when the user navigates away and back
  Given the user has sorted the contact list by email ascending
  When the user navigates to the Leads section and back to Contacts
  Then the list is still sorted by email ascending
```

## Manual Tests

**Story:** [#44 — View Contact List](../docs/011-view-contact-list.md)

### User sees all contacts in the list
1. Create 5 contacts with varied names
2. Navigate to the Contacts section
3. Confirm all contacts appear, each row showing name, email, phone, and tags
4. Confirm the default sort is alphabetical by name

### User sees the empty state with no contacts
1. Open the app with a fresh database (no contacts)
2. Navigate to the Contacts section
3. Confirm "No contacts yet" message appears
4. Confirm the "Create Your First Contact" button is visible and opens the new contact form

### User sorts by column
1. View the contact list with several contacts
2. Click the "Name" column header — confirm ascending sort and sort indicator
3. Click it again — confirm descending sort
4. Click another column — confirm sort switches to that column

### User double-clicks to open contact details
1. Double-click any contact in the list
2. Confirm the contact details view opens for that contact

### Sort is preserved after navigating away
1. Sort the contact list by email
2. Navigate to Leads, then return to Contacts
3. Confirm the sort column and direction are unchanged

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/contacts.feature` |
| BDD step defs | `tests/bdd/test_contacts.py` |
| Unit tests | `tests/unit/contacts/test_contact_list.py` |
| Manual tests | `tests/manual/contacts/contact_list.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
