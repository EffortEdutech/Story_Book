# NPUB-96 — NOVPUB v1.0.0 Final Freeze & Handover

## Purpose
Evaluate V1-01 through V1-30, create the final release/freeze records and require human production-release approval.

## Preconditions
- Operate only on a real pilot project created from an authoritative manuscript source.
- Load `publishing_state.json`, `project_manifest.json`, current approvals and hashes before acting.
- Never convert missing real-world evidence into a synthetic PASS.

## Required gate context
GATE-NOVPUB-V1

## Outputs
- `v1_release_gate.json`
- `final_release_manifest.json`
- `v1_freeze_record.json`
- `final_handover_report.md`

## Operating rules
1. Preserve upstream source-of-truth and provenance.
2. Treat fixture/simulated evidence as test data, never real pilot certification evidence.
3. Stop at all human approval and irreversible transaction boundaries.
4. Record findings rather than manually bypassing a NOVPUB defect.
5. Supersede changed artefacts; never silently overwrite historical evidence.

## Completion
This skill is complete only when its real inputs, outputs, validator results and human evidence (where required) are recorded in `pilot_evidence_matrix.json`.
