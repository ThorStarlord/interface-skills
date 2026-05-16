## Agent Brief

**Category:** enhancement
**Summary:** Extract `fixture_integrity.py` for structural pre-flight validation.

**Current behavior:**
When a promotion run fails, the harness does not always distinguish between a **Skill Behavioral Defect** and a **Fixture Input Defect**. This leads to developers wasting time debugging a skill when the source material (fixture) was actually missing files or malformed.

**Desired behavior:**
Implement `scripts/validators/fixture_integrity.py` as a deterministic pre-flight check. It must verify that a fixture is a "valid test object" (complete, coherent, compatible with the plan) before it is used to generate behavioral evidence. Failure here should trigger a **Fixture Repair Brief**, not a **Skill Improvement Brief**.

**Key interfaces:**
- `ValidatorResult` — Use the standard contract.
- `validate_fixture(fixture_path)` — Entrypoint.

**Acceptance criteria:**
- [ ] Rejects fixtures with missing source artifacts, malformed metadata, or invalid paths.
- [ ] Correctly distinguishes between a "bad fixture" (structural failure) and a "difficult fixture" (adversarial but structurally sound).
- [ ] Fails fast before the Promotion Harness invokes the skill on a defective fixture.

**Out of scope:**
- Judging the "quality" or "pedagogy" of a fixture.
- Automatically repairing fixtures.
