# Release Workflow — Manual Tests

**Story:** [#2 — Automated Release Pipeline](../../../docs/2-build-executable-on-tag.md)

## feat commit on main triggers a new release

1. Merge a `feat:` commit to main (or push directly)
2. Open GitHub Actions → Release workflow
3. Verify the **version** job runs and creates a `v0.1.0` tag
4. Verify the **build** job starts automatically after the version job
5. Verify the **publish** job creates a GitHub Release named `v0.1.0`
6. Verify `ourcrm-windows.zip` is attached as the sole Windows release asset

## fix commit on main triggers a patch bump only

1. After a prior release exists (e.g. `v0.1.0`), push a `fix:` commit to main
2. Verify the version job bumps to `v0.1.1` (patch), not `v0.2.0`

## Non-bumping commit produces no release

1. Push a `chore:` or `ci:` commit to main (no `feat:` or `fix:`)
2. Verify the version job runs but creates no new tag
3. Verify the build and publish jobs do not run

## Build failure prevents the release from being published

1. Introduce a build error and push a `feat:` commit to main
2. Verify the version job creates the tag
3. Verify the build job fails
4. Verify the publish job does not run and no GitHub Release is created
5. Revert the error

## Windows zip downloads and runs correctly

1. Download `ourcrm-windows.zip` from the GitHub Release
2. Extract the zip — you should see an `ourcrm/` folder
3. Open the `ourcrm/` folder and run `ourcrm.exe`
4. Verify the window appears with "OurCRM" in the title and shuts down cleanly
