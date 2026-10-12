# NPUB-17 — Copyright & Publication Notice Generator

## Purpose
Generate the copyright/publication page from controlled Phase 2 fields and permission credits rather than free-form improvisation.

## Preconditions
- Phase 1 `GATE-02 = PASS` for real manuscript execution.
- Load authoritative upstream records; never infer completion from filenames.

## Outputs
`copyright_page_data.json`, `COPYRIGHT_PAGE_APPROVED.md`

## Deterministic validation
Run applicable Phase 2 validators in `validators/phase2.py` and validate JSON outputs against schemas before changing project state.

## Human / legal boundary
Do not state copyright is registered merely because protection exists. MyIPO voluntary notification is optional unless project policy or another valid requirement says otherwise.

## Provenance
Every material fact must record source/evidence where applicable. Missing evidence creates a finding or human-decision requirement rather than invented data.
