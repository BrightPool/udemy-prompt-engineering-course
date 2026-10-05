#!/usr/bin/env node
// Build a notebook-match report from out/curriculum_resolved.json.
//
// We focus on Colab + Github (BrightPool) external-link supplementary assets,
// since those are the two ways the course points to a Jupyter notebook in the
// repo.
//
// Usage:
//   node scripts/udemy-sync/match_notebooks.mjs
//
// Reads:  scripts/udemy-sync/out/curriculum_resolved.json
// Writes: scripts/udemy-sync/out/notebook_matches.json
//         scripts/udemy-sync/out/notebook_matches.md  (human-readable)
import {
  readdirSync,
  statSync,
  readFileSync,
  writeFileSync,
  existsSync,
} from "node:fs";
import { join, basename, relative, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = join(__dirname, "..", "..");
const OUT_DIR = join(__dirname, "out");
const REPO_GITHUB_PREFIX = "github.com/BrightPool/udemy-prompt-engineering-course";

const SKIP_DIRS = new Set([
  "node_modules",
  ".venv",
  ".repro",
  ".ipynb_checkpoints",
  "out",
  "site-packages",
  ".git",
  ".playwright-cli",
]);

function walk(dir, acc = []) {
  for (const name of readdirSync(dir)) {
    if (SKIP_DIRS.has(name)) continue;
    const full = join(dir, name);
    const st = statSync(full);
    if (st.isDirectory()) walk(full, acc);
    else if (name.endsWith(".ipynb")) acc.push(full);
  }
  return acc;
}

function normalize(s) {
  return s
    .toLowerCase()
    .replace(/\.ipynb$/, "")
    .replace(/[^a-z0-9]+/g, "_")
    .replace(/^_+|_+$/g, "");
}

function indexRepoNotebooks() {
  const files = walk(REPO_ROOT);
  const byBase = new Map(); // normalized basename -> [paths...]
  for (const path of files) {
    const rel = relative(REPO_ROOT, path);
    const norm = normalize(basename(path));
    if (!byBase.has(norm)) byBase.set(norm, []);
    byBase.get(norm).push(rel);
  }
  return { files: files.map((p) => relative(REPO_ROOT, p)), byBase };
}

// Pull the repo path out of a github URL pointing at our repo.
function repoPathFromGithubUrl(url) {
  const m = url.match(
    new RegExp(`${REPO_GITHUB_PREFIX.replace(/\./g, "\\.")}/blob/[^/]+/(.+\\.ipynb)$`),
  );
  return m ? decodeURIComponent(m[1]) : null;
}

function classifyExternal(url) {
  if (/colab\.research\.google\.com/.test(url)) return "colab";
  if (new RegExp(REPO_GITHUB_PREFIX.replace(/\./g, "\\.")).test(url))
    return "github_repo";
  if (/github\.com/.test(url)) return "github_external";
  return "other";
}

const data = JSON.parse(
  readFileSync(join(OUT_DIR, "curriculum_resolved.json"), "utf8"),
);
const repo = indexRepoNotebooks();
console.error(`Indexed ${repo.files.length} repo notebooks.`);

const report = [];
for (const lecture of data.lectures) {
  const matches = [];
  for (const a of lecture.supplementary_assets) {
    if (a.asset_type !== "ExternalLink" || !a.external_url) continue;
    const kind = classifyExternal(a.external_url);
    if (kind !== "colab" && kind !== "github_repo") continue;

    let repoPath = null;
    let confidence = "none";

    if (kind === "github_repo") {
      const p = repoPathFromGithubUrl(a.external_url);
      if (p && existsSync(join(REPO_ROOT, p))) {
        repoPath = p;
        confidence = "exact_path";
      } else if (p) {
        // Path in URL doesn't exist — try basename fallback
        const candidates = repo.byBase.get(normalize(basename(p))) ?? [];
        if (candidates.length === 1) {
          repoPath = candidates[0];
          confidence = "basename_unique";
        } else if (candidates.length > 1) {
          repoPath = candidates[0];
          confidence = `basename_ambiguous(${candidates.length})`;
        } else {
          confidence = "url_path_missing_in_repo";
        }
      }
    } else if (kind === "colab") {
      // Title is the basename like "foo_bar.ipynb"
      const norm = normalize(a.title);
      const candidates = repo.byBase.get(norm) ?? [];
      if (candidates.length === 1) {
        repoPath = candidates[0];
        confidence = "basename_unique";
      } else if (candidates.length > 1) {
        repoPath = candidates[0];
        confidence = `basename_ambiguous(${candidates.length})`;
      } else {
        confidence = "no_basename_match";
      }
    }

    matches.push({
      asset_id: a.id,
      asset_title: a.title,
      kind,
      external_url: a.external_url,
      repo_path: repoPath,
      confidence,
    });
  }
  if (matches.length === 0) continue;
  report.push({
    section: lecture.section?.title ?? null,
    lecture_id: lecture.id,
    lecture_title: lecture.title,
    learn_url: lecture.learn_url,
    video: lecture.video
      ? {
          title: lecture.video.title,
          duration: lecture.video.duration,
          download_720p:
            lecture.video.download_urls?.find((d) => d.label === "720")?.file ??
            lecture.video.download_urls?.[0]?.file ??
            null,
        }
      : null,
    notebook_matches: matches,
  });
}

writeFileSync(
  join(OUT_DIR, "notebook_matches.json"),
  JSON.stringify(report, null, 2),
);

// Human-readable Markdown summary.
const counts = { exact_path: 0, basename_unique: 0, ambiguous: 0, missing: 0 };
const lines = [
  `# Udemy ↔ Repo Notebook Matches`,
  ``,
  `Generated from \`out/curriculum_resolved.json\`. Indexed ${repo.files.length} repo notebooks.`,
  ``,
];
for (const r of report) {
  lines.push(`## [${r.lecture_id}] ${r.lecture_title}`);
  lines.push(`Section: *${r.section ?? "—"}*  \nLearn URL: ${r.learn_url}`);
  if (r.video?.duration) lines.push(`Video: ${r.video.title} (${r.video.duration})`);
  for (const m of r.notebook_matches) {
    if (m.confidence === "exact_path") counts.exact_path++;
    else if (m.confidence === "basename_unique") counts.basename_unique++;
    else if (m.confidence.startsWith("basename_ambiguous")) counts.ambiguous++;
    else counts.missing++;
    lines.push(
      `- **${m.confidence}** — \`${m.asset_title}\` (${m.kind}) → ${m.repo_path ?? "??"}`,
    );
    lines.push(`  ${m.external_url}`);
  }
  lines.push("");
}
lines.unshift(
  `**Counts:** ${counts.exact_path} exact_path · ${counts.basename_unique} basename_unique · ${counts.ambiguous} ambiguous · ${counts.missing} unmatched`,
  ``,
);
writeFileSync(join(OUT_DIR, "notebook_matches.md"), lines.join("\n"));

console.error(
  `Lectures with notebook resources: ${report.length}\n` +
    `  exact_path:      ${counts.exact_path}\n` +
    `  basename_unique: ${counts.basename_unique}\n` +
    `  ambiguous:       ${counts.ambiguous}\n` +
    `  unmatched:       ${counts.missing}\n` +
    `→ wrote out/notebook_matches.{json,md}`,
);
