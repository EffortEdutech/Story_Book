# NPUB-49 — Amazon Listing & Post-Publication QA

## Purpose
Compare the public Amazon listing against the KDP submission freeze and canonical metadata. Check identity, price, cover, availability, format linkage and unexpected platform transformations before marking the KDP channel verified.

## Preconditions
- `GATE-07 = PASS` for real KDP commercial execution.
- Consume Phase 2 identity/rights, Phase 3 approved assets, and Phase 4 canonical metadata/commercial decisions.
- Refresh the relevant KDP official rule snapshot immediately before a live account or submission action.

## Outputs
- `amazon_listing_snapshot.json`
- `amazon_listing_qa.json`
- `format_linkage.json`
- `post_publication_issues.json`
- `kdp_completion.json`
- `phase5_completion_report.md`

## Deterministic controls
- Validate canonical metadata parity and approved asset hashes.
- Treat KDP as a downstream channel, not the source of title/author/ISBN truth.
- Refuse silent rule guesses where a critical current KDP rule is stale or unknown.
- Record every human authorization separately by edition and transaction.

## Human boundary
Publishing, KDP Select enrollment, automatic-renew preference, DRM choice, release/pre-order configuration, price changes, Expanded Distribution and proof approval remain explicit human decisions.

## Security
Never store passwords, MFA secrets, identity-document numbers, tax identifiers, or full bank credentials in NOVPUB project artefacts.
