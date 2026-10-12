# NPUB-33 — Classification & Subject Strategy

## Purpose
Build accurate BISAC, Thema, Amazon-category and regional-subject strategies. Primary classification must reflect the work as a whole, not a peripheral subplot.

## Preconditions
- `GATE-05 = PASS` and `GATE-06 = PASS` for real commercial execution.
- Use Phase 2 identity/rights and Phase 3 production artefacts as upstream authority.
- Refresh current platform rule snapshots before relying on dynamic limits or economics.

## Outputs
- `classification_master.json`
- `bisac_strategy.json`
- `thema_strategy.json`
- `amazon_category_strategy.json`
- `regional_subjects.json`

## Deterministic validation
Validate code records, relevance basis, audience compatibility, current rule freshness and KDP current category limits.

## Human boundary
Commercial positioning, final copy, prices, wholesale terms, returnability, territories and release decisions remain human-approved decisions.

## Provenance
Every material metadata/commercial field records source, version/effective date and approval. Channel forms may transform approved data but may not silently invent replacements.
