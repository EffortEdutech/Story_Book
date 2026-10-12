# NPUB-38 — Wholesale Discount & Returns Risk Strategy

## Purpose
Model Ingram wholesale discount and returnability independently. Calculate return exposure under stress scenarios before any returnable strategy can be approved.

## Preconditions
- `GATE-05 = PASS` and `GATE-06 = PASS` for real commercial execution.
- Use Phase 2 identity/rights and Phase 3 production artefacts as upstream authority.
- Refresh current platform rule snapshots before relying on dynamic limits or economics.

## Outputs
- `wholesale_strategy.json`
- `returns_model.json`
- `return_stress_test.json`
- `wholesale_approval.json`

## Deterministic validation
Validate current discount limits, compensation, return scenarios, exposure limits and explicit human approval.

## Human boundary
Commercial positioning, final copy, prices, wholesale terms, returnability, territories and release decisions remain human-approved decisions.

## Provenance
Every material metadata/commercial field records source, version/effective date and approval. Channel forms may transform approved data but may not silently invent replacements.
