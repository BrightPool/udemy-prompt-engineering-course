#!/usr/bin/env node
// Download all course videos at concurrency 10 into scripts/udemy-sync/videos/.
//
// Usage:
//   node scripts/udemy-sync/download_videos.mjs              # all 219 lectures
//   node scripts/udemy-sync/download_videos.mjs --matched    # only the 97 lectures with notebook resources
//
// - Always refreshes signed URLs from Udemy (URLs in curriculum_resolved.json
//   may have expired since the last resolve).
// - Skips any .mp4 already on disk with a non-zero size.
// - Uses 720p when available, falls back to highest-quality variant.
// - Folder layout: videos/<sectionIdx>_<section>/<lectureIdx>_<lectureId>_<lecture>.mp4
import { readFileSync, mkdirSync, existsSync, statSync, createWriteStream, unlinkSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";
import { Readable } from "node:stream";

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUT_DIR = join(__dirname, "out");
const VIDEOS_DIR = join(__dirname, "videos");
const COURSE_ID = 5238734;
const SESSION = "udemy";
const CONCURRENCY = 10;

const argv = new Set(process.argv.slice(2));
const MATCHED_ONLY = argv.has("--matched");

mkdirSync(VIDEOS_DIR, { recursive: true });

function pwEval(jsExpr) {
  const r = spawnSync("playwright-cli", ["-s=" + SESSION, "eval", jsExpr], {
    encoding: "utf8",
    maxBuffer: 64 * 1024 * 1024,
  });
  if (r.status !== 0) throw new Error(`playwright-cli eval failed: ${r.stderr}`);
  const m = r.stdout.match(/### Result\n([\s\S]*?)\n### Ran/);
  if (!m) throw new Error("Could not parse playwright-cli output:\n" + r.stdout);
  return JSON.parse(JSON.parse(m[1]));
}

function slug(s) {
  return s
    .toLowerCase()
    .replace(/&/g, "and")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80);
}

function pad(n, w) {
  return String(n).padStart(w, "0");
}

console.error("Refreshing curriculum (fresh signed URLs)...");
const fields = new URLSearchParams({
  curriculum_types: "chapter,lecture",
  page_size: "1400",
  "fields[chapter]": "title,object_index",
  "fields[lecture]": "asset,title,object_index",
  "fields[asset]": "asset_type,download_urls,filename,title,content_summary",
});
const fresh = pwEval(`async () => {
  const r = await fetch('https://www.udemy.com/api-2.0/courses/${COURSE_ID}/instructor-curriculum-items/?${fields}', {credentials:'include'});
  return JSON.stringify({status: r.status, body: await r.json()});
}`);
if (fresh.status !== 200) throw new Error("Curriculum fetch failed: " + fresh.status);

let currentSection = null;
const jobs = [];
for (const item of fresh.body.results) {
  if (item._class === "chapter") {
    currentSection = { index: item.object_index, title: item.title };
  } else if (item._class === "lecture" && item.asset?.asset_type === "Video") {
    const variants = item.asset.download_urls?.Video ?? [];
    const pick =
      variants.find((v) => v.label === "720") ??
      variants.find((v) => v.label === "1080") ??
      variants.find((v) => v.label === "480") ??
      variants[0];
    if (!pick) continue;
    jobs.push({
      sectionIdx: currentSection?.index ?? 0,
      sectionTitle: currentSection?.title ?? "untitled",
      lectureIdx: item.object_index,
      lectureId: item.id,
      lectureTitle: item.title,
      url: pick.file,
      label: pick.label,
    });
  }
}

let plan = jobs;
if (MATCHED_ONLY) {
  const matchesPath = join(OUT_DIR, "notebook_matches.json");
  if (!existsSync(matchesPath))
    throw new Error("--matched requires out/notebook_matches.json (run match_notebooks.mjs first)");
  const matched = new Set(
    JSON.parse(readFileSync(matchesPath, "utf8")).map((l) => l.lecture_id),
  );
  plan = jobs.filter((j) => matched.has(j.lectureId));
}

console.error(`Plan: ${plan.length} videos to consider (matched_only=${MATCHED_ONLY}).`);

let done = 0,
  skipped = 0,
  failed = 0;
const total = plan.length;

async function downloadOne(job) {
  const sectionDir = join(
    VIDEOS_DIR,
    `${pad(job.sectionIdx, 2)}_${slug(job.sectionTitle)}`,
  );
  mkdirSync(sectionDir, { recursive: true });
  const filename = `${pad(job.lectureIdx, 3)}_${job.lectureId}_${slug(job.lectureTitle)}.mp4`;
  const target = join(sectionDir, filename);

  if (existsSync(target) && statSync(target).size > 0) {
    skipped++;
    process.stderr.write(`SKIP  [${done + skipped + failed}/${total}] ${filename}\n`);
    return;
  }

  const tmp = target + ".part";
  try {
    const r = await fetch(job.url);
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const body = Readable.fromWeb(r.body);
    const out = createWriteStream(tmp);
    await new Promise((resolve, reject) => {
      body.pipe(out);
      body.on("error", reject);
      out.on("error", reject);
      out.on("finish", resolve);
    });
    const { renameSync } = await import("node:fs");
    renameSync(tmp, target);
    done++;
    const mb = (statSync(target).size / 1e6).toFixed(1);
    process.stderr.write(
      `DONE  [${done + skipped + failed}/${total}] ${filename} (${mb} MB, ${job.label}p)\n`,
    );
  } catch (e) {
    failed++;
    if (existsSync(tmp)) unlinkSync(tmp);
    process.stderr.write(
      `FAIL  [${done + skipped + failed}/${total}] ${filename} — ${e.message}\n`,
    );
  }
}

// Simple promise pool
async function runPool(items, n, fn) {
  const queue = items.slice();
  const workers = Array.from({ length: n }, async () => {
    while (queue.length) await fn(queue.shift());
  });
  await Promise.all(workers);
}

await runPool(plan, CONCURRENCY, downloadOne);

console.error(
  `\nFinished. downloaded=${done} skipped=${skipped} failed=${failed} total=${total}`,
);
