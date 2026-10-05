# Anti-drift doctrine

Why this skill exists.

## The problem

A course video has a long shelf life. A vendor UI does not. Every screenshot of ChatGPT,
Claude or Midjourney in a 2026 recording is a dated artefact by 2027: the sidebar moved,
the button was renamed, the setting lives two menus deeper. The teaching is still correct;
the pictures make it look wrong. Students file it as "this course is out of date" and stop
trusting the parts that *are* still true.

Re-filming because a button moved is the single most expensive kind of course maintenance.

## The rule

**The principles half of a video contains no vendor UI.**

Everything shown is a schematic mock, drawn as vector shapes, saying what the feature
*does* rather than where it currently sits on screen. The instructor demos the real,
current product in the second half, which is cheap to re-film on its own because it has no
slides to rebuild.

That split is the whole design: put the expensive-to-produce material where it does not
expire, and the expiring material where it is cheap to redo.

## What goes in each half

| Principles half (this skill) | Implementation half (filmed) |
|---|---|
| What the feature is | Where the button is |
| The mechanism | The click path |
| What it can and cannot do | Live output |
| Why it changes your results | Troubleshooting |
| When to reach for it | Current pricing and limits |

## Copy that drifts, and its durable replacement

| Drifts | Durable |
|---|---|
| "Click Settings > Personalization > Memory" | "Memory is opt-in and you can inspect it" |
| "Toggle the globe icon" | "Search is a step the model runs before answering" |
| "GPT-5 supports 400k tokens" | "Context is finite, and the limit is the thing you budget" |
| "It costs $20/month" | "The capable tier is a paid tier" |
| "The panel is on the right" | "The store is editable" |

Test each line: **would this still be true after a redesign?** If not, it belongs in the
demo half or in the spoken track, where fixing it costs one take instead of a slide rebuild.

## Mocks, not screenshots

Mock UIs in this skill are:

- **Vector.** Native shapes, so they stay crisp at any projection size, and Mike or James
  can fix a typo directly in Google Slides without regenerating an image.
- **Schematic.** Enough chrome to read as "a chat tool", never enough to be mistaken for a
  specific build. No logos, no traffic lights, no avatars, no real typography of a vendor.
- **Labelled to a fixed convention.** `ChatGPT` / `Demonstration` when showing the
  product doing a thing; `AI Assistant` / `Example` when showing a prompt pattern. Turns
  are always `User`, `AI Assistant`, `System`. Naming the product is fine - naming its
  *version or its current layout* is what drifts.
- **Small.** A mock exists to make one point. Trim the conversation to the two or three
  lines that carry the idea.

## Generated images

Use image generation for **conceptual illustration only** - a metaphor, a texture, an
abstract diagram backdrop. Never for UI.

A generated UI has all the drift risk of a screenshot plus invented affordances, garbled
microcopy and a resolution that will not survive a projector. If you want a UI on a slide,
draw it with `deckkit`.

When you do generate an illustration, match the deck: pink `#E91D63` and grey `#424242`,
flat vector, white background, no text baked into the image.

## The one screenshot exception

If the entire teaching point *is* a specific interface at a specific moment - a historical
comparison, say, or a deliberate "here is what this looked like before" - then a screenshot
is legitimate. Date it visibly on the slide so its age reads as intentional rather than as
neglect.
