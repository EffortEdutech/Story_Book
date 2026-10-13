# Interior trial build: preflight report

Date: 2026-10-13. Status: **BUILT, automated checks passed. Not approved.** GATE-05 stays PENDING until the owner reviews the proof.

## What was built

- `THE_BLUE_SILENCE_interior_5.5x8.5_TRIAL.pdf`: 614 pages, 5.5 x 8.5 in.
- `THE_BLUE_SILENCE_TRIAL.epub`: EPUB 3.3, reflowable, no cover image yet.

## Checks run (all by script, results real)

| Check | Result |
|---|---|
| Source files = frozen baseline (41 files, set hash 1cd2bbd6...4400) | PASS |
| PDF text equals manuscript text (469,144 letters and digits, header and page numbers excluded) | PASS |
| EPUB text equals manuscript text (same count) | PASS |
| epubcheck 5.3.0 | PASS: 0 fatals, 0 errors, 0 warnings |
| PDF trim size | 5.5 x 8.5 in on all pages |
| PDF fonts | Caladea Regular, Bold, Italic: all embedded and subset. No unembedded fonts |
| All 41 chapters open on a right-hand (odd) page | PASS |
| Even page count | PASS (614) |
| Glyph coverage (85 distinct characters in the manuscript) | PASS, none missing |
| Contents page numbers match actual chapter pages | PASS (built in two passes) |

## NOVPUB's own validators (same files, run 2026-10-13)

- `novpub preflight-pdf --width 5.5 --height 8.5 --pages 614`: passed, 0 errors, 0 warnings.
- `novpub validate-epub`: passed, 0 errors, 0 warnings. It reports `reading_qa: PENDING`, meaning a human still has to read the EPUB on a device or reader app.

## Layout

- 10 pt Caladea on 13.5 pt leading, justified, hyphenated (en-GB).
- Margins: inside 0.80 in, outside 0.55 in, top 0.65 in, bottom 0.75 in.
- Front matter (6 pages, unnumbered): half title, blank, title page with "A Novel", copyright page, contents (2 pages). Page 1 is the Prologue.
- Dropped from the interior: the "END CHAPTER X" lines and trailing "* * *" at the end of Ch2-8. "END OF BOOK ONE" is kept.
- Bold centred document inserts (Prologue and Ch1) are set as small bold centred lines.
- 22 blank pages come from chapters starting on right-hand pages.

## Not verified, so do not treat as done

- KDP and IngramSpark upload validators have not been run. Only the owner can do that with a real account.
- No physical proof exists. GATE-08 is far off.
- Margin rule: I used 0.80 in inside. KDP's published minimum for 501-700 pages is 0.75 in (from memory, verify on KDP's page).
- Cream paper spine estimate: 614 pages x 0.0025 in = 1.535 in. Verify with the KDP cover calculator before making the cover.
- Page count is high (614) because the book has many one-line paragraphs. It raises the print cost and spine width. Options: smaller type, or 6 x 9 in trim. This is an owner decision.
- The "TRIAL BUILD" line is on the copyright page of both files and must be removed for V1.
