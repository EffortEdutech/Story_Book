# NPUB-06 — Controlled Copyediting

## Purpose
Correct language and consistency defects while preserving voice, meaning, characterization, plot, dialogue style, and cultural expression.

## Outputs
- copyedited working manuscript (never overwrite source/freeze)
- `copyedit_changes.json`
- `copyedit_queries.json`
- `copyedit_report.md`

## Change classes
- `mechanical_correction`
- `consistency_correction`
- `clarity_suggestion`
- `style_suggestion`
- `continuity_issue`
- `factual_issue`
- `author_decision_required`

## Auto-apply rule
Only high-confidence mechanical/consistency changes authorized by project policy may be auto-applied, and every change must be logged.

## Never auto-apply
Scene rewrites, tone changes, dialogue normalization, plot alteration, character changes, culturally sensitive wording changes, or any correction that may change meaning.

## Query rule
When reasonable editorial choices exist, present options and a recommendation but keep `author_decision_required=true`.

## Regression protection
Track change counts and compare the working manuscript against the frozen baseline so large unexplained deletions/insertions are detected.

## Exit
`COPYEDIT_COMPLETE` when changes are logged and required queries are ready for resolution.