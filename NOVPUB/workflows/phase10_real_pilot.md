# Workflow: Phase 10 Real Pilot

## Objective

Instantiate `NOVPUB-PILOT-001` with the actual completed novel manuscript and run the real pilot through manuscript baseline, KDP/Ingram pilot checks, proofs, launch readiness, post-publication governance, reproducibility certification, and final v1 approval.

## Entry Conditions

- `GATE-NOVPUB-RC1` is approved by a genuine human reviewer.
- Actual completed manuscript file is available.
- Source manuscript ownership and provenance evidence are available.
- Pilot workspace exists at `NOVPUB/pilot/NOVPUB-PILOT-001/`.

## Required Evidence

- Real manuscript file inventory
- SHA-256 digest for every source manuscript file
- Source ownership/provenance evidence
- Manuscript freeze record
- KDP pilot evidence levels K1-K4
- Ingram pilot evidence levels I1-I5
- eProof evidence
- Physical proof evidence
- Human proof approval
- Defect register
- Remediation and regression evidence
- Codex real-pilot run
- Claude real-pilot run
- Final human v1 approval
- v1 release manifest

## Steps

1. Create or refresh `NOVPUB-PILOT-001`.
2. Register the actual completed novel manuscript.
3. Compute and record SHA-256 digests.
4. Capture source provenance and ownership evidence.
5. Freeze the manuscript baseline.
6. Execute Phase 1-4 pilot checks against the real manuscript.
7. Execute KDP pilot levels K1-K4.
8. Execute Ingram pilot levels I1-I5.
9. Produce and inspect eProof evidence.
10. Order and inspect real physical proofs.
11. Record human physical proof approval or defects.
12. Execute launch readiness checks.
13. Execute post-publication governance pilot checks.
14. Register all defects and root causes.
15. Remediate and re-run affected checks.
16. Run actual Codex and Claude reproducibility certification.
17. Prepare final v1 release manifest.
18. Obtain final human approval.
19. Freeze as `NOVPUB v1.0.0`.

## Exit Conditions

- `GATE-NOVPUB-V1` is approved.
- No unresolved blocking defects remain.
- Physical proof approval is recorded by a real human.
- AI systems are not listed as release approvers.
- The package is frozen as `NOVPUB v1.0.0`.

