# NPUB-37 — Pricing, Royalty & Unit Economics Engine

## Purpose
Calculate deterministic pricing scenarios for each edition/market using current channel rules, print costs and approved commercial objectives. Separate market judgment from arithmetic.

## Preconditions
- `GATE-05 = PASS` and `GATE-06 = PASS` for real commercial execution.
- Use Phase 2 identity/rights and Phase 3 production artefacts as upstream authority.
- Refresh current platform rule snapshots before relying on dynamic limits or economics.

## Outputs
- `pricing_model.json`
- `channel_costs.json`
- `royalty_scenarios.json`
- `market_prices.json`
- `pricing_approval.json`

## Deterministic validation
Use Decimal-based KDP print/eBook and Ingram compensation calculations; validate price floors, royalty bands, currencies and human approval.

## Human boundary
Commercial positioning, final copy, prices, wholesale terms, returnability, territories and release decisions remain human-approved decisions.

## Provenance
Every material metadata/commercial field records source, version/effective date and approval. Channel forms may transform approved data but may not silently invent replacements.
