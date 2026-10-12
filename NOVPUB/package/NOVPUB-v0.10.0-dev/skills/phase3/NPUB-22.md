# NPUB-22 — Page Architecture

## Purpose
Define front matter, body, back matter, folios, running heads, chapter starts and intentional blank-page rules.

## Preconditions
- `GATE-03 = PASS` and `GATE-04 = PASS` for real production execution.
- Load the authoritative Phase 1 editorial manuscript and Phase 2 edition/ISBN/publisher records.
- Refresh provider rules before relying on current manufacturing constraints.

## Outputs
page_architecture.json, front_matter_map.json, back_matter_map.json, pagination_rules.json

## Deterministic validation
Run applicable functions in `validators/phase3.py` and validate all machine-readable outputs against Phase 3 JSON Schemas.

## Core control
Every blank page and suppressed folio/header must be explainable by the architecture rather than accidental layout behavior.

## Human boundary
Subjective design approval, final interior approval, final cover approval and any physical-proof approval remain human decisions.

## Provenance
All production assets must record source IDs, hashes/version references and supersession where applicable. Never trust filenames such as `FINAL.pdf` as authority.
