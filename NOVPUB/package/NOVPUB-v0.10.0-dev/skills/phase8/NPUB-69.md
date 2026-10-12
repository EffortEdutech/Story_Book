# NPUB-69 — Pricing, Metadata & Discoverability Optimization

## Purpose
Run controlled post-publication experiments on mutable metadata and pricing without corrupting edition identity, misleading readers or losing a reversible baseline.

## Preconditions
- `GATE-09` must be PASS for public-launch-dependent operations; post-publication setup may be prepared earlier but cannot fabricate live data.
- Consume the authoritative NOVPUB edition, production, metadata, KDP, Ingram and launch records. Retailer dashboards are observations, not upstream sources of truth.
- Refresh live KDP, Ingram and Malaysian regulatory rules before executing a live mutation or legal-compliance action.

## Outputs
- `pricing_history.json`
- `metadata_history.json`
- `optimization_experiments.json`
- `keyword_history.json`
- `category_history.json`

## Deterministic controls
- Preserve raw source reports, identifiers, effective dates, currency and hashes before normalization.
- Distinguish sales/orders/returns/royalties/payments, mutable metadata versus locked edition identity, reader preference versus verified defect, and active versus superseded artefacts.
- Any live mutation must generate a post-publication change event with previous value, new value, reason, authority, approval and verification evidence.

## Human boundary
KDP Select renewal/opt-out, wide eBook activation, live price changes, returnability/wholesale changes, material corrections, new edition/format decisions, rights licences, title withdrawal and archive destruction require explicit human authorization.

## Evidence boundary
Do not mark legal deposit, payment reconciliation, physical correction, retailer state, sales, royalties or licensing complete without real evidence.
