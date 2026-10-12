# Real Certification Runbook

## Stage A: Recover Package

1. Obtain `NOVPUB-Implementation-Batch-10.zip`.
2. Place it in `NOVPUB/source_archives/`.
3. Extract into `NOVPUB/package/`.
4. Verify archive checksums against `PACKAGE_CHECKSUMS.json`.
5. Confirm package version remains `NOVPUB v0.10.0-dev` before certification.

## Stage B: Phase 9 RC

1. Run package self-checks.
2. Run schema validation.
3. Run gate/state-machine validation.
4. Run deterministic and parity validation.
5. Run adversarial catalogue validation.
6. Run Codex certification.
7. Run Claude certification.
8. Conduct professional human review.
9. Remediate defects.
10. Record human approval for `GATE-NOVPUB-RC1`.

## Stage C: Phase 10 Pilot

1. Confirm `GATE-NOVPUB-RC1` is approved.
2. Register real manuscript files in `NOVPUB-PILOT-001`.
3. Record hashes and provenance.
4. Freeze manuscript baseline.
5. Execute real pilot checks.
6. Complete KDP K1-K4.
7. Complete Ingram I1-I5.
8. Obtain eProof and physical proof evidence.
9. Complete defect remediation loop.
10. Run Codex and Claude real-pilot certification.
11. Obtain final human approval.

## Stage D: Freeze

1. Confirm `GATE-NOVPUB-V1` is approved.
2. Create final release manifest.
3. Freeze package as `NOVPUB v1.0.0`.
4. Archive final package, evidence, approvals, and handover documents.

