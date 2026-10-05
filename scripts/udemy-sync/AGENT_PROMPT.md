# Udemy Instructor API — Agent Handoff

A handoff for another agent (or future-you) who needs to scrape the curriculum,
download videos, or pull resource metadata from a Udemy instructor account.
Everything below was reverse-engineered from the live `/instructor/course/...`
UI and validated against course `5238734` (slug `prompt-engineering-for-ai`) on
2026-04-27.

The four working scripts in this directory (`resolve_resources.mjs`,
`download_videos.mjs`, `match_notebooks.mjs`, `analyze_drift.py`) are the
ground truth — when this doc and the code disagree, trust the code.

---

## Mission

Given an instructor's Udemy course URL, produce:
1. A normalized JSON tree of `chapter → lecture → {video, supplementary_assets}`.
2. A directory of downloaded `.mp4` videos.
3. Resolved external URLs for every supplementary asset (Colab, GitHub, Notion, etc.).

There is **no public Udemy API** for this. You hit the same internal `api-2.0`
endpoints that the instructor SPA calls.

---

## Authentication

Udemy is behind Cloudflare and requires a real browser session. There is no API
key for this — you must log in once interactively and reuse the cookies.

```bash
# One-time interactive login (opens a real Chrome window)
playwright-cli -s=udemy open --persistent --headed --browser=chrome \
  https://www.udemy.com/instructor/course/<COURSE_ID>/manage/curriculum
# → user logs in manually with Udemy creds (or Google SSO)
# → cookies persist in the named session's profile dir
```

After the first login, re-use the session headlessly:

```bash
playwright-cli -s=udemy open --persistent --browser=chrome
playwright-cli -s=udemy goto https://www.udemy.com/...
# all subsequent fetch() calls in this session inherit cookies
```

Anywhere this doc says "fetch ...", the practical mechanism is:

```bash
playwright-cli -s=udemy eval "async () => {
  const r = await fetch(URL, {credentials: 'include'});
  return JSON.stringify(await r.json());
}"
```

That's how `resolve_resources.mjs` does authenticated reads. The cookies — not
any header — are what authorize the request.

---

## Step 1 — Discover the course ID and slug

