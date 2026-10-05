#!/usr/bin/env node
// Scrape course reviews from Udemy via the public api-2.0 reviews endpoint.
// Pages newest-first via the `next` link, stops once it passes the cutoff
// window, then keeps only reviews that have comment text.
//
// Auth: the reviews endpoint is public, but we send HTTP Basic auth using the
// Udemy API token when available (read from 1Password, never persisted):
//   UDEMY_TOKEN=$(op read "op://api-keys/Udemy/credential") \
//     node scripts/udemy-sync/scrape_reviews.mjs [months]
//
// Usage:
//   node scripts/udemy-sync/scrape_reviews.mjs 6   # default: last 6 months
//
// Writes:
//   out/reviews.json  — full review objects (with comments, within window)
//   out/reviews.csv   — rating, date, user, content (spreadsheet-friendly)
import { writeFileSync, mkdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUT_DIR = join(__dirname, "out");
const COURSE_ID = 5238734;

// How far back to keep reviews (in months). Default 6.
const MONTHS = Number(process.argv[2] || 6);
const cutoff = new Date();
cutoff.setMonth(cutoff.getMonth() - MONTHS);

const TOKEN = process.env.UDEMY_TOKEN || "";
const headers = { Accept: "application/json" };
if (TOKEN) {
  // Udemy affiliate/instructor API uses Basic auth: client_id:client_secret.
  // The single token works as the user component with an empty secret.
  headers.Authorization =
    "Basic " + Buffer.from(`${TOKEN}:`).toString("base64");
}

// NOTES on Udemy api-2.0 quirks:
//  - is_text_review=true → only reviews that have comment text. Critical: the
//    endpoint caps pagination at 10,000 reviews total (page 100). This course
//    gets so many reviews that the newest 10k spans only ~2 months; filtering
//    to text reviews (~20% of all) makes the 10k ceiling reach well past 6mo.
//  - requesting fields[user] silently caps the endpoint to 10 results/page, so
//    reviewer names are intentionally not expanded.
const FIELDS =
  "page_size=100&ordering=-created&is_text_review=true" +
  "&fields[course_review]=id,content,rating,created,modified";

const base = `https://www.udemy.com/api-2.0/courses/${COURSE_ID}/reviews/?` + FIELDS;

console.error(
  `Scraping reviews for course ${COURSE_ID}, cutoff = ${cutoff
    .toISOString()
    .slice(0, 10)} (${MONTHS} months), auth=${TOKEN ? "token" : "none"}...`,
);

const all = [];
let page = 0;
let stop = false;

// NOTE: the endpoint only paginates fully when an explicit `page` param is
// present — without it, anonymous requests are capped to 10 results and `next`
// is null. So we iterate the page number ourselves.
while (!stop) {
  page++;
  const res = await fetch(`${base}&page=${page}`, { headers });
  if (!res.ok) {
    throw new Error(`API error ${res.status} ${res.statusText} on page ${page}`);
  }
  const data = await res.json();
  const results = data.results || [];
  if (results.length === 0) break; // ran out of pages

  for (const rv of results) {
    if (new Date(rv.created) < cutoff) {
      stop = true; // newest-first → everything after is older too
      break;
    }
    all.push(rv);
  }

  process.stderr.write(
    `\r  page ${page}: collected ${all.length} (count=${data.count ?? "?"})`,
  );
  if (!data.next) break; // last page
  if (page >= 100) {
    // Udemy hard-caps pagination at 10,000 reviews (page 100). If we hit it
    // without reaching the cutoff, the window is NOT fully covered.
    console.error(
      `\n⚠️  Hit Udemy's 10,000-review pagination ceiling before reaching the ` +
        `${MONTHS}-month cutoff. Oldest collected: ${all[all.length - 1]?.created?.slice(0, 10)}. ` +
        `Window is only partially covered — partition by rating to go deeper.`,
    );
    break;
  }
}
process.stderr.write("\n");

// Keep only reviews that actually have comment text.
const withComments = all.filter(
  (rv) => rv.content && rv.content.trim().length > 0,
);

const shaped = withComments.map((rv) => ({
  id: rv.id,
  rating: rv.rating,
  created: rv.created,
  modified: rv.modified,
  content: rv.content.trim(),
}));

mkdirSync(OUT_DIR, { recursive: true });

// --- JSON ---
writeFileSync(
  join(OUT_DIR, "reviews.json"),
  JSON.stringify(
    {
      course_id: COURSE_ID,
      scraped_through: cutoff.toISOString(),
      months: MONTHS,
      total_in_window: all.length,
      with_comments: shaped.length,
      reviews: shaped,
    },
    null,
    2,
  ),
);

// --- CSV ---
const csvCell = (v) => `"${String(v ?? "").replace(/"/g, '""')}"`;
const header = ["rating", "date", "content"];
const rows = shaped.map((rv) =>
  [rv.rating, rv.created.slice(0, 10), rv.content].map(csvCell).join(","),
);
writeFileSync(
  join(OUT_DIR, "reviews.csv"),
  [header.join(","), ...rows].join("\n") + "\n",
);

console.error(
  `Done. ${all.length} reviews in last ${MONTHS} months, ${shaped.length} with comments.\n` +
    `  → out/reviews.json\n  → out/reviews.csv`,
);
