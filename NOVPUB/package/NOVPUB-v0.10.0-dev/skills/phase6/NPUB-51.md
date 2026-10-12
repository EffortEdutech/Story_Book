# NPUB-51 — Ingram Title & Metadata Configuration

## Purpose
Map the approved metadata master into Ingram title metadata, BISAC/Thema, contributors, audience, publication/on-sale dates and territories without allowing channel drift.

## Preconditions
- `GATE-03`, `GATE-04`, `GATE-05`, `GATE-06`, and `GATE-07` must be `PASS` for live wholesale execution.
- Consume canonical rights, edition/ISBN, production and commercial artefacts; IngramSpark is never the upstream source of identity truth.
- Refresh the relevant current IngramSpark rule snapshot immediately before live account, commercial, file, proof or distribution actions.

## Outputs
- `ingram_title_metadata.json`
- `contributor_map.json`
- `subject_map.json`
- `keyword_map.json`
- `metadata_validation.json`

## Deterministic controls
- Validate ISBN, edition, metadata, manufacturing, pricing and approved asset-hash parity.
- Treat eProof as a digital manufacturing preview, not as evidence that a physical copy was inspected.
- Preserve the KDP/Ingram coexistence invariant: same print edition + publisher-owned ISBN, with KDP Expanded Distribution disabled when Ingram distributes that ISBN.
- Record return exposure, rule provenance and every live commercial mutation.

## Human boundary
Wholesale discount, returnability, return method, market activation, eProof acceptance, physical-proof acceptance and distribution activation remain explicit human decisions.

## Security
Do not store passwords, MFA secrets, bank credentials, or full sensitive account identifiers in NOVPUB project artefacts.
