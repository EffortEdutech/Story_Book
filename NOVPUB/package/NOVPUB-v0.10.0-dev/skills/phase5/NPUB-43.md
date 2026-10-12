# NPUB-43 — Kindle eBook Submission Package

## Purpose
Build the Kindle submission package from the approved EPUB, cover, metadata, rights, pricing and release strategy. Validate metadata limits, content-origin disclosure, DRM decision and Kindle preview evidence.

## Preconditions
- `GATE-07 = PASS` for real KDP commercial execution.
- Consume Phase 2 identity/rights, Phase 3 approved assets, and Phase 4 canonical metadata/commercial decisions.
- Refresh the relevant KDP official rule snapshot immediately before a live account or submission action.

## Outputs
- `kindle_metadata.json`
- `kindle_submission_manifest.json`
- `kindle_preview_report.json`
- `kindle_submission_status.json`
- `content_origin_record.json`

## Deterministic controls
- Validate canonical metadata parity and approved asset hashes.
- Treat KDP as a downstream channel, not the source of title/author/ISBN truth.
- Refuse silent rule guesses where a critical current KDP rule is stale or unknown.
- Record every human authorization separately by edition and transaction.

## Human boundary
Publishing, KDP Select enrollment, automatic-renew preference, DRM choice, release/pre-order configuration, price changes, Expanded Distribution and proof approval remain explicit human decisions.

## Security
Never store passwords, MFA secrets, identity-document numbers, tax identifiers, or full bank credentials in NOVPUB project artefacts.
