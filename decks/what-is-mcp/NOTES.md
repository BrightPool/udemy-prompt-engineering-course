# What is MCP? — deck notes

New lecture. No prior video, no transcript, no brief. Part 2 · Skills & Plugins.

Deliverables: `what-is-mcp.pptx` (12 slides), `build_what_is_mcp.py`, this file.
Linter: **clean, 12 slides, nothing to fix.**

## The three principles

- **What it is** — MCP (the Model Context Protocol) is an open standard for
  connecting an assistant to other software: the system at the other end runs a
  *server* that lists the jobs it can do, and any assistant that speaks the
  standard can use any server.
- **How it works** — the assistant connects to a server, discovers what it
  offers (tools, resources, prompts), and when you ask for something it calls one
  of those tools by name and reads the result back into the conversation.
- **Why it matters** — a connector written once works in every assistant that
  speaks the standard, which turns N×M bespoke integrations into N+M; the cost is
  that a connected server is a third party holding a set of your permissions, and
  everything it says lands in the same window as everything you say.

## Slide list

| # | Title |
|---|---|
| 1 | What is MCP? |
| 2 | What is it? - a common standard for reaching your other systems |
| 3 | A skill is not a connection |
| 4 | The problem it was invented to solve |
| 5 | How it works - tools, resources and prompts |
| 6 | It finds out what it can do when it connects |
| 7 | What actually reaches the model |
| 8 | Where a connection stops |
| 9 | Why it matters - built once, works everywhere |
| 10 | Judging a server before you connect it |
| 11 | When a connection earns its place |
| 12 | Let's see it in action |

## Research — what is true now (verified 2026-09-08)

All of the following was fetched directly from first-party pages; none of it is a
search snippet unless tagged.

**Definition and analogy** — `modelcontextprotocol.io/docs/getting-started/intro`:
"MCP (Model Context Protocol) is an open-source standard for connecting AI
applications to external systems." Their own analogy: "Think of MCP like a USB-C
port for AI applications." I deliberately kept USB-C **off** the slides — it is
the single most-repeated MCP line on the internet and reads as borrowed. It is a
good thing to say aloud in the demo half if you want it.

**Participants** — `modelcontextprotocol.io/docs/learn/architecture`:
"MCP Host": the AI application; "MCP Client": maintains a connection to one
server; "MCP Server": "A program that provides context to MCP clients". The host
creates one client per server. The deck teaches host+client as simply "the
assistant" — the host/client split is an engineering distinction and this is a
no-code course. If a student asks, the honest gloss is "the assistant is the
client".

**What a server offers** (slide 5's table is these three, verbatim in meaning):
- **Tools** — "Executable functions that AI applications can invoke to perform
  actions"
- **Resources** — "Data sources that provide contextual information"
- **Prompts** — "Reusable templates that help structure interactions"

**Discovery is the mechanism worth teaching** (slide 6). Servers advertise
capabilities through a `server/discover` request; clients call `tools/list` to
enumerate tools before calling them, and listings are explicitly dynamic. That is
why a system built last week works in an assistant built last year, and it is the
non-obvious bit students miss.

**Multi-vendor, and now vendor-neutral by governance.** On **9 December 2025**
Anthropic donated MCP to the **Agentic AI Foundation**, "a directed fund under the
Linux Foundation", co-founded by Anthropic, Block and OpenAI, with support from
Google, Microsoft, AWS, Cloudflare and Bloomberg. The Linux Foundation "will not
dictate the technical direction of MCP". Source:
`blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/`.
I kept the org names off the slide (they date) but the *fact* that no one company
owns it is on slide 4. **Worth saying aloud** — it is the strongest answer to
"why should I learn this rather than wait for it to be replaced".

**Vendor mapping — the vocabulary students trip on:**
- Anthropic's page for building Claude connectors is titled *"Building custom
  connectors — Build your own MCP servers to connect Claude to your tools and
  data"*. So on the Claude side, **a connector is an MCP server**.
- OpenAI's developer docs describe MCP as "an open protocol that's becoming the
  industry standard for extending AI models with additional tools and knowledge",
  and support connecting MCP servers both in ChatGPT and via the Responses API.
- That is why slide 3's caption says products wrap it in their own words
  ("connector", "plugin", "app") and the thing behind them is increasingly an MCP
  server. Slide 3 is the vocabulary slide; the neighbouring lectures use
  "plugins" and "connectors" and this is where those words get reconciled.

**Security, stated honestly.** The spec's own trust principles: "Users must
explicitly consent to and understand all data access and operations"; "Tools
represent arbitrary code execution and must be treated with appropriate caution";
and, load-bearing for slide 7, "descriptions of tool behavior such as annotations
should be considered untrusted, unless obtained from a trusted server". OpenAI's
docs say plainly that "custom MCP servers are not developed or verified by
OpenAI, and are third-party services" and recommend connecting only to servers
you know and trust, preferably the ones hosted by the service provider itself —
that is exactly slide 10, step 1.

**Deliberately left out of the deck** (all of it real, all of it drift):
transports (stdio, Streamable HTTP), JSON-RPC, OAuth flows, the MCP Registry, tool
result size limits, `sampling` being deprecated as of protocol version
`2026-07-28`, and any menu path for adding a server. If you want a click path on
camera, OpenAI's docs currently route it through developer mode in ChatGPT's
settings and Claude's through its connectors screen — **check both live before
filming, they move.** `[unverified against the live consumer UI — the help-centre
and settings screens were not opened for this deck]`

## What each review round found

**Round 1 — the hostile reviewer.** Seven findings, all fixed.
1. Slide 4's caption talked about "four assistants and ten systems / forty
   integrations" while the picture drew 3×3. Numbers now match the drawing and
   then scale up.
2. Slide 6's flow drifted between subjects ("It connects" / "The server lists" /
   "You ask"). Rewritten verb-led and parallel: Connect · Discover · Ask · Call.
