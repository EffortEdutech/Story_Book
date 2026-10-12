# NPUB-28 — Cover Engineering

## Purpose
Build channel-specific cover specifications from locked page count, trim, binding, paper and current provider templates.

## Preconditions
- `GATE-03 = PASS` and `GATE-04 = PASS` for real production execution.
- Load the authoritative Phase 1 editorial manuscript and Phase 2 edition/ISBN/publisher records.
- Refresh provider rules before relying on current manufacturing constraints.

## Outputs
cover_spec.json, template records, channel cover assets

## Deterministic validation
Run applicable functions in `validators/phase3.py` and validate all machine-readable outputs against Phase 3 JSON Schemas.

## Core control
No final print cover before pagination lock. KDP and Ingram templates are provider-specific and must not be interchanged.

## Human boundary
Subjective design approval, final interior approval, final cover approval and any physical-proof approval remain human decisions.

## Provenance
All production assets must record source IDs, hashes/version references and supersession where applicable. Never trust filenames such as `FINAL.pdf` as authority.
