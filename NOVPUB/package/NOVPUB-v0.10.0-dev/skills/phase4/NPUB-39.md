# NPUB-39 — Territory, Market & Distribution Strategy

## Purpose
Map distribution only to territories/formats actually authorized by the Phase 2 rights profile. Platform availability never creates rights.

## Preconditions
- `GATE-05 = PASS` and `GATE-06 = PASS` for real commercial execution.
- Use Phase 2 identity/rights and Phase 3 production artefacts as upstream authority.
- Refresh current platform rule snapshots before relying on dynamic limits or economics.

## Outputs
- `territory_strategy.json`
- `rights_distribution_matrix.json`
- `market_currency_map.json`

## Deterministic validation
Enforce distribution territory/format subset of rights, market currency completeness and human approval.

## Human boundary
Commercial positioning, final copy, prices, wholesale terms, returnability, territories and release decisions remain human-approved decisions.

## Provenance
Every material metadata/commercial field records source, version/effective date and approval. Channel forms may transform approved data but may not silently invent replacements.
