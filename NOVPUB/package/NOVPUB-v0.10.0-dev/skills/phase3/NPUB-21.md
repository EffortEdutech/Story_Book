# NPUB-21 — Typography Specification

## Purpose
Define a licensed, embeddable, glyph-complete typography system for the novel.

## Preconditions
- `GATE-03 = PASS` and `GATE-04 = PASS` for real production execution.
- Load the authoritative Phase 1 editorial manuscript and Phase 2 edition/ISBN/publisher records.
- Refresh provider rules before relying on current manufacturing constraints.

## Outputs
typography_spec.json, font_register.json, typography_spec.md

## Deterministic validation
Run applicable functions in `validators/phase3.py` and validate all machine-readable outputs against Phase 3 JSON Schemas.

## Core control
A locally installed font is not proof of embedding/print rights. Missing licence evidence or glyph coverage triggers review.

## Human boundary
Subjective design approval, final interior approval, final cover approval and any physical-proof approval remain human decisions.

## Provenance
All production assets must record source IDs, hashes/version references and supersession where applicable. Never trust filenames such as `FINAL.pdf` as authority.
