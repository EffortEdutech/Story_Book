# NPUB-03 — Structural Integrity Audit

## Purpose
Verify the manuscript is structurally intact as a document without judging whether the story is creatively good.

## Outputs
- `chapter_manifest.json`
- `structural_audit.json`
- `structural_audit_report.md`

## Checks
- Chapter IDs/order/headings and duplicate/missing/empty chapters.
- Duplicate manuscript blocks.
- Unresolved editing placeholders or notes-to-self.
- Comments/tracked-change residue where accessible.
- Broken scene separators and malformed section structure.
- Apparent truncation or accidental repeated content.
- Front/back matter represented as complete but actually incomplete.

## Placeholder handling
Search configurable patterns such as TODO/TBD/FIXME/INSERT/CHECK/REWRITE but inspect context to avoid false positives.

## Finding fields
`finding_id`, `location`, `type`, `severity`, `evidence`, `recommendation`, `requires_author_decision`, `status`.

## Blocking rule
All structural `blocking` findings must be resolved before controlled copyediting begins.

## Prohibition
Do not perform developmental rewriting to 'fix' a structural issue. Raise the issue to the author/editor when creative intent is involved.

## Exit
`STRUCTURE_CLEARED`.