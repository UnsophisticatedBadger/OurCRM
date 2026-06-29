# 97 - Save Search Criteria For Leads And Properties

**Capability:** leads
**Milestone:** v0.5.0 — MVP
**Status:** Not Done
**GitHub Issue:** #97
**Priority:** Post-MVP

## User Story
As an agent, I want to save my frequently used search and filter combinations in the Leads and Properties sections, so that I can recall complex queries instantly without re-entering them each time.

## Dependencies
- #81 — Save Search Criteria (Contacts)
- #63 — View Lead List
- #18 — View Property List

## Notes

Saved searches in Leads and Properties follow the same name-and-recall model as #81 (Contacts). Each section maintains its own separate list of saved searches.

## Acceptance Criteria
1. After applying any search or filter criteria in the Leads section, a "Save Search" button is available; the same applies in the Properties section
2. Clicking "Save Search" prompts for a name; the name must be unique within the Leads saved searches (or Properties saved searches respectively) — a duplicate name shows an error
3. A "Saved Searches" dropdown in the Leads section lists all saved lead searches; selecting one applies its criteria immediately
4. A "Saved Searches" dropdown in the Properties section lists all saved property searches; selecting one applies its criteria immediately
5. A saved search can be renamed or deleted from the dropdown management UI
6. Saved searches persist across application restarts

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/leads.feature` and `tests/bdd/features/properties.feature`.

```gherkin
@story_97
Scenario: User saves a lead filter and recalls it by name
  Given the user has filtered leads to Status "Hot" and source "Referral"
  When the user clicks "Save Search" and names it "Hot Referrals"
  Then "Hot Referrals" appears in the Saved Searches dropdown

@story_97
Scenario: Recalling a saved lead search applies its criteria
  Given the saved search "Hot Referrals" stores Status "Hot" and source "Referral"
  When the user selects "Hot Referrals" from the Saved Searches dropdown
  Then the Leads list is filtered to show only Hot leads from Referral source

@story_97
Scenario: User saves a property filter and recalls it
  Given the user has filtered properties to Status "Active" and type "Condo"
  When the user saves the search as "Active Condos"
  Then "Active Condos" appears in the Properties Saved Searches dropdown
  And selecting it re-applies those filters
```

## Manual Tests
**Story:** [#34 — Save Search Criteria for Leads and Properties](../docs/153-save-search-criteria-for-leads-and-properties.md)

### Saving and recalling a lead search
1. Apply a filter in the Leads section (e.g., Status = Hot, Source = Referral)
2. Click "Save Search" and name it "Hot Referrals"
3. Clear the filters and select "Hot Referrals" from the Saved Searches dropdown
4. Verify the filter is reapplied and the lead list updates accordingly

### Saving and recalling a property search
1. Apply a filter in the Properties section
2. Save it and verify it appears in the Properties Saved Searches dropdown
3. Clear the filters, recall the saved search, and verify it is applied

### Saved searches persist after restart
1. Save a search in Leads and one in Properties
2. Restart the app and verify both saved searches still appear in their respective dropdowns

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/leads.feature`, `tests/bdd/features/properties.feature` |
| BDD step defs | `tests/bdd/test_leads.py`, `tests/bdd/test_properties.py` |
| Unit tests | `tests/unit/leads/test_saved_searches.py`, `tests/unit/properties/test_saved_searches.py` |
| Manual tests | `tests/manual/leads/saved-searches.md`, `tests/manual/properties/saved-searches.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
