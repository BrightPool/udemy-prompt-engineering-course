#!/usr/bin/env python3
"""
deckkit - build "principles of X" decks in the Prompt Engineering Bootcamp style.

Everything is native PowerPoint/Slides vector shapes. No screenshots, no bitmaps.
Slide chrome (title, body, footer, slide number) inherits from the template master,
so titles are Oswald 30pt and body is Source Code Pro 18pt/115% without us ever
setting a font. Mock UI panels and concept diagrams are drawn from the token set
below, lifted from "Give Direction v-infinity.pptx".

Build, then ALWAYS lint:
    uv run --with python-pptx python scripts/example_deck.py out/deck.pptx
    uv run --with python-pptx python scripts/check_deck.py  out/deck.pptx
"""
from __future__ import annotations

import contextlib
import copy
from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"

# --------------------------------------------------------------------------
# Design tokens (extracted from the source deck - do not invent new values)
# --------------------------------------------------------------------------
SLIDE_W, SLIDE_H = 10.0, 5.625          # inches, 16:9
FOOTER_Y = 5.10                         # nothing may cross this line
DASH_Y = 1.39                           # the layout's dashed divider under the title
CONTENT_TOP = 1.52                      # first safe y for content beneath it

# Mock UI (dark) - only ever used inside a mock window
PANEL      = "303138"   # window body, message rows
HEADER     = "25262C"   # title bar, darker than the body
BUBBLE     = "3C3D46"   # nested response bubble, composer input
HL         = "71334D"   # dim-pink pill behind emphasised text
CHIP       = "E4E5EA"   # light send button
TEXT       = "F7F7FA"   # primary text on dark
MUTED      = "C6C7D0"   # role labels, placeholder text, tags

# Slide surface (light) - everything outside a mock window
ACCENT     = "E91D63"   # brand pink
ARROW      = "ED1763"   # annotation arrow pink
INK        = "424242"   # body text on white (theme dk2)
SOFT_INK   = "6B6B6B"   # secondary text on white
RULE       = "D8D8DE"   # hairlines, table rules
NODE_BG    = "F5F5F7"   # diagram node fill (light grey)
NODE_ACC   = "FBE4EC"   # diagram node fill, emphasised (pink tint)

UI_FONT    = "Arial"    # mock UI type - deliberately NOT the slide fonts
HEAD_FONT  = "Oswald"
BODY_FONT  = "Source Code Pro"

# Mock UI type scale, in points, as used in the source deck
SZ_APP     = 12.0       # app name in the title bar
SZ_BODY    = 11.25      # message text
SZ_LABEL   = 8.85       # "User" / "AI Assistant" labels, corner tag
SZ_TINY    = 8.25

# Slide-surface type scale. Nothing on the white area goes below SZ_CAPTION.
SZ_DIAGRAM   = 13.0     # diagram node labels
SZ_TABLE     = 12.0     # table cells
SZ_CAPTION   = 12.0     # notes beside a diagram or table  <- minimum on white

# Vertical rhythm, inches
HEADER_H   = 0.33
LINE_H     = 0.23
PAD_X      = 0.16
GAP        = 0.10
LABEL_GAP  = 0.10       # breathing room between a label and its sub-label

# House convention for mock windows. See references/mock-ui-recipes.md.
APP_PRODUCT = ("ChatGPT", "Demonstration")   # showing the product doing a thing
APP_GENERIC = ("AI Assistant", "Example")    # showing a prompt pattern
ROLE_USER, ROLE_AI, ROLE_SYSTEM = "User", "AI Assistant", "System"

# The three-part arc. Used as title prefixes, never as standalone divider slides.
# "What is it?" carries no prefix: the title slide has already named the concept,
# so the next slide leads straight with the answer. How and Why still announce
# themselves, because they mark a turn in the argument.
PHASES = {"what": None, "how": "How it works", "why": "Why it matters"}

# Slide titles are Title Case. These stay lowercase unless they open or close the
# title, or follow a dash or colon.
SMALL_WORDS = {
    # "so" and "yet" are left out: here they are nearly always adverbs ("so far",
    # "not yet"), and "The Conversation so Far" reads like a typo.
    "a", "an", "the", "and", "but", "or", "nor", "for",
    "at", "by", "in", "into", "of", "off", "on", "onto", "to",
    "as", "via", "with", "from", "than", "per", "vs",
    # "up" and "over" stay capitalised: they are far more often part of a verb
    # here ("hand over", "ends up") than a preposition, and a lowercased phrasal
    # verb reads like a typo.
}

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "template.pptx"


def _cap(w: str) -> str:
    """Capitalise the first letter of a word, leaving the rest alone."""
    if any(c.isupper() for c in w[1:]):
        return w
    j = next((k for k, c in enumerate(w) if c.isalpha()), None)
    return w if j is None else w[:j] + w[j].upper() + w[j + 1:]


def title_case(text: str) -> str:
    """Title Case a slide title, leaving small words and real names alone.

    Words that already carry their own capitals (ChatGPT, MCP, IDs, tiktoken)
    are returned untouched, so this never fights a product's spelling.
    """
    words = text.split(" ")
    out, last = [], len(words) - 1
    force = True                      # first word is always capitalised
    for i, w in enumerate(words):
        if not w:
            out.append(w)
            continue
        core = w.strip("([\"'“‘")
        if core and (core.isupper() or any(c.isupper() for c in core[1:])
                     or core.startswith(("/", "<", "{", "`", "."))
                     # filenames and domains: customers.csv, claude.com
                     or "." in core.rstrip(".,:;?!)]\"'”’")):
            out.append(w)             # ChatGPT, /commands, <placeholders>, .csv - as written
        elif not force and i != last and core.lower().strip(".,:;?!)]\"'”’") in SMALL_WORDS:
            out.append(w.lower())
        else:
            # Hyphenated compounds capitalise every part: "Plain-Language".
            out.append("-".join(_cap(part) for part in w.split("-")))
        force = w.endswith(("-", ":", "\u2013", "\u2014"))
    return " ".join(out)


