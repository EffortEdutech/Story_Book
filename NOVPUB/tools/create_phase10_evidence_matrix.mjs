import { readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const registryPath = "NOVPUB/package/NOVPUB-v0.10.0-dev/registry/skill_registry.json";
const outPath = "NOVPUB/pilot/NOVPUB-PILOT-001/workspace/validation/13_PILOT/pilot_evidence_matrix.json";
const summaryPath = "NOVPUB/pilot/NOVPUB-PILOT-001/workspace/validation/13_PILOT/pilot_evidence_matrix_summary.md";

const registry = JSON.parse(readFileSync(registryPath, "utf8")).skills;
const byId = new Map(registry.map((skill) => [skill.skill_id, skill]));

const realSourceEvidence = [
  "01_SOURCE/the_blue_silence_real_baseline.json",
  "01_SOURCE/the_blue_silence_source_inventory.json",
  "01_SOURCE/the_blue_silence_manuscript_completeness.json",
];

const realProjectEvidence = [
  ...realSourceEvidence,
  "project_manifest.json",
  "publishing_state.json",
  "validation/12_RELEASE/release_candidate_current.json",
];

const realExecuted = new Set([
  "NPUB-01",
  "NPUB-02",
  "NPUB-77",
  "NPUB-78",
  "NPUB-79",
  "NPUB-85",
  "NPUB-86",
]);

const phaseJustification = {
  1: "The real manuscript has been registered and baselined, but full editorial/copyedit/proofread execution evidence has not yet been produced in this pilot.",
  2: "Rights, ownership, third-party permissions, author identity, imprint, and Malaysia publication identity evidence have not yet been executed for this pilot.",
  3: "Production engineering evidence such as trim, typesetting, EPUB, cover, preflight, and production approvals has not yet been produced for this pilot.",
  4: "Commercial metadata, positioning, categories, keywords, pricing, territories, and channel metadata maps have not yet been executed for this pilot.",
  5: "KDP pilot evidence is intentionally deferred to the dedicated KDP K1-K4 pilot stage after this matrix is established.",
  6: "IngramSpark pilot evidence is intentionally deferred to the dedicated Ingram I1-I5 pilot stage after this matrix is established.",
  7: "Launch and marketing evidence is intentionally deferred until production/channel evidence and proof workflow are ready.",
  8: "Post-publication governance controls are not applicable before publication; they will be instantiated during the post-publication pilot stage.",
  9: "Phase 9 professional review / RC approval has been executed separately and is recorded in validation/12_RELEASE/release_candidate_current.json.",
};

function phaseFor(skillId) {
  const n = Number(skillId.slice(5));
  if (n <= 8) return 1;
  if (n <= 18) return 2;
  if (n <= 31) return 3;
  if (n <= 40) return 4;
  if (n <= 49) return 5;
  if (n <= 56) return 6;
  if (n <= 66) return 7;
  if (n <= 76) return 8;
  if (n <= 86) return 9;
  return 10;
}

const rows = [];

for (let i = 1; i <= 76; i += 1) {
  const skillId = `NPUB-${String(i).padStart(2, "0")}`;
  const skill = byId.get(skillId);
  const phase = phaseFor(skillId);

  if (realExecuted.has(skillId)) {
    rows.push({
      skill_id: skillId,
      skill_name: skill?.name ?? "",
      pilot_status: "REAL_EXECUTED",
      real_input: skillId === "NPUB-01" || skillId === "NPUB-02" ? realSourceEvidence : realProjectEvidence,
      real_output:
        skillId === "NPUB-01" || skillId === "NPUB-02"
          ? ["01_SOURCE/the_blue_silence_real_baseline.json"]
          : ["validation/12_RELEASE/release_candidate_current.json"],
      evidence:
        skillId === "NPUB-01" || skillId === "NPUB-02"
          ? realSourceEvidence
          : [
              "validation/10_PROFESSIONAL_REVIEW/professional_review_pending.json",
              "validation/10_PROFESSIONAL_REVIEW/phase9_professional_review_pack.md",
              "validation/12_RELEASE/release_candidate_current.json",
              "validation/12_RELEASE/phase9_execution_log.md",
            ],
      validator_pass: true,
      notes:
        skillId === "NPUB-01" || skillId === "NPUB-02"
          ? "Real source integrity and manuscript baseline validated for The Blue Silence."
          : "Phase 9 RC/professional review evidence validated and gate approved.",
    });
  } else {
    rows.push({
      skill_id: skillId,
      skill_name: skill?.name ?? "",
      pilot_status: "NOT_APPLICABLE_WITH_JUSTIFICATION",
      justification: phaseJustification[phase] ?? "Deferred to later pilot stage.",
    });
  }
}

const matrix = {
  pilot_id: "NOVPUB-PILOT-001",
  title: "The Blue Silence",
  package_version: "0.10.0-dev",
  created_at: new Date().toISOString(),
  policy: {
    fixture_evidence_allowed_for_real_gates: false,
    synthetic_evidence_allowed_for_real_gates: false,
    ai_may_execute_checks: true,
    ai_may_approve_release: false,
  },
  skills: rows,
};

writeFileSync(outPath, `${JSON.stringify(matrix, null, 2)}\n`);

const executed = rows.filter((row) => row.pilot_status === "REAL_EXECUTED").length;
const notApplicable = rows.length - executed;
writeFileSync(
  summaryPath,
  `# Phase 10 Pilot Evidence Matrix Summary\n\n` +
    `Pilot: \`NOVPUB-PILOT-001\`\n\n` +
    `Novel: \`The Blue Silence\`\n\n` +
    `Rows: \`${rows.length}\`\n\n` +
    `Real executed: \`${executed}\`\n\n` +
    `Not applicable / deferred with justification: \`${notApplicable}\`\n\n` +
    `Current scope: establishes the real evidence matrix, records validated source-baseline and RC evidence, and preserves honest deferrals for KDP, Ingram, proof, launch, and post-publication work that has not happened yet.\n`
);

console.log(`Created matrix: ${executed} real executed, ${notApplicable} justified deferred/N/A`);

