# 167 - PDF Manual Auto-generation

**Capability:** infrastructure
**Milestone:** Production
**Status:** Not Started
**GitHub Issue:** #167

## User Story

As a user, I want a PDF manual bundled with every release, so I can reference the documentation offline without needing a browser or a GitHub account.

## Dependencies

- #2 — Automated Release Pipeline
- Wiki documentation must be written for all MVP capabilities before this story is worked

## Acceptance Criteria

1. The release workflow pulls the GitHub Wiki and converts it to a single PDF using pandoc
2. The PDF is named `ourcrm-<version>-manual.pdf` (e.g. `ourcrm-v1.0.0-manual.pdf`)
3. The PDF is attached to the GitHub Release alongside the platform executables
4. A PDF generation failure prevents the release from being published
5. The PDF includes a cover page with the version number and release date

## Test Locations

| Artifact | Path |
|----------|------|
| Manual tests | `tests/manual/infrastructure/pdf_documentation.md` |

## Definition of Done

- [ ] `ruff`, `mypy --strict` clean
- [ ] PDF generated locally from the wiki and reviewed for formatting
- [ ] PDF attached to a real GitHub Release and confirmed downloadable
- [ ] Wiki documentation written, or marked N/A with a reason
