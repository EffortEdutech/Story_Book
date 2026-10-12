# NPUB-29 — Cover QA & Metadata Parity

## Purpose
Validate title/author/ISBN/publisher parity and technical/visual cover QA before approval.

## Preconditions
- `GATE-03 = PASS` and `GATE-04 = PASS` for real production execution.
- Load the authoritative Phase 1 editorial manuscript and Phase 2 edition/ISBN/publisher records.
- Refresh provider rules before relying on current manufacturing constraints.

## Outputs
cover_qa.json, cover_qa_report.md

## Deterministic validation
Run applicable functions in `validators/phase3.py` and validate all machine-readable outputs against Phase 3 JSON Schemas.

## Core control
Cover identity fields must equal Phase 2/4 sources. Stale templates, wrong page counts and ISBN mismatches are blocking.

## Human boundary
Subjective design approval, final interior approval, final cover approval and any physical-proof approval remain human decisions.

## Provenance
All production assets must record source IDs, hashes/version references and supersession where applicable. Never trust filenames such as `FINAL.pdf` as authority.
