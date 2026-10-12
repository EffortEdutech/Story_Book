# NPUB-57 — ARC Production & Distribution Management

## Purpose
Create controlled advance reader copies, version them, mark their non-retail status, log every recipient and prevent any review obligation or review incentive.

## Preconditions
- `GATE-05`, `GATE-06`, `GATE-07`, and applicable channel readiness/proof controls must be valid for any public launch action.
- Consume approved NOVPUB manuscript, rights, production, metadata and channel records; launch material is downstream and cannot redefine book facts.
- Refresh current Amazon community/review and Author Central rules before live review campaigns or Author Central execution.

## Outputs
- `arc_manifest.json`
- `arc_recipient_register.json`
- `arc_distribution_log.json`
- `arc_followup.json`

## Deterministic controls
- Validate claim provenance, manuscript quotations, review independence, reviewer conflicts, retailer-link identity, launch dependencies and source-attributed metrics.
- Do not treat an ARC recipient, launch-team member, paid promoter, family member, employee or financially interested person as automatically eligible for an Amazon customer review.
- Preserve public claims, external review quotations, publication links and campaign assets with evidence/version references.

## Human boundary
Public launch authorization, paid promotion/spend, external endorsements, sensitive author-profile choices, publication-day activation and any material marketing claim remain human-controlled decisions.

## Review-integrity boundary
A free ARC may be offered, but the recipient must not be required to review it, rewarded for reviewing it, asked for a positive/star-specific review, or given a future benefit conditional on review content.
