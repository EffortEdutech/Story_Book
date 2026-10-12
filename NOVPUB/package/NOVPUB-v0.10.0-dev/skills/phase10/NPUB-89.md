# NPUB-89 — End-to-End Phase 1–4 Pilot Execution

## Purpose
Execute NPUB-01 through NPUB-40 on the real novel and record real gate evidence for GATE-02 through GATE-07.

## Preconditions
- Operate only on a real pilot project created from an authoritative manuscript source.
- Load `publishing_state.json`, `project_manifest.json`, current approvals and hashes before acting.
- Never convert missing real-world evidence into a synthetic PASS.

## Required gate context
GATE-02, GATE-03, GATE-04, GATE-05, GATE-06, GATE-07

## Outputs
- `phase1_4_pilot_execution.json`
- `pilot_evidence_matrix.json`

## Operating rules
1. Preserve upstream source-of-truth and provenance.
2. Treat fixture/simulated evidence as test data, never real pilot certification evidence.
3. Stop at all human approval and irreversible transaction boundaries.
4. Record findings rather than manually bypassing a NOVPUB defect.
5. Supersede changed artefacts; never silently overwrite historical evidence.

## Completion
This skill is complete only when its real inputs, outputs, validator results and human evidence (where required) are recorded in `pilot_evidence_matrix.json`.
