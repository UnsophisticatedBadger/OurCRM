# 47 - View Due Callbacks

**Capability:** Contacts
**Milestone:** MVP
**Status:** Done
**GitHub Issue:** #47

## User Story

As a real estate agent, I want to see at a glance which callbacks are due this week, so that I know exactly who to prioritise when I sit down to make calls.

## Dependencies

- #46 — Set callback timeframe

## Acceptance Criteria

1. A "Show only callbacks due this week" checkbox is available in the Call List view, unchecked by default
2. Checking it narrows the Call List to contacts with an overdue, due-today, or due-this-week callback, hiding contacts with no callback set and contacts whose latest outcome isn't Call Back
3. Overdue callbacks are visually highlighted with a red-tinted row and an "⚠ Overdue" badge on the contact's name, and continue to sort to the top (as established in #46)
4. Every Call Back contact's Last Outcome cell shows a relative day count instead of an absolute date: "N days overdue", "due today", or "due in N days" — this applies whenever the contact is visible in the Call List, independent of the filter checkbox
5. Unchecking the filter returns to the full call list

## BDD Scenarios

```gherkin
@story_47
Scenario: The due-this-week filter is available in the call list
  Given a contact "Mona NoCallback" has no callback set
  When the user opens the call list
  Then a "Show only callbacks due this week" checkbox is shown

@story_47
Scenario: Checking the filter hides contacts with no callback due
  Given a contact "Gina NoCallback" has no callback set
  And a contact "Hank ThisWeek" has a callback due later this week
  When the user opens the call list
  And the user checks the "Show only callbacks due this week" filter
  Then "Hank ThisWeek" appears in the call list
  And "Gina NoCallback" does not appear in the call list

@story_47
Scenario: Unchecking the filter restores the full call list
  Given a contact "Ivan NoCallback" has no callback set
  When the user opens the call list
  And the user checks the "Show only callbacks due this week" filter
  And the user unchecks the "Show only callbacks due this week" filter
  Then "Ivan NoCallback" appears in the call list

@story_47
Scenario: An overdue callback is highlighted with a red row and a badge
  Given a contact "Judy Overdue" has an overdue callback
  When the user opens the call list
  Then "Judy Overdue" is shown with a red-tinted row
  And "Judy Overdue" is shown with an "⚠ Overdue" badge

@story_47
Scenario: An overdue callback shows how many days overdue
  Given a contact "Ken Overdue" has a callback that was due 3 days ago
  When the user opens the call list
  Then "Ken Overdue" shows "3 days overdue"

@story_47
Scenario: A callback due today shows "due today"
  Given a contact "Mia DueToday" has a callback due today
  When the user opens the call list
  Then "Mia DueToday" shows "due today"

@story_47
Scenario: A callback due later this week shows how many days remain
  Given a contact "Liz ThisWeek" has a callback due in 2 days
  When the user opens the call list
  Then "Liz ThisWeek" shows "due in 2 days"
```

## Manual Tests

**Story:** [#47 — View Due Callbacks](47-view-due-callbacks.md)

### Filtering to just this week's callbacks
1. Open the Call List with a mix of contacts: some with overdue callbacks, some due this week, some with no callback set
2. Check "Show only callbacks due this week"
3. Confirm only the overdue/due-today/due-this-week contacts remain visible
4. Uncheck the filter and confirm the full call list returns

### Overdue callbacks are highlighted
1. Arrange a contact with an overdue callback
2. Open the Call List
3. Confirm the row has a red tint and an "⚠ Overdue" badge on the contact's name

### Relative day counts display correctly
1. Arrange contacts with an overdue callback, a callback due today, and a callback due later this week
2. Open the Call List
3. Confirm each shows the correct relative text: "N days overdue", "due today", or "due in N days"

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/contacts.feature` |
| BDD step defs | `tests/bdd/test_contacts.py` |
| Unit tests | `tests/unit/contacts/test_due_callbacks.py` |
| Manual tests | `tests/manual/contacts/view_due_callbacks.md` |

## Definition of Done

- [x] BDD scenarios pass
- [x] `ruff`, `mypy --strict` clean
- [x] Checking the filter narrows the Call List to overdue/due-today/due-this-week contacts only; overdue rows show a red tint and badge; relative day counts display correctly; unchecking restores the full list
- [x] Wiki documentation written, or marked N/A with a reason
