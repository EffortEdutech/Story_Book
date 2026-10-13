# Gate: GATE-P10-01 Real Source Integrity

Status: `PASS`

## Purpose

Prove that `NOVPUB-PILOT-001` uses the actual completed novel manuscript and not a fixture, sample, placeholder, or synthetic substitute.

## Required Evidence

- Manuscript file inventory
- SHA-256 digest for each manuscript source file
- Source location
- Ownership/provenance evidence
- Manuscript freeze record
- Human confirmation that the manuscript is the actual completed novel intended for publication

## Rejection Conditions

- Placeholder manuscript
- Test fixture
- Simulated manuscript
- Synthetic evidence
- Missing digest
- Missing source provenance
- AI-only approval

## Sign-off

- Decision: `PASS`
- Reviewer: eff
- Role: Author / owner of the manuscript
- Date: 2026-10-13
- Scope: manuscript baseline of `The Blue Silence`, 41 files, set SHA-256 `1cd2bbd65bad4b3caacd76514576860f52347c2ed81f85b08c0523828cb24400`, frozen from commit `7d962d7`
- Approval evidence: owner instruction in session (see `approval_register.json`); freeze record `workspace/01_SOURCE/the_blue_silence_manuscript_freeze_record.md`
- AI approver: none
