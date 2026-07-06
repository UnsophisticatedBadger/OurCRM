# CI Pipeline — Manual Tests

**Story:** [#1 — CI Pipeline](../../../docs/1-setup-ci-pipeline.md)

## User triggers a push and the pipeline runs

1. Push a commit to a feature branch
2. Open the GitHub Actions tab
3. Verify the workflow starts automatically
4. Verify all steps (Lint, Format check, Type check, Tests) appear with their names in the log

## Pipeline fails on a lint violation and shows a clear error

1. Introduce an intentional ruff violation (e.g. unused import)
2. Push the commit
3. Verify the Lint step fails and the log shows the file, line number, and rule code
4. Revert the violation

## Pipeline fails on a type error and shows a clear error

1. Introduce an intentional mypy error (e.g. wrong return type annotation)
2. Push the commit
3. Verify the Type check step fails and identifies the file and line
4. Revert the change

## Pipeline fails on a test failure and shows a clear error

1. Introduce an intentional test failure (e.g. `assert False`)
2. Push the commit
3. Verify the Tests step fails with a clear failure message showing the test name
4. Revert the change

## uv caching reduces install time on repeat runs

1. Trigger the pipeline twice in succession
2. Compare the Install dependencies step duration between runs
3. Verify the second run is faster due to the uv cache

## Pipeline status is visible on a pull request before merge

1. Open a pull request targeting main
2. Verify the CI check appears in the PR checks section
3. Verify the status updates to pass or fail as the run completes
