# NPUB-94 — Pilot Defect, Finding & Remediation Loop

## Purpose
Register every real pilot defect, require root cause and regression coverage, and prevent workarounds from masquerading as closure.

## Preconditions
- Operate only on a real pilot project created from an authoritative manuscript source.
- Load `publishing_state.json`, `project_manifest.json`, current approvals and hashes before acting.
- Never convert missing real-world evidence into a synthetic PASS.

## Required gate context
No new master gate; obey all upstream gates.

## Outputs
- `pilot_findings.json`
- `pilot_defect_register.json`
- `pilot_remediation.json`

## Operating rules
1. Preserve upstream source-of-truth and provenance.
2. Treat fixture/simulated evidence as test data, never real pilot certification evidence.
3. Stop at all human approval and irreversible transaction boundaries.
4. Record findings rather than manually bypassing a NOVPUB defect.
5. Supersede changed artefacts; never silently overwrite historical evidence.

## Completion
This skill is complete only when its real inputs, outputs, validator results and human evidence (where required) are recorded in `pilot_evidence_matrix.json`.
