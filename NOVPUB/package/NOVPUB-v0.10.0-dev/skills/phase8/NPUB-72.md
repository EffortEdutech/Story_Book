# NPUB-72 — Ingram Returns, Wholesale & Distribution Monitoring

## Purpose
Reconcile return transactions and publisher compensation, track open return exposure including current 180-day tail risk after returnability changes, and maintain trade-term history.

## Preconditions
- `GATE-09` must be PASS for public-launch-dependent operations; post-publication setup may be prepared earlier but cannot fabricate live data.
- Consume the authoritative NOVPUB edition, production, metadata, KDP, Ingram and launch records. Retailer dashboards are observations, not upstream sources of truth.
- Refresh live KDP, Ingram and Malaysian regulatory rules before executing a live mutation or legal-compliance action.

## Outputs
- `returns_ledger.json`
- `return_exposure.json`
- `compensation_reconciliation.json`
- `trade_terms_history.json`
- `retailer_distribution_status.json`

## Deterministic controls
- Preserve raw source reports, identifiers, effective dates, currency and hashes before normalization.
- Distinguish sales/orders/returns/royalties/payments, mutable metadata versus locked edition identity, reader preference versus verified defect, and active versus superseded artefacts.
- Any live mutation must generate a post-publication change event with previous value, new value, reason, authority, approval and verification evidence.

## Human boundary
KDP Select renewal/opt-out, wide eBook activation, live price changes, returnability/wholesale changes, material corrections, new edition/format decisions, rights licences, title withdrawal and archive destruction require explicit human authorization.

## Evidence boundary
Do not mark legal deposit, payment reconciliation, physical correction, retailer state, sales, royalties or licensing complete without real evidence.
