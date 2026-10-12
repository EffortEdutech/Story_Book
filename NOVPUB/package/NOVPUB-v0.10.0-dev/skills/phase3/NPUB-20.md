# NPUB-20 — Trim Size & Physical Product Engineering

## Purpose
Evaluate trim candidates, page-count implications, bleed/margins and cross-channel compatibility.

## Preconditions
- `GATE-03 = PASS` and `GATE-04 = PASS` for real production execution.
- Load the authoritative Phase 1 editorial manuscript and Phase 2 edition/ISBN/publisher records.
- Refresh provider rules before relying on current manufacturing constraints.

## Outputs
trim_profiles.json, platform_trim_matrix.json, trim_decision.md

## Deterministic validation
Run applicable functions in `validators/phase3.py` and validate all machine-readable outputs against Phase 3 JSON Schemas.

## Core control
Use current channel constraints and never select 6×9 by habit. Human approval locks the selected physical geometry.

## Human boundary
Subjective design approval, final interior approval, final cover approval and any physical-proof approval remain human decisions.

## Provenance
All production assets must record source IDs, hashes/version references and supersession where applicable. Never trust filenames such as `FINAL.pdf` as authority.
