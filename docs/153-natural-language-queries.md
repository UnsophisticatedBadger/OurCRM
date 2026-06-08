# US-153: Natural Language Queries

## User Story

**As an** agent  
**I want to** search my data using natural language  
**So that** I can find information without knowing exact field names or filters

## Priority

**Future:** Post-MVP

**Rationale:** Natural language search makes the CRM more accessible. Instead of learning filter options, agents can ask questions like "Show me hot leads from last month" and get relevant results.

## Estimated Effort

**Size:** Large (L) - 5-8 days

**Breakdown:**
- 3 hours: Design natural language search UI
- 4 hours: Implement AI query parsing
- 3 hours: Map queries to database filters
- 3 hours: Handle ambiguous queries
- 3 hours: Test query accuracy
- 3 hours: Test on all platforms

## Dependencies

**Depends on:** US-064 (Configure AI Settings), US-060 (Search Contacts Globally)

**Blocks:** None

## Description

Users should be able to search using natural language queries like:
- "Show me hot leads from Zillow"
- "Find contacts I emailed last week"
- "Properties sold in the last 30 days"
- "Tasks due this week that are overdue"

The AI parses the query and applies appropriate filters across the database.

## BDD Scenarios

### Scenario 1: Search with natural language

Given I am in the search interface And AI is configured When I type "Show me hot leads from Zillow" And I press Enter Then hot leads from Zillow should be shown


### Scenario 2: Search by date range

Given I am searching When I type "Contacts added last month" Then contacts from last month should be shown


### Scenario 3: Search by activity

Given I am searching When I type "Leads I emailed this week" Then leads emailed this week should be shown


### Scenario 4: Search by status

Given I am searching When I type "Pending properties" Then properties with pending status should be shown


### Scenario 5: Handle ambiguous queries

Given I type an ambiguous query When the AI processes it Then it should ask for clarification Or make best guess and show results


### Scenario 6: Search across all sections

Given I search with natural language When results appear Then they should be grouped by section:

Contacts
Leads
Properties
Transactions

### Scenario 7: Refine search

Given I have search results When I refine my query Then results should update With the new criteria


### Scenario 8: Save natural language search

Given I have a useful natural language query When I save it Then I can reuse it later As a saved search


## Manual Testing Steps

### Test 1: Search with natural language

1. Go to search
2. Type "hot leads from Zillow"
3. Press Enter
4. Verify correct results

### Test 2: Test date queries

1. Search "last month"
2. Verify date range applied
3. Test "this week"
4. Verify correct

### Test 3: Test activity queries

1. Search "emailed this week"
2. Verify email activity filtered
3. Test other activities

### Test 4: Test status queries

1. Search "pending properties"
2. Verify status filter applied

### Test 5: Test ambiguous queries

1. Type vague query
2. Verify clarification or best guess

### Test 6: Test cross-section search

1. Search broadly
2. Verify results from all sections
3. Verify grouped correctly

### Test 7: Test refine

1. Get results
2. Refine query
3. Verify results update

### Test 8: Test on all platforms

1. Test Windows, macOS, Linux
2. Verify all work

## Acceptance Criteria

- [ ] Natural language search input available
- [ ] AI parses queries correctly
- [ ] Date ranges understood
- [ ] Activity queries work
- [ ] Status queries work
- [ ] Ambiguous queries handled gracefully
- [ ] Results grouped by section
- [ ] Can refine searches
- [ ] Can save natural language searches
- [ ] Works with Ollama and OpenAI
- [ ] Works on Windows, macOS, and Linux
- [ ] Query processing completes in under 5 seconds