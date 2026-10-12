# NPUB-16 — PNM PDP / CIP Workflow

## Purpose
Prepare and reconcile Pengkatalogan Dalam Penerbitan (PDP/CIP) data as a pre-publication workflow.

## Preconditions
- Phase 1 `GATE-02 = PASS` for real manuscript execution.
- Load authoritative upstream records; never infer completion from filenames.

## Outputs
`pdp_application_pack/`, PNM return record, updated `pnm_status.json`

## Deterministic validation
Run applicable Phase 2 validators in `validators/phase2.py` and validate JSON outputs against schemas before changing project state.

## Human / legal boundary
PDP/CIP values must come from approved author, publisher, edition and ISBN records. Never invent cataloguing data.

## Provenance
Every material fact must record source/evidence where applicable. Missing evidence creates a finding or human-decision requirement rather than invented data.
