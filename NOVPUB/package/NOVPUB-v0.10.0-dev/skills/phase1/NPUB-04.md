# NPUB-04 — Continuity Audit

## Purpose
Build a factual model of the novel and identify contradictions without inventing story facts or rewriting plot.

## Outputs
- `character_registry.json`
- `location_registry.json`
- `timeline_registry.json`
- `terminology_registry.json`
- `continuity_issues.json`
- `continuity_report.md`

## Audit dimensions
Characters, names/aliases, titles/ranks, relationships, established physical facts, locations, chronology, travel/time logic, recurring objects, organisations, and special terminology.

## Certainty
Every inferred continuity fact must use one of: `explicit`, `strongly_supported`, `probable`, `uncertain`.

## Rule
Do not report uncertain inference as established canon. When a contradiction can only be resolved creatively, create an author query rather than selecting an answer.

## Typical findings
`CONT-001` canonical-name conflict; `CONT-002` character-state contradiction; `CONT-003` timeline contradiction; `CONT-004` location contradiction; `CONT-005` relationship contradiction; `CONT-006` terminology inconsistency; `CONT-007` object continuity conflict; `CONT-008` rank/title conflict.

## Exit
`CONTINUITY_REVIEWED` when blocking issues are resolved or explicitly escalated.