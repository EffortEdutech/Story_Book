# Cover QA (trial) - automated and visual checks by Claude

Status: **BUILT. Not approved.** GATE-06 stays PENDING until the owner approves the cover files.

## Checks done

- Ebook cover is 1600 x 2560 px, RGB JPEG, ratio 1.6. The title and pen name are readable at 160 px wide (thumbnail test).
- Print wrap is 3834 x 2624 px at 300 dpi (12.78 x 8.75 in). Layout: 0.125 in bleed, 5.5 in back, 1.535 in spine, 5.5 in front, 0.125 in bleed.
- Spine text fits inside the spine with clear margins. Title and pen name do not overlap.
- Back-cover text sits at least 0.55 in inside the trim. A 2 x 1.2 in white barcode area is left at the bottom right.
- No gun, no blood, no signage, no AI-rendered text. (v3's police-division sign problem does not exist in v4.)

## Open problems (do not approve until these are settled)

1. **Spine width 1.535 in:** confirmed by the owner on 2026-10-13. Re-check on the KDP calculator and IngramSpark template before V1.
2. **Low source resolution:** the v4 art is 896 px wide across a 5.625 in front, about 159 ppi. KDP and IngramSpark may warn about low resolution. The owner chose to keep it for the trial. For V1, upscale with a proper AI upscaler or regenerate at 1650 x 2550 px or larger.
2b. **Extended ceiling and floor:** v4 is 3:4, so about 20% of the height is synthetic dark extension (mirrored and blurred). A faint seam can be seen in the ebook cover near the top. Check it.
2c. **Author name on the front** crosses the first ceiling light. It is readable but busy. Move it if you prefer.
3. **Barcode:** the white box is a placeholder. KDP can add its own barcode. IngramSpark needs the ISBN barcode.
4. **ISBNs missing:** the copyright page still has placeholders.
5. **Back-cover blurb:** approved by the owner on 2026-10-13.
6. **AI disclosure:** tool name unconfirmed and prompt not saved (see cover_provenance.md).
7. **Printed colours:** deep blues often print darker than on screen. Only a physical proof can settle this (GATE-08).
8. **Size check:** the PDF page is exactly 12.785 x 8.75 in. The image is 0.04% smaller than that. Replace it with KDP's exact size once known.
