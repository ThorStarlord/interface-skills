# ADR 0001: Interface Skills uses skill chains and spec packages as its system contract

## Status

Accepted

## Context

Interface Skills started as individual UI-related skills. As the repository grew, repeated issues appeared:
- skills produced artifacts with inconsistent names
- reports from different workflow moments contradicted each other
- agents could not always find active specs
- draft skills needed realistic fixtures before promotion

## Decision

Interface Skills will treat the spec package as the primary system contract.

A workflow is valid when it produces or updates a spec package with:
- canonical artifact names
- `00-index.md` as the entry point
- active vs historical reports
- traceable `based_on` references
- deterministic validation where possible
- human review for judgment-based outputs

## Consequences

- Skills must output artifacts that other skills can consume.
- Reports need lifecycle metadata when superseded.
- Fixtures are required before promoting draft skills.
- Validators should catch structural drift.
- Humans still decide whether outputs are useful and not misleading.

## Alternatives considered

- Keep skills independent with no shared package format.
- Use a single monolithic orchestrator.
- Let each product repo invent its own conventions.

## Why not

Independent skills drift.
A monolithic orchestrator becomes too hard to adapt.
Per-repo conventions make outputs hard to validate.
