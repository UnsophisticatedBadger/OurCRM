# US-154: Fuzzy Search / Typo Tolerance

## User Story

**As an** agent  
**I want to** find contacts even when I misspell their name  
**So that** I can quickly find people without worrying about exact spelling

## Priority

**Future:** Post-MVP

**Rationale:** Fuzzy search improves user experience by finding results even with typos, partial matches, or phonetic similarities. This is especially useful when agents remember approximate names or spellings.

## Estimated Effort

**Size:** Medium (M) - 3-5 days

**Breakdown:**
- 2 hours: Research fuzzy search algorithms
- 3 hours: Implement fuzzy matching
- 2 hours: Add typo tolerance
- 2 hours: Configure match thresholds
- 2 hours: Test search quality
- 2 hours: Test on all platforms

## Dependencies

**Depends on:** US-028 (Search Contacts), US-060 (Search Contacts Globally)

**Blocks:** None

## Description

Search should tolerate:
- Typos and misspellings
- Partial matches
- Phonetic similarities
- Common abbreviations

Results should be ranked by match quality, with exact matches first followed by fuzzy matches.

## BDD Scenarios

### Scenario 1: Find contact with typo

Given I have a contact named "Johnson" When I search for "Jonson" Then the contact should still be found With a note that it's a fuzzy match


### Scenario 2: Find contact with partial name

Given I have a contact named "Elizabeth Smith" When I search for "Liz" Then the contact should be found If "Liz" is a known nickname


### Scenario 3: Find contact with phonetic match

Given I have a contact named "Smith" When I search for "Smyth" Then the contact should be found As a phonetic match


### Scenario 4: Exact matches ranked first

Given I search for a term And there are exact and fuzzy matches When results appear Then exact matches should be first Followed by fuzzy matches


### Scenario 5: Configurable match threshold

Given I am in search settings When I adjust fuzzy match threshold Then search should be more or less strict Based on my setting


### Scenario 6: Works across all fields

Given I search with fuzzy matching When results appear Then fuzzy matching should work for:

Names
Emails
Phone numbers
Addresses

### Scenario 7: Highlight differences

Given I have a fuzzy match When I view the result Then the differences should be highlighted So I can see why it matched


### Scenario 8: Disable fuzzy search

Given I prefer exact matches When I disable fuzzy search Then only exact matches should be shown


## Manual Testing Steps

### Test 1: Find contact with typo

1. Create contact "Johnson"
2. Search "Jonson"
3. Verify found
4. Verify marked as fuzzy

### Test 2: Test partial names

1. Create contact with nickname
2. Search nickname
3. Verify found

### Test 3: Test phonetic matches

1. Create contact "Smith"
2. Search "Smyth"
3. Verify found

### Test 4: Test ranking

1. Have exact and fuzzy matches
2. Search
3. Verify exact first

### Test 5: Test threshold

1. Adjust threshold
2. Search
3. Verify results change

### Test 6: Test all fields

1. Test fuzzy on names
2. Test on emails
3. Test on phones
4. Verify all work

### Test 7: Test highlighting

1. Get fuzzy match
2. Verify differences highlighted

### Test 8: Test on all platforms

1. Test Windows, macOS, Linux
2. Verify all work

## Acceptance Criteria

- [ ] Fuzzy search finds typos
- [ ] Phonetic matching works
- [ ] Partial matches supported
- [ ] Exact matches ranked first
- [ ] Match threshold configurable
- [ ] Works across all fields
- [ ] Differences highlighted in results
- [ ] Can disable fuzzy search
- [ ] Search performance remains good
- [ ] Works on Windows, macOS, and Linux
- [ ] False positives minimized