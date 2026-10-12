# Discussion Extraction

Source conversation: `Publish Novel Indie Style`

## Final Stated Status

The NOVPUB codebase was upgraded through `NOVPUB v0.10.0-dev`, with NPUB-01 through NPUB-96 / Phases 1-10 implemented.

The discussion explicitly keeps the live release records pending:

```text
GATE-NOVPUB-RC1 = PENDING
GATE-NOVPUB-V1  = PENDING
PACKAGE         = NOVPUB v0.10.0-dev
```

The package must not be renamed to `NOVPUB v1.0.0` until real review, real manuscript pilot, proofing, remediation, and final human approval are complete.

## Batch 10 Extract

Batch 10 completed:

- NPUB-87 Real Pilot Project Instantiation
- NPUB-88 Real Manuscript Baseline & Evidence Capture
- NPUB-89 End-to-End Phase 1-4 Pilot Execution
- NPUB-90 Real KDP Adapter Pilot
- NPUB-91 Real IngramSpark Adapter Pilot
- NPUB-92 Proof, Publication & Launch Readiness Pilot
- NPUB-93 Post-Publication Governance Pilot
- NPUB-94 Pilot Defect, Finding & Remediation Loop
- NPUB-95 Codex / Claude Reproducibility Certification
- NPUB-96 NOVPUB v1.0.0 Final Freeze & Handover
- GATE-P10-01 Real Source Integrity
- V1-01 through V1-30 validation for GATE-NOVPUB-V1
- `init-pilot` workflow
- Real manuscript SHA-256/source-evidence controls
- `pilot_evidence_matrix.json` covering NPUB-01-76
- KDP pilot levels K1-K4
- Ingram pilot levels I1-I5
- Physical-proof evidence enforcement
- Real pilot defect/root-cause/regression controls
- Actual Codex-vs-Claude execution certification structure
- Final v1 release manifest, freeze and handover machinery

Critical control:

- Fixture, simulated, or synthetic evidence cannot satisfy real manuscript/pilot evidence requirements.
- AI/Codex/Claude cannot be the human approver for physical proof, release gates, or production certification.

## Verification Claimed In Discussion

- 251/251 non-CLI cross-phase tests
- 10/10 Phase 3-5 CLI/workspace tests
- 7/7 Phase 6 CLI/workspace tests
- 7/7 Phase 7 CLI/workspace tests
- 9/9 Phase 8 CLI/workspace tests
- 8/8 Phase 9 CLI/workspace tests
- 9/9 Phase 10 CLI/workspace tests
- Aggregate: 301/301 PASS
- 167 valid JSON Schemas
- 96 implemented skill files
- 14 registered gates
- Clean pilot-workspace initialization
- Package structural self-check PASS
- Clean ZIP extraction PASS
- ZIP integrity PASS
- 648/648 SHA-256 package files verified

## Earlier Batches Captured

- Batch 6: NPUB-50 through NPUB-56, IngramSpark adapter and GATE-INGRAM-01.
- Batch 7: NPUB-57 through NPUB-66, launch and marketing layer and GATE-09.
- Batch 8: NPUB-67 through NPUB-76, post-publication governance and GATE-10.
- Batch 9: NPUB-77 through NPUB-86, stabilization, adversarial testing, professional review, remediation, and GATE-NOVPUB-RC1.
- Batch 10: NPUB-87 through NPUB-96, real pilot and v1 freeze machinery.

