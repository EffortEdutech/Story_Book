import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";

const root = process.argv[2] ?? "NOVPUB/package/NOVPUB-v0.10.0-dev";
const manifestPath = join(root, "PACKAGE_CHECKSUMS.json");
const manifest = JSON.parse(readFileSync(manifestPath, "utf8"));

const failures = [];

for (const file of manifest.files) {
  const filePath = join(root, file.path);
  if (!existsSync(filePath)) {
    failures.push(`missing: ${file.path}`);
    continue;
  }

  const data = readFileSync(filePath);
  const sha256 = createHash("sha256").update(data).digest("hex");
  if (sha256 !== file.sha256 || data.length !== file.size) {
    failures.push(`mismatch: ${file.path}`);
  }
}

if (failures.length > 0) {
  console.error(`FAILED: ${failures.length}/${manifest.files.length} files failed`);
  console.error(failures.slice(0, 50).join("\n"));
  process.exit(1);
}

console.log(`PASS: ${manifest.files.length}/${manifest.files.length} files verified`);

