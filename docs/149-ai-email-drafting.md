# US-149: AI Email Drafting

## User Story

**As an** agent  
**I want to** use AI to draft emails for me  
**So that** I can send professional emails faster without writing from scratch

## Priority

**Future:** Post-MVP

**Rationale:** AI email drafting saves significant time on routine communications. Agents can generate first drafts for common scenarios (follow-ups, introductions, property announcements) and then personalize as needed.

## Estimated Effort

**Size:** Medium (M) - 3-5 days

**Breakdown:**
- 2 hours: Design AI email draft UI
- 3 hours: Implement AI prompt engineering for emails
- 2 hours: Add email draft generation endpoint
- 2 hours: Integrate with email compose form
- 2 hours: Test with various email types
- 2 hours: Test on all platforms

## Dependencies

**Depends on:** US-064 (Configure AI Settings), US-070 (Send Email to Contact)

**Blocks:** None

## Description

Users should be able to generate email drafts using AI. When composing an email, they can click "Draft with AI" and provide:
- Email purpose (follow-up, introduction, listing announcement, etc.)
- Key points to include
- Tone (professional, friendly, urgent, etc.)

The AI generates a complete draft that the user can edit before sending.

## BDD Scenarios

### Scenario 1: Generate email draft with AI

Given I am composing an email And AI is configured When I click "Draft with AI" And I enter the email purpose and key points And I click "Generate" Then an email draft should be generated And I can edit it before sending


### Scenario 2: Choose email tone

Given I am generating an email draft When I select a tone (professional, friendly, urgent) Then the generated email should match that tone


### Scenario 3: Regenerate draft

Given I have generated a draft When I'm not satisfied with it And I click "Regenerate" Then a new draft should be generated With different wording


### Scenario 4: Insert draft into compose form

Given an email draft has been generated When I click "Use This Draft" Then the draft should be inserted into the email compose form And I can edit it further


### Scenario 5: AI uses contact context

Given I am emailing a specific contact When I generate a draft Then the AI should use contact information Like name, recent interactions, preferences


### Scenario 6: Save draft templates

Given I have generated and edited a good draft When I save it as a template Then I can reuse it for future emails


### Scenario 7: AI suggests subject line

Given I am generating an email draft When the AI generates the draft Then it should also suggest a subject line That matches the email content


### Scenario 8: Works offline (if local AI)

Given I am using Ollama (local AI) When I generate an email draft Then it should work without internet


## Manual Testing Steps

### Test 1: Generate email draft

1. Open email compose
2. Click "Draft with AI"
3. Enter purpose and points
4. Generate draft
5. Verify draft is created

### Test 2: Test tone selection

1. Generate with professional tone
2. Generate with friendly tone
3. Verify tones are different

### Test 3: Test regenerate

1. Generate a draft
2. Click regenerate
3. Verify new wording

### Test 4: Test insert into compose

1. Generate draft
2. Click "Use This Draft"
3. Verify it's in the compose form

### Test 5: Test contact context

1. Compose email to specific contact
2. Generate draft
3. Verify contact info is used

### Test 6: Test save as template

1. Generate and edit draft
2. Save as template
3. Verify it's reusable

### Test 7: Test subject line

1. Generate draft
2. Verify subject line is suggested
3. Verify it matches content

### Test 8: Test on all platforms

1. Test Windows, macOS, Linux
2. Verify all work

## Acceptance Criteria

- [ ] "Draft with AI" button in email compose
- [ ] Can specify email purpose
- [ ] Can specify key points to include
- [ ] Can choose tone (professional, friendly, urgent)
- [ ] AI generates complete email draft
- [ ] AI suggests subject line
- [ ] Can regenerate draft
- [ ] Can insert draft into compose form
- [ ] Can edit draft before sending
- [ ] Uses contact context when available
- [ ] Can save drafts as templates
- [ ] Works with Ollama and OpenAI
- [ ] Works on Windows, macOS, and Linux