# NPUB-31 — Metadata Master & Source-of-Truth Registry

## Purpose
Create the canonical commercial metadata master. Locked identity fields must trace to Phase 2 and product fields to Phase 3. Channel forms are downstream mappings, never authoritative sources.

## Preconditions
- `GATE-05 = PASS` and `GATE-06 = PASS` for real commercial execution.
- Use Phase 2 identity/rights and Phase 3 production artefacts as upstream authority.
- Refresh current platform rule snapshots before relying on dynamic limits or economics.

## Outputs
- `metadata_master.yaml`
- `metadata_master.json`
- `metadata_manifest.json`
- `metadata_lock.json`

## Deterministic validation
Validate identity/product parity, provenance, required fields, mutability class and metadata lock.

## Human boundary
Commercial positioning, final copy, prices, wholesale terms, returnability, territories and release decisions remain human-approved decisions.

## Provenance
Every material metadata/commercial field records source, version/effective date and approval. Channel forms may transform approved data but may not silently invent replacements.
