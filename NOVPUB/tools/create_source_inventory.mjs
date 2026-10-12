import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { basename, extname, join, relative } from "node:path";

const [sourceDir, outDir] = process.argv.slice(2);

if (!sourceDir || !outDir) {
  console.error("Usage: node create_source_inventory.mjs <sourceDir> <outDir>");
  process.exit(2);
}

if (!existsSync(sourceDir)) {
  console.error(`Source directory not found: ${sourceDir}`);
  process.exit(1);
}

function walk(dir) {
  const entries = readdirSync(dir, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name));
  return entries.flatMap((entry) => {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) return walk(path);
    if (entry.isFile()) return [path];
    return [];
  });
}

const files = walk(sourceDir);
const now = new Date().toISOString();

const inventory = files.map((filePath) => {
  const data = readFileSync(filePath);
  const stat = statSync(filePath);
  const name = basename(filePath);
  const role = /manuscript/i.test(filePath) ? "CURRENT_MANUSCRIPT_SOURCE" : "SUPPORTING_PROVENANCE";
  return {
    pilot_id: "NOVPUB-PILOT-001",
    title: "The Blue Silence",
    file_name: name,
    source_path: relative(process.cwd(), filePath).replaceAll("\\", "/"),
    file_type: extname(filePath).replace(".", "").toLowerCase(),
    role,
    size_bytes: stat.size,
    last_modified_local: stat.mtime.toISOString(),
    sha256: createHash("sha256").update(data).digest("hex"),
    baseline_status: role === "CURRENT_MANUSCRIPT_SOURCE" ? "REGISTERED_NOT_FINAL_PUBLICATION_MANUSCRIPT" : "REGISTERED_SUPPORTING_EVIDENCE",
    inventoried_at: now,
  };
});

mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, "the_blue_silence_source_inventory.json"), `${JSON.stringify({ generated_at: now, files: inventory }, null, 2)}\n`);
writeFileSync(
  join(outDir, "the_blue_silence_source_inventory.csv"),
  [
    "pilot_id,title,file_name,source_path,file_type,role,size_bytes,last_modified_local,sha256,baseline_status,inventoried_at",
    ...inventory.map((row) =>
      [
        row.pilot_id,
        row.title,
        row.file_name,
        row.source_path,
        row.file_type,
        row.role,
        row.size_bytes,
        row.last_modified_local,
        row.sha256,
        row.baseline_status,
        row.inventoried_at,
      ]
        .map((value) => `"${String(value).replaceAll('"', '""')}"`)
        .join(",")
    ),
  ].join("\n") + "\n"
);

console.log(`Inventoried ${inventory.length} files`);

