# US-167: Database Indexing for Performance

## User Story

**As a** user  
**I want to** the database to be optimized for fast queries  
**So that** the application remains responsive even with lots of data

## Priority

**Future:** Post-MVP

**Rationale:** As data grows, database performance can degrade. Proper indexing ensures searches, filters, and loads remain fast regardless of data volume.

## Estimated Effort

**Size:** Medium (M) - 3-5 days

**Breakdown:**
- 3 hours: Analyze query patterns
- 4 hours: Design database indexes
- 3 hours: Implement index creation
- 2 hours: Test query performance
- 2 hours: Test with large datasets
- 2 hours: Test on all platforms

## Dependencies

**Depends on:** US-014 (Create Encrypted Database)

**Blocks:** None

## Description

Database indexes should be created for:
- Contact name, email, phone
- Lead status, source, created date
- Property address, status, price
- Transaction dates, status
- Task due dates, priority
- All frequently searched fields

Indexes should be created automatically on first run and maintained through migrations.

## BDD Scenarios

### Scenario 1: Indexes created automatically

Given I start OurCRM for the first time When the database is initialized Then indexes should be created automatically


### Scenario 2: Search is fast with indexes

Given I have 10,000 contacts When I search for a contact Then results should appear in under 500ms


### Scenario 3: Filter is fast with indexes

Given I have 10,000 leads When I filter by status Then results should appear in under 500ms


### Scenario 4: Indexes maintained through migrations

Given I have a database migration When I run the migration Then indexes should be maintained Or recreated appropriately


### Scenario 5: Index on frequently searched fields

Given I search certain fields often When I check the database Then those fields should be indexed


### Scenario 6: No duplicate indexes

Given indexes are created When I check the database Then there should be no duplicate indexes Wasting space


### Scenario 7: Indexes don't slow writes

Given I have indexes When I create new records Then performance should still be good Not significantly slower


### Scenario 8: Can rebuild indexes

Given indexes exist When I click "Rebuild Indexes" Then indexes should be rebuilt For optimal performance


## Manual Testing Steps

### Test 1: Test index creation

1. Start fresh database
2. Check indexes created
3. Verify appropriate fields

### Test 2: Test search performance

1. Create 10,000 contacts
2. Search
3. Verify under 500ms

### Test 3: Test filter performance

1. Create 10,000 leads
2. Filter
3. Verify under 500ms

### Test 4: Test migrations

1. Run migration
2. Verify indexes maintained

### Test 5: Test indexed fields

1. Check which fields indexed
2. Verify frequently searched included

### Test 6: Test no duplicates

1. Check indexes
2. Verify no duplicates

### Test 7: Test write performance

1. Create many records
2. Verify not significantly slower

### Test 8: Test on all platforms

1. Test Windows, macOS, Linux
2. Verify all work

## Acceptance Criteria

- [ ] Indexes created automatically
- [ ] Search is fast (under 500ms with 10K records)
- [ ] Filter is fast
- [ ] Indexes maintained through migrations
- [ ] Frequently searched fields indexed
- [ ] No duplicate indexes
- [ ] Write performance not significantly impacted
- [ ] Can rebuild indexes
- [ ] Indexes documented
- [ ] Works on Windows, macOS, and Linux