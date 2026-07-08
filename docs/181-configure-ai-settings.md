# 181 - Configure AI Settings

**Capability:** AI Features
**Milestone:** Post-Production
**Status:** Not Done
**GitHub Issue:** #181

## User Story

As a real estate agent, I want to configure my AI provider and model in the Settings window, so that I can enable AI features such as lead qualification.

## Dependencies

- #11 — Open Settings Window
- #12 — Configure General Settings

## Notes

**Third-party testability:** The "Test Connection" BDD scenario requires a live AI provider to be reachable and cannot run reliably in CI. Tag those scenarios `@live_ai` and skip them by default. Cover the connection-check logic with a unit test that stubs the provider's HTTP response instead.

## Acceptance Criteria

1. An "AI" section is accessible within the Settings window
2. The provider can be set to Ollama (local/offline), OpenAI (cloud), or None (disabled)
3. When Ollama is selected, settings show: host URL (default `localhost:11434`) and a model selection dropdown
4. When OpenAI is selected, settings show: a masked API key field and a model selection dropdown
5. The OpenAI API key is stored in the OS keyring and is never written to the application database or config file; after saving, the field displays a placeholder (e.g., "••••••••") rather than the key
6. A "Test Connection" button verifies the configured provider is reachable and displays either a success confirmation or a clear error message describing the failure
7. Selecting None disables AI features throughout the application (AI-related actions are hidden or disabled)
8. AI settings persist correctly across application restarts, including loading the API key from the OS keyring

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/ai.feature`.

```gherkin
@story_181
Scenario: User opens Settings and finds the AI section
  Given the Settings window is open
  When the user selects the "AI" category
  Then provider options Ollama, OpenAI, and None are shown

@story_181
Scenario: User selects OpenAI, enters an API key, and saves
  Given the AI settings page is open
  When the user selects "OpenAI" as the provider
  And enters a valid API key "sk-test-1234"
  And clicks Save
  Then the API key is stored in the OS keyring
  And the key field displays a placeholder instead of the key text

@story_181
Scenario: User clicks Test Connection with valid Ollama configuration and sees success
  Given the AI settings page has Ollama selected with host "localhost:11434"
  And an Ollama instance is running at that address
  When the user clicks "Test Connection"
  Then a success message is shown

@story_181
Scenario: User clicks Test Connection with an invalid API key and sees an error
  Given the AI settings page has OpenAI selected with an invalid API key
  When the user clicks "Test Connection"
  Then an error message is shown describing the failure

@story_181
Scenario: User selects None and AI features are disabled
  Given the AI settings page is open
  When the user selects "None" as the provider and saves
  Then AI-related actions are hidden or disabled throughout the application

@story_181
Scenario: AI settings persist after the application restarts
  Given the user configured OpenAI with a valid API key and saved
  When the user restarts the application and opens AI settings
  Then the provider is still set to "OpenAI"
  And the API key field shows a placeholder indicating a key is stored
```

## Manual Tests

**Story:** [#135 — Configure AI Settings](../docs/146-configure-ai-settings.md)

### AI section is accessible in Settings
1. Open the Settings window
2. Click the "AI" category
3. Confirm provider selection (Ollama / OpenAI / None), a model selector, and a Test Connection button are all visible

### Configuring Ollama
1. Select "Ollama" as the provider
2. Confirm the host URL field appears, pre-filled with `localhost:11434`
3. Confirm the model selector appears (populated with models returned by Ollama if running)
4. Click "Test Connection"
5. Confirm either a success message (if Ollama is running) or a clear error message (if not)

### Configuring OpenAI
1. Select "OpenAI" as the provider
2. Enter a test API key in the key field
3. Confirm the field masks the key as you type (shows bullets/dots)
4. Click Save
5. Reopen AI settings and confirm the key field shows a placeholder, not the raw key
6. Confirm the key is stored in the OS keyring (check keyring tool for your OS)

### Test Connection — success and failure
1. With Ollama running locally, configure Ollama and click Test Connection — confirm success
2. Change the host to an unreachable address and click Test Connection — confirm a clear error
3. With OpenAI selected and a valid API key, click Test Connection — confirm success
4. Change the API key to an invalid value and click Test Connection — confirm a clear auth error

### Disabling AI with None
1. Select "None" as the provider and save
2. Navigate to any feature that uses AI (e.g., lead qualification)
3. Confirm AI actions are hidden or disabled
4. Re-enable Ollama and confirm AI actions return

### Settings persist across restarts
1. Configure OpenAI with a valid API key and save
2. Close and reopen the application
3. Open AI settings and confirm the provider is still "OpenAI" and the key placeholder is shown
4. Click Test Connection and confirm the stored key is used correctly

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/ai.feature` |
| BDD step defs | `tests/bdd/test_ai.py` |
| Unit tests | `tests/unit/ai/test_ai_settings.py` |
| Manual tests | `tests/manual/ai/ai_settings.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
