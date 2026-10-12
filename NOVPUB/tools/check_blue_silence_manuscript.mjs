import { createHash } from "node:crypto";
import { readdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { basename, join } from "node:path";

const manuscriptDir = "01_The_Blue_Silence/Manuscript";
const outJson = "NOVPUB/pilot/NOVPUB-PILOT-001/workspace/01_SOURCE/the_blue_silence_manuscript_completeness.json";
const outMd = "NOVPUB/pilot/NOVPUB-PILOT-001/workspace/01_SOURCE/the_blue_silence_manuscript_completeness.md";

const files = readdirSync(manuscriptDir, { withFileTypes: true })
  .filter((entry) => entry.isFile() && entry.name.toLowerCase().endsWith(".docx"))
  .map((entry) => join(manuscriptDir, entry.name))
  .sort((a, b) => basename(a).localeCompare(basename(b)));

const chapterFiles = new Map();
let prologueToChapter8 = null;

for (const filePath of files) {
  const name = basename(filePath);
  const range = name.match(/Prologue_Chapter_(\d+)/i);
  if (range) prologueToChapter8 = { through_chapter: Number(range[1]), file_name: name, source_path: filePath.replaceAll("\\", "/") };

  const match = name.match(/Chapter_(\d+)/i);
  if (match) chapterFiles.set(Number(match[1]), { file_name: name, source_path: filePath.replaceAll("\\", "/") });
}

const covered = new Set(chapterFiles.keys());
if (prologueToChapter8) {
  for (let i = 1; i <= prologueToChapter8.through_chapter; i += 1) covered.add(i);
}

const expected = Array.from({ length: 40 }, (_, index) => index + 1);
const missing = expected.filter((chapter) => !covered.has(chapter));

const manifest = files.map((filePath) => {
  const data = readFileSync(filePath);
  const stat = statSync(filePath);
  return {
    file_name: basename(filePath),
    source_path: filePath.replaceAll("\\", "/"),
    size_bytes: stat.size,
    sha256: createHash("sha256").update(data).digest("hex"),
  };
});

const report = {
  pilot_id: "NOVPUB-PILOT-001",
  title: "The Blue Silence",
  checked_at: new Date().toISOString(),
  manuscript_dir: manuscriptDir,
  expected_chapters: "1-40 plus prologue",
  manuscript_docx_file_count: files.length,
  detected_prologue_to_chapter8_bundle: prologueToChapter8,
  individually_detected_chapters: [...chapterFiles.keys()].sort((a, b) => a - b),
  covered_chapters: [...covered].sort((a, b) => a - b),
  missing_chapters: missing,
  completeness_status: missing.length === 0 ? "COMPLETE_CANDIDATE" : "INCOMPLETE_MISSING_CHAPTER_FILES",
  baseline_recommendation:
    missing.length === 0
      ? "Ready for human source confirmation and NOVPUB real-baseline validation."
      : "Do not pass GATE-P10-01 yet. Add missing chapter files or provide one consolidated full manuscript.",
  files: manifest,
};

writeFileSync(outJson, `${JSON.stringify(report, null, 2)}\n`);
writeFileSync(
  outMd,
  `# The Blue Silence Manuscript Completeness\n\n` +
    `Pilot: \`NOVPUB-PILOT-001\`\n\n` +
    `Status: \`${report.completeness_status}\`\n\n` +
    `Detected DOCX manuscript files: \`${files.length}\`\n\n` +
    `Covered chapters: \`${report.covered_chapters.join(", ")}\`\n\n` +
    `Missing chapters: \`${missing.length ? missing.join(", ") : "None"}\`\n\n` +
    `Recommendation: ${report.baseline_recommendation}\n`,
);

console.log(`${report.completeness_status}: missing ${missing.length ? missing.join(", ") : "none"}`);

