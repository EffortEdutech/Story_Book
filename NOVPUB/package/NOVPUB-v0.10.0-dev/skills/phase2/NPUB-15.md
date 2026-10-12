# NPUB-15 — Malaysia ISBN / eISBN Workflow

## Purpose
Prepare and reconcile Malaysian ISBN/eISBN application data through Perpustakaan Negara Malaysia (PNM), using current official requirements.

## Preconditions
- Phase 1 `GATE-02 = PASS` for real manuscript execution.
- Load authoritative upstream records; never infer completion from filenames.

## Outputs
`isbn_application_pack/`, `pnm_status.json`, `malaysia_rules_snapshot.json`

## Deterministic validation
Run applicable Phase 2 validators in `validators/phase2.py` and validate JSON outputs against schemas before changing project state.

## Human / legal boundary
This skill is a workflow manager, not an ISBN generator. Before a live application, refresh PNM requirements and preserve the rule/source snapshot.

## Provenance
Every material fact must record source/evidence where applicable. Missing evidence creates a finding or human-decision requirement rather than invented data.