3. Slide 8 stopped at y=3.98 with no honest failure mode. Added the caption
   about a server changing what it offers without announcing it.
4. Ragged start heights — visuals started variously at 1.52, 1.56 and 1.58.
   Everything now starts at 1.56.
5. Slide 5's table was short and the slide read empty; table height 1.90 → 2.20,
   caption moved down with it.
6. "£" added to the mock invoice total, which read as a bare number.
7. `right_heading` "Leave it alone when" → "Do not bother when".
Layout pass: also confirmed the nine hand-drawn diagonals on slide 4 render as
real connectors (deckkit only draws axis-aligned rules, so that slide uses
`add_connector` through the documented `s.raw` escape hatch).

**Round 2 — the student.** Four substantive findings, all fixed.
1. **"server" was never defined** — it first appeared in a caption on slide 3 and
   was load-bearing from slide 5 onward. Now defined on slide 2, at first
   contact, and again in slide 3's caption.
2. **"tool" was used before it was defined** — the flow slide called one a slide
   *before* the table that explains what tools are. The two slides are swapped,
   so the mechanism section now runs nouns-then-verbs, and the phase title moved
   with it.
3. Slide 10 never answered the obvious no-code question, "am I supposed to
   *build* one of these?" Its caption now says plainly that you almost never
   write one; your job is choosing which to trust.
4. Slide 3's caption then overran the footer band (5.22"). Compare panels
   shortened to 2.40" and the caption tightened.

**Round 3** (run because round 2 found more than two substantive issues). Six
craft-level findings, no substance changes.
1. Slide 6's title just listed the diagram beneath it ("Connect, discover, ask,
   call") — replaced with the claim the diagram proves, "It finds out what it can
   do when it connects".
2. Slide 5's phase title then read too close to it; changed to name the three
   primitives it actually shows.
3. Two consecutive captions both opened with "Three"; slide 5's reworded.
4. Slide 8's caption opened with "the other side of the line", which meant
   nothing — now "The boundary only protects you in one direction".
5. Captions beside a visual aligned at 1.60" on both slides that use the pattern
   (was 1.60 and 1.62).
6. Third handoff card's sub-label made parallel with the other two.

## For James

**1. The lecture title is misleading and I did not silently change it.**
The manifest says *"What is MCP? (Plugins for OpenAI)"*. MCP is not OpenAI's — it
came from Anthropic, and since December 2025 it has been governed by the Agentic
AI Foundation under the Linux Foundation, with OpenAI as a **co-founder of the
foundation**, not the owner of the protocol. Teaching it as OpenAI's plug-in
system is the one thing about MCP that is actually wrong, and it undercuts the
whole point of the lecture (that the connector you write once works everywhere).
The deck is built accurately — open standard, multi-vendor, vendor-neutral mocks.

Suggested rename: **"What is MCP? (How your assistant plugs into everything
else)"**, or simply **"What is MCP?"**. If the parenthetical exists for Udemy
search, **"What is MCP? (Connectors and Plugins)"** keeps the searchable words
without asserting ownership. Your call — I have not changed the manifest.

**2. I chose the angle, so here it is explicitly.**
No brief was given. The angle is *"how your assistant plugs into the rest of your
software"* — a **no-code, buyer's-eye** treatment, not an engineering spec. There
is no JSON, no transport, no SDK and no code anywhere in the deck. The load-bearing
visual is slide 4: 3×3 wired by hand versus one protocol in the middle. The
load-bearing *idea* is the last row of slide 9's table: the old problem was that
your assistant could not reach your systems, and the new problem is deciding which
of them it should.

I rejected two alternative angles: (a) "how to build an MCP server", which belongs
in a developer course and duplicates nothing we have; and (b) "a tour of available
servers", which would be out of date before the course ships.

**3. The skill / MCP boundary is slide 3, and it is deliberate.**
Per the section brief, students conflate these constantly. The deck states it as:
a **skill** is instructions the assistant follows; **MCP** is a live link to
another system. A skill changes *how it works*; a connection changes *what it can
reach*. Slide 3 also reconciles the vocabulary — "connector", "plugin", "app" —
because the neighbouring lectures use those words and nothing else in the section
tells students they are largely the same thing. Please keep that reconciliation
somewhere in the section even if this slide changes.

**4. Overlap check with neighbouring lectures.** No duplication found, but two
seams to be aware of when you film:
- `agent-mode` covers prompt injection at the *action* level (hidden text on a
  web page steering an agent). This deck covers it at the *connection* level (a
  server's tool descriptions and results are that server's words, arriving in the
  same context as yours). Slide 7 reinforces rather than repeats — worth an
  explicit callback on camera: "same failure, one layer down".
- `practicing-plugins` is the hands-on version of this lecture. This deck ends on
  a handoff that leads straight into connecting one server; if you film them close
  together, do not re-explain tools/resources/prompts there.

**5. One thing I could not primary-verify.** Nothing on a slide depends on it,
but the click paths for adding a server — in ChatGPT and in Claude — were not
opened live for this deck. Both vendors' *developer* docs describe them, and both
have moved in the last year. Check them on camera before filming the demo half.
