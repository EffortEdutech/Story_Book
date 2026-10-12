# NPUB-40 — Publication Date, Pre-order & Release Strategy

## Purpose
Create a controlled publication/release calendar distinguishing publication, on-sale, preorder, submission and launch dates. Live channel timing constraints remain adapter rules.

## Preconditions
- `GATE-05 = PASS` and `GATE-06 = PASS` for real commercial execution.
- Use Phase 2 identity/rights and Phase 3 production artefacts as upstream authority.
- Refresh current platform rule snapshots before relying on dynamic limits or economics.

## Outputs
- `publication_strategy.json`
- `release_calendar.json`
- `preorder_strategy.json`
- `release_approval.json`
- `kdp_metadata_map.json`
- `ingram_metadata_map.json`
- `pnm_metadata_map.json`
- `metadata_parity_report.json`
- `commercial_approval.json`

## Deterministic validation
Validate chronological dependencies, release buffers, channel mappings, proof dependency and GATE-07 human approval.

## Human boundary
Commercial positioning, final copy, prices, wholesale terms, returnability, territories and release decisions remain human-approved decisions.

## Provenance
Every material metadata/commercial field records source, version/effective date and approval. Channel forms may transform approved data but may not silently invent replacements.
