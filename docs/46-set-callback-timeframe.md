# 46 - Set Callback Timeframe

**Capability:** Contacts
**Milestone:** MVP
**Status:** Done
**GitHub Issue:** #46

## User Story

As a real estate agent, I want to set a vague callback timeframe when someone asks me to call back later, so that the contact surfaces again at the right time without me having to remember it.

## Dependencies

- #45 — Log call outcome

## Acceptance Criteria

1. When the Call Back outcome is selected, a timeframe picker appears before confirming
2. Timeframe options are: This Week, Next Week, In Two Weeks, This Month
3. Selecting a timeframe saves a target callback date range on the contact
4. The contact is removed from the active call list and placed in the callback queue
5. When the target date range arrives, the contact reappears in the call list, with its next callback due date shown
6. The call list's full priority order is: overdue callbacks first (most overdue at top), then callbacks due today, then callbacks due this week, then new contacts not yet called, then contacts with no callback set

## BDD Scenarios

```gherkin
@story_46
Scenario: Selecting Call Back shows a timeframe picker
  Given a contact is open in the call list detail view
  When the user logs the outcome "Call Back"
  Then a timeframe picker is shown with options "This Week", "Next Week", "In Two Weeks", and "This Month"

@story_46
Scenario: Choosing a timeframe and confirming saves a callback date range
  Given a contact is open in the call list detail view
  When the user logs the outcome "Call Back" with timeframe "Next Week"
  Then the contact's callback date range is saved for next week

@story_46
Scenario: Logging Call Back removes the contact from the active call list
  Given a contact is open in the call list detail view
  When the user logs the outcome "Call Back" with timeframe "Next Week"
  Then the contact no longer appears in the call list

@story_46
Scenario: A callback due this week keeps the contact visible with its due date shown
  Given a contact has a callback due this week
  When the user opens the call list
  Then the contact appears in the call list
  And its next callback due date is shown

@story_46
Scenario: A callback whose window has just started reappears in the call list
  Given a contact has a callback starting today
  When the user opens the call list
  Then the contact appears in the call list

@story_46
Scenario: Overdue callbacks sort to the top, most overdue first
  Given a contact "Alice Overdue" has a callback that was due 5 days ago
  And a contact "Bob Overdue" has a callback that was due 1 day ago
  When the user opens the call list
  Then "Alice Overdue" appears above "Bob Overdue"

@story_46
Scenario: The call list priority order places overdue, then due today, then due this week, then everyone else
  Given a contact "Carol Overdue" has an overdue callback
  And a contact "Dana Today" has a callback due today
  And a contact "Erin ThisWeek" has a callback due later this week
  And a contact "Frank NoCallback" has no callback set
  When the user opens the call list
  Then the contacts appear in the order "Carol Overdue", "Dana Today", "Erin ThisWeek", "Frank NoCallback"
```

## Manual Tests

**Story:** [#46 — Set Callback Timeframe](46-set-callback-timeframe.md)

### Logging Call Back opens a timeframe picker
1. Open a contact from the call list and click Log Outcome
2. Select "Call Back"
3. Confirm a timeframe picker appears with options This Week, Next Week, In Two Weeks, and This Month

### Setting a callback removes the contact from the active call list
1. Log "Call Back" on a contact and choose "Next Week"
2. Confirm the contact disappears from the Call List view
3. Confirm the contact still appears in the All Contacts view

### A callback reappears in the call list once its window arrives
1. Log "Call Back" and choose "This Week" (a window that starts today)
2. Confirm the contact still appears in the Call List view with its callback due date shown
3. For a callback set with a later timeframe (e.g. "Next Week"), confirm it stays hidden from the Call List until its start date arrives, then reappears with its due date shown

### Call list priority order
1. Arrange several contacts with an overdue callback, a callback due today, a callback due this week, and no callback set
2. Open the Call List view
3. Confirm the order is: most overdue first, then due today, then due this week, then everyone else

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/contacts.feature` |
| BDD step defs | `tests/bdd/test_contacts.py` |
| Unit tests | `tests/unit/contacts/test_callback_timeframe.py` |
| Manual tests | `tests/manual/contacts/set_callback_timeframe.md` |

## Definition of Done

- [x] BDD scenarios pass
- [x] `ruff`, `mypy --strict` clean
- [x] Callback set for next week; contact disappears from active list; after simulating date change contact reappears with due date shown, sorted ahead of new contacts; full overdue/due-today/due-this-week/new/no-callback priority order verified by inspection
- [x] Wiki documentation written, or marked N/A with a reason