def _label_case(text):
    """Labels are Title Case (James's house rule). Sentences are left alone.

    Card, node and layer labels and their short sub-labels are labels, so they are
    cased here and build scripts can write them naturally. Anything ending in a full
    stop reads as a sentence and keeps its casing.
    """
    if not text or str(text).rstrip().endswith((".", "?", "!")):
        return text
    if str(text).lstrip().startswith("/"):
        return text                   # "/goal pause" is a command, typed exactly
    return title_case(str(text))


def _rgb(hexstr: str) -> RGBColor:
    return RGBColor.from_string(hexstr)


def _text_height(text: str, w: float, size_pt: float,
                 factor: float = 0.58, leading: float = 1.25) -> float:
    """Estimated rendered height, in inches, for text wrapped into width `w`.

    Used so boxes size themselves to their content instead of carrying a
    hardcoded height that rots when the copy changes.

    `factor` is deliberately a little wider than check_deck.py's 0.55, so an
    auto-sized box is never one line short of what the linter thinks it needs.
    """
    per_line = max(1, int(w * 72 / (size_pt * factor)))
    lines = sum(max(1, -(-len(block) // per_line))
                for block in str(text).split("\n"))
    return max(0.28, lines * size_pt * leading / 72)


def _est_width(text: str, size_pt: float, bold: bool = False) -> float:
    """Rough rendered width of Arial text, in inches. Used to size highlight pills."""
    factor = 0.58 if bold else 0.52
    return len(text) * size_pt * factor / 72.0


# --------------------------------------------------------------------------
# Deck
# --------------------------------------------------------------------------
class Deck:
    """A presentation built on the bootcamp template."""

    def __init__(self, template: str | Path = TEMPLATE):
        self.prs = Presentation(str(template))
        self._layouts = {l.name: l for l in self.prs.slide_masters[0].slide_layouts}

    # -- layout helpers ----------------------------------------------------
    def _add(self, layout_name: str) -> "Slide":
        layout = self._layouts[layout_name]
        slide = self.prs.slides.add_slide(layout)
        _clone_slide_number(slide, layout)
        return Slide(slide, self)

    def title(self, title: str, subtitle: str = "") -> "Slide":
        """Opening slide. Big Oswald title over a Source Code Pro subtitle."""
        s = self._add("TITLE")
        s.set_ph(0, title_case(title))
        if subtitle:
            s.set_ph(1, subtitle)
            _bullet_policy(s._ph(1).text_frame)
        else:
            s.drop_ph(1)
        return s

    def content(self, title: str, phase: str | None = None) -> "Slide":
        """Workhorse slide: title + free canvas.

        `phase` prefixes the title with one of the three arc labels. There are
        deliberately no full-page divider slides - a slide that says only
        "What is it?" is fluff, so the phase rides on the slide that answers it.
        """
        s = self._add("TITLE_AND_BODY")
        prefix = PHASES[phase] if phase else None
        s.set_ph(0, title_case(f"{prefix} - {title}" if prefix else title))
        return s

    def what(self, title: str) -> "Slide":
        """Opens the what-is-it arc. No prefix - the title leads with the answer."""
        return self.content(title, phase="what")

    def how(self, title: str) -> "Slide":
        """Opens the mechanism arc: 'How it works - <the point>'."""
        return self.content(title, phase="how")

    def why(self, title: str) -> "Slide":
        """Opens the consequences arc: 'Why it matters - <the point>'."""
        return self.content(title, phase="why")

    def two_columns(self, title: str, left, right,
                    left_heading: str | None = None,
                    right_heading: str | None = None) -> "Slide":
        """Two columns of bullets, each with an optional heading.

        Pass headings as arguments rather than as a first line followed by a blank
        line - a blank paragraph inside the placeholder renders as an empty bullet
        and a ragged gap.
        """
        s = self._add("TITLE_AND_TWO_COLUMNS")
        s.set_ph(0, title_case(title))
        top = 1.61
        if left_heading or right_heading:
            top = 2.05
            for x, head in ((0.34, left_heading), (5.28, right_heading)):
                if head:
                    s.text(x, 1.58, 4.37, 0.30, head, size=14, color=INK,
                           bold=True, font=BODY_FONT)
        for idx, col in ((1, left), (2, right)):
            items = [col] if isinstance(col, str) else list(col)
            s.set_ph(idx, "\n".join(items))
            s.move_ph(idx, top=top, height=FOOTER_Y - 0.12 - top)
            _bullet_policy(s._ph(idx).text_frame)
        return s

    def exercise(self, title: str, eyebrow: str = "EXERCISE",
                 minutes: int | None = None) -> "Slide":
        """A hands-on slide, with a header that says so at a glance.

        Built on BLANK, so it carries neither the layout's dashed divider nor a
        bulleted body placeholder. The accent band marks the moment the lecture
        stops explaining and asks the student to do something - the same signal
        every time it happens, in any deck.

        Content below the band starts at 1.10".
        """
        s = self._add("BLANK")
        band_h = 0.76                     # one line: title left, timing right
        s.rect(0, 0, SLIDE_W, band_h, fill=ACCENT)
        mid = band_h / 2

        tag = eyebrow.upper()
        if minutes:
            tag += f"  \u00b7  {minutes} MINUTE" + ("S" if minutes > 1 else "")

        # Real character tracking, not padding with spaces: spaces would inflate
        # the width and squeeze the title beside it.
        TRACK = 180                       # hundredths of a point
        tag_w = len(tag) * (SZ_CAPTION * 0.60 + TRACK / 100) / 72
        right = SLIDE_W - 0.55
        tag_x = right - tag_w
        cd = 0.185
        cx, cy = tag_x - cd - 0.13, mid - cd / 2

        face = s.raw.shapes.add_shape(MSO_SHAPE.OVAL, Inches(cx), Inches(cy),
                                      Inches(cd), Inches(cd))
        face.fill.background()
        face.line.color.rgb = _rgb("FBE4EC")
        face.line.width = Pt(1.1)
        face.shadow.inherit = False
        face.text_frame.text = ""
        mx, my = cx + cd / 2, cy + cd / 2
        s.rect(mx - 0.006, my - 0.055, 0.012, 0.055, fill="FBE4EC")   # hour hand
        s.rect(mx, my - 0.006, 0.050, 0.012, fill="FBE4EC")           # minute hand

        # 12pt is the floor everywhere on a slide, eyebrows included.
        _tag = s.text(tag_x, 0, tag_w + 0.06, band_h, tag, size=SZ_CAPTION,
                      color="FBE4EC", bold=True, font=BODY_FONT, anchor="m",
                      wrap=False)
        for _p in _tag.text_frame.paragraphs:
            for _r in _p.runs:
                _r.font._rPr.set("spc", str(TRACK))
        # The title takes whatever is left, so a long one cannot run under the
        # clock - and it steps down a size rather than wrapping inside a band that
        # is only one line tall.
        avail = cx - 0.55 - 0.30
        cased = title_case(title)
        size = 26
        while size > 18 and len(cased) * size * 0.55 / 72 > avail:
            size -= 2
        s.text(0.55, 0, avail, band_h, cased, size=size,
               color="FFFFFF", font=HEAD_FONT, anchor="m", wrap=False)
        return s

    def handoff(self, items, title: str = "Let's see it in action",
                lead: str | None = None) -> "Slide":
        """The closing slide: a full-page transition into the instructor demo.

        Built on BLANK so it carries neither the layout's dashed divider nor a
        bulleted body placeholder - the whole page is composed here. `items` are
        the two to four things the instructor is about to do live.
        """
        s = self._add("BLANK")
        band_h = 1.72
        s.rect(0, 0, SLIDE_W, band_h, fill=ACCENT)
        s.text(0.55, 0, 8.9, band_h, title_case(title), size=40, color="FFFFFF",
               font=HEAD_FONT, anchor="m")
        top = band_h + 0.34
        if lead:
            s.text(0.55, top, 8.9, 0.42, lead, size=15, color=INK,
                   font=BODY_FONT, spacing=1.2)
            top += 0.62
        s.cards(0.55, top, 8.9, items, h=min(1.85, FOOTER_Y - 0.25 - top))
        return s

    def prompt_template(self, title: str, body: str) -> "Slide":
        """Full-width monospace block - for prompt templates with {placeholders}."""
        s = self._add("TITLE_AND_BODY")
        s.set_ph(0, title_case(title))
        s.set_ph(1, body)
        _bullet_policy(s._ph(1).text_frame, force_off=True)
        return s

    def save(self, path: str | Path) -> Path:
        for s in self.prs.slides:
            _drop_empty_placeholders(s)
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.prs.save(str(path))
        return path


def _bullet_policy(text_frame, force_off: bool = False) -> None:
    """Bullets mark a list. One point is a sentence, so it gets no glyph."""
    paras = [p for p in text_frame.paragraphs
             if "".join(r.text for r in p.runs).strip()]
    if force_off or len(paras) <= 1:
        for para in text_frame.paragraphs:
            _no_bullet(para)


def _no_bullet(paragraph) -> None:
    """Suppress the inherited bullet glyph on a paragraph.

    Bullet elements must sit after the spacing elements and before defRPr, so
    insert rather than append.
    """
    pPr = paragraph._p.get_or_add_pPr()
    # A bullet also carries a left margin and a negative first-line indent. Leave
    # those behind and the copy renders with a ragged hanging indent.
    pPr.set("marL", "0")
    pPr.set("indent", "0")
    for tag in ("buChar", "buAutoNum", "buNone", "buSzPts", "buSzPct"):
        for old in pPr.findall(f"{A}{tag}"):
            pPr.remove(old)
    bu = etree.Element(f"{A}buNone")
    defRPr = pPr.find(f"{A}defRPr")
    if defRPr is not None:
        defRPr.addprevious(bu)
    else:
        pPr.append(bu)


def _clone_slide_number(slide, layout) -> None:
    """Copy the layout's slide-number placeholder onto the slide.

    python-pptx only clones body/title placeholders, so without this the page
    numbers silently vanish.
    """
    for ph in layout.placeholders:
        if ph.placeholder_format.idx == 12:
            slide.shapes._spTree.append(copy.deepcopy(ph._element))
            return


def _drop_empty_placeholders(slide) -> None:
    """Remove untouched placeholders so editors don't show 'Click to add text'."""
    for ph in list(slide.placeholders):
        if ph.placeholder_format.idx == 12:
            continue
        if not ph.text_frame.text.strip():
            ph._element.getparent().remove(ph._element)


# --------------------------------------------------------------------------
# Slide
# --------------------------------------------------------------------------
class Slide:
    def __init__(self, slide, deck: Deck):
        self._s = slide
        self._deck = deck

    @property
    def raw(self):
        return self._s

    # -- placeholders ------------------------------------------------------
    def set_ph(self, idx: int, text: str) -> None:
        """Fill a placeholder. Never sets a font - inheritance carries Oswald /
        Source Code Pro down from the master, which keeps every deck on-style."""
        tf = self._ph(idx).text_frame
        lines = [ln for ln in text.split("\n")]
        tf.text = lines[0]
        for line in lines[1:]:
            tf.add_paragraph().text = line

    def _ph(self, idx: int):
        for ph in self._s.placeholders:
            if ph.placeholder_format.idx == idx:
                return ph
        raise KeyError(f"no placeholder idx={idx} on this layout")

    def drop_ph(self, idx: int) -> None:
        ph = self._ph(idx)
        ph._element.getparent().remove(ph._element)

    def layout_box(self, idx: int):
        """Inherited geometry of a placeholder, read off the slide's layout."""
        for lph in self._s.slide_layout.placeholders:
            if lph.placeholder_format.idx == idx:
                return lph.left, lph.top, lph.width, lph.height
        return None

    def move_ph(self, idx: int, left=None, top=None, width=None, height=None):
        """Reposition a placeholder without losing its inherited geometry.

        A cloned placeholder usually carries no <a:xfrm> - position comes from the
        layout. Setting only .top would create an xfrm with x=0 and slam the shape
        against the left edge, so resolve all four values first.
        """
        ph = self._ph(idx)
        box = self.layout_box(idx)
        lx, lt, lw, lh = box if box else (ph.left, ph.top, ph.width, ph.height)
        ph.left = Inches(left) if left is not None else (ph.left if ph.left is not None else lx)
        ph.top = Inches(top) if top is not None else (ph.top if ph.top is not None else lt)
        ph.width = Inches(width) if width is not None else (ph.width if ph.width is not None else lw)
        ph.height = Inches(height) if height is not None else (ph.height if ph.height is not None else lh)
        return ph

    def body(self, text: str, box: tuple | None = None) -> None:
        """Body copy. With no box, uses the layout's body placeholder position."""
        ph = self._ph(1)
        if box:
            ph.left, ph.top, ph.width, ph.height = (Inches(v) for v in box)
        tf = ph.text_frame
        tf.word_wrap = True
        lines = text.split("\n")
        tf.text = lines[0]
        for line in lines[1:]:
            tf.add_paragraph().text = line
        _bullet_policy(tf)

    def beside(self, visual, text, gap=0.55, margin=0.34, h=None) -> None:
        """Place body copy in the space left over beside a visual.

        Derives the box from the visual's *actual* geometry, so copy stays put
        when a mock is resized by .fit() or .composer(pin=False). Prefer this to
        passing a hardcoded box - hardcoded numbers rot the moment the mock
        changes size.

        `visual` is a Mock, or any object exposing .x / .y / .w / .h.
        """
        vx, vy, vw, vh = visual.x, visual.y, visual.w, visual.h
        right = SLIDE_W - margin - (vx + vw + gap)
        left = (vx - gap) - margin
        x, w = ((vx + vw + gap), right) if right >= left else (margin, left)
        w = max(w, 1.5)

        # Size the box to the copy, not to the visual. Body text inherits 18pt, so
        # a paragraph that reads fine beside a tall mock silently overflows beside
        # a short one. Grow past the visual when needed, stay inside the canvas,
        # and keep the block centred on the visual so the pairing still reads.
        if h is not None:
            height, top = h, vy
        else:
            needed = _text_height(text, w, 18.0, factor=0.58, leading=1.20) + 0.12
            # Never grow up into the title band: cap at the usable canvas first,
            # so the centring clamp below cannot push the box above CONTENT_TOP.
            # If the copy still will not fit, the linter's text-overflow rule
            # says so - which is the honest signal that the copy is too long.
            usable = FOOTER_Y - 0.10 - CONTENT_TOP
            height = min(max(vh, needed), usable)
            top = min(max(CONTENT_TOP, vy + vh / 2 - height / 2),
                      FOOTER_Y - 0.10 - height)
        ph = self._ph(1)
        ph.left, ph.top = Inches(x), Inches(top)
        ph.width, ph.height = Inches(w), Inches(height)
        tf = ph.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE      # optically balanced with the mock
        lines = text.split("\n")
        tf.text = lines[0]
        for line in lines[1:]:
            tf.add_paragraph().text = line
        _bullet_policy(tf)

    # -- primitives --------------------------------------------------------
    def rect(self, x, y, w, h, fill=None, rounded=False, radius=0.06,
             line=None, line_w=1.0):
        shape = self._s.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
            Inches(x), Inches(y), Inches(w), Inches(h),
        )
        if rounded:
            with contextlib.suppress(Exception):
                shape.adjustments[0] = min(0.5, radius / max(min(w, h), 0.01))
        if fill:
            shape.fill.solid()
            shape.fill.fore_color.rgb = _rgb(fill)
        else:
            shape.fill.background()
        if line:
            shape.line.color.rgb = _rgb(line)
            shape.line.width = Pt(line_w)
        else:
            shape.line.fill.background()
        shape.shadow.inherit = False
        shape.text_frame.text = ""
        return shape

    def text(self, x, y, w, h, text, size=SZ_BODY, color=TEXT, bold=False,
             font=UI_FONT, align="l", anchor="t", wrap=True, spacing=None):
        box = self._s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = box.text_frame
        tf.word_wrap = wrap
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE,
                              "b": MSO_ANCHOR.BOTTOM}[anchor]
        for i, line in enumerate(str(text).split("\n")):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER,
                           "r": PP_ALIGN.RIGHT}[align]
            if spacing:
                p.line_spacing = spacing
            run = p.add_run()
            run.text = line
            run.font.name = font
            run.font.size = Pt(size)
            run.font.bold = bold
            run.font.color.rgb = _rgb(color)
        return box

    def disc(self, x, y, d, label, fill=ACCENT, color="FFFFFF", size=17):
        """A filled circle with a centred numeral - the step markers on cards."""
        shape = self._s.shapes.add_shape(
            MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
        shape.fill.solid()
        shape.fill.fore_color.rgb = _rgb(fill)
        shape.line.fill.background()
        shape.shadow.inherit = False
        shape.text_frame.text = ""
        self.text(x, y, d, d, label, size=size, color=color, bold=True,
                  font=HEAD_FONT, align="c", anchor="m")
        return shape

    def arrow(self, x, y, w, h=0.12, color=ARROW, direction="right"):
        shape = self._s.shapes.add_shape(
            {"right": MSO_SHAPE.RIGHT_ARROW, "left": MSO_SHAPE.LEFT_ARROW,
             "up": MSO_SHAPE.UP_ARROW, "down": MSO_SHAPE.DOWN_ARROW}[direction],
            Inches(x), Inches(y), Inches(w), Inches(h),
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = _rgb(color)
        shape.line.fill.background()
        shape.shadow.inherit = False
        return shape

    def caption(self, x, y, w, text, size=SZ_CAPTION, color=SOFT_INK, h=None):
        """Note on the white area. Source Code Pro, never below 12pt.

        Height is measured from the text rather than fixed, so a caption never
        claims space it does not use and never trips the footer band by accident.
        """
        size = max(size, SZ_CAPTION)
        if h is None:
            h = _text_height(text, w, size, factor=0.55, leading=1.35)
        return self.text(x, y, w, h, text, size=size,
                         color=color, font=BODY_FONT, spacing=1.25)

    # -- components --------------------------------------------------------
    def mock(self, x, y, w, h, app=None, tag=None, generic=False) -> "Mock":
        """A tool window.

        Defaults to the house convention: ChatGPT / Demonstration when showing the
        product, AI Assistant / Example when showing a generic prompt pattern
        (pass generic=True). Override `app`/`tag` only with a reason.
        """
        d_app, d_tag = APP_GENERIC if generic else APP_PRODUCT
        return Mock(self, x, y, w, h, app or d_app, tag or d_tag)

    # -- canonical mock patterns -------------------------------------------
    # The three panels the source deck uses over and over. Reference images live
    # in assets/reference/pattern-*.png. Reach for these before hand-rolling a
    # mock, so the same idea looks the same in every lecture.

    def chat_demo(self, x, y, w, h, prompt, results=None, reply=None,
                  cols=2, app=None, tag=None, generic=False,
                  note=None, highlight=None, composer=True) -> "Mock":
        """Pattern 1 - a chat turn with a listed answer.

        assets/reference/pattern-chat-demo.png

        `results` renders as a numbered multi-column list (the 10 product names);
        `reply` is a plain sentence instead. `note` adds a trailing labelled line,
        e.g. ("Memory updated", "Writes in British English.").
        """
        m = self.mock(x, y, w, h, app=app, tag=tag, generic=generic)
        m.label(ROLE_USER)
        m.para(prompt)
        m.gap(0.08)
        with m.bubble():
            m.label(ROLE_AI)
            if results:
                m.columns(list(results), cols=cols)
            if reply:
                m.line(reply, highlight=(highlight == "reply"))
        if note:
            m.gap(0.04)
            m.label(note[0]).line(note[1], highlight=(highlight == "note"))
        if composer:
            m.composer(pin=False)
        else:
            m.fit()
        return m

    def prompt_example(self, x, y, w, h, prompt, table=None, reply=None,
                       app=None, tag=None, generic=True,
                       col_widths=None, fit=False) -> "Mock":
        """Pattern 2 - a long structured prompt and its tabular answer.

        assets/reference/pattern-prompt-example.png

        `prompt` may contain blank lines; they are preserved, which is what makes
        a multi-part prompt (examples, criteria, steps) readable.
        """
        m = self.mock(x, y, w, h, app=app, tag=tag, generic=generic)
        m.label(ROLE_USER)
        m.para(prompt, size=SZ_LABEL + 0.9)
        m.gap(0.10)
        with m.bubble():
            m.label(ROLE_AI)
            if table:
                m.table(table, col_widths=col_widths)
            if reply:
                m.line(reply)
        if fit:
            m.fit()
        return m

    def image_generator(self, x, y, w, h, prompt, images=None, negative=None,
                        reference=None, app="Image Generator", tag="Example",
                        cols=2) -> "Mock":
        """Pattern 3 - a prompt beside the images it produced.

        assets/reference/pattern-image-generator.png

        `images` is a list of file paths; pass None entries (or fewer paths than
        tiles) to draw empty placeholder tiles. Generated illustration is the one
        place bitmaps belong - see references/anti-drift.md.
        """
        m = self.mock(x, y, w, h, app=app, tag=tag)
        text_w = w * 0.46
        m._width_override = text_w - 2 * PAD_X   # set before any text is written
        m.label("Prompt")
        m.para(prompt, size=SZ_BODY)
        if negative:
            m.gap(0.16)
            m.label("Negative prompt")
            m.para(negative, size=SZ_BODY)
        if reference:
            m.gap(0.14)
            m.label("Reference image")

        # image grid on the right
        grid_x = x + text_w
        grid_w = w - text_w - PAD_X
        rows = -(-max(len(images or []), cols) // cols)
        tile = min((grid_w - 0.14 * (cols - 1)) / cols,
                   (h - HEADER_H - 0.34 - 0.14 * (rows - 1)) / rows)
        for i in range(rows * cols):
            gx = grid_x + (i % cols) * (tile + 0.14)
            gy = y + HEADER_H + 0.20 + (i // cols) * (tile + 0.14)
            path = (images or [None] * (rows * cols))[i] if i < len(images or []) else None
            if path:
                self._s.shapes.add_picture(str(path), Inches(gx), Inches(gy),
                                           Inches(tile), Inches(tile))
            else:
                self.rect(gx, gy, tile, tile, fill=BUBBLE, rounded=True, radius=0.05)
                self.text(gx, gy, tile, tile, "generated\nimage", size=SZ_LABEL,
                          color=MUTED, align="c", anchor="m")
        return m

    def message_row(self, x, y, w, h=0.85) -> "Row":
        """A single exchange row sitting directly on the slide, no window chrome."""
        self.rect(x, y, w, h, fill=PANEL, rounded=True)
        return Row(self, x, y, w, h)

    def table(self, x, y, w, h, data, col_widths=None, size=SZ_TABLE,
              zebra=False):
        """A light editorial table: white cells, horizontal rules only.

        Deliberately not the dark mock-UI palette - a table is slide content, not
        a screenshot of a product, so it lives on the white surface.
        """
        rows, cols = len(data), len(data[0])
        gfx = self._s.shapes.add_table(rows, cols, Inches(x), Inches(y),
                                       Inches(w), Inches(h))
        tbl = gfx.table
        _plain_table(tbl)
        if col_widths:
            total = sum(col_widths)
            for i, cw in enumerate(col_widths):
                tbl.columns[i].width = Emu(int(Inches(w) * cw / total))
        for r, row in enumerate(data):
            tbl.rows[r].height = Inches(max(0.30, h / rows))
            for c, val in enumerate(row):
                cell = tbl.cell(r, c)
                bg = "FFFFFF"
                if r > 0 and zebra and r % 2 == 0:
                    bg = "FAFAFB"
                cell.fill.solid()
                cell.fill.fore_color.rgb = _rgb(bg)
                cell.margin_left = cell.margin_right = Inches(0.10)
                cell.margin_top = cell.margin_bottom = Inches(0.04)
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                tf = cell.text_frame
                tf.word_wrap = True
                p = tf.paragraphs[0]
                run = p.add_run()
                run.text = str(val)
                run.font.name = BODY_FONT
                run.font.size = Pt(size)
                run.font.bold = (r == 0)
                run.font.color.rgb = _rgb(INK)
                # Rule under the header is heavier; body rows get a hairline.
                _cell_rules(cell,
                            bottom=(INK, 1.25) if r == 0 else (RULE, 0.75),
                            top=(RULE, 0.75) if r == 0 else None)
        return gfx

    def steps(self, x, y, w, items, gap=0.14, h=0.52, size=SZ_DIAGRAM):
        """Numbered mechanism steps as stacked pills - for 'How it works'."""
        cur = y
        for i, item in enumerate(items, 1):
            self.rect(x, cur, w, h, fill=NODE_BG, rounded=True,
                      line=RULE, line_w=0.75)
            self.text(x + 0.18, cur, 0.32, h, f"{i}", size=size, color=ACCENT,
                      bold=True, font=BODY_FONT, anchor="m")
            self.text(x + 0.56, cur, w - 0.74, h, item, size=size, color=INK,
                      font=BODY_FONT, anchor="m")
            cur += h + gap
        return cur

    def cards(self, x, y, w, items, h=2.00, gap=0.28, size=SZ_DIAGRAM):
        """Numbered cards across the width. Used by the closing handoff slide.

        Each item is "Label" or ("Label", "sub-label").

        Title Case labels run long, so the card lays out top-down instead of
        pinning the sub-label to the bottom: every sub-label starts on one shared
        line just under the tallest label, and the cards grow (never past the
        footer) when the copy needs it. Label and sub-label never collide, and the
        label keeps its full size so the two stay visibly different.
        """
        n = len(items)
        cw = (w - gap * (n - 1)) / n
        tw = cw - 0.44
        pairs = []
        for item in items:
            label, sub = item if isinstance(item, (tuple, list)) else (item, None)
            pairs.append((_label_case(label), _label_case(sub)))
        # Padded estimates: Keynote wraps earlier than the character count suggests.
        lab_h = max(_text_height(l, tw, size, factor=0.64, leading=1.2)
                    for l, _ in pairs)
        sub_h = max((_text_height(s, tw, SZ_CAPTION, factor=0.64, leading=1.15)
                     for _, s in pairs if s), default=0.0)
        top = 0.74
        sub_y = top + lab_h + (LABEL_GAP + 0.04 if sub_h else 0.0)
        need = sub_y + sub_h + 0.18
        h = min(max(h, need), FOOTER_Y - 0.12 - y)
        for i, (label, sub) in enumerate(pairs):
            cx = x + i * (cw + gap)
            self.rect(cx, y, cw, h, fill="FFFFFF", rounded=True, radius=0.05,
                      line=RULE, line_w=0.75)
            self.disc(cx + 0.24, y + 0.24, 0.42, f"{i + 1}")
            self.text(cx + 0.22, y + top, tw, lab_h, label, size=size, color=INK,
                      font=BODY_FONT, spacing=1.2)
            if sub:
                self.text(cx + 0.22, y + sub_y, tw, sub_h, sub, size=SZ_CAPTION,
                          color=SOFT_INK, font=BODY_FONT, spacing=1.15)
        return y + h

    # -- vector concept art -------------------------------------------------
    def node(self, x, y, w, h, label, sub=None, accent=False, size=SZ_DIAGRAM):
        """A labelled box. The atom of every concept diagram."""
        label, sub = _label_case(label), _label_case(sub)
        self.rect(x, y, w, h, fill=NODE_ACC if accent else NODE_BG, rounded=True,
                  radius=0.05, line=ACCENT if accent else RULE,
                  line_w=1.0 if accent else 0.75)
        if sub:
            # Label sits bottom-anchored in the upper half, sub top-anchored below,
            # with a real gap between them. These two boxes used to overlap by 3%
            # of the node height, which read as cramped type in every diagram.
            # Measure both, then centre the pair as one block with a real gap
            # between them. Splitting the node in half instead leaves the two
            # lines cramped in a short node and stranded apart in a tall one.
            # Padded like cards(): Keynote wraps Title Case labels earlier than
            # the character count predicts, and an unpadded estimate collides.
            lab_h = _text_height(label, w - 0.20, size, factor=0.64, leading=1.15)
            sub_h = _text_height(sub, w - 0.20, SZ_CAPTION, factor=0.64, leading=1.15)
            top = y + max(0.06, (h - (lab_h + LABEL_GAP + sub_h)) / 2)
            self.text(x + 0.10, top, w - 0.20, lab_h, label, size=size,
                      color=INK, bold=True, font=BODY_FONT, align="c", anchor="t",
                      spacing=1.15)
            self.text(x + 0.10, top + lab_h + LABEL_GAP, w - 0.20, sub_h, sub,
                      size=SZ_CAPTION, color=SOFT_INK, font=BODY_FONT,
                      align="c", anchor="t", spacing=1.15)
        else:
            self.text(x + 0.10, y, w - 0.20, h, label, size=size, color=INK,
                      bold=accent, font=BODY_FONT, align="c", anchor="m")
        return (x, y, w, h)

    def flow(self, x, y, w, items, h=0.80, accent_last=False, loop=None):
        """Left-to-right pipeline of boxes joined by arrows.

        items may be "Label" or ("Label", "sub-label").
        loop="text" draws a return arrow underneath, for cyclic mechanisms.
        """
        n = len(items)
        arrow_w = 0.34
        box_w = (w - arrow_w * (n - 1)) / n
        boxes = []
        for i, item in enumerate(items):
            label, sub = item if isinstance(item, (tuple, list)) else (item, None)
            bx = x + i * (box_w + arrow_w)
            boxes.append(self.node(bx, y, box_w, h, label, sub=sub,
                                   accent=(accent_last and i == n - 1)))
            if i < n - 1:
                self.arrow(bx + box_w + 0.07, y + h / 2 - 0.05, arrow_w - 0.14, 0.10)
        if loop:
            ly = y + h + 0.30
            self.rect(x + box_w / 2, ly, w - box_w, 0.012, fill=ARROW)
            self.rect(x + w - box_w / 2, y + h, 0.012, ly - y - h, fill=ARROW)
            self.arrow(x + box_w / 2 - 0.02, y + h, 0.10, ly - y - h,
                       direction="up")
            self.text(x, ly + 0.08, w, 0.26, loop, size=SZ_CAPTION,
                      color=SOFT_INK, font=BODY_FONT, align="c")
        return boxes

    def layers(self, x, y, w, items, h=0.46, gap=0.07, size=SZ_DIAGRAM):
        """Stacked bands - the best way to draw 'what actually reaches the model'.

        Each item is "Label", ("Label", "note") or ("Label", "note", accent).
        """
        cur = y
        for item in items:
            label, note, accent = (item, None, False) if isinstance(item, str) \
                else (tuple(item) + (None, False))[:3]
            accent = bool(accent)
            label, note = _label_case(label), _label_case(note)
            self.rect(x, cur, w, h, fill=NODE_ACC if accent else NODE_BG,
                      rounded=True, radius=0.04,
                      line=ACCENT if accent else RULE, line_w=1.0 if accent else 0.75)
            self.text(x + 0.16, cur, w * 0.52, h, label, size=size, color=INK,
                      bold=accent, font=BODY_FONT, anchor="m")
            if note:
                self.text(x + w * 0.55, cur, w * 0.43 - 0.16, h, note,
                          size=SZ_CAPTION, color=SOFT_INK, font=BODY_FONT,
                          align="r", anchor="m")
            cur += h + gap
        return cur

    def compare(self, y, left_title, left_items, right_title, right_items,
                x=0.34, w=9.32, gap=0.40, h=2.60):
        """Two labelled panels side by side - before/after, does/doesn't."""
        col = (w - gap) / 2
        for cx, title, items, accent in (
            (x, left_title, left_items, False),
            (x + col + gap, right_title, right_items, True),
        ):
            self.rect(cx, y, col, h, fill="FFFFFF", rounded=True,
                      line=ACCENT if accent else RULE, line_w=1.0 if accent else 0.75)
            self.text(cx + 0.20, y + 0.16, col - 0.40, 0.30, _label_case(title),
                      size=14, color=ACCENT if accent else INK, bold=True,
                      font=BODY_FONT)
            cur = y + 0.60
            for item in items:
                # Rows size to their text, so a longer item wraps instead of
                # overflowing. A single-line row keeps its original 0.34" step.
                line = f"—  {item}"
                ih = max(0.30, _text_height(line, col - 0.40, SZ_DIAGRAM,
                                            leading=1.20))
                self.text(cx + 0.20, cur, col - 0.40, ih, line,
                          size=SZ_DIAGRAM, color=INK, font=BODY_FONT,
                          spacing=1.15)
                cur += ih + 0.04
        return y + h


def _plain_table(tbl) -> None:
    """Strip PowerPoint's banded default so our own cell fills and rules show."""
    tbl.first_row = False
    tbl.horz_banding = False
    tblPr = tbl._tbl.tblPr
    for child in list(tblPr):
        if child.tag.endswith("}tableStyleId"):
            tblPr.remove(child)
    el = etree.SubElement(tblPr, f"{A}tableStyleId")
    # "No Style, No Grid" - we draw our own horizontal rules and want no others.
    el.text = "{2D5ABB26-0587-4C30-8999-92F81FD0307C}"


def _cell_rules(cell, bottom=None, top=None, left=None, right=None) -> None:
    """Cell borders. Schema order is lnL, lnR, lnT, lnB, all before any fill."""
    tcPr = cell._tc.get_or_add_tcPr()
    for tag in (f"{A}lnL", f"{A}lnR", f"{A}lnT", f"{A}lnB"):
        for old in tcPr.findall(tag):
            tcPr.remove(old)
    # insert in reverse schema order, each at 0, so the result is L, R, T, B
    for tag, spec in ((f"{A}lnB", bottom), (f"{A}lnT", top),
                      (f"{A}lnR", right), (f"{A}lnL", left)):
        if not spec:
            continue
        color, width_pt = spec
        ln = etree.Element(tag)
        ln.set("w", str(int(width_pt * 12700)))
        ln.set("cap", "flat")
        fill = etree.SubElement(ln, f"{A}solidFill")
        clr = etree.SubElement(fill, f"{A}srgbClr")
        clr.set("val", color)
        tcPr.insert(0, ln)


# --------------------------------------------------------------------------
# Mock window - flowing layout
# --------------------------------------------------------------------------
class Mock:
    """A tool window drawn as vector shapes. Content flows top-down."""

    def __init__(self, slide: Slide, x, y, w, h, app, tag):
        self.s, self.x, self.y, self.w, self.h = slide, x, y, w, h
        self._panel = slide.rect(x, y, w, h, fill=PANEL, rounded=True)
        slide.rect(x, y, w, HEADER_H, fill=HEADER, rounded=True)
        # square off the title bar's lower corners, exactly as the source deck does
        slide.rect(x, y + HEADER_H * 0.64, w, HEADER_H * 0.36, fill=HEADER)
        slide.text(x + PAD_X, y + 0.09, w * 0.7, 0.20, app,
                   size=SZ_APP, color=TEXT, bold=True)
        if tag:
            slide.text(x + w - PAD_X - 1.2, y + 0.11, 1.2, 0.19, tag,
                       size=SZ_LABEL, color=MUTED, align="r")
        self._y = y + HEADER_H + 0.14
        self._stack: list[float] = []
        self._width_override: float | None = None

    # -- flow --------------------------------------------------------------
    @property
    def cursor(self) -> float:
        return self._y

    def gap(self, amount=GAP) -> "Mock":
        self._y += amount
        return self

    def label(self, text: str) -> "Mock":
        """Small muted role label. Prefer .user() / .assistant() / .system()."""
        self.s.text(self._inset(), self._y, 1.9, 0.19, text,
                    size=SZ_LABEL, color=MUTED, bold=True)
        self._y += 0.22
        return self

    def line(self, text: str, highlight=False, color=TEXT, size=SZ_BODY) -> "Mock":
        """One line of message text, optionally on a highlight pill."""
        x = self._inset()
        if highlight:
            pill_w = min(_est_width(text, size) + 0.10, self._width() + 0.02)
            self.s.rect(x - 0.05, self._y - 0.01, pill_w, LINE_H - 0.01,
                        fill=HL, rounded=True, radius=0.04)
        self.s.text(x, self._y, self._width(), LINE_H, text,
                    size=size, color=color, wrap=False)
        self._y += LINE_H
        return self

    def para(self, text: str, size=SZ_BODY, color=TEXT) -> "Mock":
        """Wrapped block of message text. Height is estimated from the box width."""
        w = self._width()
        chars_per_line = max(1, int(w * 72 / (size * 0.52)))
        n = sum(max(1, -(-len(b) // chars_per_line)) for b in text.split("\n"))
        h = n * LINE_H
        self.s.text(self._inset(), self._y, w, h, text,
                    size=size, color=color, spacing=1.0)
        self._y += h + 0.04
        return self

    # -- roles (house convention) -------------------------------------------
    def user(self, *lines, highlight=False) -> "Mock":
        return self._turn(ROLE_USER, lines, highlight)

    def assistant(self, *lines, highlight=False) -> "Mock":
        return self._turn(ROLE_AI, lines, highlight)

    def system(self, *lines, highlight=False) -> "Mock":
        return self._turn(ROLE_SYSTEM, lines, highlight)

    def _turn(self, role, lines, highlight) -> "Mock":
        self.label(role)
        for i, ln in enumerate(lines):
            self.line(ln, highlight=highlight and i == 0)
        return self.gap(0.06)

    def table(self, data, col_widths=None, size=SZ_LABEL, row_h=0.26) -> "Mock":
        """A table *inside* the mock, as a product would render it.

        Dark cells, white hairline grid, Arial - this one stays dark on purpose:
        it is mocked product output, not slide content. The light editorial table
        is `slide.table()`; do not mix the two up.
        """
        rows, cols = len(data), len(data[0])
        w = self._width()
        h = rows * row_h
        gfx = self.s.raw.shapes.add_table(rows, cols, Inches(self._inset()),
                                          Inches(self._y), Inches(w), Inches(h))
        tbl = gfx.table
        _plain_table(tbl)
        if col_widths:
            total = sum(col_widths)
            for i, cw in enumerate(col_widths):
                tbl.columns[i].width = Emu(int(Inches(w) * cw / total))
        for r, row in enumerate(data):
            tbl.rows[r].height = Inches(row_h)
            for c, val in enumerate(row):
                cell = tbl.cell(r, c)
                cell.fill.solid()
                cell.fill.fore_color.rgb = _rgb(PANEL)
                cell.margin_left = cell.margin_right = Inches(0.05)
                cell.margin_top = cell.margin_bottom = Inches(0.01)
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                run = cell.text_frame.paragraphs[0].add_run()
                run.text = str(val)
                run.font.name = UI_FONT
                run.font.size = Pt(size)
                run.font.bold = (r == 0)
                run.font.color.rgb = _rgb(TEXT)
                _cell_rules(cell, bottom=(TEXT, 0.5), top=(TEXT, 0.5),
                            left=(TEXT, 0.5), right=(TEXT, 0.5))
        self._y += h + 0.06
        return self

    def divider(self) -> "Mock":
        self.s.rect(self._inset(), self._y + 0.04, self._width(), 0.01, fill=BUBBLE)
        self._y += 0.14
        return self

    def columns(self, items, cols=2, size=SZ_BODY) -> "Mock":
        """Numbered results laid out in columns."""
        per = -(-len(items) // cols)
        col_w = (self._width() - 0.1) / cols
        top = self._y
        for i, item in enumerate(items):
            c, r = divmod(i, per)
            self.s.text(self._inset() + c * col_w, top + r * LINE_H,
                        col_w - 0.06, LINE_H, item, size=size, color=TEXT, wrap=False)
        self._y = top + per * LINE_H
        return self

    @contextlib.contextmanager
    def bubble(self, pad=0.13):
        """Nested response panel. Open it BEFORE writing the lines it contains."""
        start = self._y
        self._stack.append(pad)
        self._y += pad
        insert_at = len(self.s.raw.shapes._spTree)
        yield self
        self._stack.pop()
        end = self._y + pad
        shape = self.s.rect(self.x + 0.12, start, self.w - 0.24, end - start,
                            fill=BUBBLE, rounded=True, radius=0.05)
        sp_tree = self.s.raw.shapes._spTree
        sp_tree.remove(shape._element)
        sp_tree.insert(insert_at, shape._element)
        self._y = end + 0.04

    def fit(self, pad=0.16) -> "Mock":
        """Shrink the window to the content actually written into it.

        Shrink only. If the content is taller than the box you asked for, the box
        stays put and the copy is too long - shorten it or start with a taller
        panel. Growing here would silently push the panel off the slide.
        """
        wanted = max(HEADER_H + 0.3, (self._y - self.y) + pad)
        self.h = min(self.h, wanted)
        self._panel.height = Inches(self.h)
        return self

    def composer(self, placeholder="Send a message…", pin=True) -> "Mock":
        """Input bar. pin=False flows it after the content and fits the panel."""
        if not pin:
            self.h = (self._y - self.y) + 0.33 + 0.24
            self._panel.height = Inches(self.h)
        bar_y = self.y + self.h - 0.33 - 0.12
        self.s.rect(self.x + PAD_X, bar_y, self.w - 2 * PAD_X, 0.33,
                    fill=BUBBLE, rounded=True, radius=0.05)
        self.s.text(self.x + PAD_X + 0.13, bar_y + 0.08, self.w - 1.0, 0.19,
                    placeholder, size=SZ_LABEL, color=MUTED)
        chip = self.x + self.w - PAD_X - 0.30
        self.s.rect(chip, bar_y + 0.05, 0.23, 0.23, fill=CHIP, rounded=True, radius=0.05)
        self.s.text(chip, bar_y + 0.05, 0.23, 0.23, "↑",
                    size=SZ_BODY, color=HEADER, align="c", anchor="m")
        return self

    # -- internals ---------------------------------------------------------
    def _inset(self) -> float:
        return self.x + PAD_X + (0.12 if self._stack else 0.0)

    def _width(self) -> float:
        if self._width_override is not None:
            return self._width_override
        return self.w - 2 * PAD_X - (0.24 if self._stack else 0.0)


class Row:
    """A single exchange row sitting directly on the slide (no window chrome)."""

    def __init__(self, slide: Slide, x, y, w, h):
        self.s, self.x, self.y, self.w, self.h = slide, x, y, w, h
        self._y = y + 0.13

    def label(self, text: str) -> "Row":
        self.s.text(self.x + 0.22, self._y, 1.9, 0.19, text,
                    size=SZ_LABEL, color=MUTED, bold=True)
        self._y += 0.23
        return self

    def line(self, text: str, highlight=False, size=SZ_BODY) -> "Row":
        x = self.x + 0.22
        if highlight:
            pill_w = min(_est_width(text, size) + 0.10, self.w - 0.4)
            self.s.rect(x - 0.05, self._y, pill_w, LINE_H, fill=HL,
                        rounded=True, radius=0.04)
        self.s.text(x, self._y + 0.01, self.w - 0.44, LINE_H, text,
                    size=size, color=TEXT, wrap=False)
        self._y += LINE_H
        return self
