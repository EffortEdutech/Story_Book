# NPUB-23 — Print Typesetting

## Purpose
Render the approved literary content into a production layout while preserving text integrity and recording pagination.

## Preconditions
- `GATE-03 = PASS` and `GATE-04 = PASS` for real production execution.
- Load the authoritative Phase 1 editorial manuscript and Phase 2 edition/ISBN/publisher records.
- Refresh provider rules before relying on current manufacturing constraints.

## Outputs
PRINT_MASTER_SOURCE, PRINT_MASTER_PDF, pagination_manifest.json, typesetting_report.md

## Deterministic validation
Run applicable functions in `validators/phase3.py` and validate all machine-readable outputs against Phase 3 JSON Schemas.

## Core control
The renderer may alter layout but not literary content. A page-count lock is created before final cover engineering.

## Human boundary
Subjective design approval, final interior approval, final cover approval and any physical-proof approval remain human decisions.

## Provenance
All production assets must record source IDs, hashes/version references and supersession where applicable. Never trust filenames such as `FINAL.pdf` as authority.
