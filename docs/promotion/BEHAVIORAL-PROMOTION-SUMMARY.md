# Behavioral Promotion Summary

## Confirmed / Promoted
- `ui-surface-inventory` — confirmed individually stable with synced behavioral evidence.
- `ui-to-issues` — promoted from draft to individually stable.

## Promotion Type
- individual stable promotion / confirmation
- simulated/real handoff status recorded
- no full-chain stability claimed (per ADR 0006)

## Evidence
- `promotion-runs/2026-05-15-20-29-12-ui-surface-inventory`
- `promotion-runs/2026-05-15-20-23-16-ui-to-issues`
- `examples/promotion/ui-surface-inventory/reference/`
- `examples/promotion/ui-to-issues/reference/`

## Validation
- `python scripts/stable-skill-regression.py` passed in a temp clone of `e04bc2e`.
- `python scripts/run-promotion-suite.py --skill ui-surface-inventory` passed in a temp clone of `e04bc2e`.
- `python scripts/run-promotion-suite.py --skill ui-to-issues` passed in a temp clone of `e04bc2e`.
- `python -m unittest discover scripts -p "test_*.py"` passed.

## Note
These skills are individually stable for their own output contracts. This does not imply full-chain stability for the entire interface-skills workflow chain.
