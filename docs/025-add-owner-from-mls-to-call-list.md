# US-025 — Add Property Owner to Call List from MLS

**Capability:** mls
**Milestone:** v0.5.0 — MVP
**Status:** Not Started

## Dependencies

- US-023 — Search HAR MLS listings
- US-024 — View HAR listing details
- US-016 — Manually add contact to call list

## User Story

As a real estate agent, I want to add a property owner directly to my call list from an MLS listing, so that I can go from searching properties to having the owner queued for a call in one action.

## Acceptance Criteria

1. A property listing detail view has an "Add Owner to Call List" button
2. Tapping the button opens a pre-filled form with the owner's name and property address pulled from the MLS listing
3. The user must enter or confirm the owner's phone number before saving (MLS data does not include phone numbers)
4. Saving adds the owner to the call list and returns to the listing detail view
5. If the phone number already exists in the call list, a warning is shown before allowing a duplicate
6. The added contact is marked as sourced from MLS so the property link is preserved

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/mls.feature` |
| BDD step defs | `tests/bdd/test_mls.py` |
| Unit tests | `tests/unit/mls/test_add_owner_from_mls.py` |
| Manual tests | `tests/manual/mls/add_owner_from_mls.md` |

## Definition of Done

- [ ] BDD scenarios pass
- [ ] `ruff`, `mypy --strict` clean
- [ ] MLS listing found, owner added to call list with phone number entered, contact appears in call list linked to the MLS property
