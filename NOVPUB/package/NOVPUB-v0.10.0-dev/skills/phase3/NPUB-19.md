# NPUB-19 — Format & Manufacturing Strategy

## Purpose
Define the actual print/digital products and channel-compatible manufacturing profiles without hard-wiring provider rules into the core.

## Preconditions
- `GATE-03 = PASS` and `GATE-04 = PASS` for real production execution.
- Load the authoritative Phase 1 editorial manuscript and Phase 2 edition/ISBN/publisher records.
- Refresh provider rules before relying on current manufacturing constraints.

## Outputs
format_strategy.json, manufacturing_profiles.json, format_strategy_report.md

## Deterministic validation
Run applicable functions in `validators/phase3.py` and validate all machine-readable outputs against Phase 3 JSON Schemas.

## Core control
Validate selected editions against current KDP/Ingram rule snapshots. A format is created only when approved in the edition manifest.

## Human boundary
Subjective design approval, final interior approval, final cover approval and any physical-proof approval remain human decisions.

## Provenance
All production assets must record source IDs, hashes/version references and supersession where applicable. Never trust filenames such as `FINAL.pdf` as authority.
