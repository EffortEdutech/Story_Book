from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = Path(r"C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe")
RENDERER = Path(r"C:\Users\user\.codex\plugins\cache\openai-primary-runtime\documents\26.909.12148\skills\documents\render_docx.py")
MANUSCRIPT = ROOT / "02_After_Igari" / "Manuscript"
OUT = ROOT / "02_After_Igari" / "Gate" / "rendered_after_remediation"

FILES = [
    "AFTER_IGARI_Chapter_01_The_Message.docx",
    "AFTER_IGARI_Chapter_04_Before_the_Door_Closes_REISSUED.docx",
    "AFTER_IGARI_Chapter_05_Takeoff.docx",
    "AFTER_IGARI_Chapter_06_Cruise.docx",
    "AFTER_IGARI_Chapter_07_Thirty_Five_Thousand_Feet.docx",
    "AFTER_IGARI_Chapter_08_Good_Night.docx",
    "AFTER_IGARI_Chapter_09_IGARI.docx",
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        source = MANUSCRIPT / name
        target = OUT / source.stem
        target.mkdir(parents=True, exist_ok=True)
        print(f"Rendering {name}")
        subprocess.run(
            [str(PYTHON), str(RENDERER), str(source), "--output_dir", str(target), "--emit_pdf"],
            check=True,
        )
        pages = sorted(target.glob("page-*.png"))
        pdfs = sorted(target.glob("*.pdf"))
        print(f"  pages={len(pages)} pdfs={len(pdfs)} out={target}")


if __name__ == "__main__":
    main()
