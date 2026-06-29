# US-196 — Analyse Document with AI

**Capability:** ai
**Status:** Not Done
**GitHub Issue:** #200
**Priority:** Post-MVP

## User Story
As an agent, I want to use AI to analyse uploaded contracts and disclosures, so that I can quickly extract key dates, amounts, parties, and obligations without reading every page.

## Dependencies
- #135 — Configure AI Settings
- #54 — Upload Document to Contact

## Acceptance Criteria
1. An "Analyse with AI" button appears on each document entry in the contact's document list
2. Clicking it sends the document to the configured AI provider and returns a structured extraction of:
   - Key dates (closing date, contingency deadlines, inspection periods)
   - Financial amounts (purchase price, earnest money, fees)
   - Parties involved (buyer, seller, agents, lenders)
   - Contingencies and conditions
   - Action items and obligations
3. Results are displayed in a structured panel alongside the document view
4. A confidence indicator is shown for each extracted field (High / Medium / Low)
5. For scanned PDFs, OCR is applied before analysis to extract the text
6. Individual extracted items can be copied to the clipboard
7. If AI is not configured, the "Analyse with AI" button is disabled with a tooltip directing the user to Settings → AI

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/ai.feature`.

```gherkin
@us152
Scenario: User analyses a document and sees structured extraction results
  Given AI is configured
  And a PDF document is uploaded to a contact
  When the user clicks "Analyse with AI"
  Then a structured panel shows extracted dates, amounts, parties, and contingencies

@us152
Scenario: Confidence indicator is shown for each extracted field
  Given an analysis has completed
  When the user views the extraction panel
  Then each field shows a High, Medium, or Low confidence indicator

@us152
Scenario: Scanned PDF is processed via OCR before analysis
  Given a scanned PDF is uploaded
  When the user clicks "Analyse with AI"
  Then OCR is applied and the analysis proceeds on the extracted text

@us152
Scenario: "Analyse with AI" is disabled when AI is not configured
  Given AI is not configured
  When the user views the document list
  Then the "Analyse with AI" button is disabled
  And hovering shows a tooltip directing the user to Settings → AI

@us152 @live_ai
Scenario: Real AI provider extracts key dates and amounts from a contract PDF
  Given a real AI provider is configured
  And a contract PDF with known dates and amounts is uploaded
  When the user clicks "Analyse with AI"
  Then the extraction panel shows non-empty dates and financial amounts
```

## Manual Tests
**Story:** [US-185 — Analyse Document with AI](../docs/185-ai-document-analysis.md)

### User analyses a contract and sees structured results
1. Upload a contract PDF to a contact
2. Click "Analyse with AI" on the document entry
3. Verify a panel appears showing extracted dates, amounts, parties, and contingencies

### Confidence indicators are shown for each field
1. After analysis, review the extraction panel
2. Verify each field shows High, Medium, or Low confidence

### Scanned PDF is processed via OCR
1. Upload a scanned (image-only) PDF
2. Click "Analyse with AI" and verify it processes successfully
3. Verify extracted content reflects the scanned text

### "Analyse with AI" is disabled when AI is not configured
1. Remove AI configuration from Settings → AI
2. View the document list and verify the button is disabled with a tooltip

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/ai.feature` |
| BDD step defs | `tests/bdd/test_ai.py` |
| Unit tests | `tests/unit/ai/test_document_analysis.py` |
| Manual tests | `tests/manual/ai/document-analysis.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
