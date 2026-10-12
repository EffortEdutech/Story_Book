# NOVPUB — Agent Operating Contract

## When to invoke NOVPUB

Use NOVPUB when the task is to publish, prepare, validate, distribute, launch, maintain, or revise a novel/book publication under the NOVPUB workflow. NOVPUB is designed for independent publishing and its v1.0 target channels are Amazon KDP + IngramSpark with Malaysia publishing/compliance support.

## Mandatory startup sequence

1. Locate the project root.
2. Read `publishing_state.json`.
3. Read `project_manifest.json`.
4. Validate current state and gate evidence before acting.
5. Load the relevant authoritative artefacts and hashes.
6. Determine the next eligible skill from `registry/skill_registry.json`.
7. Run deterministic validation before making judgment calls.
8. Stop at any required human-decision boundary.
9. Persist outputs, issue records, decisions, approvals, and state changes.
10. Never infer completion from filenames alone.

## Source-of-truth hierarchy

1. Phase/foundation policy and human approvals.
2. Authoritative manuscript freeze / editorial-approved manuscript.
3. Rights, publisher, edition, ISBN records.
4. Production locks and approved assets.
5. Commercial metadata lock.
6. Channel submission freezes.
7. Live-channel snapshots.
8. Post-publication change events.

When a downstream value conflicts with an upstream authoritative record, emit `SOURCE_OF_TRUTH_CONFLICT`; do not silently overwrite upstream data.

## Human approval boundaries

The agent must not autonomously:

- approve the final manuscript;
- declare or assign rights without evidence;
- invent or reassign ISBNs;
- choose/alter publisher identity or pen-name strategy;
- approve final cover or physical proof;
- enroll KDP Select;
- enable KDP Expanded Distribution;
- choose Ingram returnability/return method;
- change live prices or territories;
- submit/publish/unpublish a live edition;
- authorize spend or paid transactions;
- fabricate PNM/MyIPO/platform evidence.

## Author voice protection

Literary text is controlled content. The agent may identify, classify, explain, or propose changes. It may auto-apply only high-confidence mechanical/consistency corrections allowed by project policy and must log them. It must not silently normalize dialect, rewrite dialogue, change plot/characterization, or alter cultural expression.

## Rule freshness

KDP, IngramSpark, PNM, MyIPO and other external requirements are adapters. Before any live submission or materially time-sensitive calculation, refresh relevant official rules and store a rule snapshot. If a critical current rule cannot be verified, block the live transaction rather than guessing.

## Resumability

On resume, validate existing artefacts and gate evidence. Do not recreate identifiers, approvals, or files merely because a new session began. If an action status is `UNKNOWN`, reconcile it before repeating a potentially irreversible transaction.

## Current implementation coverage

This build implements the full Phase 1–10 architecture (`NPUB-01`–`NPUB-96`). Implementation completeness does not equal production certification: `GATE-NOVPUB-RC1` and `GATE-NOVPUB-V1` require real evidence and human approval.

## Implemented through Phase 10
`NPUB-01` through `NPUB-96` are implemented. Phase 10 instantiates and validates a real-novel pilot, requires real manuscript/proof/platform/agent evidence, records pilot defects, compares actual Codex and Claude runs, and evaluates `GATE-NOVPUB-V1`. The package must remain `0.10.0-dev` until real professional review and pilot release evidence support a human-approved `1.0.0` freeze.
