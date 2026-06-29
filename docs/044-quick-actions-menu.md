# US-044 — Quick Actions in Global Search

**Capability:** App Shell
**Status:** Not Done

## User Story

As a real estate agent, I want to type action commands into the global search to create records or jump to sections, so that I can perform common tasks without navigating through menus.

## Dependencies

- US-030 — Search Contacts Globally
- US-031 — Search Across All Sections

## Acceptance Criteria

1. Typing "new" or "create" in the global search shows quick action suggestions: New Contact, New Lead, New Property, New Transaction, New Showing
2. Typing a section name ("contacts", "leads", "properties", "transactions", "calendar", "settings") shows a "Go to …" navigation action for that section
3. Typing "settings" shows an "Open Settings" action
4. Quick actions are shown in a visually distinct group above record results when both are present
5. Selecting a quick action (Enter or click) executes it and closes the overlay

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/shell.feature`.

```gherkin
@us062
Scenario: Typing "new" shows creation quick actions
  Given the global search overlay is open
  When the user types "new"
  Then quick action suggestions appear: "New Contact", "New Lead", "New Property", "New Transaction", "New Showing"

@us062
Scenario: Selecting "New Contact" opens the contact creation form
  Given the global search overlay shows the "New Contact" quick action
  When the user selects "New Contact"
  Then the new contact creation form opens
  And the overlay closes

@us062
Scenario: Typing "leads" shows a navigation quick action
  Given the global search overlay is open
  When the user types "leads"
  Then a "Go to Leads" quick action appears

@us062
Scenario: Selecting a navigation action takes the user to that section
  Given the global search overlay shows "Go to Properties"
  When the user selects "Go to Properties"
  Then the Properties section opens
  And the overlay closes

@us062
Scenario: Typing "settings" shows the Open Settings action
  Given the global search overlay is open
  When the user types "settings"
  Then an "Open Settings" quick action appears
  And selecting it opens the Settings window

@us062
Scenario: Quick actions and record results appear together with actions separated visually
  Given a contact "Alice Smith" exists
  And the user types "new" in the global search
  Then quick action suggestions appear
  And if "Alice Smith" also matches, it appears in a separate results section below the actions
```

## Manual Tests

**Story:** [US-032 — Quick Actions in Global Search](../docs/032-quick-actions-menu.md)

### Creation quick actions appear when typing "new" or "create"
1. Open global search (Ctrl+K)
2. Type "new"
3. Confirm quick action chips appear for New Contact, New Lead, New Property, New Transaction, New Showing
4. Type "create" and confirm the same actions appear
5. Clear the input and confirm the actions disappear

### Selecting a creation action opens the correct form
1. Type "new" and select "New Contact"
2. Confirm the contact creation form opens and the overlay is closed
3. Repeat for New Lead, New Property, and New Transaction

### Section navigation quick actions
1. Type "contacts" in global search
2. Confirm "Go to Contacts" appears
3. Select it and confirm the Contacts section opens
4. Repeat for "leads", "properties", "calendar", and "settings"

### Quick actions are visually separated from record results
1. Type a term that produces both quick actions and record results (e.g., "new" when contacts also match "new")
2. Confirm actions appear in a distinct group above the record results

### Open Settings quick action
1. Type "settings" in global search
2. Select "Open Settings"
3. Confirm the Settings window opens and the overlay closes

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_quick_actions.py` |
| Manual tests | `tests/manual/shell/quick_actions.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
