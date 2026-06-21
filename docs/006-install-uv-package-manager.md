# US-006: Install UV Package Manager

## User Story

**As a** developer  
**I want to** install the UV package manager  
**So that** I can manage Python dependencies and run the project

## Priority

**MVP:** Must Have

**Rationale:** UV is the chosen package manager for OurCRM. Without it, developers cannot install dependencies or run the project.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Document installation methods for each platform
- 1 hour: Test installation on Windows
- 1 hour: Test installation on macOS
- 1 hour: Test installation on Linux
- 1 hour: Verify UV works correctly
- 1 hour: Add installation instructions to README

## Dependencies

**Depends on:** None (prerequisite for US-001)

**Blocks:** US-001 (Setup Development Environment), US-002 (Run Application)

## Description

A developer should be able to install UV on their system using the appropriate method for their operating system. UV should install quickly and work immediately after installation without requiring additional configuration. The installation process should be well-documented with clear instructions for each platform.

UV is a fast Python package and project manager written in Rust. It replaces pip, pip-tools, poetry, pyenv, and virtualenv. Installing UV is a prerequisite for setting up the OurCRM development environment.

## Acceptance Criteria

- [ ] UV installs successfully on Windows — see tests/manual/infrastructure.md
- [ ] UV installs successfully on macOS — see tests/manual/infrastructure.md
- [ ] UV installs successfully on Linux — see tests/manual/infrastructure.md
- [x] Installation instructions are clear and complete
- [x] `uv --version` works after installation
- [x] UV is in PATH after installation
- [ ] Installation completes in under 5 minutes — see tests/manual/infrastructure.md
- [x] No errors during installation
- [x] UV can be updated to latest version
- [x] Installation instructions are in README
- [x] Multiple installation methods are documented (script, package manager)