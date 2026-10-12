# NPUB-35 — Retail Book Description & Sales Copy

## Purpose
Produce approved hooks and retailer/back-cover descriptions from verified story facts while controlling spoilers and unsupported claims.

## Preconditions
- `GATE-05 = PASS` and `GATE-06 = PASS` for real commercial execution.
- Use Phase 2 identity/rights and Phase 3 production artefacts as upstream authority.
- Refresh current platform rule snapshots before relying on dynamic limits or economics.

## Outputs
- `hooks.md`
- `retail_descriptions.json`
- `retailer_description.md`
- `back_cover_copy.md`

## Deterministic validation
Validate claim provenance, spoiler level, approved status, manuscript fact consistency and cover-text revalidation dependency.

## Human boundary
Commercial positioning, final copy, prices, wholesale terms, returnability, territories and release decisions remain human-approved decisions.

## Provenance
Every material metadata/commercial field records source, version/effective date and approval. Channel forms may transform approved data but may not silently invent replacements.
