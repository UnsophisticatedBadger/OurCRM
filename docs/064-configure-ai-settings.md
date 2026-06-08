# US-064: Configure AI Settings

## User Story

**As an** agent  
**I want to** configure my AI provider and settings  
**So that** I can use AI features for lead qualification

## Priority

**MVP:** Must Have

**Rationale:** AI features are part of MVP (lead qualification). Users need to be able to configure which AI provider to use (local Ollama or cloud OpenAI), enter API keys, and adjust AI behavior. Without configuration, AI features can't be used.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design AI settings UI
- 2 hours: Create provider selection (Ollama/OpenAI)
- 1 hour: Implement API key entry for cloud providers
- 1 hour: Add model selection
- 1 hour: Test connection to AI provider
- 1 hour: Add settings validation
- 1 hour: Test AI configuration
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-017 (Open Settings Window), US-018 (Configure General Settings)

**Blocks:** US-065 (Qualify Lead with AI), US-066 (View AI Qualification Results)

## Description

Users should be able to configure AI settings including which provider to use (local Ollama for privacy/offline use, or cloud OpenAI for better quality), API keys for cloud providers, and model selection. The settings should be in a dedicated AI section in the Settings window.

The configuration should include a "Test Connection" button to verify the setup works before using AI features. Settings should be validated and clear error messages should be shown if configuration is incorrect.

## BDD Scenarios

### Scenario 1: Open AI settings

```
Given the Settings window is open
When I click on the "AI" category
Then I should see AI configuration options:
  - Provider selection (Ollama/OpenAI/None)
  - API key field (for cloud providers)
  - Model selection
  - Test Connection button
```

### Scenario 2: Configure local AI (Ollama)

```
Given I am in AI settings
When I select "Ollama" as the provider
Then I should see:
  - Ollama host (default: localhost)
  - Model selection (dropdown of available models)
  - Test Connection button
  And no API key is required
```

### Scenario 3: Configure cloud AI (OpenAI)

```
Given I am in AI settings
When I select "OpenAI" as the provider
Then I should see:
  - API key field (password field)
  - Model selection (gpt-4o-mini, gpt-4o, etc.)
  - Test Connection button
```

### Scenario 4: Enter API key

```
Given I am configuring OpenAI
When I enter my API key
  And I click "Save"
Then the API key should be stored securely in the OS keyring
  And not displayed in plain text after saving
```

### Scenario 5: Test AI connection

```
Given I have configured an AI provider
When I click "Test Connection"
Then the system should attempt to connect
  And show a success message if it works
  Or an error message if it fails
```

### Scenario 6: Select AI model

```
Given I am configuring Ollama
When I click the model dropdown
Then I should see available models
  And I can select one
  And the selection is saved
```

### Scenario 7: Disable AI

```
Given I am in AI settings
When I select "None" as the provider
Then AI features should be disabled
  And I should not see AI options in the UI
  Or they should be grayed out
```

### Scenario 8: Settings persist across restarts

```
Given I have configured AI settings
When I close the application
  And I restart the application
  And I open AI settings
Then my configuration should be saved
  And the API key should be loaded from the keyring
```

## Manual Testing Steps

### Test 1: Open AI settings

1. Open Settings
2. Click on "AI" category
3. Verify all expected options are present
4. Check that the UI is clear

### Test 2: Configure Ollama

1. Select "Ollama" as the provider
2. Verify the host field is shown
3. Verify model selection is available
4. Select a model
5. Click "Test Connection"
6. Verify it connects successfully

### Test 3: Configure OpenAI

1. Select "OpenAI" as the provider
2. Enter an API key
3. Select a model
4. Click "Test Connection"
5. Verify it works
6. Save the settings
7. Verify the API key is not shown in plain text

### Test 4: Test connection

1. Configure an AI provider
2. Click "Test Connection"
3. Verify success message
4. Try with invalid configuration
5. Verify error message
6. Try with no internet (for cloud)
7. Verify appropriate error

### Test 5: Test model selection

1. Open the model dropdown
2. Verify available models are listed
3. Select a model
4. Save the settings
5. Verify the selection is saved

### Test 6: Test disabling AI

1. Select "None" as the provider
2. Save the settings
3. Verify AI features are disabled in the UI
4. Test that AI actions don't appear or are grayed out

### Test 7: Test persistence

1. Configure AI settings
2. Save and close the application
3. Restart the application
4. Open AI settings
5. Verify everything is saved
6. Verify API key is loaded from keyring

### Test 8: Test on all platforms

1. Test AI settings on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] AI settings category is accessible
- [ ] Provider selection (Ollama/OpenAI/None) works
- [ ] API keys are stored securely in OS keyring
- [ ] API keys are not displayed in plain text
- [ ] Model selection is available
- [ ] Test Connection button works
- [ ] Connection errors are clearly displayed
- [ ] Settings persist across restarts
- [ ] AI can be disabled
- [ ] Works on Windows, macOS, and Linux
- [ ] Configuration is validated
- [ ] Clear error messages for invalid configuration
- [ ] UI is intuitive and well-organized