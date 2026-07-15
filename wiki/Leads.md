# Leads

The Leads section helps you track prospects from first contact through conversion. OurCRM works fully offline.

**Current limitation:** Lead data for the conversion report is held in an in-memory repository for this release. Leads exist only for the current app session and are lost when OurCRM restarts. Persistent lead storage and the lead pipeline UI depend on [#67 — Mark Lead as Converted](https://github.com/UnsophisticatedBadger/OurCRM/issues/67) and [#69 — Track Conversion Rate](https://github.com/UnsophisticatedBadger/OurCRM/issues/69). Until those stories land, the **Pipeline** tab shows a placeholder and the report starts empty on a fresh launch.

## Lead Conversion Report

Open **Leads → Conversion Report** to measure how effectively you turn new leads into clients.

### What the report shows

For the selected date range, the report displays:

- **Total leads** — leads whose *creation date* falls in the period
- **Converted** — leads whose *conversion date* falls in the period (even if they were created earlier)
- **Conversion rate** — converted ÷ total when at least one lead was created in the period; shows **—** when conversions exist but no new leads were created in that period (the rate is undefined, not zero)
- **Average days to convert** — average time from creation to conversion for leads converted in the period

Below the summary, a **Conversion by source** table breaks down totals and rates per source (Zillow, Referral, Walk-in, Other). A **Conversion rate trend** chart plots weekly or monthly buckets across the period.

### Filtering the period

Use the **Period** preset (**This Month**, **Last Month**, or **Custom**) and adjust the **From / To** dates when Custom is selected. The report recalculates automatically when the range changes.

### Comparing periods

Check **Compare to previous period** to show the immediately preceding range of equal length side-by-side with the current period.

### Exporting

Use **Export to CSV** for spreadsheet analysis, or **Export to PDF** for a printable report including summary text and trend charts.
