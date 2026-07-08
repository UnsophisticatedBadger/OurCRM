# 32 - Additional Language Support

**Capability:** shell
**Milestone:** Secure Shell
**Status:** Not Done
**GitHub Issue:** #32
**Priority:** Post-MVP

## User Story
As a non-English-speaking agent, I want to switch OurCRM to my preferred language, so that I can work without language barriers.

## Dependencies
- #12 — Configure General Settings

## Acceptance Criteria
1. An i18n framework is in place that externalises all UI strings into locale files; adding a new language requires only a new locale file, no code changes
2. Settings → General → Language includes a language selector; English is the default
3. Spanish is provided as the first additional locale
4. Selecting and saving a language immediately applies the translation to all UI text: labels, buttons, menus, dialogs, error messages, and notifications
5. Dates are formatted according to the selected locale (e.g. DD/MM/YYYY for es-ES)
6. Numbers are formatted according to the selected locale (e.g. period as thousands separator and comma as decimal for es-ES)
7. Any string that lacks a translation for the selected locale falls back to the English string rather than showing blank or a key
8. The selected language persists across app restarts

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/shell.feature`.

```gherkin
@story_32
Scenario: User switches to Spanish and the UI is displayed in Spanish
  Given the user opens Settings → General → Language
  When the user selects "Español" and saves
  Then all visible UI labels and buttons are displayed in Spanish

@story_32
Scenario: Date format matches the selected locale
  Given the user has selected Spanish (Spain) as the language
  When a date is displayed in the app
  Then it uses the DD/MM/YYYY format

@story_32
Scenario: Missing translation falls back to English
  Given a UI string has no Spanish translation
  When the app renders that string with Spanish selected
  Then the English string is shown instead of a blank or raw key

@story_32
Scenario: Language persists after app restart
  Given the user has saved Spanish as the language
  When the user restarts the app
  Then the UI is still displayed in Spanish

@story_32
Scenario: Switching back to English restores English text
  Given Spanish is the active language
  When the user selects "English" and saves
  Then all UI text is displayed in English
```

## Manual Tests
**Story:** [#171 — Additional Language Support](../docs/112-additional-language-translations.md)

### Switching to Spanish translates the full UI
1. Open Settings → General → Language, select "Español," and save
2. Navigate to the Contacts, Leads, and Settings screens
3. Verify all labels, buttons, and menu items appear in Spanish

### Date format follows the selected locale
1. With Spanish selected, view a contact's last-contacted date
2. Verify the date is formatted as DD/MM/YYYY

### Missing translations fall back to English
1. With Spanish selected, locate any untranslated string (if any)
2. Verify the English text is shown, not a blank field or raw key

### Language persists after restart
1. Save Spanish as the language and restart the app
2. Verify the UI is still in Spanish

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_language_support.py` |
| Manual tests | `tests/manual/shell/language-support.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
