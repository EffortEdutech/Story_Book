# NOVPUB — Professional Indie Novel Publishing Skill

NOVPUB is a vendor-neutral, resumable professional novel-publishing workflow for Codex, Claude and compatible agents.

## Current build

**Version:** `0.10.0-dev` — Implementation Batch 10

Implemented: **NPUB-01 through NPUB-96 (Phases 1–10)**.

This build completes the implementation architecture with the real-novel professional pilot layer: pilot workspace instantiation, authoritative manuscript baseline/freeze, real Phase 1–4 evidence, KDP K1–K4 and Ingram I1–I5 pilot controls, real physical-proof/launch readiness, post-publication governance instantiation, pilot defect/remediation, actual Codex/Claude reproducibility certification, and `GATE-NOVPUB-V1`.

**Important:** implementation completeness is not production certification. `GATE-NOVPUB-RC1` and `GATE-NOVPUB-V1` remain PENDING until their real professional-review, real manuscript, proof, agent-run and human-approval evidence exists. The package must not represent `0.10.0-dev` as `1.0.0`.

## Core commands

```bash
python novpub_cli.py init ./MY-NOVEL
python novpub_cli.py init-pilot ./NOVPUB-PILOT-001
python novpub_cli.py status ./NOVPUB-PILOT-001
python novpub_cli.py validate-phase9-package
python novpub_cli.py validate-real-baseline <json>
python novpub_cli.py validate-pilot-evidence <json>
python novpub_cli.py validate-kdp-pilot <json>
python novpub_cli.py validate-ingram-pilot <json>
python novpub_cli.py validate-real-pilot-parity <json>
python novpub_cli.py validate-v1-release <json>
```

## Safety boundary

NOVPUB can prepare, validate and audit publication actions. It cannot self-approve professional review, physical proofs, rights, release certification or irreversible platform transactions. Missing real evidence remains pending.
