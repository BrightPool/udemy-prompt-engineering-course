#!/usr/bin/env python3
"""Build the five-slide principles deck for connecting a custom MCP server."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "principles-deck" / "scripts"))
from deckkit import Deck  # noqa: E402

out = Path(
    sys.argv[1]
    if len(sys.argv) > 1
    else Path(__file__).resolve().parent / "custom-mcp-servers.pptx"
)

d = Deck()

d.title(
    "Custom MCP Servers in ChatGPT",
    "How a connection gives ChatGPT access to a tool or data source you choose.",
)

s = d.what("a live connection to capabilities you choose")
m = s.mock(0.40, 1.52, 4.60, 3.58)
m.user("Create a support ticket from this summary.")
with m.bubble():
    m.assistant("Created ticket SUP-184 and added the summary.")
m.label("Tool used").line("create_support_ticket", highlight=True)
m.composer(pin=False)
s.beside(
    m,
    "A custom MCP server gives ChatGPT a defined route into another system. "
    "The server exposes specific tools and data, so the conversation can use "
    "live information or complete approved actions.",
)

s = d.how("the server describes what ChatGPT can call")
s.flow(
    0.34,
    1.52,
    9.32,
    [
        ("Connect", "to one server"),
        ("Discover", "its available tools"),
        ("Choose", "the tool that fits"),
        ("Return", "the result to the chat"),
    ],
    h=1.10,
    accent_last=True,
    loop="the connection stays available for later requests",
)
s.caption(
    0.34,
    3.62,
    9.32,
    "The server publishes names, descriptions and input rules for its tools. "
    "ChatGPT reads that catalogue when it connects, then selects a matching tool "
    "when your request needs it.",
)

s = d.why("your own systems become part of the conversation")
s.table(
    0.34,
    1.52,
    9.32,
    2.30,
    [
        ["", "Without a connection", "With a trusted connection"],
        ["Information", "Paste a snapshot", "Read live, permitted data"],
        ["Action", "Describe what to do", "Call an exposed tool"],
        ["Customisation", "Use general capabilities", "Add a workflow you chose"],
        ["Failure mode", "Missing or stale context", "A server exposes too much"],
    ],
    col_widths=[1.70, 3.70, 3.92],
)
s.caption(
    0.34,
    4.02,
    9.32,
    "The connection is also a trust boundary. Review the server, its tools and "
    "their permissions before you give it access to real data or actions.",
)

d.handoff(
    [
        ("Add one trusted server", "use a trusted endpoint"),
        ("Review its tools", "check tools and access"),
        ("Ask for a real result", "watch ChatGPT choose a tool"),
        ("Check what changed", "verify it in the source"),
    ],
    lead="That is the principle. Now we connect a new tool inside ChatGPT.",
)

path = d.save(out)
print(f"wrote {path}  ({len(d.prs.slides._sldIdLst)} slides)")
