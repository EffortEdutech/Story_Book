# NPUB-56 — File Submission, eProof, Physical Proof & Distribution QA

## Purpose
Control Ingram file processing, eProof review, real physical-proof inspection, GATE-08 completion, distribution activation and representative retailer propagation QA.

## Preconditions
- `GATE-03`, `GATE-04`, `GATE-05`, `GATE-06`, and `GATE-07` must be `PASS` for live wholesale execution.
- Consume canonical rights, edition/ISBN, production and commercial artefacts; IngramSpark is never the upstream source of identity truth.
- Refresh the relevant current IngramSpark rule snapshot immediately before live account, commercial, file, proof or distribution actions.

## Outputs
- `eproof_register.json`
- `eproof_findings.json`
- `eproof_approval.json`
- `proof_orders.json`
- `proof_findings.json`
- `proof_approval.json`
- `distribution_status.json`
- `retailer_listing_snapshot.json`
- `distribution_qa.json`
- `ingram_completion.json`
- `phase6_completion_report.md`

## Deterministic controls
- Validate ISBN, edition, metadata, manufacturing, pricing and approved asset-hash parity.
- Treat eProof as a digital manufacturing preview, not as evidence that a physical copy was inspected.
- Preserve the KDP/Ingram coexistence invariant: same print edition + publisher-owned ISBN, with KDP Expanded Distribution disabled when Ingram distributes that ISBN.
- Record return exposure, rule provenance and every live commercial mutation.

## Human boundary
Wholesale discount, returnability, return method, market activation, eProof acceptance, physical-proof acceptance and distribution activation remain explicit human decisions.

## Security
Do not store passwords, MFA secrets, bank credentials, or full sensitive account identifiers in NOVPUB project artefacts.
