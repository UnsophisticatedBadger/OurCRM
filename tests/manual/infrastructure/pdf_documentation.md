# PDF Documentation — Manual Tests

**Story:** [US-194 — PDF Manual Auto-generation](../../../docs/194-pdf-documentation.md)

## PDF is generated and attached to the release

1. Push a `feat:` commit to main to trigger a release
2. Navigate to the GitHub Release page
3. Verify `ourcrm-<version>-manual.pdf` is listed as a release asset
4. Download the PDF and open it
5. Verify it contains a cover page showing the version number and release date

## PDF generation failure blocks the release

1. Introduce an error in the pandoc step and push a `feat:` commit
2. Verify the PDF generation step fails
3. Verify no GitHub Release is published
4. Revert the error

## PDF content is complete and readable

1. Download the PDF from the release
2. Verify all MVP capability sections are present (Contacts, Leads, MLS Integration)
3. Verify screenshots and diagrams render correctly
4. Verify the document is navigable with a table of contents
