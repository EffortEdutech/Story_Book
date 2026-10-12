# NPUB-12 — Publisher / Imprint Establishment

## Purpose
Establish publisher and imprint records independently from distribution platforms. KDP and IngramSpark are channels, not the default publisher identity.

## Preconditions
- Phase 1 `GATE-02 = PASS` for real manuscript execution.
- Load authoritative upstream records; never infer completion from filenames.

## Outputs
`publisher_profile.json`, `imprint_profile.json`, `publisher_approval.json`

## Deterministic validation
Run applicable Phase 2 validators in `validators/phase2.py` and validate JSON outputs against schemas before changing project state.

## Human / legal boundary
Publisher/imprint values become controlled source data. A material naming conflict may trigger `TRADEMARK_REVIEW_RECOMMENDED`; NOVPUB does not perform trademark clearance.

## Provenance
Every material fact must record source/evidence where applicable. Missing evidence creates a finding or human-decision requirement rather than invented data.
