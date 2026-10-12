# NPUB-14 — ISBN Registry & Assignment Control

## Purpose
Maintain permanent ISBN provenance and bind each verified ISBN to one specific edition identity.

## Preconditions
- Phase 1 `GATE-02 = PASS` for real manuscript execution.
- Load authoritative upstream records; never infer completion from filenames.

## Outputs
`isbn_registry.json`, `isbn_assignments.json`, `isbn_evidence/`

## Deterministic validation
Run applicable Phase 2 validators in `validators/phase2.py` and validate JSON outputs against schemas before changing project state.

## Human / legal boundary
NOVPUB must never fabricate an ISBN. An identifier may enter the registry only from verified allocation or existing-edition evidence. Paperback and hardcover cannot silently share the same ISBN.

## Provenance
Every material fact must record source/evidence where applicable. Missing evidence creates a finding or human-decision requirement rather than invented data.
