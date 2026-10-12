# NPUB-07 — Final Proofreading

## Purpose
Perform minimum-intervention final-language verification after copyedit decisions are resolved.

## Outputs
- proof working manuscript
- `proof_changes.json`
- `proof_report.md`

## Scope
Typos, punctuation, spelling, capitalization, accidental missing/duplicate words, headings, scene separators, paragraph breaks, spacing, malformed quotation marks, residual comments/annotations, and unresolved placeholders.

## Principle
Proofreading is not a second copyedit. Substantial rewriting or meaning-level issues return to editorial reconciliation.

## Regression checks
- chapter count/order unchanged unless approved;
- no paragraph/scene lost;
- no unintended mass replacement;
- no new continuity conflict introduced;
- protected style features remain protected.

## Proof finding classes
`typo`, `punctuation`, `spelling`, `formatting`, `heading`, `spacing`, `unresolved_annotation`, `possible_editorial_issue`.

## Exit
`PROOFREAD_COMPLETE`.