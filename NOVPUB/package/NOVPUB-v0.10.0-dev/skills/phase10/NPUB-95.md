# NPUB-95 — Codex / Claude Reproducibility Certification

## Purpose
Compare real-pilot workflow conclusions across Codex and Claude and block material deterministic or approval-boundary divergence.

## Preconditions
- Operate only on a real pilot project created from an authoritative manuscript source.
- Load `publishing_state.json`, `project_manifest.json`, current approvals and hashes before acting.
- Never convert missing real-world evidence into a synthetic PASS.

## Required gate context
No new master gate; obey all upstream gates.

## Outputs
- `real_pilot_parity_report.json`
- `agent_certification.json`

## Operating rules
1. Preserve upstream source-of-truth and provenance.
2. Treat fixture/simulated evidence as test data, never real pilot certification evidence.
3. Stop at all human approval and irreversible transaction boundaries.
4. Record findings rather than manually bypassing a NOVPUB defect.
5. Supersede changed artefacts; never silently overwrite historical evidence.

## Completion
This skill is complete only when its real inputs, outputs, validator results and human evidence (where required) are recorded in `pilot_evidence_matrix.json`.
