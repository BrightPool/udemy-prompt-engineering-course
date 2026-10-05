#!/usr/bin/env python3
"""Exploring Other Model Providers - principles deck.

    uv run --with python-pptx python decks/other-providers/build_other_providers.py

The lecture's job is to widen the frame after a long ChatGPT deep dive: several
labs build these assistants, they all expose the same handful of controls, and
so the course's skills are portable. Deliberately no league table and no model
names - both date within weeks and would make this the most drift-prone lecture
in the course. See NOTES.md.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]
                      / ".claude" / "skills" / "principles-deck" / "scripts"))

from pptx.util import Inches, Pt  # noqa: E402
from pptx.dml.color import RGBColor  # noqa: E402
from pptx.enum.shapes import MSO_SHAPE  # noqa: E402
from deckkit import (Deck, title_case, INK, SOFT_INK, ACCENT, RULE,  # noqa: E402
                     NODE_BG, NODE_ACC, ARROW, BODY_FONT, SZ_CAPTION, SZ_DIAGRAM,
                     _rgb)

ASSETS = Path(__file__).resolve().parent / "assets"


def mark(s):
    """Shape count now, so the shapes drawn next can be grouped afterwards."""
    return len(s.raw.shapes)


def group(s, since, name):
    """Group every shape drawn since `since`, so it moves as one unit."""
    shapes = list(s.raw.shapes)[since:]
    if len(shapes) > 1:
        g = s.raw.shapes.add_group_shape(shapes)
        g.name = name
        return g
    return shapes[0] if shapes else None


def picture(s, png, x, y, sz):
    return s.raw.shapes.add_picture(str(ASSETS / png), Inches(x), Inches(y),
                                    Inches(sz), Inches(sz))


def badge(s, icon, x, y, d=0.42, fill="FFFFFF", line=RULE, tint="ink"):
    """A Lucide line icon (ISC licence) centred in a circle."""
    o = s.raw.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d),
                               Inches(d))
    o.fill.solid()
    o.fill.fore_color.rgb = _rgb(fill)
    o.line.color.rgb = _rgb(line)
    o.line.width = Pt(0.75)
    o.shadow.inherit = False
    g = d * 0.56
    picture(s, f"icon-{icon}-{tint}.png", x + (d - g) / 2, y + (d - g) / 2, g)


def link(box, url):
    run = box.text_frame.paragraphs[0].runs[0]
    run.hyperlink.address = url
    run.font.underline = True
    run.font.color.rgb = RGBColor.from_string(ACCENT)


LABS = [  # png, visual scale (app icons carry padding), name, lab
    ("claude.png", 1.00, "Claude", "Anthropic"),
    ("gemini.png", 0.74, "Gemini", "Google"),
    ("grok-mark.png", 0.78, "Grok", "xAI"),
    ("chatgpt.png", 1.00, "ChatGPT", "OpenAI"),
]

def label_table(rows, label_cols=(0,)):
    """Title Case the header row and the label columns; leave other cells alone."""
    return [[title_case(c) if (r == 0 or j in label_cols) and c else c
             for j, c in enumerate(row)] for r, row in enumerate(rows)]


OUT = Path(__file__).resolve().parent / "other-providers.pptx"


def build() -> Path:
    d = Deck()

    # 1 -----------------------------------------------------------------
    d.title(
        "Exploring Other Model Providers",
        "Several labs build these assistants, and they all expose the same "
        "handful of controls.",
    )

    # 2 -----------------------------------------------------------------
    s = d.what("the same kind of assistant, from several labs")
    m = s.chat_demo(
        0.40, 1.56, 4.60, 3.58,
        prompt="Read the attached contract and list anything that commits us "
               "beyond twelve months.",
        results=[
            "Section 4.2 - renews automatically each year",
            "Section 9 - data retained for 36 months",
            "Section 12 - exit needs 90 days' notice",
        ],
        cols=1,
        generic=True,
    )
    # The same window shape, four labs: show it rather than say it.
    rx = m.x + m.w + 0.55
    s.text(rx, 1.64, 9.66 - rx, 0.30, title_case("Same shape, four labs"),
           size=14, color=INK, bold=True, font=BODY_FONT)
    for i, (png, scale, name, _lab) in enumerate(LABS):
        gx = rx + (i % 2) * 1.62
        gy = 2.14 + (i // 2) * 1.12
        start = mark(s)
        sz = 0.62 * scale
        picture(s, png, gx + (0.62 - sz) / 2, gy + (0.62 - sz) / 2, sz)
        s.text(gx - 0.20, gy + 0.68, 1.02, 0.26, name, size=SZ_CAPTION, color=INK,
               bold=True, font=BODY_FONT, align="c")
        group(s, start, name)
    s.text(rx, 4.44, 9.66 - rx, 0.50, "Swap the lab. The prompt needs no edit.",
           size=SZ_CAPTION, color=SOFT_INK, font=BODY_FONT)

    # 3 -----------------------------------------------------------------
    s = d.content("Four labs, and what shaped each one")
    # Logos, not boxes: each lab is recognisable at a glance. The macOS app icons
    # carry their own padding, so the full-bleed marks are drawn a little smaller
    # to match their visual weight.
    assets = ASSETS
    labs = [
        ("claude.png", 1.00, "Claude", "Anthropic",
         "Safety and behaviour at the centre of its pitch."),
        ("gemini.png", 0.74, "Gemini", "Google",
         "Sits beside your search, mail and documents."),
        ("grok-mark.png", 0.78, "Grok", "xAI",
         "Leans on what is being posted right now."),
        ("chatgpt.png", 1.00, "ChatGPT", "OpenAI",
         "Took chat mainstream. The one we demo on."),
    ]
    col = 9.32 / 4
    icon = 1.10
    for i, (png, scale, name, lab, line) in enumerate(labs):
        cx = 0.34 + i * col + col / 2
        sz = icon * scale
        s.raw.shapes.add_picture(str(assets / png), Inches(cx - sz / 2),
                                 Inches(1.70 + (icon - sz) / 2), Inches(sz), Inches(sz))
        s.text(cx - col / 2 + 0.10, 2.98, col - 0.20, 0.34, name, size=16,
               color=INK, bold=True, font=BODY_FONT, align="c")
        s.text(cx - col / 2 + 0.10, 3.32, col - 0.20, 0.26, lab, size=SZ_CAPTION,
               color=ACCENT, bold=True, font=BODY_FONT, align="c")
        s.text(cx - col / 2 + 0.16, 3.72, col - 0.32, 0.70, line, size=SZ_CAPTION,
               color=SOFT_INK, font=BODY_FONT, align="c", spacing=1.15)

    # 4 -----------------------------------------------------------------
    s = d.how("every request is assembled the same way")
    parts = [
        ("scroll-text", "System instruction", "standing rules"),
        ("messages-square", "The conversation so far", "earlier turns"),
        ("paperclip", "Files and tool results", "what it fetched"),
        ("send", "Your message", "typed just now"),
    ]
    y, rh, lw = 1.56, 0.52, 5.10
    for icon, label, note in parts:
        start = mark(s)
        s.rect(0.34, y, lw, rh, fill=NODE_BG, rounded=True, radius=0.05,
               line=RULE, line_w=0.75)
        badge(s, icon, 0.46, y + 0.05)
        s.text(1.02, y, 2.50, rh, title_case(label), size=SZ_CAPTION, color=INK,
               bold=True, font=BODY_FONT, anchor="m")
        s.text(3.56, y, lw - 3.36, rh, title_case(note), size=SZ_CAPTION,
               color=SOFT_INK, font=BODY_FONT, anchor="m", align="r")
        group(s, start, label)
        y += rh + 0.06
    s.arrow(0.34 + lw / 2 - 0.17, y + 0.02, 0.34, 0.22, direction="down")
    req_y = y + 0.30
    s.node(0.34, req_y, lw, 0.56, "One request", accent=True)
    # Fan out: the same request goes to whichever lab you pick.
    bus_x, logo_x, req_cy = 6.10, 6.80, req_y + 0.28
    s.rect(0.34 + lw, req_cy - 0.006, bus_x - 0.34 - lw, 0.012, fill=ARROW)
    centres = [1.82 + i * 0.76 for i in range(4)]
    s.rect(bus_x - 0.006, centres[0], 0.012, req_cy - centres[0], fill=ARROW)
    for (png, scale, name, lab), cy in zip(LABS, centres):
        start = mark(s)
        s.arrow(bus_x, cy - 0.05, logo_x - bus_x - 0.10, 0.10)
        sz = 0.56 * scale
        picture(s, png, logo_x + (0.56 - sz) / 2, cy - sz / 2, sz)
        s.text(logo_x + 0.70, cy - 0.15, 2.10, 0.30, name, size=SZ_CAPTION,
               color=INK, bold=True, font=BODY_FONT, anchor="m")
        group(s, start, name)
    s.text(logo_x, req_cy + 0.12, 9.66 - logo_x, 0.46,
           "The lab changes. The request does not.", size=SZ_CAPTION,
           color=SOFT_INK, font=BODY_FONT)

    # 5 -----------------------------------------------------------------
    s = d.content("The same dials, under different names")
    dials = [
        ("hash", "Tokens", "How your text is counted and billed",
         "The tokenizer, so counts differ"),
        ("book-open", "Context window", "How much it holds at once",
         "The size, and how it behaves at the edge"),
        ("scroll-text", "System instruction", "The standing rules for every turn",
         "Where in the product you write it"),
        ("wrench", "Tools", "What it can call out to and act on",
         "Which ones ship built in"),
        ("gauge", "Reasoning effort", "How long it thinks before replying",
         "The name of the setting"),
    ]
    cx = (0.34, 3.00, 6.40)
    for x, head in zip(cx, ("Dial", "What it controls", "What differs between labs")):
        s.text(x, 1.56, 3.30, 0.28, title_case(head), size=SZ_CAPTION, color=INK,
               bold=True, font=BODY_FONT)
    s.rect(0.34, 1.88, 9.32, 0.012, fill=INK)
    y, rh = 1.96, 0.58
    for icon, label, controls, differs in dials:
        start = mark(s)
        badge(s, icon, 0.34, y + 0.08, fill=NODE_ACC, line=ACCENT, tint="pink")
        s.text(0.90, y, 2.10, rh, title_case(label), size=SZ_DIAGRAM, color=INK,
               bold=True, font=BODY_FONT, anchor="m")
        s.text(cx[1], y, 3.24, rh, controls, size=SZ_CAPTION, color=INK,
               font=BODY_FONT, anchor="m")
        s.text(cx[2], y, 3.26, rh, differs, size=SZ_CAPTION, color=SOFT_INK,
               font=BODY_FONT, anchor="m")
        s.rect(0.34, y + rh - 0.004, 9.32, 0.008, fill=RULE)
        group(s, start, label)
        y += rh

    # 6 -----------------------------------------------------------------
    # Prices move weekly, so the slide links out and the student looks them up.
    s = d.exercise("Compare what four labs charge", minutes=3)
    s.text(0.55, 1.10, 8.90, 0.50,
           "For each lab, find the cheapest paid plan per month, and the API "
           "price per million input and output tokens.",
           size=14, color=INK, font=BODY_FONT, spacing=1.15)
    pricing = [
        ("claude.png", 1.00, "Claude",
         "claude.com/pricing", "https://claude.com/pricing",
         "claude.com/pricing#api", "https://claude.com/pricing#api"),
        ("gemini.png", 0.74, "Gemini",
         "gemini.google/subscriptions", "https://gemini.google/subscriptions/",
         "ai.google.dev/.../pricing", "https://ai.google.dev/gemini-api/docs/pricing"),
        ("grok-mark.png", 0.78, "Grok",
         "grok.com/plans", "https://grok.com/plans",
         "docs.x.ai/.../models", "https://docs.x.ai/developers/models"),
        ("chatgpt.png", 1.00, "ChatGPT",
         "chatgpt.com/pricing", "https://chatgpt.com/pricing",
         "openai.com/api/pricing", "https://openai.com/api/pricing/"),
    ]
    cols = (0.55, 2.55, 6.00)          # lab, subscription, API
    hy = 1.72
    for x, head in zip(cols, ("Lab", "Subscription", "API")):
        s.text(x, hy, 3.20, 0.28, title_case(head), size=SZ_CAPTION, color=INK,
               bold=True, font=BODY_FONT)
    s.rect(0.55, hy + 0.34, 8.90, 0.012, fill=INK)
    row, y = 0.56, hy + 0.44
    for png, scale, name, sub_t, sub_u, api_t, api_u in pricing:
        start = mark(s)
        sz = 0.40 * scale
        s.raw.shapes.add_picture(str(assets / png), Inches(0.55 + (0.40 - sz) / 2),
                                 Inches(y + (row - sz) / 2 - 0.04), Inches(sz),
                                 Inches(sz))
        s.text(1.10, y, 1.40, row - 0.08, name, size=14, color=INK, bold=True,
               font=BODY_FONT, anchor="m")
        for x, label, url in ((cols[1], sub_t, sub_u), (cols[2], api_t, api_u)):
            box = s.text(x, y, 3.30, row - 0.08, label, size=SZ_CAPTION,
                         color=ACCENT, font=BODY_FONT, anchor="m")
            link(box, url)
        s.rect(0.55, y + row - 0.02, 8.90, 0.008, fill=RULE)
        group(s, start, f"{name} pricing")
        y += row
    s.text(0.55, y + 0.16, 8.90, 0.30,
           "Then decide: for your use, is a flat plan or pay-per-use cheaper?",
           size=SZ_CAPTION, color=SOFT_INK, font=BODY_FONT)

    # 8 -----------------------------------------------------------------
    s = d.content("What transfers, and what you relearn")
    panels = [
        ("Transfers unchanged", True, [
            ("layout-list", "Prompt structure"), ("users", "Examples and roles"),
            ("coins", "Token and context budgeting"), ("scale", "Judging an answer")]),
        ("You relearn", False, [
            ("settings", "Where the settings live"), ("tag", "What features are called"),
            ("plug", "Which tools it can reach"), ("palette", "Its house style and tone")]),
    ]
    pw, ph = 4.55, 3.04
    for i, (head, keep, items) in enumerate(panels):
        px = 0.34 + i * (pw + 0.22)
        start = mark(s)
        s.rect(px, 1.56, pw, ph, fill="FFFFFF", rounded=True, radius=0.05,
               line=ACCENT if keep else RULE, line_w=1.0 if keep else 0.75)
        s.text(px + 0.24, 1.70, pw - 0.48, 0.34, title_case(head), size=14,
               color=ACCENT if keep else INK, bold=True, font=BODY_FONT)
        iy = 2.20
        for icon, text in items:
            badge(s, icon, px + 0.24, iy, fill=NODE_ACC if keep else NODE_BG,
                  line=ACCENT if keep else RULE, tint="pink" if keep else "ink")
            s.text(px + 0.82, iy, pw - 1.06, 0.42, title_case(text), size=SZ_DIAGRAM,
                   color=INK, font=BODY_FONT, anchor="m")
            iy += 0.62
        group(s, start, head)

    # 9 -----------------------------------------------------------------
    s = d.content("Choosing per task, not once and for all")
    questions = [
        ("plug", "Can it reach the data and tools you need?"),
        ("shield-check", "What is your organisation allowed to send it?"),
        ("timer", "Do you want a fast answer or a considered one?"),
        ("git-compare", "Run your own prompt on two of them and compare."),
    ]
    qy = 1.56
    for icon, q in questions:
        start = mark(s)
        s.rect(0.34, qy, 5.30, 0.66, fill=NODE_BG, rounded=True, radius=0.05,
               line=RULE, line_w=0.75)
        badge(s, icon, 0.48, qy + 0.12)
        s.text(1.04, qy, 4.46, 0.66, q, size=SZ_CAPTION, color=INK,
               font=BODY_FONT, anchor="m", spacing=1.1)
        group(s, start, q)
        qy += 0.78
    # Leaderboards move weekly, so link out instead of printing a ranking.
    picture(s, "icon-trophy-pink.png", 6.04, 1.58, 0.28)
    s.text(6.40, 1.56, 3.26, 0.30, title_case("Check the leaderboards"),
           size=14, color=INK, bold=True, font=BODY_FONT)
    boards = [
        ("LMArena", "https://arena.ai/leaderboard", "people vote on answers"),
        ("Artificial Analysis", "https://artificialanalysis.ai/leaderboards/models",
         "speed, price, quality"),
        ("OpenRouter", "https://openrouter.ai/rankings", "what people actually use"),
        ("Epoch AI", "https://epoch.ai/benchmarks", "test scores over time"),
    ]
    by = 2.00
    for name, url, note in boards:
        start = mark(s)
        box = s.text(6.04, by, 3.62, 0.26, name, size=SZ_CAPTION, color=ACCENT,
                     bold=True, font=BODY_FONT)
        link(box, url)
        s.text(6.04, by + 0.24, 3.62, 0.24, title_case(note), size=SZ_CAPTION,
               color=SOFT_INK, font=BODY_FONT)
        group(s, start, name)
        by += 0.62
    s.text(6.04, by + 0.04, 3.62, 0.46, "Rankings shift weekly. Test your own prompt.",
           size=SZ_CAPTION, color=INK, font=BODY_FONT)

    # 10 ----------------------------------------------------------------
    d.handoff([
        ("Open another lab", "with the prompt you just used"),
        ("Find the controls", "instructions, tools, effort"),
        ("Compare answers", "for style, not for a score"),
    ], lead="Next, we run one prompt through two "
            "different labs.")

    return d.save(OUT)


if __name__ == "__main__":
    print(build())
