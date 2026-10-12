# NPUB-01 — Manuscript Intake

## Purpose
Establish the manuscript as a controlled publication asset before editorial work begins.

## Required inputs
- Candidate manuscript file(s).
- Any declared master/version information.
- Optional title/author information; do not invent missing values.

## Required outputs
- `02_EDITORIAL/00_INTAKE/manuscript_intake.json`
- `02_EDITORIAL/00_INTAKE/source_inventory.json`
- `02_EDITORIAL/00_INTAKE/intake_report.md`

## Procedure
1. Inventory all candidate source files without modifying them.
2. Determine the likely authoritative source by evidence, not filename aesthetics.
3. If multiple masters conflict, emit `INTAKE-002` and request a human decision.
4. Extract basic statistics: readable status, format, word count, detected chapters, front/back matter, comments/tracked changes, embedded assets.
5. Identify corruption, obvious truncation, duplicate exports, or extraction gaps.
6. Preserve provenance for every source file.
7. Validate `manuscript_intake.json` against its schema.

## Blocking findings
- `INTAKE-001` no readable manuscript.
- `INTAKE-002` ambiguous authoritative source.
- `INTAKE-003` corrupted source.
- `INTAKE-004` materially incomplete extraction.
- `INTAKE-005` source provenance unavailable.

## Human boundary
The agent may recommend the likely master but must not silently choose between materially conflicting manuscript versions.

## Exit
`INTAKE_COMPLETE` only when one authoritative source is identified and preserved.