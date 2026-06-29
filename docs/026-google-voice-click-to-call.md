# US-026 — Google Voice Click-to-Call

**Capability:** telephony
**Milestone:** v0.5.0 — MVP
**Status:** Not Started

## User Story

As a real estate agent, I want to click a button next to a contact and have Google Voice open ready to dial, so that I never have to manually type a phone number while working through my call list.

## Dependencies

- US-004 — Create master password on first launch
- US-006 — Encrypt database at rest
- US-010 — Add property owner to call list

## Acceptance Criteria

1. During initial setup the user is prompted to enter their Google Voice phone number
2. The number is validated for format and stored in the local database
3. The Google Voice number can be updated at any time from the Settings panel
4. Once configured, a Call button appears next to every contact in the call list
5. Clicking Call opens Google Voice in the default browser with the contact's number pre-filled and ready to dial
6. If Google Voice is not configured, the Call button is replaced with a plain-text phone number the user can dial manually

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/telephony.feature` |
| BDD step defs | `tests/bdd/test_telephony.py` |
| Unit tests | `tests/unit/telephony/test_google_voice_config.py` |
| Manual tests | `tests/manual/telephony/google_voice_setup.md` |

## Definition of Done

- [ ] BDD scenarios pass
- [ ] `ruff`, `mypy --strict` clean
- [ ] Google Voice number configured in the app, Call button clicked, Google Voice opens in browser with number pre-filled and call connects through headset
