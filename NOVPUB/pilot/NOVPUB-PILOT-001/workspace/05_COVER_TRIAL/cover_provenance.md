# Cover provenance (trial)

Date: 2026-10-15. Pilot: NOVPUB-PILOT-001.

## Source art

- File: `01_The_Blue_Silence/Publish/CoverFront_300DPI_v2.png` (1006 x 1564 px, ratio 1.5547, SHA-256 `2be4059eca79c45f59ffba95aa43420eb859e9d0559c59b72aa94f3f38a2e9fd`).
- Replaces v4 (`CoverFront_v4.jpg`, 896 x 1200). Earlier files not used: v1, v2 and v3 of the first set, `CoverFront_300DPI.jpg` (v4 with a 300 dpi label only, same pixels), `CoverFront_300DPI_v1.png` (1024 x 1536).
- Made by AI. Owner message on 2026-10-13: "use banana to generate the image cover". I understand this as Nano Banana (Google's image model). **Not confirmed.**
- Prompt: the owner pasted a prompt written by Claude (text-free corridor, 5:8, dark top and bottom), then asked for 300 dpi versions. **Owner to confirm the tool name and paste the final prompt here.**
- No people, no logos, no signs, no readable text in the art. CCTV cameras and two red fire extinguishers are visible; the extinguisher labels are soft smudges with no legible words.
- The file name says 300 DPI, but the pixel size is 1006 px wide, about 179 ppi across the 5.625 in print front. It is not 300 dpi.

## What Claude did

- Cropped the art to the target shape (the print front needs no extension; the ebook crop trims about 3% of the width).
- Enlarged with Lanczos resampling (1.6x for the ebook, 1.9x for the print front), light sharpening and fine grain.
- Set the title, pen name, tagline and blurb in real fonts (DejaVu Sans Condensed Bold, Caladea). No AI-rendered text.
- Back cover: mirrored, darkened, blurred copy of the art. Spine: plain dark blue.
- Script: `build_script/cover.py`. It needs Pillow, numpy and reportlab, and the source at the path above.

## Output files

| File | Pixels | SHA-256 |
|---|---|---|
| THE_BLUE_SILENCE_ebook_cover_1600x2560_TRIAL.jpg | 1600 x 2560 | 9b54225391aeac0600b346f59e219ebb272ef82c4780f6c4ab428a70b173c52d |
| THE_BLUE_SILENCE_print_wrap_12.785x8.75in_TRIAL.jpg | 3834 x 2624 | 974186d350d75e33938b4cdd258a5eed7c2ae208df73c342a20e4eb8d9279db8 |
| THE_BLUE_SILENCE_print_cover_wrap_TRIAL.pdf | 12.785 x 8.75 in | 451d59f16f71095f4c38483c578c1afc0439d907d529b208e43776050ec21bc6 |

## Owner decisions

- 2026-10-13: spine width 1.535 in confirmed; back-cover blurb approved; trial cover approved (GATE-06 CONDITIONAL).
- 2026-10-15: new art (v2 PNG) supplied. Approval of the rebuilt files: pending owner look.
