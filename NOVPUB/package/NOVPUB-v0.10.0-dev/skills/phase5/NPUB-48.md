# NPUB-48 — KDP Preview, Proof & Submission Gate

## Purpose
Validate Kindle preview, Print Previewer, physical-proof evidence, asset hashes, release configuration and edition-specific human authorization before any live publish transaction.

## Preconditions
- `GATE-07 = PASS` for real KDP commercial execution.
- Consume Phase 2 identity/rights, Phase 3 approved assets, and Phase 4 canonical metadata/commercial decisions.
- Refresh the relevant KDP official rule snapshot immediately before a live account or submission action.

## Outputs
- `kdp_proof_requests.json`
- `kdp_proof_findings.json`
- `kdp_proof_approval.json`
- `kdp_submission_checklist.json`
- `publication_authorization.json`
- `kdp_submission_freeze.json`

## Deterministic controls
- Validate canonical metadata parity and approved asset hashes.
- Treat KDP as a downstream channel, not the source of title/author/ISBN truth.
- Refuse silent rule guesses where a critical current KDP rule is stale or unknown.
- Record every human authorization separately by edition and transaction.

## Human boundary
Publishing, KDP Select enrollment, automatic-renew preference, DRM choice, release/pre-order configuration, price changes, Expanded Distribution and proof approval remain explicit human decisions.

## Security
Never store passwords, MFA secrets, identity-document numbers, tax identifiers, or full bank credentials in NOVPUB project artefacts.
