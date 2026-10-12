# NPUB-08 — Editorial Change Reconciliation

## Purpose
Resolve all Phase 1 findings, changes, author decisions, exceptions, and proof corrections into the authoritative editorial-approved manuscript.

## Inputs
Frozen manuscript; structural/continuity findings; Style Bible; copyedit changes/queries; proof changes; human decisions.

## Outputs
- `editorial_change_register.json`
- `unresolved_queries.json`
- `editorial_decisions.json`
- `reconciliation_report.md`
- `EDITORIAL_APPROVED_MANUSCRIPT.*`
- `editorial_approval.json`
- `phase1_completion_report.md`

## Reconciliation rules
- Every material change must be traceable.
- No blocking structural/continuity/query issue may remain open at approval.
- No active comments/tracked changes/placeholders may remain unintentionally.
- Final manuscript must comply with the approved Style Bible.
- Generate and register final manuscript SHA-256.

## GATE-02
PASS requires intake/freeze integrity, structural clearance, blocking continuity resolution, approved Style Bible, completed copyedit/proof, zero unresolved blocking issues, final hash, and explicit human editorial approval.

## Human boundary
The agent may recommend GATE-02 PASS but cannot set `EDITORIAL_APPROVED` without a valid human approval record.

## Exit
`EDITORIAL_APPROVED` and Phase 2 becomes eligible.