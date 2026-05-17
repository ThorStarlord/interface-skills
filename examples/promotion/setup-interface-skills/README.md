# Clean Fixture: Setup Interface Skills

This fixture validates the `setup-interface-skills` skill. The objective of this skill is to initialize the repository's configuration for the **Interface Skills Specification Layer**, wiring all relevant AI agent entry points (`CLAUDE.md`, `AGENTS.md`, etc.) and defining a centralized, single source of UI policy in `INTERFACE_SKILLS.md`.

## Starting Context
 AI agents operating in this repository need to discover which folder contains the active specifications before modifying any UI or route codes.
To make this possible, this skill patches agent-facing documentation to direct agents to the `INTERFACE_SKILLS.md` file, which maps routes to UI spec packages.

## Expected Outputs
Upon successful setup, the following artifacts must be created and fully populated:
1. `INTERFACE_SKILLS.md` at the repository root containing the spec directory path and routing logic rules.
2. `.interface-skills.yaml` containing the specs root configuration and agent entry points registry.
3. Patched `CLAUDE.md` and `AGENTS.md` with active bounding markers.
