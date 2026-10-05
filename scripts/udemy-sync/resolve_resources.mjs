#!/usr/bin/env node
// Resolve supplementary-asset details (external URLs etc.) for every lecture
// in out/curriculum.json. Uses the playwright-cli `udemy` session so that
// browser cookies authenticate the fetch.
//
// Usage:
//   node scripts/udemy-sync/resolve_resources.mjs
//
// Reads:  scripts/udemy-sync/out/curriculum.json
// Writes: scripts/udemy-sync/out/curriculum_resolved.json
import { readFileSync, writeFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUT_DIR = join(__dirname, "out");
const COURSE_ID = 5238734;
const COURSE_SLUG = "prompt-engineering-for-ai";
const SESSION = "udemy";

function pwEval(jsExpr) {
  const r = spawnSync("playwright-cli", ["-s=" + SESSION, "eval", jsExpr], {
    encoding: "utf8",
    maxBuffer: 64 * 1024 * 1024,
  });
  if (r.status !== 0) throw new Error(`playwright-cli eval failed: ${r.stderr}`);
  // Output blocks: ### Result\n<json string>\n### Ran ...
  const m = r.stdout.match(/### Result\n([\s\S]*?)\n### Ran/);
  if (!m) throw new Error("Could not parse playwright-cli output:\n" + r.stdout);
  // The result is a JSON-encoded string (because eval returned a string)
  return JSON.parse(JSON.parse(m[1]));
}

// Each item: {assetId, lectureId}
async function resolveBatch(items) {
  const expr = `async () => {
    const items = ${JSON.stringify(items)};
    const courseId = ${COURSE_ID};
    const out = {};
    await Promise.all(items.map(async ({assetId, lectureId}) => {
      const fields = '?fields[asset]=external_url,source_url,asset_type,filename,title,download_urls,is_external';
      const tryUrls = [
        'https://www.udemy.com/api-2.0/assets/' + assetId + '/' + fields,
        'https://www.udemy.com/api-2.0/users/me/subscribed-courses/' + courseId + '/lectures/' + lectureId + '/supplementary-assets/' + assetId + '/' + fields,
      ];
      for (const u of tryUrls) {
        try {
          const r = await fetch(u, {credentials:'include'});
          if (!r.ok) continue;
          const j = await r.json();
          out[assetId] = {
            asset_type: j.asset_type,
            title: j.title,
            filename: j.filename,
            external_url: j.external_url || null,
            source_url: j.source_url || null,
            download_urls: j.download_urls || null,
            is_external: j.is_external || false,
          };
          if (j.external_url) return; // good enough; stop trying
        } catch (e) { /* try next */ }
      }
      if (!out[assetId]) out[assetId] = {error: 'all endpoints failed'};
    }));
    return JSON.stringify(out);
  }`;
  return pwEval(expr);
}

function chunk(arr, n) {
  const out = [];
  for (let i = 0; i < arr.length; i += n) out.push(arr.slice(i, i + n));
  return out;
}

const curriculum = JSON.parse(
  readFileSync(join(OUT_DIR, "curriculum.json"), "utf8"),
);

// Build an ordered list of lectures with their section.
let currentSection = null;
const lectures = [];
for (const item of curriculum.results) {
  if (item._class === "chapter") {
    currentSection = { id: item.id, title: item.title, index: item.object_index };
  } else if (item._class === "lecture") {
    lectures.push({
      id: item.id,
      title: item.title,
      object_index: item.object_index,
      section: currentSection,
      learn_url: `https://www.udemy.com/course/${COURSE_SLUG}/learn/lecture/${item.id}#overview`,
      video: item.asset
        ? {
            id: item.asset.id,
            title: item.asset.title,
            filename: item.asset.filename,
            duration: item.asset.content_summary,
            seconds: item.asset.time_estimation,
            download_urls: item.asset.download_urls?.Video ?? null,
          }
        : null,
      supplementary_assets: (item.supplementary_assets || []).map((a) => ({
        id: a.id,
        asset_type: a.asset_type,
        title: a.title,
        filename: a.filename,
        external_url: null,
      })),
    });
  }
}

// Collect every external-link asset id (with its lecture id) to resolve.
const toResolve = [];
for (const l of lectures)
  for (const a of l.supplementary_assets)
    if (a.asset_type === "ExternalLink")
      toResolve.push({ assetId: a.id, lectureId: l.id });

console.error(
  `Resolving ${toResolve.length} ExternalLink assets across ${lectures.length} lectures...`,
);

const resolved = {};
const batches = chunk(toResolve, 20);
let done = 0;
for (const batch of batches) {
  const r = await resolveBatch(batch);
  Object.assign(resolved, r);
  done += batch.length;
  process.stderr.write(`\r  resolved ${done}/${toResolve.length}`);
}
process.stderr.write("\n");

// Stitch back into the lecture list.
for (const l of lectures) {
  for (const a of l.supplementary_assets) {
    const r = resolved[a.id];
    if (r && r.external_url) a.external_url = r.external_url;
  }
}

writeFileSync(
  join(OUT_DIR, "curriculum_resolved.json"),
  JSON.stringify({ course_id: COURSE_ID, slug: COURSE_SLUG, lectures }, null, 2),
);
console.error(`Wrote ${lectures.length} lectures → out/curriculum_resolved.json`);
