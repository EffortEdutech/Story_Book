# NPUB-18 — Malaysian Legal Deposit & Compliance

## Purpose
Register and calculate Malaysian legal-deposit obligations, deadlines, evidence requirements, and post-publication closure state.

## Preconditions
- Phase 1 `GATE-02 = PASS` for real manuscript execution.
- Load authoritative upstream records; never infer completion from filenames.

## Outputs
`legal_deposit_obligations.json`, `compliance_calendar.json`, Phase 2 compliance report

## Deterministic validation
Run applicable Phase 2 validators in `validators/phase2.py` and validate JSON outputs against schemas before changing project state.

## Human / legal boundary
Phase 2 plans the obligation; it must not falsely mark legal deposit complete before publication/evidence. Live execution refreshes current Act 331/PNM instructions.

## Provenance
Every material fact must record source/evidence where applicable. Missing evidence creates a finding or human-decision requirement rather than invented data.
