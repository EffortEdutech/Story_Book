# Foundation Runtime

## Runtime model

`Project -> State -> Eligible Skill -> Inputs -> Outputs -> Validators -> Findings -> Human Decisions -> Gate -> Next State`

## Core root records

- `project_manifest.json` — identity/configuration for a publication project.
- `publishing_state.json` — current phase/state/gate summary.
- `decision_log.jsonl` — append-only material human/agent decisions.
- `issue_register.json` — open/resolved findings.
- `approval_register.json` — human approvals and evidence.
- `artifact_manifest.json` — authoritative/superseded artefact map.

## Invariants

1. No source manuscript overwrite.
2. No silent literary rewrite.
3. No invented identifiers/evidence.
4. Human gates cannot be self-approved by an agent.
5. Gate PASS requires evidence.
6. Active artefacts must be traceable to a producer and source.
7. Later phases consume upstream locks and do not redefine them.
8. Platform rules are versioned snapshots.
9. Historical records are retained.
10. Resume uses persisted state, not conversational memory.
