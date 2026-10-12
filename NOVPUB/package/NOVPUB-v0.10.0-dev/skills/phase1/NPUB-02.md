# NPUB-02 — Manuscript Freeze

## Purpose
Create the immutable editorial baseline.

## Inputs
- NPUB-01 authoritative source.
- Intake record.

## Outputs
- `manuscript_freeze.json`
- `manuscript_manifest.json`
- `checksums.json`
- frozen source copy or immutable source reference.

## Procedure
1. Copy/reference the authoritative source into the freeze area without editing it.
2. Compute SHA-256 of the source and frozen copy.
3. Verify expected identity/equivalence.
4. Record word/chapter counts and freeze timestamp.
5. Allocate a unique freeze ID.
6. Create the editorial working copy separately.
7. Register frozen source in the artifact manifest as authoritative and immutable.

## Rules
- Never edit the frozen baseline in place.
- A material author revision creates a new freeze/version; it does not replace the historical freeze.
- Hash mismatch is blocking unless an explicitly documented transformation explains it.

## Findings
`FREEZE-001` missing hash; `FREEZE-002` unexpected source/freeze difference; `FREEZE-003` extraction materially changed text; `FREEZE-004` baseline changed after freeze; `FREEZE-005` incomplete freeze metadata.

## Exit
`MANUSCRIPT_FROZEN`.