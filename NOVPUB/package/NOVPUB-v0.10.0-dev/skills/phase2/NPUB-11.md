# NPUB-11 — Author & Publishing Identity

## Purpose
Separate private/legal identity from public author identity, including pen-name mappings, contributors, and platform display names.

## Preconditions
- Phase 1 `GATE-02 = PASS` for real manuscript execution.
- Load authoritative upstream records; never infer completion from filenames.

## Outputs
`author_identity.json`, `pen_name_record.json`, `identity_approval.json`

## Deterministic validation
Run applicable Phase 2 validators in `validators/phase2.py` and validate JSON outputs against schemas before changing project state.

## Human / legal boundary
Do not expose the legal identity behind a pen name merely because the project contains it. Public identity changes require explicit approval.

## Provenance
Every material fact must record source/evidence where applicable. Missing evidence creates a finding or human-decision requirement rather than invented data.
