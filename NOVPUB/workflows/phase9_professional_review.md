# Workflow: Phase 9 Professional Review / RC Approval

## Objective

Move `GATE-NOVPUB-RC1` from `PENDING` to approved only after genuine professional human review, real evidence inspection, defect handling, and explicit human approval.

## Entry Conditions

- NOVPUB package archive is available and extracted.
- Build report and checksums are available.
- Package self-checks pass from the extracted source.
- Professional reviewer identities and roles are recorded.
- No AI system is listed as the human approver.

## Required Evidence

- Package manifest
- Build report
- Package checksums
- Schema validation results
- Gate registry validation results
- Adversarial catalogue results
- Codex execution transcript
- Claude execution transcript
- Professional review notes
- Defect register
- Remediation log
- Final RC approval record

## Steps

1. Verify package extraction and checksum integrity.
2. Run the package structural self-check.
3. Run schema and contract validation.
4. Run deterministic engine verification.
5. Run state-machine and gate validation.
6. Run cross-phase provenance and parity validation.
7. Run adapter freshness and regression checks.
8. Run adversarial catalogue checks.
9. Execute Codex certification run.
10. Execute Claude certification run.
11. Compare Codex/Claude reproducibility evidence.
12. Conduct professional human review.
13. Register every defect, concern, waiver, or remediation.
14. Re-run affected validations after remediation.
15. Record final human RC approval.

## Exit Conditions

- `GATE-NOVPUB-RC1` has a real human approval record.
- All blocking defects are closed or formally waived by an authorized human.
- Certification evidence is stored in `NOVPUB/evidence/phase9/`.
- RC approval is not based on synthetic fixtures alone.

