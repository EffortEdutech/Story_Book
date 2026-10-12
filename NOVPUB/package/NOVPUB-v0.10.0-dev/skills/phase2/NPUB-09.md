# NPUB-09 — Rights & Ownership Audit

## Purpose
Establish authorship, copyright ownership, publishing authority, territorial rights, language rights, format rights, prior publication, and prior assignments. The skill manages publishing evidence; it does not substitute for legal advice.

## Preconditions
- Phase 1 `GATE-02 = PASS` for real manuscript execution.
- Load authoritative upstream records; never infer completion from filenames.

## Outputs
`rights_profile.json`, `ownership_evidence.json`, `territorial_rights.json`, `rights_findings.json`, `rights_audit_report.md`

## Deterministic validation
Run applicable Phase 2 validators in `validators/phase2.py` and validate JSON outputs against schemas before changing project state.

## Human / legal boundary
Never infer ownership from authorship alone. Any disputed, ambiguous, assigned, commissioned, employment-created, estate-controlled, or contract-limited right remains unresolved until supported by evidence or human/legal review.

## Provenance
Every material fact must record source/evidence where applicable. Missing evidence creates a finding or human-decision requirement rather than invented data.
