# Phase 8 — Post-Publication Governance Architecture

Phase 8 governs a novel after launch. It keeps live platform data downstream of NOVPUB's authoritative edition, rights, production, metadata and approval records.

## Core invariants

1. Preserve raw financial reports before normalization.
2. Distinguish orders, sales, shipments, returns, royalty-eligible transactions and payments.
3. Preserve historical platform rules for historical transaction reconciliation.
4. Treat KDP Select as a recurring, human-controlled digital-exclusivity decision.
5. Treat post-publication metadata updates separately from locked edition identity.
6. Classify corrections, material revisions, new editions and new formats before mutation.
7. Track Ingram return exposure after commercial setting changes.
8. Treat reader feedback as a signal until verified.
9. Close Malaysian legal deposit only with current-rule validation and real submission evidence.
10. Preserve active and superseded assets with checksums and provenance.
11. Require GATE-10 human approval before the publication is declared governed.

## Current dated adapter baselines

- KDP Select snapshot: verified 2026-10-10; 90-day digital exclusivity and automatic renewal unless disabled.
- KDP post-publication details snapshot: verified 2026-10-10; mutable commercial metadata is distinguished from locked edition identity.
- Ingram returns lifecycle snapshot: verified 2026-10-10; current returnable-to-non-returnable tail is 180 days.
- Malaysia PNM legal-deposit snapshot: verified 2026-10-10; current baseline records five printed copies within one month and two non-printed units within one year, subject to live refresh before execution.

These are adapter snapshots, not permanent core constants.
