#!/usr/bin/env python3
"""Build the principles deck for the "What is ChatGPT?" lecture.

    uv run --with python-pptx python decks/what-is-chatgpt/build_what_is_chatgpt.py

The deck is the foundational overview of Part 2. It teaches the thing that
survives a model generation - a next-token predictor with a product wrapped
around it - and introduces the six capabilities that turned the text box into a
system. Each of those six has its own lecture later, so every one of them gets a
single line here and nothing more.
"""
from pathlib import Path
import sys

SKILL = Path(__file__).resolve().parents[2] / ".claude" / "skills" / "principles-deck"
sys.path.insert(0, str(SKILL / "scripts"))

from deckkit import (  # noqa: E402
    BODY_FONT, SOFT_INK, SZ_CAPTION, Deck, ROLE_AI, ROLE_USER,
)
from pptx.util import Inches  # noqa: E402

ASSETS = Path(__file__).resolve().parent / "assets"


def picture(s, name, x, y, w, ratio):
    """Place a diagram from assets/, height derived from its real aspect ratio."""
    h = w / ratio
    s.raw.shapes.add_picture(str(ASSETS / name), Inches(x), Inches(y),
                             Inches(w), Inches(h))
    return y + h


OUT = Path(__file__).resolve().parent / "what-is-chatgpt.pptx"


