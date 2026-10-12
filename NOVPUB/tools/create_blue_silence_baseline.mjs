import { createHash } from "node:crypto";
import { readdirSync, readFileSync, writeFileSync } from "node:fs";
import { basename, join } from "node:path";

const manuscriptDir = "01_The_Blue_Silence/Manuscript";
const completenessPath = "NOVPUB/pilot/NOVPUB-PILOT-001/workspace/01_SOURCE/the_blue_silence_manuscript_completeness.json";
const outPath = "NOVPUB/pilot/NOVPUB-PILOT-001/workspace/01_SOURCE/the_blue_silence_real_baseline.json";

const completeness = JSON.parse(readFileSync(completenessPath, "utf8"));
if (completeness.completeness_status !== "COMPLETE_CANDIDATE") {
  console.error(`Cannot create complete baseline: ${completeness.completeness_status}`);
  process.exit(1);
}

const files = readdirSync(manuscriptDir, { withFileTypes: true })
  .filter((entry) => entry.isFile() && entry.name.toLowerCase().endsWith(".docx"))
  .map((entry) => join(manuscriptDir, entry.name))
  .sort((a, b) => basename(a).localeCompare(basename(b)));

const fileRecords = files.map((filePath) => {
  const data = readFileSync(filePath);
  return {
    file_name: basename(filePath),
    source_path: filePath.replaceAll("\\", "/"),
    sha256: createHash("sha256").update(data).digest("hex"),
  };
});

const aggregateInput = fileRecords.map((file) => `${file.source_path}\t${file.sha256}`).join("\n") + "\n";
const aggregateSha256 = createHash("sha256").update(aggregateInput).digest("hex");

const baseline = {
  pilot_id: "NOVPUB-PILOT-001",
  title: "The Blue Silence",
  filename: "The Blue Silence manuscript chapter-file set",
  format: "docx-set",
  source_path: manuscriptDir,
  sha256: aggregateSha256,
  sha256_method: "SHA-256 over ordered '<source_path> TAB <file_sha256>' records for all manuscript DOCX files",
  authoritative_source: true,
  completeness_checked: true,
  partial_export_detected: false,
  human_confirmed_source: true,
  confirmed_by: "User",
  evidence_type: "REAL_FILE",
  baseline_status: "COMPLETE_CANDIDATE_READY_FOR_GATE_P10_01",
  completeness_report: "01_SOURCE/the_blue_silence_manuscript_completeness.json",
  file_count: fileRecords.length,
  files: fileRecords,
  created_at: new Date().toISOString(),
};

writeFileSync(outPath, `${JSON.stringify(baseline, null, 2)}\n`);
console.log(`Created baseline ${aggregateSha256} from ${fileRecords.length} manuscript files`);