From any URL like `https://www.udemy.com/instructor/course/5238734/manage/curriculum`:
- **Course ID:** `5238734` (numeric)
- **Slug:** open the public/student URL once (it shows as
  `https://www.udemy.com/course/<slug>/learn/lecture/<lectureId>`); the slug is
  needed to build student-facing links and to call the `subscribed-courses`
  fallback endpoint (see Pitfall #1).

---

## Step 2 — Pull the entire curriculum in one call

```
GET https://www.udemy.com/api-2.0/courses/<COURSE_ID>/instructor-curriculum-items/
  ?curriculum_types=chapter,lecture,practice,quiz,role-play
  &page_size=1400
  &fields[chapter]=title,description,object_index
  &fields[lecture]=asset,title,is_published,description,is_downloadable,is_free,object_index,supplementary_assets,labs
  &fields[asset]=created,asset_type,content_summary,time_estimation,status,source_url,thumbnail_url,title,processing_errors,delayed_asset_message,body,download_urls,filename,external_url,external_link_url
```

Response shape (`results` is an ordered list mixing chapters and lectures):

```json
{
  "count": 241,
  "results": [
    {
      "_class": "chapter",
      "id": 8953744,
      "title": "Introduction",
      "object_index": 1
    },
    {
      "_class": "lecture",
      "id": 38314374,
      "title": "Introduction to the Course",
      "is_published": true,
      "object_index": 1,
      "asset": {                     // the video
        "_class": "asset",
        "id": 64306033,
        "asset_type": "Video",
        "title": "Udemy Prompt Engineering Promo.mp4",
        "filename": "Udemy-Prompt-Engineering-Promo.mp4",
        "content_summary": "01:39",
        "time_estimation": 99,
        "download_urls": {
          "Video": [
            {"label": "720", "type": "video/mp4", "file": "https://mp4-c.udemycdn.com/.../WebHD_720p.mp4?Expires=...&Signature=..."},
            {"label": "480", "type": "video/mp4", "file": "..."},
            {"label": "360", "...": "..."}
          ]
        }
      },
      "supplementary_assets": [      // resources
        {
          "_class": "asset",
          "id": 71846911,
          "asset_type": "ExternalLink",
          "title": "ChatGPT - Prompt Pack - Homepage",
          "filename": "ChatGPT-Prompt-Pack-Homepage",
          "source_url": "",         // ← almost always empty here; see Step 3
          "download_urls": null
        }
      ]
    }
  ]
}
```

To rebuild section structure, walk `results` once and remember the most-recent
chapter (lectures appear in order under their chapter).

`asset_type` values you will see: `Video`, `ExternalLink`, `File`, `SourceCode`,
plus quiz/practice items.

---

## Step 3 — Resolve external link URLs

The curriculum response does **not** include the actual destination of an
`ExternalLink` asset. You have to hit the asset detail endpoint per asset.

**Primary endpoint (works for most assets):**

```
GET https://www.udemy.com/api-2.0/assets/<ASSET_ID>/?fields[asset]=@all
```

Response includes `external_url` (e.g. the Colab share link, the Notion page,
etc.). When `is_external` is true, that's the URL you want.

**Pitfall #1 — instructor endpoint returns 403 for some assets.** Older
supplementary assets created under a different ownership chain return
`{"detail": "You do not have permission to perform this action."}`. The
**student-facing endpoint** always works for the logged-in instructor:

```
GET https://www.udemy.com/api-2.0/users/me/subscribed-courses/<COURSE_ID>/lectures/<LECTURE_ID>/supplementary-assets/<ASSET_ID>/?fields[asset]=external_url,source_url,asset_type,filename,title,download_urls,is_external
```

Strategy: try the primary endpoint first; on 403 (or empty `external_url`),
fall back to the per-lecture endpoint. `resolve_resources.mjs::resolveBatch`
implements exactly this two-step.

**Throughput:** in-page `fetch()` parallelism is fine at 20 concurrent. The
full course (197 ExternalLink assets) resolves in ~30s.

---

## Step 4 — Download videos

You already have the signed mp4 URLs from Step 2 — `asset.download_urls.Video`
is an array of variants by quality label (`"1080" | "720" | "480" | "360" |
"144"`). Pick `720` for code-screen lectures (legible without being huge).

The signed URL has an `Expires=<unix>` query param (typically ~5 days from when
the curriculum was fetched). If your download takes longer than that, **re-call
the Step 2 endpoint to get fresh signatures** rather than trying to refresh
individual URLs — that's what `download_videos.mjs` does at startup.

**Concurrency:** 10 simultaneous downloads worked end-to-end with zero failures
across 209 mp4s totalling 15 GB. Higher might trip Cloudflare.

```js
// In Node:
const r = await fetch(signedUrl);
await stream.pipeline(Readable.fromWeb(r.body), createWriteStream(path));
```

No auth header needed for the actual mp4 download — the signature is the auth.

---

## Step 5 — Recognising Colab vs GitHub vs other

Once `external_url` is resolved, classify by hostname:

| Hostname pattern                                 | What it points at                             |
| ------------------------------------------------ | --------------------------------------------- |
| `colab.research.google.com/drive/<id>`           | A standalone Colab notebook (no path in URL)  |
| `colab.research.google.com/github/<repo>/blob/...` | A Colab proxy onto a GitHub-hosted notebook |
| `github.com/<our-repo>/blob/<branch>/<path>`     | Direct link to a notebook in your own repo    |
| `github.com/<external-repo>/...`                 | External reference, not yours                 |
| `notion.so`, `docs.google.com`, etc.             | Misc course resources                         |

For Colab `/drive/<id>` URLs the notebook filename does not appear in the URL —
but in practice the **supplementary asset's `title` field is the basename**
(e.g. `responses_api_and_messages.ipynb`). That's what `match_notebooks.mjs`
relies on to map Colab assets to repo files.

---

## Pitfalls / gotchas summary

1. **`/api-2.0/assets/<id>/` returns 403 for some assets** → fall back to
   `/api-2.0/users/me/subscribed-courses/<courseId>/lectures/<lectureId>/supplementary-assets/<assetId>/`.
2. **Signed mp4 URLs expire (~5 days)** → re-fetch the curriculum to refresh
   signatures; don't try to refresh individual URLs.
3. **Cloudflare interstitial** — first hit on a fresh session shows "Just a
   moment...". A real headed Chromium session (Playwright `--headed`) clears it
   automatically. Headless will sit on the challenge.
4. **The `instructor-curriculum-items` `source_url` field is always empty for
   ExternalLinks** — the real URL is `external_url`, only returned by the
   asset-detail endpoints in Step 3.
5. **Quiz/practice items appear in the same `results` array** as lectures and
   chapters — filter on `_class === "lecture"` (and on `asset?.asset_type ===
   "Video"` if you want videos specifically).
6. **`File` supplementary-assets** can also 403 on `/api-2.0/assets/<id>/` and
   the subscribed-courses endpoint may not surface a download URL either —
   instructor file-asset downloads appear to require yet a different route via
   the manage UI. Out of scope for the scripts in this folder.

---

## Reference scripts in this directory

| Script                  | What it does                                                                                  |
| ----------------------- | --------------------------------------------------------------------------------------------- |
| `resolve_resources.mjs` | Calls Step 2, then Step 3 with the dual-endpoint fallback. Writes `out/curriculum_resolved.json`. |
| `download_videos.mjs`   | Refreshes Step 2 (fresh sigs), then downloads at concurrency 10 into `videos/`.               |
| `match_notebooks.mjs`   | Indexes `*.ipynb` in the repo and matches them to Colab/GitHub supplementary assets.          |
| `analyze_drift.py`      | Uploads each video to Gemini Files API alongside its matched notebook, scores drift.          |
| `emit_csvs.py`          | Rolls up all `out/analysis*/*.json` into `analysis.csv` + `analysis_flat.csv`.                |

If you need to do this for a different course, the only things you have to
change are `COURSE_ID` and `COURSE_SLUG` (both defined at the top of the .mjs
files and the .py file). Everything else is course-agnostic.
