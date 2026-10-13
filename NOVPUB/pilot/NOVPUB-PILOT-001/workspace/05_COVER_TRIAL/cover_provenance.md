# Cover provenance (trial)

Date: 2026-10-13. Pilot: NOVPUB-PILOT-001.

## Source art

- File: `01_The_Blue_Silence/Publish/CoverFront_v3.jpg` (816 x 1312 px, SHA-256 `26d887d16857cc0de8b121478f7299298c9673129e0aacaa4cbad5b08015f1a9`).
- Earlier candidates in the same folder: `CoverFront.jpg` (v1, had AI-rendered text and a division sign), `CoverFront_v2.jpg` (3:4 shape, too small).
- Made by AI. Owner message on 2026-10-13: "use banana to generate the image cover". I understand this as Nano Banana (Google's image model). **Not confirmed.**
- **Prompt: not provided yet.** The owner must save the exact prompt and tool name here before any upload. KDP and IngramSpark require AI-generated images to be disclosed. I have not verified their current rules.
- No people, no logos, no real signage and no text appear in the art.

## What Claude did

- Cropped v3 to the target ratio and enlarged it with Lanczos resampling (about 2x), light sharpening and fine grain.
- Set the title, pen name, tagline and blurb in real fonts (DejaVu Sans Condensed Bold, Caladea). No AI-rendered text is used.
- Built the back cover from a mirrored, darkened and blurred copy of the art, and a plain dark-blue spine.
- Script: `build_script/cover.py`. It needs Pillow, numpy and reportlab, and v3 at the path above.

## Output files

| File | Pixels | SHA-256 |
|---|---|---|
| THE_BLUE_SILENCE_ebook_cover_1600x2560_TRIAL.jpg | 1600 x 2560 | f67412b1299ee6085ca5bf6a928ed3b4c6c828716805bff434f0145ccbc1a18e |
| THE_BLUE_SILENCE_print_wrap_12.785x8.75in_TRIAL.jpg | 3834 x 2624 | f92b09326658203fad9c67c81d1a0c8daf1cca3a06247190f1ba1a51ac94cf8d |
| THE_BLUE_SILENCE_print_cover_wrap_TRIAL.pdf | 12.785 x 8.75 in | 2c30b794a50fe3c3769c6b5efe6aa9bf493abd9ce36ae79bcd0f3e24ce43ad4d |
