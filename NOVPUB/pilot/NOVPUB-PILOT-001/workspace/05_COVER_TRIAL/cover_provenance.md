# Cover provenance (trial)

Date: 2026-10-13. Pilot: NOVPUB-PILOT-001.

## Source art

- File: `01_The_Blue_Silence/Publish/CoverFront_v4.jpg` (896 x 1200 px, 3:4, SHA-256 `af131bac2133784e586a61393bc0f292b85404a3147c7f565a47781d54027d9e`).
- Replaces v3 (`CoverFront_v3.jpg`, 816 x 1312 px) as the cover source. v1 and v2 are not used.
- Made by AI. Owner message on 2026-10-13: "use banana to generate the image cover". I understand this as Nano Banana (Google's image model). **Not confirmed.**
- Prompt used for v4: I wrote it and the owner pasted it into the tool (text-free corridor, 5:8, dark top and bottom). Keep the exact text with the file. **Owner to confirm the tool name and paste the final prompt here.**
- The tool returned 896 x 1200, not the 1600 x 2560 asked for.
- No people, no logos, no signs, no readable text in the art. CCTV cameras and two red fire extinguishers are visible.
- The two extinguisher labels are tiny and unreadable. Check them at full size.

## What Claude did

- Added extra dark ceiling above and dark floor below (mirrored, blurred, darkened) to reach 1:1.6. The art itself is unchanged in the middle.
- Enlarged with Lanczos resampling (about 1.8x), light sharpening and fine grain.
- Set the title, pen name, tagline and blurb in real fonts (DejaVu Sans Condensed Bold, Caladea). No AI-rendered text.
- Back cover: mirrored, darkened, blurred copy of the art. Spine: plain dark blue.
- Script: `build_script/cover.py`. It needs Pillow, numpy and reportlab, and v4 at the path above.

## Output files

| File | Pixels | SHA-256 |
|---|---|---|
| THE_BLUE_SILENCE_ebook_cover_1600x2560_TRIAL.jpg | 1600 x 2560 | a367673281fac6b10a528938b02d01ec777d7f8f7608d747c512c96f0ef2a3c8 |
| THE_BLUE_SILENCE_print_wrap_12.785x8.75in_TRIAL.jpg | 3834 x 2624 | 1c04476e0d00d90baab200f7d87054468e84058576e8751b920a7fbfa6dad201 |
| THE_BLUE_SILENCE_print_cover_wrap_TRIAL.pdf | 12.785 x 8.75 in | 2d53cdb049df8320e5d6650923a56e8555db04cfc5163025193dc12630c6d38d |

## Owner decisions (2026-10-13)

- Spine width 1.535 in: confirmed by owner.
- Keep this low-resolution art for the trial (Option B).
- Back-cover blurb: approved.
