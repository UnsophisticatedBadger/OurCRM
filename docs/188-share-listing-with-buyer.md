# US-188 — Share MLS Listing with Buyer

**Capability:** email
**Status:** Not Done
**Priority:** Post-MVP

## User Story
As an agent, I want to email an MLS listing's details to a contact from within the listing detail view, so that I can share properties with buyers without copying and pasting information manually.

## Dependencies
- US-088 — View MLS Listing Details
- US-079 — Send Email to Contact

## Acceptance Criteria
1. A "Share with Buyer" button appears on the MLS listing detail view
2. Clicking it opens the email compose form with: a recipient picker pre-populated from the agent's contacts, the subject pre-filled as "Property at [address]", and the email body pre-filled with: address, list price, beds/baths/sqft, and a link or note to contact the agent for more details
3. The user can edit the recipient, subject, and body before sending
4. Sending follows the same flow as US-079 (via configured email provider)

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/email.feature`.

```gherkin
@us210
Scenario: Share with Buyer opens the compose form pre-filled with listing details
  Given an MLS listing detail is open for "456 Oak Ave" with list price $450,000
  When the user clicks "Share with Buyer"
  Then the email compose form opens with subject "Property at 456 Oak Ave"
  And the body contains the address, list price, and property details

@us210
Scenario: User can edit the pre-filled compose form before sending
  Given the compose form is open from Share with Buyer
  When the user changes the subject and adds a personal message to the body
  Then the edited subject and message are used when the email is sent
```

## Manual Tests
**Story:** [US-177 — Share MLS Listing with Buyer](../docs/177-share-listing-with-buyer.md)

### Compose form is pre-filled with listing details
1. Open an MLS listing detail and click "Share with Buyer"
2. Verify the subject contains the address and the body contains price and property details
3. Select a recipient contact and verify the form is ready to send

### Pre-filled content can be edited
1. Change the subject and add a personal message
2. Send the email and verify the recipient receives the edited version

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/email.feature` |
| BDD step defs | `tests/bdd/test_email.py` |
| Unit tests | `tests/unit/email/test_share_listing.py` |
| Manual tests | `tests/manual/email/share-listing-with-buyer.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
