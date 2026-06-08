# US-152: AI Document Analysis

## User Story

**As an** agent  
**I want to** use AI to analyze uploaded documents  
**So that** I can quickly extract key information from contracts and disclosures

## Priority

**Future:** Post-MVP

**Rationale:** Real estate documents are lengthy and complex. AI analysis can extract key dates, amounts, contingencies, and obligations, helping agents quickly understand document contents without reading every page.

## Estimated Effort

**Size:** Large (L) - 5-8 days

**Breakdown:**
- 3 hours: Design document analysis UI
- 4 hours: Implement AI document processing
- 3 hours: Add OCR for scanned documents
- 3 hours: Extract key information
- 3 hours: Display analysis results
- 3 hours: Test with various document types
- 3 hours: Test on all platforms

## Dependencies

**Depends on:** US-064 (Configure AI Settings), US-090 (Upload Document to Contact)

**Blocks:** None

## Description

Users should be able to upload a document and have AI analyze it to extract:
- Key dates (closing, contingencies, deadlines)
- Financial amounts (price, earnest money, fees)
- Parties involved
- Key terms and contingencies
- Action items and obligations

The analysis is displayed in a structured format alongside the original document.

## BDD Scenarios

### Scenario 1: Analyze uploaded document

Given I have uploaded a document And AI is configured When I click "Analyze with AI" Then the document should be analyzed And key information extracted


### Scenario 2: Extract key dates

Given I analyze a contract When the analysis completes Then key dates should be extracted:

Closing date
Contingency deadlines
Inspection periods

### Scenario 3: Extract financial amounts

Given I analyze a contract When the analysis completes Then financial amounts should be extracted:

Purchase price
Earnest money
Fees and costs

### Scenario 4: Identify parties

Given I analyze a document When the analysis completes Then parties should be identified:

Buyer
Seller
Agents
Lenders

### Scenario 5: Extract contingencies

Given I analyze a contract When the analysis completes Then contingencies should be listed:

Financing
Inspection
Appraisal
Other conditions

### Scenario 6: Handle scanned documents (OCR)

Given I upload a scanned document When I analyze it Then OCR should extract the text And analysis should proceed


### Scenario 7: Analysis confidence score

Given I analyze a document When the analysis completes Then a confidence score should be shown So I know how reliable the extraction is


### Scenario 8: Export analysis

Given I have analyzed a document When I click "Export Analysis" Then the extracted information should be exportable As structured data


## Manual Testing Steps

### Test 1: Analyze uploaded document

1. Upload a contract
2. Click "Analyze with AI"
3. Wait for analysis
4. Verify results

### Test 2: Test date extraction

1. Analyze document with dates
2. Verify dates are extracted
3. Verify they're accurate

### Test 3: Test financial extraction

1. Analyze document with amounts
2. Verify amounts extracted
3. Verify accuracy

### Test 4: Test party identification

1. Analyze multi-party document
2. Verify parties identified
3. Verify roles are correct

### Test 5: Test contingency extraction

1. Analyze contract with contingencies
2. Verify all are listed
3. Verify deadlines included

### Test 6: Test OCR

1. Upload scanned PDF
2. Analyze
3. Verify text extracted
4. Verify analysis works

### Test 7: Test confidence score

1. Analyze clear document
2. Verify high confidence
3. Analyze poor quality
4. Verify lower confidence shown

### Test 8: Test on all platforms

1. Test Windows, macOS, Linux
2. Verify all work

## Acceptance Criteria

- [ ] "Analyze with AI" option for documents
- [ ] Key dates extracted
- [ ] Financial amounts extracted
- [ ] Parties identified
- [ ] Contingencies listed
- [ ] Action items identified
- [ ] OCR works for scanned documents
- [ ] Confidence score displayed
- [ ] Can export analysis
- [ ] Works with contracts, disclosures, addenda
- [ ] Works on Windows, macOS, and Linux
- [ ] Analysis completes in under 30 seconds