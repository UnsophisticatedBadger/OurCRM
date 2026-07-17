# 102 - Twilio Calling Integration

**Capability:** telephony
**Milestone:** Production
**Status:** Not Started
**GitHub Issue:** #102

## User Story

As a real estate agent, I want to configure Twilio as a calling option so that I can make calls natively through the app with a headset instead of switching to a browser, and choose between Twilio and Google Voice depending on the situation.

## Dependencies

- #54 — Google Voice Click-to-Call
- #3 — Create master password on first launch
- #5 — Encrypt database at rest

## Acceptance Criteria

1. The user can enter their Twilio Account SID, Auth Token, and Twilio phone number in the Settings panel
2. The app validates the credentials against the Twilio API before saving — a failed validation shows a plain-language error with a corrective step
3. Credentials are stored encrypted in the local database, never in plain text
4. When only Twilio is configured, clicking Call initiates a call through Twilio via the connected headset
5. When only Google Voice is configured, clicking Call opens Google Voice in the browser
6. When both are configured, a dropdown on the Call button lets the user choose which interface to use
7. The user can set a preferred calling interface in Settings to skip the per-call dropdown

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/telephony.feature` |
| BDD step defs | `tests/bdd/test_telephony.py` |
| Unit tests | `tests/unit/telephony/test_twilio_config.py` |
| Manual tests | `tests/manual/telephony/twilio_setup.md` |

## Definition of Done

- [ ] BDD scenarios pass
- [ ] `ruff`, `mypy --strict` clean
- [ ] Twilio credentials configured in a real account, test call completed through the app using a headset
- [ ] Both Google Voice and Twilio configured simultaneously; per-call selection verified
- [ ] Wiki documentation written, or marked N/A with a reason
