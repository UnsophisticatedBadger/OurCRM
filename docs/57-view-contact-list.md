# 57 - View Contact List

**Capability:** Contacts
**Milestone:** MVP
**Status:** Done
**GitHub Issue:** #57

## User Story

As a real estate agent, I want to see all my contacts in a sortable list, so that I can find anyone I work with at a glance.

## Dependencies

- #56 — Create a New Contact

## Acceptance Criteria

1. The Contacts section displays a table of all contacts with first name, last name, street address, city, email, phone, and tags columns; sorted by last name by default
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
  And the list is sorted by last name by default

@story_57
Scenario: User with no contacts sees an empty state
  Given the user has no contacts
  When the user opens the Contacts section
  Then "No contacts yet" is shown
  And a "Create Your First Contact" button is visible

@story_57
Scenario: User sorts the contact list by clicking a column header
  Given the user is viewing a contact list with multiple contacts
  When the user clicks the "Last Name" column header
  Then the contacts are sorted by last name descending
  When the user clicks the "Last Name" column header again
  Then the contacts are sorted alphabetically by last name ascending

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
  And the scroll position is unchanged
```

## Manual Tests

**Story:** [#57 — View Contact List](57-view-contact-list.md)
### User sees all contacts in the list
1. Create 5 contacts with varied names
2. Navigate to the Contacts section
3. Confirm all contacts appear, each row showing first name, last name, street address, city, email, phone, and tags
4. Confirm the default sort is alphabetical by last name

### User sees the empty state with no contacts
1. Open the app with a fresh database (no contacts)
2. Navigate to the Contacts section
3. Confirm "No contacts yet" message appears
4. Confirm the "Create Your First Contact" button is visible and opens the new contact form

### User sorts by column
1. View the contact list with several contacts (sorted by last name ascending by default)
2. Click the "Last Name" column header — confirm descending sort and the sort indicator flips
3. Click it again — confirm ascending sort
4. Click another column — confirm sort switches to that column, ascending

### User double-clicks to open contact details
1. Double-click any contact in the list
2. Confirm the contact details view opens for that contact

### Sort is preserved after navigating away
1. Sort the contact list by email
2. Scroll partway down the list
3. Navigate to Leads, then return to Contacts
4. Confirm the sort column and direction are unchanged
5. Confirm the scroll position is unchanged

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/contacts.feature` |
| BDD step defs | `tests/bdd/test_contacts.py` |
| Unit tests | `tests/unit/contacts/test_contacts_page.py`, `test_contact_detail_dialog.py`, `test_contact_repository.py` |
| Manual tests | `tests/manual/contacts/contact_list.md` |

## Definition of Done

- [x] BDD scenarios pass end-to-end
- [x] Feature reachable from the running app
- [x] `ruff`, `mypy --strict` clean
- [x] Manual tests documented and verified
- [x] Wiki documentation written, or marked N/A with a reason
