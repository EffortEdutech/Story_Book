# NPUB-10 — Third-Party Content & Permissions Audit

## Purpose
Identify material that may be owned by a third party: lyrics, poems, epigraphs, substantial quotations, photographs, maps, illustrations, correspondence, translated material, screenshots, logos, and other inserted works.

## Preconditions
- Phase 1 `GATE-02 = PASS` for real manuscript execution.
- Load authoritative upstream records; never infer completion from filenames.

## Outputs
`third_party_content_register.json`, `permissions_register.json`, `permissions_report.md`

## Deterministic validation
Run applicable Phase 2 validators in `validators/phase2.py` and validate JSON outputs against schemas before changing project state.

## Human / legal boundary
Do not assume that short use is automatically permitted. Public-domain or permission-not-required conclusions require a recorded basis; uncertain cases escalate to `LEGAL_REVIEW_REQUIRED`.

## Provenance
Every material fact must record source/evidence where applicable. Missing evidence creates a finding or human-decision requirement rather than invented data.
