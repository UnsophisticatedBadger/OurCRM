Feature: Leads

  @story_95
  Scenario: Report shows total leads, converted leads, and conversion rate for the period
    Given 10 leads were created this month and 3 were converted
    When the user opens the Lead Conversion Report with the current month selected
    Then the report shows: Total leads: 10, Converted: 3, Conversion rate: 30%

  @story_95
  Scenario: Date range filter updates the report
    Given leads and conversions exist across multiple months
    When the user changes the date range to last month
    Then the report recalculates using only leads from last month

  @story_95
  Scenario: Conversion rate is broken down by lead source
    Given converted leads exist from Zillow and Referral sources
    When the user views the Lead Conversion Report
    Then the report shows a separate conversion rate for each source

  @story_95
  Scenario: Average time to convert is calculated correctly
    Given two leads were converted: one after 10 days and one after 20 days
    When the user views the report
    Then the average time to convert shows 15 days

  @story_95
  Scenario: Report data can be exported to CSV
    Given the Lead Conversion Report is displaying data
    When the user clicks "Export to CSV"
    Then a CSV file is saved containing the report data

  @story_95
  Scenario: Report can be exported to PDF
    Given the Lead Conversion Report is displaying data
    When the user clicks "Export to PDF"
    Then a PDF file is saved containing the report including charts
