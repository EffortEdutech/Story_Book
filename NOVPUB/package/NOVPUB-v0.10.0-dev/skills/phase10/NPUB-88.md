# NPUB-88 — Real Manuscript Baseline & Evidence Capture

## Purpose
Freeze the real source manuscript with checksum, completeness evidence and human source confirmation.

## Preconditions
- Operate only on a real pilot project created from an authoritative manuscript source.
- Load `publishing_state.json`, `project_manifest.json`, current approvals and hashes before acting.
- Never convert missing real-world evidence into a synthetic PASS.

## Required gate context
GATE-P10-01

## Outputs
- `source_inventory.json`
- `manuscript_intake.json`
- `manuscript_manifest.json`
- `checksums.json`
- `baseline_report.md`

## Operating rules
1. Preserve upstream source-of-truth and provenance.
2. Treat fixture/simulated evidence as test data, never real pilot certification evidence.
3. Stop at all human approval and irreversible transaction boundaries.
4. Record findings rather than manually bypassing a NOVPUB defect.
5. Supersede changed artefacts; never silently overwrite historical evidence.

## Completion
This skill is complete only when its real inputs, outputs, validator results and human evidence (where required) are recorded in `pilot_evidence_matrix.json`.