def build() -> Path:
    d = Deck()

    # ---------------------------------------------------------------- title
    d.title(
        "What is ChatGPT?",
        "An assistant built on a next-token predictor, which now also searches, "
        "computes and acts on your behalf.",
    )

    # ------------------------------------------------------------ what is it
    s = d.what("a next-token predictor with a product wrapped around it")
    m = s.mock(0.40, 1.56, 4.60, 3.58)
    m.user("The students opened their")
    m.gap(0.06)
    with m.bubble():
        m.label("Candidate next tokens")
        m.line("books  ·  31%")
        m.line("laptops  ·  24%")
        m.line("minds  ·  12%")
        m.line("exams  ·  7%")
    m.gap(0.06)
    m.label("Chosen").line("books", highlight=True)
    m.fit()
    s.beside(
        m,
        "Every reply is produced one token at a time. The model scores its whole "
        "vocabulary against the text so far, picks one, and scores again.",
    )

    # The two diagrams from the original lecture: the intuition, then the
    # mechanism behind it. Both are third-party figures, credited on the slide.
    s = d.content("What would be the next word in this sentence?")
    picture(s, "next-word.png", 1.10, 1.86, 7.80, 3.51)
    s.caption(0.34, 4.12, 9.32,
              "Every one of those is a reasonable continuation. The model does not "
              "choose the right word - it scores them all, and one of them wins.")

    s = d.content("Predicting the next word (token)")
    picture(s, "predicting-token.png", 4.30, 1.56, 5.36, 1.60)
    s.body("A large language model is selecting the next most probable token, "
           "given a known vocabulary - then feeding its own answer back in and "
           "doing it again.",
           box=(0.34, 1.70, 3.60, 2.20))

    s = d.content("Six core ChatGPT features")
    s.table(0.34, 1.58, 9.32, 2.80, [
        ["Capability", "What it adds to a plain answer"],
        ["Web Search", "Live pages, read and cited at the moment you ask"],
        ["Deep Research", "A long multi-source investigation, returned as a report"],
        ["Data Analysis", "Code written and run over your files, rather than guessed at"],
        ["Agent Mode", "Multi-step tasks it carries out in a browser for you"],
        ["Plugins", "Connections to outside services, and the actions they allow"],
        ["Skills", "A workflow you wrote once, followed the same way every time"],
    ], col_widths=[2.0, 6.4])
    s.caption(0.34, 4.54, 9.32,
              "Each gets its own lecture later. Every one of them also costs "
              "something: time, tokens, or a service you have to trust.")

    s = d.content("One model, many surfaces")
    box_w, gap = (9.32 - 3 * 0.24) / 4, 0.24
    for i, (label, sub) in enumerate([
        ("The web app", "where most people meet it"),
        ("Desktop and mobile", "the same account, everywhere"),
        ("The API", "the engine, with no product"),
        ("Inside other tools", "reached through plugins"),
    ]):
        bx = 0.34 + i * (box_w + gap)
        s.node(bx, 1.58, box_w, 1.02, label, sub=sub)
        s.arrow(bx + box_w / 2 - 0.15, 2.68, 0.30, 0.52, direction="down")
    s.node(0.34, 3.32, 9.32, 0.76, "One family of models underneath",
           sub="ChatGPT is the product built around it", accent=True)
    s.caption(0.34, 4.24, 9.32,
              "The same model reaches you through all four. Which one you pick "
              "changes the tools it can call and the price you pay, not the "
              "intelligence underneath.")

    s = d.content("What it is not")
    s.compare(1.58,
              "A common picture", [
                  "It looks the answer up",
                  "It knows what happened today",
                  "It obeys your instructions",
              ],
              "What is actually happening", [
                  "It predicts a likely continuation",
                  "It knows nothing until it fetches",
                  "It generates tokens based on the current context",
              ], h=2.60)
    s.caption(0.34, 4.34, 9.32,
              "The gap between those two columns is where most disappointing "
              "answers come from.")

    # ----------------------------------------------------------- how it works
    s = d.how("train it to predict, then tune it to assist")
    s.steps(0.34, 1.58, 5.40, [
        "Pre-train on text until it predicts well",
        "Tune on answers humans ranked as better",
        "Let it practise against that ranking",
        "Wrap it in tools, and ship it as a product",
    ], h=0.62, gap=0.16)
    s.caption(6.06, 2.14, 3.60,
              "Step one buys fluency. Steps two and three buy manners: helpful, "
              "ordered, willing to refuse.\n\n"
              "Step four is the part that has moved most recently, and it is "
              "what the rest of this deck is about.")


    s = d.content("Training ChatGPT")
    # 16:9 figure - fit it by height, or it runs off the bottom of the slide
    picture(s, "training-chatgpt.png", 0.34, 1.58, 5.34, 1.78)
    s.body("Three passes: learn to predict text, learn what people preferred, "
           "then optimise against that preference.",
           box=(6.00, 1.70, 3.66, 1.60))

    s = d.content("A turn is a loop, not a single shot")
    s.flow(0.34, 1.58, 9.32, [
        ("You ask", "the question"),
        ("It plans", "what it needs to find out"),
        ("It uses a tool", "search, code, a connected service"),
        ("It answers", "from what came back"),
    ], h=1.45, accent_last=True,
        loop="each result is appended, and it decides again")
    s.caption(0.34, 3.78, 9.32,
              "Nothing about the tools is magic. Whatever one returns is pasted "
              "back into the same block of text the model is reading - its "
              "context - and it carries on predicting from there.")

    s = d.content("Every setting you touch ends up here")
    bottom = s.layers(0.34, 1.58, 5.90, [
        ("Standing instructions", "set once, sent every time"),
        ("What it remembers of you", "carried between chats"),
        ("Files and pages fetched", "pulled in for this task"),
        ("Results from tools it ran", "code output, search hits"),
        ("Your message", "typed just now", True),
    ], h=0.44)
    s.arrow(3.12, bottom - 0.05, 0.34, 0.20, direction="down")
    s.node(0.34, bottom + 0.22, 5.90, 0.60, "It all arrives as one prompt",
           accent=True)
    s.caption(6.55, 2.20, 3.11,
              "Nothing on this stack is privileged. A page it retrieved and a "
              "sentence you typed look the same to the model.\n\n"
              "That is why one bad source spoils an answer, and why saying plainly "
              "what you want still beats anything clever.")

    s = d.content("Fast answers, or slow ones")
    s.table(0.34, 1.58, 9.32, 2.30, [
        ["", "Answers straight away", "Thinks before answering"],
        ["Good for", "Recall, drafting, chat", "Maths, planning, code"],
        ["It costs you", "Almost nothing", "Time, and far more tokens"],
        ["You get it wrong by", "Asking something hard", "Asking something trivial"],
    ], col_widths=[1.8, 3.7, 3.7])
    s.caption(0.34, 4.04, 9.32,
              "Each new generation moves the same three dials: better reasoning, "
              "a longer context window, a lower price per token. The model names will "
              "have changed by the time you watch this. The dials will not.")

    # --------------------------------------------------------- why it matters
    s = d.why("the failure modes become predictable")
    s.table(0.34, 1.58, 9.32, 2.60, [
        ["What goes wrong", "Why", "What fixes it"],
        ["A confident wrong fact", "Nothing was fetched", "Give it sources"],
        ["Yesterday's answer", "Trained, not live", "Let it search"],
        ["Arithmetic that looks right", "Text, not calculation", "Make it run code"],
        ["Your instruction ignored", "Buried in a long context", "Say it up front"],
    ], col_widths=[2.6, 3.2, 2.6])
    s.caption(0.34, 4.34, 9.32,
              "None of these is the model being stupid. Each one is a missing tool, "
              "or a context you did not supply.")

    d.two_columns(
        "When to reach for it, and when not to",
        ["Work you can describe but do not want to start",
         "Reading that already exists and just needs doing",
         "A process you would otherwise repeat by hand"],
        ["Judgement you are accountable for",
         "Anything you will not read before sending",
         "Work where the struggle is the point"],
        left_heading="Worth handing over",
        right_heading="Keep it yourself",
    )

    s = d.content("What this looks like in one turn")
    m = s.mock(0.40, 1.56, 5.05, 3.49)
    m.label(ROLE_USER)
    m.para("Compare our three pricing pages, and check what rivals changed "
           "this quarter.")
    m.gap(0.06)
    m.label("Ran").line("a web search, then code over your data")
    m.gap(0.06)
    with m.bubble():
        m.label(ROLE_AI)
        m.para("Page B converts 2.1x better than A. Two rivals dropped their "
               "entry tier in March - sources listed below.")
    m.composer(pin=False)
    s.beside(
        m,
        "Same text box, same predictor. What is different is that it went and "
        "fetched things first, and that the answer says where they came from. "
        "That is the shift the rest of this course is built on.",
    )

    # ------------------------------------------------------------- handoff
    d.handoff([
        ("Open a fresh chat", "and look at what it offers"),
        ("Ask something live", "watch it search before it answers"),
        ("Hand it a file", "and let it run code over it"),
    ], lead="That is the principle. Now let's open it up and drive.")

    return d.save(OUT)


if __name__ == "__main__":
    print(build())
