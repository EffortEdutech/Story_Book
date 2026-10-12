# NPUB-27 — Cover Creative Brief

## Purpose
Translate the real book positioning into an approved cover brief without inventing story elements or spoilers.

## Preconditions
- `GATE-03 = PASS` and `GATE-04 = PASS` for real production execution.
- Load the authoritative Phase 1 editorial manuscript and Phase 2 edition/ISBN/publisher records.
- Refresh provider rules before relying on current manufacturing constraints.

## Outputs
creative_brief.md, cover_brief.json, concept_register.json

## Deterministic validation
Run applicable functions in `validators/phase3.py` and validate all machine-readable outputs against Phase 3 JSON Schemas.

## Core control
Every central cover element must be supported by manuscript/positioning evidence. Final creative direction requires human selection.

## Human boundary
Subjective design approval, final interior approval, final cover approval and any physical-proof approval remain human decisions.

## Provenance
All production assets must record source IDs, hashes/version references and supersession where applicable. Never trust filenames such as `FINAL.pdf` as authority.
