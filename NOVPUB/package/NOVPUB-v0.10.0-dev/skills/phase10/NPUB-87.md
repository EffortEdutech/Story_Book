# NPUB-87 — Real Pilot Project Instantiation

## Purpose
Create the authoritative NOVPUB pilot workspace for a real completed novel and bind it to the current release candidate.

## Preconditions
- Operate only on a real pilot project created from an authoritative manuscript source.
- Load `publishing_state.json`, `project_manifest.json`, current approvals and hashes before acting.
- Never convert missing real-world evidence into a synthetic PASS.

## Required gate context
GATE-NOVPUB-RC1

## Outputs
- `project_manifest.json`
- `pilot_decision_register.json`
- `pilot_evidence_matrix.json`

## Operating rules
1. Preserve upstream source-of-truth and provenance.
2. Treat fixture/simulated evidence as test data, never real pilot certification evidence.
3. Stop at all human approval and irreversible transaction boundaries.
4. Record findings rather than manually bypassing a NOVPUB defect.
5. Supersede changed artefacts; never silently overwrite historical evidence.

## Completion
This skill is complete only when its real inputs, outputs, validator results and human evidence (where required) are recorded in `pilot_evidence_matrix.json`.
