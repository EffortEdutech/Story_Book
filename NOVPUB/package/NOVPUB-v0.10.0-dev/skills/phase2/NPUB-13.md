# NPUB-13 — Edition Architecture

## Purpose
Define actual publishable products such as Kindle, EPUB, paperback and hardcover, each with a stable `edition_id`.

## Preconditions
- Phase 1 `GATE-02 = PASS` for real manuscript execution.
- Load authoritative upstream records; never infer completion from filenames.

## Outputs
`edition_manifest.json`, `format_decisions.json`

## Deterministic validation
Run applicable Phase 2 validators in `validators/phase2.py` and validate JSON outputs against schemas before changing project state.

## Human / legal boundary
Do not create unused editions. Material changes to format, language, publisher, edition statement or content require edition/identifier review.

## Provenance
Every material fact must record source/evidence where applicable. Missing evidence creates a finding or human-decision requirement rather than invented data.
