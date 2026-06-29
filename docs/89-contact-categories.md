# US-130 — Contact Categories

**Capability:** Contacts
**Status:** Not Done
**GitHub Issue:** #89
**Priority:** Should Have (deferrable to post-MVP)

## User Story

As a real estate agent, I want to assign each contact to a category so that I can segment my database into meaningful groups and quickly filter to the contacts I need.

## Dependencies

- #43 — Create a New Contact
- #44 — View Contact List

## Notes

Categories are a distinct field from tags (US-022). Tags are flexible many-per-contact labels; a category is a single structured classification per contact. A contact may have many tags and one category (or none).

Default categories are pre-seeded on a fresh install and can be renamed or deleted like any other category.

## Acceptance Criteria

1. A "Category" dropdown field is available on the Create Contact (US-016) and Edit Contact (US-019) forms; the field is optional and defaults to no selection
2. The following default categories are pre-seeded on a fresh install: Past Client, Current Client, Prospect, Vendor, Referral Partner, Other
3. A "Manage Categories" action in the Contacts section opens a panel where users can create new categories (name only) and see all existing categories
4. Any category can be renamed; the new name is reflected immediately on all contacts assigned to that category
5. Any category can be deleted; if contacts are assigned to it, a confirmation prompt asks to move affected contacts to "Other" or cancel; if no contacts are assigned, deletion proceeds without a prompt
6. A contact's category is shown in the contact detail view and as a column in the contact list
7. The contact list supports filtering by category (single selection); a category filter can be combined with an active tag filter (US-023) to narrow results further

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/contacts.feature`.

```gherkin
@us130
Scenario: New contact can be assigned a category
  Given the Create Contact form is open
  When the user selects "Prospect" from the Category dropdown and saves
  Then the contact is created with category "Prospect"
  And "Prospect" is shown in the contact detail view

@us130
Scenario: Category is visible as a column in the contact list
  Given contacts exist with different categories
  When the user views the contact list
  Then a Category column is shown and each contact displays its assigned category

@us130
Scenario: Filtering by category shows only matching contacts
  Given contacts exist with categories "Prospect" and "Past Client"
  When the user filters by "Prospect"
  Then only contacts with category "Prospect" are shown in the list

@us130
Scenario: Creating a new category makes it available on contact forms
  Given the user opens Manage Categories and creates a category "Investor"
  When the user opens the Create Contact form
  Then "Investor" is available in the Category dropdown

@us130
Scenario: Renaming a category updates all assigned contacts
  Given 3 contacts are assigned category "Prospect"
  When the user renames "Prospect" to "Active Lead"
  Then all 3 contacts show "Active Lead" as their category

@us130
Scenario: Deleting a category with assigned contacts requires confirmation
  Given contacts are assigned to category "Vendor"
  When the user deletes "Vendor"
  Then a confirmation prompt asks whether to move those contacts to "Other" or cancel
  And choosing "Move to Other" updates those contacts and removes the category

@us130
Scenario: Deleting a category with no assigned contacts needs no confirmation
  Given a category "Archived" has no contacts assigned
  When the user deletes "Archived"
  Then the category is removed immediately without a confirmation prompt
```

## Manual Tests

**Story:** [US-119 — Contact Categories](../docs/119-contact-categories.md)

### Default categories are available on a fresh install
1. On a fresh install, open the Create Contact form
2. Confirm the Category dropdown lists: Past Client, Current Client, Prospect, Vendor, Referral Partner, Other

### Assigning a category to a contact
1. Create a new contact and select "Prospect" from the Category dropdown
2. Save and open the contact detail view
3. Confirm "Prospect" is shown in the details
4. Confirm the category is also visible in the contact list column

### Filtering contacts by category
1. Create contacts with at least two different categories
2. Filter the contact list by one of those categories
3. Confirm only contacts with that category are shown
4. Apply a tag filter alongside the category filter and confirm both are respected simultaneously
5. Clear the category filter and confirm all contacts return

### Creating and using a custom category
1. Open Manage Categories and create a new category "Investor"
2. Confirm it appears in the category list
3. Open the Create Contact form and confirm "Investor" is in the dropdown
4. Assign it and save — confirm the contact shows "Investor" as its category

### Renaming a category updates all assigned contacts
1. Assign several contacts to "Prospect"
2. Rename "Prospect" to "Active Lead" in Manage Categories
3. Confirm all those contacts now show "Active Lead"

### Deleting a category
1. Delete a category that has no assigned contacts — confirm it disappears immediately
2. Create contacts assigned to another category, then delete that category
3. Confirm the prompt appears offering to move contacts to "Other" or cancel
4. Choose "Move to Other" and confirm the contacts now show "Other" and the deleted category is gone

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/contacts.feature` |
| BDD step defs | `tests/bdd/test_contacts.py` |
| Unit tests | `tests/unit/contacts/test_contact_categories.py` |
| Manual tests | `tests/manual/contacts/contact_categories.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
